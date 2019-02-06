# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:18:40 2019

@author: CLAM
"""
import gc
gc.collect()



class SHAPE:
    def __init__(self, ID):
        self.ID                 = ID
        self.coordinates        = (0, 0)
        self.cells              = set()
        self.neighboring_cells  = {}
        self.neighboring_shapes = {}
    def __repr__(self):
        msg  = "ID:{} Coordinate(s): ".format(self.ID)
        for c in self.coordinates:
            msg += "{}, ".format(c)
        return msg

class CELL:
    def __init__(self, ID):
        self.ID                 = ID
        self.coordinates        = (0, 0)
        self.shapes             = set()
        self.neighboring_cells  = {}
        self.neighboring_shapes = {}
    def __repr__(self):
        msg = "ID[{}] Coordinate: ({}, {})".format(self.ID, self.coordinates[0], self.coordinates[1])
        return msg

def gen_shape(size):
    world = [['.' for j in range(size)] for i in range(size)]
    data = {}
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            if i * j == size:
                data[(i, j)] = {}
#                print(i, j)
                for k in range(i):
                    for l in range(j):
                        data[(i, j)][(k, l)] = None
#                        print("\t{}, {}".format(k, l))
    return data

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent      = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar          = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()    
        
        
        
lines = []
with open(r"C:\Users\clam\Desktop\HashCode_Pizza\grid_combination\Google Hash Code\d_big.in", "r") as f:
    lines = f.readlines()        
lines = [ l.replace("\n", "") for l in lines]

headings = lines[0].split(" ")
headings = [int(h) for h in headings]


height    = headings[0]
width     = headings[1]
t_minimum = headings[2]
m_minimum = headings[2]
min_slice = headings[2] * 2
max_slice = headings[3]

pizza     = [[lines[i][j] for j in range(width)] for i in range(1, height + 1)]
world     = [[lines[i][j] for j in range(width)] for i in range(1, height + 1)]


slice_by_coord = {}
slice_by_index = {}
cells_by_coord = {}
cells_by_index = {}

iteration = 1
for i in range(height):
    for j in range(width):
        cell                      = CELL(iteration)
        cell.coordinates          = (i, j)
        cells_by_index[iteration] = cell
        world[i][j]               = cell
        iteration += 1

data = {}
for size in range(min_slice, max_slice+1):
    data[size] = gen_shape(size)

# Generate unique list of shapes

def gen_shapes1(height, width):    
    total = height * width
    list_of_shapes = set()
    for x1 in range(height):
        for y1 in range(width):
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
                        else:
                            break
                    # Valid slice
                    if counter['T'] >= t_minimum and counter['M'] >= m_minimum and (counter['T'] + counter['M'] == size):
                        list_of_shapes.add(tuple(coords))
        printProgressBar(world[x1][y1].ID, total)
    print("\n")

def gen_shapes2(height, width):    
    total = height * width
    list_of_shapes = []
    for x1 in range(height):
        for y1 in range(width):
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
                        else:
                            break                            
                    # Valid slice
                    if counter['T'] >= t_minimum and counter['M'] >= m_minimum and (counter['T'] + counter['M'] == size):
                        list_of_shapes.append(tuple(coords))
        printProgressBar(world[x1][y1].ID, total)        
    list_of_shapes = list(set(list_of_shapes))
    print("\n")

len(list_of_shapes)








len(pizza)
len(pizza[0])
pizza[0]







    



    

slice_by_coord = {}
slice_by_index = {}
cells_by_coord = {}
cells_by_index = {}

# Create cell nodes
iteration = 1
for x1 in range(len(pizza)):
    for y1 in range(len(pizza[0])):
        c = CELL(iteration)
        c.coordinates = (x1, y1)
        cells_by_coord[c.coordinates] = c
        cells_by_index[iteration] = c
        iteration += 1

# Link cell nodes to each other
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
                neighbor = cells_by_coord[(x2, y2)]
                cells_by_coord[(x1, y1)].neighboring_cells[neighbor.ID] = neighbor

#
#for i in range(1, len(cells_by_index)+1):
#    print("[{}] Number of Links: {}".format(cells_by_index[i].ID, len(cells_by_index[i].neighboring_cells)))






# Link each coordinate to a shape
for x1 in range(height):
    for y1 in range(width):
        slice_by_coord[(x1, y1)] = {}


# Create a unique index number and link it to a shape node
iteration = 1
for s in list_of_shapes:    
    shape                     = SHAPE(iteration)
    shape.coordinates         = [each for each in s]
    slice_by_index[iteration] = shape
    
    for c in shape.coordinates:
        cell                         = cells_by_coord[c]
        slice_by_coord[c][iteration] = shape
        shape.cells[cell.ID]         = cell
        cell.shapes[iteration]       = shape

    for c in shape.cells:
        cell = shape.cells[c]
        for index in cell.neighboring_cells:
            n_cell = cell.neighboring_cells[index]
            if n_cell.ID not in shape.cells:
                shape.neighboring_cells[n_cell.ID] = n_cell
    iteration += 1

# Find the neighboring shapes that don't overlap with itself
    
    
#neighbors = {}
    
#len(slice_by_index) + 1
def n_shapes1(size):
    import datetime as dt
    total     = len(slice_by_index) + 1
    starttime = dt.datetime.now()
    for i in range(1, size):
        shape                    = slice_by_index[i]
        # Cells that make up the shape
        cell_ids                 = {key: None for key in shape.cells}
        # Shapes that overlap the cells
        remove_IDs               = {key: None for index in cell_ids for key in cells_by_index[index].shapes}
        

#neighbors = {}
def n_shapes2(size):
    import datetime as dt
    total     = len(slice_by_index) + 1
    starttime = dt.datetime.now()
    for i in range(1, size):
        shape                    = slice_by_index[i]
        # Shapes that overlap the cells
        remove_IDs               = {key: None for index in shape.cells for key in shape.cells[index].shapes}



arr1 = [each for each in range(1000000)]
dic1 = {each: None for each in range(1000000)}

class NODE:
    def __init__(self, ID):
        self.ID   = ID
        self.link = None
        
chain = [NODE(each) for each in range(1000000)]

for i in range(1000000):
    
    next_link = (i + 1) % (1000000 - 1)
    
    chain[i].link = chain[next_link]

chain[0].link

def traverse_linkedlist(ll):
    node = ll[0]
    for i in range(1000000):
        node = node.link

def traverse_array(arr):
    for i in range(1000000):
        arr[i]



s = set()
d1 = {}
d2 = {}
import gc
gc.collect()

size = 1000000

def add_set(size):
    s = set()
    for i in range(size):
        s.add(i)

def add_dic1(size):
    d = {}
    for i in range(size):
        d[i] = None

def add_dic2(size):
    d = {i: None for i in range(size)}


def get_set(size, s):
    for i in range(size):
        s.add(i)

A = set()
B = set()

for i in range(500000):
    A.add(i)
    
    
    
for i in range(500000-1, 1000000):
    B.add(i)


def set_intersect(A, B):
    A.intersection(B)

C = A - B

len(C)

A_dict = {i: None for i in range(500000)}
B_dict = {i: None for i in range(500000-1, 1000000)}
def dic_intersect(A_dict, B_dict):
    C_dict = {i: None for i in range(1000000) if i in A_dict and i in B_dict}
       
        
    # Neighboring cells
    n_cell_ids               = {key: None for key in shape.neighboring_cells}
    # Shapes that overlap neighboring cells
    keep_IDs                 = {key: None for index in n_cell_ids for key in shape.neighboring_cells[index].shapes}
    # Get neighboring shapes that don't overlap with existing cells
    shape.neighboring_shapes = {key: None for key in keep_IDs if key not in remove_IDs}
    
    
#    neighbors[i]             = shape.neighboring_shapes
    if i % (len(slice_by_index) // 5 - 1) == 0:
        time = dt.datetime.now() - starttime
        msg  = "{} / {}\t{}".format(i, total, time.total_seconds() / 60)        
        printProgressBar(i, total, suffix = msg)
    
#    for n in shape.neighboring_shapes:
#        neighbors[i][n] = None



# Check all neighboring shapes for overlap.
for i in range(1, len(slice_by_index)+1):
    shape = slice_by_index[1]
    for shape_num in shape.neighboring_shapes:
        n_shape = slice_by_index[shape_num]
        coords  = n_shape.coordinates
        for c in coords:
            if c in shape.coordinates:
                print(i)


slice_by_coord[(5, 0)]







sizes     = {i: len(slice_by_index[i].coordinates) for i in range(1, len(slice_by_index) + 1)}
# Find cell with smallest number of shapes
cell_shape_count = {}
min_count        = len(slice_by_index)
coords           = []
for i in range(1, len(cells_by_index) + 1):
    cell  = cells_by_index[i]
    count = len(cell.shapes)
    if count not in cell_shape_count:
        cell_shape_count[count] = {}
    cell_shape_count[count][cell.ID] = cell
    if count < min_count:
        min_count = count
        coords = [cell.coordinates]
    elif count == min_count:
        coords.append(cell.coordinates)

min_shapes = {}
for each in cell_shape_count[7]:
    cell = cells_by_index[each]
    for index in cell.shapes:
        min_shapes[index] = None
len(min_shapes)


# Find maximum number of slices
queue     = [[sizes[key], [key], len(slice_by_index[key].coordinates)] for key in min_shapes]
queue.sort()
final     = []
max_total = 0
count     = len(queue)
num_cells = height * width
starttime = dt.datetime.now()
visited_combinations = {}


while queue:
    record   = queue.pop(-1)
    total    = record[0]
    arr      = record[1]
    arr.sort()
    unique_id = tuple(arr)
    if unique_id not in visited_combinations:
        visited_combinations[unique_id] = None
        o_shapes  = {s: None for i in arr for c in slice_by_index[i].cells for s in slice_by_index[i].cells[c].shapes}
        n_shapes  = {n: None for i in arr for n in slice_by_index[i].neighboring_shapes if n not in arr and n not in o_shapes}
        
#        if len(n_shapes) > 1:
#            greatest = [[sizes[key], key] for key in n_shapes]
#            greatest.sort()
#            
#            flag = False
#            while greatest and flag == False:
#                next_elem = greatest.pop(-1)
#                append    = next_elem[1]
#                new_arr   = arr + [append]
#                new_arr.sort()
#                if tuple(new_arr) not in visited_combinations:
#                    flag = True
#                    break
#            
#            if flag:
#                count  += 1
#                key     = append
#                score   = sizes[key] + total
#                if score < num_cells:
#                    queue += [[total, [each for each in arr]], [score, [each for each in arr] + [key]]]
#                elif score == num_cells:
#                    final.append(arr + [key])
#                if max_total < score <= num_cells:
#                    max_total = sizes[key] + total
#                    final     = [each for each in arr] + [key]
#        elif len(n_shapes) == 1:
#            count += 1
#            key = list(n_shapes.keys())[0]
#            score = sizes[key] + total
#            if score < num_cells:
#                queue += [[score, [each for each in arr] + [key]]]
#            elif score == num_cells:
#                final.append(arr + [key])
#            if max_total < score <= num_cells:
#                max_total = sizes[key] + total

        
        new_queue = []
        for i in n_shapes:
            count += 1
            score  = sizes[i] + total
            if score < num_cells:
                new_queue.append([score, [each for each in arr] + [i]])
            elif score == num_cells:
                final.append([each for each in arr] + [i])
                queue     = []
                new_queue = []
            if max_total < score <= num_cells:
                max_total = sizes[i] + total
                final     = [each for each in arr] + [i]
        new_queue.sort()
        queue = new_queue

        time = dt.datetime.now() - starttime
        msg  = "{} / {}\t{}\t{}".format(len(queue), count, max_total, time)        
        printProgressBar(len(queue), count, suffix = msg)
        gc.collect()
    
        if len(queue) % 5 == 0:
            sorted(queue)
            time = dt.datetime.now() - starttime
            msg  = "{} / {}\t{}\t{}".format(count - len(queue), count, max_total, time)        
            printProgressBar(count - len(queue), count, suffix = msg)


























arr = [74, 140, 131, 84, 102, 96, 89, 103, 78, 114]
cells = []
for i in arr:
    shape = slice_by_index[i]
    for c in shape.coordinates:
        cells.append(c)

cells = list(set(cells))
len(cells)




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


    
    


world = [[lines[i][j] for j in range(width)] for i in range(1, height)]



for i in range(len(pizza)):
    msg = ""
    for j in range(len(pizza[i])):
        if (i, j) not in max_coords:
            msg += pizza[i][j]
        else:
            msg += 'X'
    print(msg)

















