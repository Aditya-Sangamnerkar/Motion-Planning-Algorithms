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

	def isCrossingObstacle(self,point2,segments):
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
		for x in range(int(x1),int(x2),segments):			
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

	def generateNewNode(self,point2,epsilon):
		x1 = self.coordinate[0]
		y1 = self.coordinate[1]
		x2 = point2.coordinate[0]
		y2 = point2.coordinate[1]
		qNew = Point()
		r = self.calculateDistance(point2)
		x = x1 + epsilon*((x2-x1)/r)
		y = y1 + epsilon*((y2-y1)/r)
		qNew.coordinate = (x,y)
		return qNew

class Obstacle():

	def __init__(self,h,k,radius):
		self.h = h
		self.k = k
		self.radius = radius
		self.color = (100,100,255)
		pygame.draw.circle(screen,self.color,(self.h,self.k),self.radius)
		obstacles.append(self)

# RRT Parameters
epsilon = 20
max_connect_length = 50
segments = 5
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

	while not destination_found and count == 2:
		pygame.display.flip()
		# generate a random node - qRandom
		qRandom = Point()
		qRandomX = random.randint(0,600)
		qRandomY = random.randint(0,600)
		qRandom.coordinate = (qRandomX,qRandomY)
		pygame.draw.circle(screen,(255,0,0),(qRandom.coordinate[0],qRandom.coordinate[1]),qRandom.radius,3)
		
		# find node closest to qRandom from tree - qNear
		neighbour_distances = []
		for neighbour in tree_connections:
			neighbour_distances.append(qRandom.calculateDistance(neighbour))
		min_distance = 100000
		min_distance_node_index = -1
		for i in range(0,len(neighbour_distances)):
			if(neighbour_distances[i]<min_distance):
				min_distance = neighbour_distances[i]
				min_distance_node_index = i
		qNear = tree_connections[min_distance_node_index]
		
		# generate a node epsilon distance away from qNear in direction of qRandom - qNew
		qNew = qNear.generateNewNode(qRandom,epsilon)
		#qNew = qRandom
		# check if qNew is a valid node
		# --> check if not repeated
		flag = False
		for node in tree_connections:
			if(node.coordinate == qNew.coordinate):
				flag = True
				break
		if flag == True:
			continue
		# --> check if not within any obstacle
		if(qNew.isInObstacle()):
			continue

		# check if obstacle between qNear and qNew
		if(qNear.isCrossingObstacle(qNew,segments)):
			continue

		# add qNew to the tree
		qNew.parent = qNear
		tree_connections.append(qNew)
		pygame.draw.circle(screen,qNew.color,(qNew.coordinate[0],qNew.coordinate[1]),qNew.radius,3)
		pygame.draw.lines(screen,(100,100,100),False,[qNew.coordinate,qNew.parent.coordinate],1)

		# check if we are close to destination
		# --> check if destination within reach
		if(qNew.calculateDistance(destinationPoint)<=max_connect_length):
			# --> check if obstacle between destination and qNew
			if(qNew.isCrossingObstacle(destinationPoint,segments)):
				continue
			destinationPoint.parent = qNew
			tree_connections.append(destinationPoint)
			pygame.draw.lines(screen,(100,100,100),False,[qNew.coordinate,destinationPoint.coordinate],1)
			destination_found = True
		pygame.display.flip()
		

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


	
		


