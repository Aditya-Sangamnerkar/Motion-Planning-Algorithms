import pygame
import sys
import random


class Point():

	def __init__(self):
		self.coordinate = ()
		self.color = (0,255,0)
		self.radius = 3
		self.parent = None

class Obstacle():

	def __init__(self):
		self.h = 0
		self.k = 0
		self.radius = 0
		self.color = (100,100,255)


def calculateDistance(point1,point2):
	x = (point1[0] - point2[0])**2
	y = (point1[1] - point2[1])**2
	distance = (x + y) ** (0.5)
	return distance


def isInObstacle(point):
	for obstacle in obstacles:
		equation_value = (point.coordinate[0] - obstacle.h) ** 2 + (point.coordinate[1] - obstacle.k) **2
		if(equation_value <= (obstacle.radius ** 2)):
			return True
	return False


def isCrossingObstacle(point1,point2):
	
	p = point2.coordinate[1]-point1.coordinate[1]
	q = point2.coordinate[0]-point1.coordinate[0]
	# for the simplicity of implementation the point that will form line parallel to y axis are ignored
	if(q == 0):
		return True
	m = p/q
	x = point1.coordinate[0]
	y = point1.coordinate[1]
	c = y - m*x


	for obstacle in obstacles:
		h = obstacle.h
		k = obstacle.k
		r = obstacle.radius
		a = 1 + (m*m)
		b = (2*m*c) - (2*m*k) - (2*h)
		c = (h**2) + (c**2) + (k**2) - (r**2) - (2*c*k) 
		discriminant = (b**2) - (4*a*c)

		if(discriminant>=0):
			return True
	return False

	

# RRT Parameters
max_connect_length = 50
destination_found = False
tree_connections = []
obstacles = []
random.seed(10)
count = 0

# input parameters
size = height,width =  600,600
screenColor = (255,255,255)
done = False
running = True

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(screenColor)

# draw the obstacles
obstacle1 = Obstacle()
obstacle1.h = 400
obstacle1.k = 300
obstacle1.radius = 30
pygame.draw.circle(screen,obstacle1.color,(obstacle1.h,obstacle1.k),obstacle1.radius)
obstacles.append(obstacle1)

obstacle2 = Obstacle()
obstacle2.h = 100
obstacle2.k = 150
obstacle2.radius = 30
pygame.draw.circle(screen,obstacle2.color,(obstacle2.h,obstacle2.k),obstacle2.radius)
obstacles.append(obstacle2)


obstacle3 = Obstacle()
obstacle3.h = 100
obstacle3.k = 400
obstacle3.radius = 30
pygame.draw.circle(screen,obstacle3.color,(obstacle3.h,obstacle3.k),obstacle3.radius)
obstacles.append(obstacle3)

obstacle4 = Obstacle()
obstacle4.h = 300
obstacle4.k = 500
obstacle4.radius = 30
pygame.draw.circle(screen,obstacle4.color,(obstacle4.h,obstacle4.k),obstacle4.radius)
obstacles.append(obstacle4)


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
					pygame.draw.circle(screen,initialPoint.color,(initialPoint.coordinate[0],initialPoint.coordinate[1]),initialPoint.radius,3)
					tree_connections.append(initialPoint)
					count+=1
				else:
					destinationPoint.coordinate = event.pos
					pygame.draw.circle(screen,initialPoint.color,(destinationPoint.coordinate[0],destinationPoint.coordinate[1]),destinationPoint.radius,3)
					count+=1


	while not destination_found and count==2:
		
		# generate a node at a random location in screen	
		newPoint = Point()
		newPointX = random.randint(0,600)
		newPointY = random.randint(0,600)
		newPoint.coordinate = (newPointX,newPointY)

		# check if node is a valid node

		# --> check if it is not a repeated node
		for node in tree_connections:
			if(node.coordinate == newPoint.coordinate):
				continue
		# --> check if the node is not within any obstacle
		if(isInObstacle(newPoint)):
			continue
		


		neighbour_distances = []
		for neighbour in tree_connections:
			neighbour_distances.append(calculateDistance(newPoint.coordinate,neighbour.coordinate))

		min_distance = 100000
		min_distance_node_index = -1

		for i in range(0,len(neighbour_distances)):
			if(neighbour_distances[i]<min_distance):
				min_distance = neighbour_distances[i]
				min_distance_node_index = i

		# --> check if obstacle between the closest node and the newPoint node
		if(isCrossingObstacle(newPoint,tree_connections[min_distance_node_index])):
			continue
		
		# --> add this node as a node to tree connections if the distance is less than then maximum connect length
		if(min_distance < max_connect_length):
			newPoint.parent = tree_connections[min_distance_node_index]
			tree_connections.append(newPoint)
			pygame.draw.circle(screen,newPoint.color,(newPoint.coordinate[0],newPoint.coordinate[1]),newPoint.radius,3)
			pygame.draw.lines(screen,(100,100,100),False,[newPoint.coordinate,newPoint.parent.coordinate],1)
		else:
			continue


		# check if we are close to the destination point

		# --> check if the destination point is within reach
		if(calculateDistance(destinationPoint.coordinate,newPoint.coordinate)<=max_connect_length):
			destination_found=True
			destinationPoint.parent = newPoint
			# --> check if there is obstacle between the node and destination point
			if(isCrossingObstacle(newPoint,newPoint.parent)):
				continue
			tree_connections.append(destinationPoint)
			pygame.draw.lines(screen,(0,0,255),False,[destinationPoint.parent.coordinate,destinationPoint.coordinate])
		

		
		pygame.display.flip()

	# construct the path to the start node
	if(destination_found == True):
		temp = destinationPoint
		while(temp.parent != None):
			pygame.draw.lines(screen,(255,140,0),False,[temp.coordinate,temp.parent.coordinate],3)
			temp = temp.parent


	pygame.display.flip()

