
'''
 - The input for obstacles can be given by modifying the 'draw the obstacles portion of the code
 - The initial and destination points should be provided via mouse clicks when the program is executed
 - This is a modified version of rrt algorithm where in my qRandom and qNew are both the same node.
 - qRandom is generated such that it lies within the grid and then checking is done for validity etc.
'''
import pygame
import random
import sys
import copy

class Point():

	def __init__(self):
		self.coordinate = ()
		self.color = (0,255,0)
		self.radius = 3
		self.parent = None

	def isInObstacle(self):
		for obstacle in obstacles:
			equation_value = (self.coordinate[0] - obstacle.h) ** 2 + (self.coordinate[1] - obstacle.k) **2
			if(equation_value <= (obstacle.radius ** 2)):
				return True
		return False
	def isCrossingObstacle(self,point2):
		p = point2.coordinate[1]-self.coordinate[1]
		q = point2.coordinate[0]-self.coordinate[0]
		x1 = self.coordinate[0]
		y1 = self.coordinate[1]
		x2 = point2.coordinate[0]
		y2 = point2.coordinate[1]
		m = 0
		c = 0
		if q == 0:
			return True
		else:
			m = p/q
			c = y1 - (m*x1)
		for x in range(x1,x2,1):			
			y = m*x + c
			qNode = Point()
			qNode.coordinate = (x,y)
			if(qNode.isInObstacle()):
				return True
		return False
	def calculateDistance(self,point2):
		# eucledian distance formula is used to calculate the distance between two points.
		x = (self.coordinate[0] - point2.coordinate[0])**2
		y = (self.coordinate[1] - point2.coordinate[1])**2
		distance = (x + y) ** (0.5)
		return distance


class Obstacle():

	def __init__(self,h,k,radius):
		self.h = h
		self.k = k
		self.radius = radius
		self.color = (100,100,255)
		pygame.draw.circle(screen,self.color,(self.h,self.k),self.radius)
		obstacles.append(self)

# RRT Parameters
max_connect_length = 50
destination_found = False
tree_connections = []
obstacles = []
random.seed(10)
count = 0 # counter variable to check for user input of starting and destination points.
done = False
running = True
distance = 0
show_stats = False

# initialize the pygame window
size = height,width =  600,600
screenColor = (255,255,255)
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(screenColor)

# draw the obstacles
obstacle1 = Obstacle(400,300,30)
obstacle2 = Obstacle(100,150,30)
obstacle3 = Obstacle(100,400,30)
obstacle4 = Obstacle(300,500,30)

# initialize the initial point 
initialPoint = Point()
initialPoint.coordinate = ()
initialPoint.color = (255,0,0)
initialPoint.radius = 7

	
# initialize the destination point
destinationPoint = Point()
destinationPoint.coordinate = ()
destinationPoint.color = (255,0,0)
destinationPoint.radius = 7


while running:

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and count<2:
				if count == 0:
					initialPoint.coordinate = event.pos
					if(initialPoint.isInObstacle()):
						print('## Invalid position for the initial point')
						sys.exit()

					pygame.draw.circle(screen,initialPoint.color,(initialPoint.coordinate[0],initialPoint.coordinate[1]),initialPoint.radius,3)
					tree_connections.append(initialPoint)
					count+=1
				else:
					destinationPoint.coordinate = event.pos
					if(destinationPoint.isInObstacle()):
						print('## Invalid position for the destination point')
						sys.exit()
					pygame.draw.circle(screen,initialPoint.color,(destinationPoint.coordinate[0],destinationPoint.coordinate[1]),destinationPoint.radius,3)
					count+=1


	while not destination_found and count==2:
		
		# generate a node at a random location in screen - qNew 
		qNew = Point()
		qNewX = random.randint(0,600)
		qNewY = random.randint(0,600)
		qNew.coordinate = (qNewX,qNewY)

		# check if node is a valid node

		# --> check if it is not a repeated node
		for node in tree_connections:
			if(node.coordinate == qNew.coordinate):
				continue
		# --> check if the node is not within any obstacle
		if(qNew.isInObstacle()):
			continue
		
		# find the node closest to the new node - qNear
		neighbour_distances = []
		for neighbour in tree_connections:
			neighbour_distances.append(qNew.calculateDistance(neighbour))

		min_distance = 100000
		min_distance_node_index = -1

		for i in range(0,len(neighbour_distances)):
			if(neighbour_distances[i]<min_distance):
				min_distance = neighbour_distances[i]
				min_distance_node_index = i

		qNear = tree_connections[min_distance_node_index]
				
		# --> check if obstacle between the closest node and the newPoint node
		if(qNew.isCrossingObstacle(qNear)):
			continue
		
		# --> add this node as a node to tree connections if the distance is less than then maximum connect length
		if(min_distance < max_connect_length):
			qNew.parent = qNear
			tree_connections.append(qNew)
			pygame.draw.circle(screen,qNew.color,(qNew.coordinate[0],qNew.coordinate[1]),qNew.radius,3)
			pygame.draw.lines(screen,(100,100,100),False,[qNew.coordinate,qNew.parent.coordinate],1)
		else:
			continue


		# check if we are close to the destination point

		# --> check if the destination point is within reach
		if(qNew.calculateDistance(destinationPoint)<=max_connect_length):
			# --> check if there is obstacle between the node and destination point
			if(qNew.isCrossingObstacle(destinationPoint)):
				continue
			destination_found=True
			destinationPoint.parent = qNew
			tree_connections.append(destinationPoint)
			pygame.draw.lines(screen,(0,0,255),False,[destinationPoint.parent.coordinate,destinationPoint.coordinate])
			
		
		pygame.display.flip()

	# construct the path to the start node
	if(destination_found == True and show_stats == False) :
		temp = copy.copy(destinationPoint)
		while(temp.parent != None):
			pygame.draw.lines(screen,(255,140,0),False,[temp.coordinate,temp.parent.coordinate],3)
			distance+=temp.calculateDistance(temp.parent)
			temp = temp.parent
		print("Distance : {0}".format(distance))
		print("Total Nodes : {0}".format(len(tree_connections)-2))
		show_stats = True

	pygame.display.flip()


