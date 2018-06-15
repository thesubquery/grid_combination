
from random import randint, shuffle

class World:
	"""
	A testing World class to handle :
	 ` adding shapes to the world
	 ` check availablilty 

	"""
	def __init__(self, x, y):

		self.row = x
		self.col = y
		self.grid = []
		self.emptyCell = 0
		self.counter = 0
		self.shapes = []
		self.setEmptyGrid()


	def setEmptyGrid(self):
		"""
		
		Reset the whole class, everything back to original
		
		"""
		self.grid = [[ "."  for i in range(self.col)] for j in range(self.row)]
		self.emptyCell = self.col * self.row
		self.counter = 1

	def display(self):
		"""
		Print out the grid

		"""
		for r in range(self.row):
			print(self.grid[r])

	def checkAvailability(self, r, c):
		"""
		Check if the given cell is avaliable		
		
		Arguments:
			r {int} -- [row]
			c {int} -- [col]
		
		Returns:
			bool -- [Available?]
		"""
		if( r < 0 ) or ( c < 0) or (r >= self.row) or ( c >= self.col): 
			return False
		else:
			return self.grid[r][c] == "."

	def getNextAvailability(self, random = False):
		"""
		Return the next available cell
		
		If random is true, get the empty cell by random		
		
		Keyword Arguments:
			random {bool} -- [description] (default: {False})
		Returns:
			list([int, int]) -- [Next available cell]

		"""
		list_ava = [] 
        for r in range(self.row):
            for c in range(self.col):
                if self.checkAvailability(r, c):
                    list_ava.append([c, r])

        if random == True:
            num = randint(0, len(list_ava)-1)
        else:
            num = 0 
        return list_ava[num]


	def placeBlock(self, r, c, count, place_holder = None):
		"""

		Placing the grid with the counter number
		
		Arguments:
			r {int} -- [row]
			c {int} -- [col]
			count {int} -- [counter]
		
		Keyword Arguments:
			place_holder {string} -- You can put it as '[]' or '[x]'' (default: {None})
		"""
		if place_holder != None:
			self.grid[r][c] = place_holder
		else:
			if count < 10 :
				count = '0' +str(count)
			else:
				count = str(count)
			
			self.grid[r][c] = count

	def addShapes(self, shapes):
		"""
		Update the shapes list from external source

		Arguments:
			shapes {[array]} -- [All possible shapes]
		"""
		self.shapes = shapes

	def fillGrid(self):
		"""
		
		"""
		while self.emptyCell != 0:
			position = self.getNextAvailability() #Set the position with next available cell
			#Shuffle the list of all shapes. Hence, select shapes randomly
			shuffle(self.shapes) 
			s = 0
			placed = False

			while placed == False:
				list_to_check = []

				for each in self.shapes[s]: # for each coord of the shape
					# get a list of cells for the given shape starting from the current position 
					list_to_check.append([position[0]+each[0], position[1]+each[1]])
				
				# check if those cells are available
				ava = [self.checkAvailability(x[1],x[0]) for x in list_to_check]


				if all( x == True for x in ava): 
					# if all the cells are available, place the blocks on the grid.
					[self.placeBlock(x[1], x[0], self.counter) for x in list_to_check]
					print('Placed: ',list_to_check, ' as ', self.counter, ava)
					self.counter += 1
					placed = True
					self.emptyCell -= len(list_to_check) #update the number of empty cell
				else:
					# if not all the cells are available, get the next shape
					s +=1 

"""
Sample test case:
"""

shapes = [
    #1
    [[0, 0]],
    #2
    [[0, 0], [1, 0]],
    [[0, 0], [-1, 0]],
    [[-1, 0], [0, 0]],
    [[1, 0], [0, 0]]
]

w = World(4,4)
w.addShapes(shapes)
w.fillGrid() 
w.display()