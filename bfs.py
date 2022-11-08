import copy

class Node():
	def __init__(self):
		self.x = -1
		self.y = -1
		self.parent = None

R = 5
C = 7
m = [['S','.','.','#','.','.','E'],
	['.','#','.','.','.','#','.'],
	['.','#','.','.','.','.','.'],
	['.','.','#','#','.','.','.'],
	['#','.','#','.','.','#','.']]

rq = [] # empty row queue
cq = [] # empty column queue
# variables used to track the number of steps taken
move_count = 0
nodes_left_in_layer = 1
nodes_in_next_layer = 0
# variables used to track the number of steps taken
move_count = 0
nodes_left_in_layer = 1
nodes_in_next_layer = 0
# variable used to track whether the 'E' character is reached
reached_end = False
# R X C matrix of false values used to track if a node is visited or not
visited =[ [False for i in range(C)] for j in range(R)]
# north, south, east, west direction vectors
dr = [-1,1,0,0]
dc = [0,0,1,-1]
sr = 0 # start row
sc = 0 # start column
reached_end = False # variable to check if we reached the node with 'E'
tree_connections = [] # tree that will trace the path to the 'S' node
# insert node in the tree
start = Node()
start.x = 0
start.y = 0
start.parent = None
tree_connections.append(start)


def insert(r,c,rr,rc):
	temp = Node()
	temp.x = rr
	temp.y = rc
	for node in tree_connections:
		if node.x == r and node.y == c:
			temp.parent = node
			tree_connections.append(temp)
			break

def trace():
	end = Node()
	for temp in tree_connections:
		if temp.x == 0 and temp.y == 6:
			end = copy.copy(temp)
			break
	end = end.parent	
	while(end.parent!=None):
		m[end.x][end.y] = '*'
		end = end.parent


def explore_neighbours(r,c):
	global dr,dc,R,C,rq,cq,nodes_in_next_layer
	for i in range(0,4):
		rr = r + dr[i]
		cc = c + dc[i]

		if rr < 0 or cc < 0:
			continue
		if rr >= R or cc >=C:
			continue
		if visited[rr][cc]:
			continue
		if m[rr][cc] == '#':
			continue
		
		rq.append(rr)
		cq.append(cc)
		visited[rr][cc] = True
		insert(r,c,rr,cc)
		nodes_in_next_layer+=1

			
def display(arr):
	for i in range(0,R):
		print()
		for j in range(0,C):
			print(arr[i][j], end = ' ')


def solve():

	global rq,cq,visited,sr,sc,m,nodes_left_in_layer,nodes_in_next_layer,reached_end,move_count
	
	rq.append(sr)
	cq.append(sc)
	visited[sr][sc] = True

	while(len(rq) > 0):
		r = rq.pop(0)
		c = cq.pop(0)
		if m[r][c] == 'E':
			reached_end = True
		explore_neighbours(r,c)
		nodes_left_in_layer-=1
		if nodes_left_in_layer == 0:
			nodes_left_in_layer = nodes_in_next_layer
			nodes_in_next_layer = 0	
			move_count+=1
		if reached_end == True:
			return move_count
	return -1

display(m)
print(solve())
trace()
display(m)
