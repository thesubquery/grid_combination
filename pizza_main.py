# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:18:40 2019

@author: CLAM
"""
import gc
gc.collect()


lines = []
with open(r"C:\Users\clam\Desktop\HashCode_Pizza\grid_combination\Google Hash Code\b_small.in", "r") as f:
    lines = f.readlines()        
lines = [ l.replace("\n", "") for l in lines]


height    = len(lines) - 1
width     = len(lines[1])
t_minimum = 1
m_minimum = 1

pizza     = [[lines[i][j] for j in range(width)] for i in range(1, height + 1)]



def gen_shape(size):
    world = [['.' for j in range(size)] for i in range(size)]
    data = {}
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            if i * j == size:
                data[(i, j)] = {}
                print(i, j)
                for k in range(i):
                    for l in range(j):
                        data[(i, j)][(k, l)] = None
                        print("\t{}, {}".format(k, l))
    return data

data = {}
for size in range(2, 5+1):
    data[size] = gen_shape(size)
    

class shape:
    def __init__(self, ID):
        self.ID          = ID
        self.links       = {}
        self.coordinates = (0, 0)
    def __repr__(self):
        msg  = "ID:{} Coordinate(s): ".format(self.ID)
        for c in self.coordinates:
            msg += "{}, ".format(c)
        return msg

class cell:
    def __init__(self, ID):
        self.ID          = ID
        self.links       = {}
        self.coordinates = (0, 0)
    def __repr__(self):
        msg = "ID[{}] Coordinate: ({}, {})".format(self.ID, self.coordinates[0], self.coordinates[1])
        return msg

    

slice_by_coord = {}
slice_by_index = {}
cells_by_coord = {}
cells_by_index = {}
iteration = 1
for x1 in range(height):
    for y1 in range(width):
        c = cell(iteration)
        c.coordinates = (x1, y1)
        cells_by_coord[c.coordinates] = c
        cells_by_index[iteration] = c
        iteration += 1

cells_by_coord[c.coordinates]
cells_by_index[5].links


for x1 in range(height):
    for y1 in range(width):
        directions = [[-1,  0],
                      [ 1,  0],
                      [ 0,  1],
                      [ 0, -1],
                      [ 1,  1],
                      [ 1, -1],
                      [-1,  1],
                      [-1, -1]]
        for d in directions:
            x2 = x1 + d[0]
            y2 = y1 + d[1]
            if 0 <= x2 < height and 0 <= y2 < width:
                cells_by_coord[(x1, y1)].links[(x2, y2)] = cells_by_coord[(x2, y2)]


list_of_shapes = []
for x1 in range(height):
    for y1 in range(width):
        cell = (x1, y1)
        slices[cell] = {}
        for size in data:
            for dim in data[size]:
                
                counter = {'T': 0, 'M': 0}
                coords  = []
                for piece in data[size][dim]:
                    x2 = piece[0]
                    y2 = piece[1]
                    x3 = x1 + x2
                    y3 = y1 + y2
                    if 0 <= x3 < height and 0 <= y3 < width:
                        counter[pizza[x3][y3]] += 1
                        coords.append((x3, y3))                

                if counter['T'] >= t_minimum and counter['M'] >= m_minimum and (counter['T'] + counter['M'] == size):
                    list_of_shapes.append(tuple(coords))
list_of_shapes = list(set(list_of_shapes))
len(list_of_shapes)

for x1 in range(height):
    for y1 in range(width):
        slice_by_coord[(x1, y1)] = {}


iteration = 1
for s in list_of_shapes:
    new_shape = shape(iteration)
    new_shape.coordinates = [each for each in s]
    slice_by_index[iteration] = new_shape
    for c in new_shape.coordinates:
        slice_by_coord[c][iteration] = new_shape 
    iteration += 1

for i in range(1, len(slice_by_index)+1):
    i    = 1

    node = slice_by_index[i]
    for c in node.coordinates:
        index = cells_by_coord[c].ID
        print(index)
    








    
slices = {}
cells  = {}
for x1 in range(height):
    for y1 in range(width):
        cells[(x1, y1)] = []


for x1 in range(height):
    for y1 in range(width):
        cell = (x1, y1)
        slices[cell] = {}
        for size in data:
            for dim in data[size]:
                
                
                counter = {'T': 0, 'M': 0}
                coords  = []
                for piece in data[size][dim]:
                    x2 = piece[0]
                    y2 = piece[1]
                    x3 = x1 + x2
                    y3 = y1 + y2
                    if 0 <= x3 < height and 0 <= y3 < width:
                        counter[pizza[x3][y3]] += 1
                        coords.append((x3, y3))                

                if counter['T'] >= t_minimum and counter['M'] >= m_minimum and (counter['T'] + counter['M'] == size):

                    slices[cell][dim] = {}

                    for c in coords:
                        x4 = c[0]
                        y4 = c[1]
                        slices[cell][dim][(x4, y4)] = None
                        cells[(x4, y4)].append(slices[cell][dim])

surroundings = {}
for x1 in range(height):
    for y1 in range(width):
        surroundings[(x1, y1)] = {}
        directions = [[-1,  0],
                      [ 1,  0],
                      [ 0,  1],
                      [ 0, -1],
                      [ 1,  1],
                      [ 1, -1],
                      [-1,  1],
                      [-1, -1]]
        for d in directions:
            x2 = x1 + d[0]
            y2 = y1 + d[1]
            if 0 <= x2 < height and 0 <= y2 < width:
                surroundings[(x1, y1)][(x2, y2)] = None
                      

iteration = 0
total     = []
for x1 in range(height):
    for y1 in range(width):
        iteration += 1
        msg = "{} - ({}, {}) - {}".format(iteration, x1, y1, len(cells[(x1, y1)]))
        total.append(len(cells[(x1, y1)]))
        print(msg)

shapes = []
for i in cells:
    
    for j in cells[i]:
        coords = []
        for k in j:
            coords.append(k)
        shapes.append(coords)
        print(i, coords)

shapes_index = {}
for s in shapes:
    shapes_index[tuple(s)] = None
    print(tuple(s))



queue = {}

for each in cells.keys():
    if len(cells[each]) == 1:
        for shape in cells[each]:
            key = [coord for coord in shape]
            key.sort()
            queue[tuple(key)] = [[coord for coord in key]]


#key   = (5, 0)
#key   = [coord for coord in cells[key]]
#queue = {tuple(key): [[coord for coord in key]]}

#queue      = sorted(queue)
max_size   = 0
max_coords = []
total      = len(queue)

while queue:
    coords = ""
    for each in queue:
        coords = each
        break
    
    
    # Generates a list of surrounding cells
    toCheck = [c2 for c1 in coords for c2 in surroundings[c1]]
    toCheck = list(set(toCheck))
    toCheck = [each for each in toCheck if each not in coords]
    toCheck = sorted(toCheck)
    
    # Check each surrounding cell
    for i in range(len(toCheck)):
        # Check each shape that fits the surrounding cell
        for new_shape in cells[toCheck[i]]:
                        
            size       = len(new_shape)
            new_coords = [new_coord for new_coord in new_shape if new_coord not in coords]
            # If all cells in the new_shape doesn't overlap with existing cells
            if len(new_coords) == size:
            
                new_key           = list(coords) + new_coords
                count             = len(new_key)
                new_key.sort()
                queue[tuple(new_key)]    = queue[tuple(coords)] + [new_coords]
                total += 1
                if max_size < count:
                    max_size   = count
                    max_coords = {i: [j for j in queue[tuple(new_key)][i]] for i in range(len(queue[tuple(new_key)]))}
                    msg = "{} / {} Max: {}".format(total - len(queue), total, max_size)
                    printProgressBar(total - len(queue), total, suffix = msg)
    del queue[tuple(coords)]


    
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent      = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar          = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()    


world = [[lines[i][j] for j in range(width)] for i in range(1, height)]



for i in range(len(pizza)):
    msg = ""
    for j in range(len(pizza[i])):
        if (i, j) not in max_coords:
            msg += pizza[i][j]
        else:
            msg += 'X'
    print(msg)

















