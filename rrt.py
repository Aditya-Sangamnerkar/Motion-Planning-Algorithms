import pygame
import sys
import random

class Point():

	def __init__(self):
		self.coordinate = ()
		self.color = (0,255,0)
		self.radius = 3
		self.parent = None


def calculateDistance(point1,point2):
	x = (point1[0] - point2[0])**2
	y = (point1[1] - point2[1])**2
	distance = (x + y) ** (0.5)
	return distance

# RRT Parameters
max_connect_length = 50
segments = 100
destination_found = False
nodes = 1
tree_connections = []

# input parameters
size = height,width =  600,600
screenColor = (255,255,255)
done = False
running = True

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(screenColor)

# draw the initial point on the screen and add it as root of tree connections
initialPoint = Point()
initialPoint.coordinate = (100,100)
initialPoint.color = (255,0,0)
initialPoint.radius = 7
pygame.draw.circle(screen,initialPoint.color,(initialPoint.coordinate[0],initialPoint.coordinate[1]),initialPoint.radius,3)
tree_connections.append(initialPoint)			

# draw the destination point on the screen
destinationPoint = Point()
destinationPoint.coordinate = (450,350)
destinationPoint.color = (255,0,0)
destinationPoint.radius = 7
pygame.draw.circle(screen,initialPoint.color,(destinationPoint.coordinate[0],destinationPoint.coordinate[1]),destinationPoint.radius,3)


while running:

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

	while not destination_found:
		

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
	

		# connect the new node to the closest node

		# --> check if within range
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
			tree_connections.append(destinationPoint)
			pygame.draw.lines(screen,(0,0,255),False,[destinationPoint.parent.coordinate,destinationPoint.coordinate])
		# --> check if there is obstacle between the node and destination point

		
		pygame.display.flip()

	# construct the path to the start node
	if(destination_found == True):
		temp = destinationPoint
		while(temp.parent != None):
			pygame.draw.lines(screen,(255,140,0),False,[temp.coordinate,temp.parent.coordinate],3)
			temp = temp.parent


	pygame.display.flip()

