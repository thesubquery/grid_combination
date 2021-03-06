# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:18:40 2019

@author: CLAM
"""

import gc
import os
import datetime as dt
gc.collect()
import numpy as np
os.chdir(r'C:\Users\clam\Desktop\HashCode_Pizza\grid_combination')


class SHAPE:
    def __init__(self, ID):
        self.ID                 = ID
        self.coordinates        = (0, 0)
        self.cells              = set()
        self.neighboring_cells  = set()
        self.neighboring_shapes = set()
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
        self.neighboring_cells  = set()
        self.neighboring_shapes = set()
    def __repr__(self):
        msg = "ID[{}] Coordinate: ({}, {})".format(self.ID, self.coordinates[0], self.coordinates[1])
        return msg

class BOARD:
    def __init__(self, filepath):
        self.filepath  = filepath
        self.height    = None
        self.width     = None
        self.t_minimum = None
        self.m_minimum = None
        self.min_slice = None
        self.max_slice = None
        self.shape_dim = None
        self.board     = None

        self.slice_by_coord = {}
        self.slice_by_index = {}
        self.cells_by_coord = {}
        self.cells_by_index = {}
    
    def __repr__(self):
        msg  = "Pizza Size: {} by {}\n".format(self.height, self.width)
        msg += "Minimum {} Tomates and Mushrooms per Slice\n".format(self.t_minimum)
        msg += "Slice: Min [{}] Max [{}]\n".format(self.min_slice, self.max_slice)
        
        msg += "Slice Dimensions:\n"
        for size in self.shape_dim:
            msg += "  Size: {}\n".format(size)
            for dim in self.shape_dim[size]:
                msg += "    Dimensions: {}\n".format(dim)
#                msg += "      Coordinates:\n".format(dim)
#                for coord in self.shape_dim[size][dim]:
#                    msg += "      {}\n".format(coord)
                    
        return msg
    
    def load_file(self, file):
        
        function_start = dt.datetime.now()
        print("START OF load_files(): {}\n".format(function_start))

        # Read in files
        mod_start = dt.datetime.now()
        print("{}: Read in files".format(mod_start))
        lines = []
        with open(self.filepath + '\\' + file, "r") as f:
            lines = f.readlines()        
        lines = [ l.replace("\n", "") for l in lines]
        headings = lines[0].split(" ")
        headings = [int(h) for h in headings]
        self.height    = headings[0]
        self.width     = headings[1]
        self.t_minimum = headings[2]
        self.m_minimum = headings[2]
        self.min_slice = headings[2] * 2
        self.max_slice = headings[3]
        self.shape_dim = self.gen_shape(self.min_slice, self.max_slice)
        self.board     = [[lines[i][j] for j in range(self.width)] for i in range(1, self.height + 1)]
        self.board2    = [[lines[i][j] for j in range(self.width)] for i in range(1, self.height + 1)]
        print("{}: Completed\n".format(dt.datetime.now() - mod_start))
        

        # Create CELL nodes and references
        mod_start = dt.datetime.now()
        print("{}: Create CELL nodes and references".format(mod_start))      
        num = 1
        for i in range(self.height):
            for j in range(self.width):
                cell                     = CELL(num)
                cell.coordinates         = (i, j)
                self.cells_by_index[num] = cell
                self.board2[i][j]        = cell
                num                     += 1
        print("{}: Completed\n".format(dt.datetime.now() - mod_start))
        
        
        # Generate unique list of shapes
        mod_start = dt.datetime.now()
        print("{}: Generate unique list of shapes".format(mod_start))          
        total = self.height * self.width
        self.list_of_shapes = set()
        for x1 in range(self.height):
            for y1 in range(self.width):
                for size in self.shape_dim:
                    for dim in self.shape_dim[size]:
                        
                        counter = {'T': 0, 'M': 0}
                        coords  = []
                        for piece in self.shape_dim[size][dim]:
                            x2 = piece[0]
                            y2 = piece[1]
                            x3 = x1 + x2
                            y3 = y1 + y2
                            if 0 <= x3 < self.height and 0 <= y3 < self.width:
                                counter[self.board[x3][y3]] += 1
                                coords.append((x3, y3))
                            else:
                                break
                        # Valid slice
                        if counter['T'] >= self.t_minimum and counter['M'] >= self.m_minimum and (counter['T'] + counter['M'] == size):
                            coords.sort()
                            self.list_of_shapes.add(tuple(coords))
            self.printProgressBar(self.board2[x1][y1].ID, total, length=50)
        print("{}: Completed".format(dt.datetime.now() - mod_start))
        
        # Link cells to neighbor cells
        mod_start = dt.datetime.now()
        print("{}: Link cells to neighbor cells".format(mod_start))         
        for x1 in range(self.height):
            for y1 in range(self.width):
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
                    if 0 <= x2 < self.height and 0 <= y2 < self.width and not (x1 == x2 and y1 == y2):
                        neighbor = self.board2[x2][y2]
                        self.board2[x1][y1].neighboring_cells.add(neighbor)
        print("{}: Completed\n".format(dt.datetime.now() - mod_start))
                
        # Create a unique index number and link it to a shape node
        mod_start = dt.datetime.now()
        print("{}: Create a unique index number and link it to a shape node\n".format(mod_start))          
        iteration = 1
        total     = len(self.list_of_shapes)
        for s in self.list_of_shapes:    
            shape                          = SHAPE(iteration)
            shape.coordinates              = [each for each in s]
            self.slice_by_index[iteration] = shape
            
            for c in shape.coordinates:
                cell                       = self.board2[c[0]][c[1]]
                shape.cells.add(cell)
                cell.shapes.add(shape)
        
            for cell in shape.cells:
                for n_cell in cell.neighboring_cells:
                    shape.neighboring_cells.add(n_cell)
            iteration += 1
            msg  = "{} / {}\t{}".format(iteration, total, dt.datetime.now() - mod_start)        
            self.printProgressBar(iteration, total, suffix = msg, length=50)
            
        print("\n{}: Completed\n".format(dt.datetime.now() - mod_start))

        # Link shapes to neighboring shapes
#        mod_start = dt.datetime.now()
#        print("{}: Link shapes to neighboring shapes\n".format(mod_start))              
#        size      = len(self.slice_by_index)
#        total     = len(self.slice_by_index) + 1
#        for i in range(1, size):
#            
#            shape      = self.slice_by_index[i]
#            # Shapes that overlap the cells
#            remove_IDs = set(shape for cell in shape.cells for shape in cell.shapes)
#            # Shapes that overlap neighboring cells
#            keep_IDs   = set(shape for n_cell in shape.neighboring_cells for shape in n_cell.shapes)
#            # Get neighboring shapes that don't overlap with existing cells
#            keep_IDs   = set(keep_IDs) - set(remove_IDs)
#            
#            for each in keep_IDs:
#                shape.neighboring_shapes.add(each)
#            
#            msg  = "{} / {}\t{}".format(i, total, dt.datetime.now() - mod_start)        
#            self.printProgressBar(i, total, suffix = msg, length=50)
#            
#        time = dt.datetime.now() - mod_start
#        print("\n{}: Completed\n".format(time.total_seconds() / 60))
        
        print(self)
        
    def gen_shape(self, min_slice, max_slice):
        
        data = {}
        
        for size in range(min_slice, max_slice+1):
            data[size] = {}
            for i in range(1, size + 1):
                for j in range(1, size + 1):
                    if i * j == size:
                        data[size][(i, j)] = {}
                        for k in range(i):
                            for l in range(j):
                                data[size][(i, j)][(k, l)] = None
        return data

    def printProgressBar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        percent      = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar          = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total:
            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        else:
            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    def run_diagnostics(self):
        # Diagnostics
        
        # Check cell count
        if len(self.cells_by_index) == self.width * self.height:
            print(True)
        
        # Check neighboring cells
        size = self.width * self.height
        for i in range(1, size + 1):
            cell = self.cells_by_index[i]
            x1   = cell.coordinates[0]
            y1   = cell.coordinates[1]
            for n in cell.neighboring_cells:
                coord = n.coordinates
                x2    = coord[0]
                y2    = coord[1]
                if x1 == x2 and y1 == y2:
                    print(True)
                    break
        
        # Check if all shape coordinates are linked to the right cells
        for i in range(1, len(self.slice_by_index) + 1):
            shape = self.slice_by_index[i]
            coord = list(shape.coordinates)
            cells = [cell.coordinates for cell in shape.cells]
            for row in coord:
                x1 = row[0]
                y1 = row[1]
                if (x1, y1) not in cells:
                    print(True)
                    break
            for row in cells:
                x1 = row[0]
                y1 = row[1]
                if (x1, y1) not in coord:
                    print(True)
                    break
                
    def get_cell_by_id(self, x, y):
        return self.board2[x][y]
    
def save_map(board, visited, shape, filename):
    
    file = 'data.txt'
    
    world = [['X' if (x, y) in visited else board.board[x][y] for y in range(board.width)] for x in range(board.height)]
    for each in shape.coordinates:
        world[each[0]][each[1]] = '*'
    
    with open(file, 'a+') as f:
        f.write(filename + '\n')
        for each in world:
            msg = "".join(each)
            f.write(msg + "\n")
        f.write('\n\n')
            
def find_islands(visited, shape, max_x, max_y):
    visited = {each: None for each in visited}
    
    coords  = shape.coordinates
    for c in coords:
        visited[c] = None
        
        
#    world   = [['X' if (x, y) in visited else '*' for y in range(max_y+1)] for x in range(max_x+1)]
    queue   = [[x, y] for x in range(max_x+1) for y in range(max_y+1) if (x, y) not in visited]
    SCC     = {}
#    len(SCC) len(queue)
    if queue:
        queue   = [queue[0]]
        island  = []        
        while queue:
            coord = queue.pop(0)
            if tuple(coord) not in visited and tuple(coord) not in SCC:
#                print(True)
                SCC[tuple(coord)] = None
                x = coord[0]
                y = coord[1]
                neighbors = pizza.get_cell_by_id(x, y).neighboring_cells
    
                # Check if at least one neighbor is not in visited
                proceed = False
                for n_cell in neighbors:
                    n_coords = n_cell.coordinates
                    x2 = n_coords[0]
                    y2 = n_coords[1]    
                    if x2 <= max_x and y2 <= max_y:
                        queue.append([x2, y2])
    if len(SCC) == len([[1, [[x, y]]] for x in range(max_x+1) for y in range(max_y+1) if (x, y) not in visited]):
        return False
    else:
        return True




    
    
filepath = r"C:\Users\clam\Desktop\HashCode_Pizza\grid_combination\Google Hash Code"
file     = "c_medium.in"
pizza    = BOARD(filepath)
pizza.load_file(file)





size = pizza.height * pizza.width

cell_sol_count = {}
for i in range(1, size + 1):
    cell = pizza.cells_by_index[i]
    count = len(cell.shapes)
    if count not in cell_sol_count:
        cell_sol_count[count] = []
    cell_sol_count[count].append(i)

    
cell_sol_count[min(list(cell_sol_count.keys()))]

visited        = {}
queue          = [pizza.cells_by_index[i].coordinates for i in cell_sol_count[min(list(cell_sol_count.keys()))]] + [pizza.cells_by_index[i].coordinates for i in pizza.cells_by_index]
total          = len(queue)
islands        = []
run            = True
coord_history  = []
restricted     = {}
iteration      = 1
gc.collect()
starttime = dt.datetime.now()
print("START RUN()")
while queue and run:


    coord  = queue.pop(0)
    
    if coord not in visited:
        iteration += 1
        cell   = pizza.get_cell_by_id(coord[0], coord[1])
        shapes = list(cell.shapes)
        
        max_x = pizza.height - 1
        max_y = pizza.width - 1
#        max_x = 0
#        max_y = 0
#        for each in visited:
#            x = each[0]
#            y = each[1]
#            max_x = max(x, max_x)
#            max_y = max(y, max_y)
        
        shape_found = False
        for shape in shapes:
            
            proceed = True
            
            if shape.ID in restricted:
                proceed = False
            
            # Check if the cells of the shape is available
            if proceed:
                for points in shape.coordinates:
                    if points in visited:
                        proceed = False
                        break
            
            # Check if an island has formed
            if proceed and coord != (0, 0):
#                starttime = dt.datetime.now()
                
                pre_total = len(visited)
                islands   = find_islands(visited, shape, max_x, max_y)
                
#                msg       = "Coord: {} ShapeID: {}\t{}".format(coord, shape.ID, dt.datetime.now() - starttime)
#                pizza.printProgressBar(total - len(queue), total, length = 50, suffix = msg)
                
                if pre_total != len(visited):
                    print("Visited Changed!")
                    proceed = False
                    break
                if islands:
                    filename = '{} - ({}, {}) shapeID:{} Action: {}'.format(iteration, coord[0], coord[1], shape.ID, 'Found Island')
                    save_map(pizza, visited, shape, filename)
                    proceed = False
                    break
            
            if proceed:
                filename = '{} - ({}, {}) shapeID:{} Action: {}'.format(iteration, coord[0], coord[1], shape.ID, 'Added Shape')
                save_map(pizza, visited, shape, filename)                
                shape_found = True
                for points in shape.coordinates:
                    visited[points] = shape
                restricted = {}
                break

            msg  = "Coord: {} ShapeID: {}\t{}".format(coord, shape.ID, dt.datetime.now() - starttime)
            pizza.printProgressBar(total - len(queue), total, length = 50, suffix = msg)
            
        if shape_found == False:
            
            # Find neighboring cells
            cell              = pizza.get_cell_by_id(coord[0], coord[1])
            neighboring_cells = [each for each in cell.neighboring_cells if each.coordinates in visited]
            
            # Which one has a shape in visited
            shape = None
            
            neighboring_cells = list(np.random.choice(neighboring_cells, len(neighboring_cells), replace = False))
            
            for each in neighboring_cells:
                if each.coordinates in visited:
                    # Put shape in restricted list
                    shape = visited[each.coordinates]
                    restricted[shape.ID] = shape
                    # Remove shape
                    for each in shape.cells:
                        if each.coordinates in visited:
                            del visited[each.coordinates]
                        else:
                            print("Shape not in visited!!")
                    filename = '{} - ({}, {}) shapeID:{} Action: {}'.format(iteration, coord[0], coord[1], shape.ID, 'Removed Shape')
                    save_map(pizza, visited, shape, filename)                               
                    break            
            # Restart queue
            queue = [pizza.cells_by_index[i].coordinates for i in pizza.cells_by_index]

        else:
            coord_history.append(coord)
            
print(coord, len(visited))
islands = find_islands(visited, shape, max_x, max_y)
print(islands)
print(len(visited))


shape

print("Covered area: {} / {} {}".format(len(visited), total, len(visited)/total))




















world = [['X' if (x, y) in visited else '*' for y in range(pizza.width)] for x in range(pizza.height)]

os.chdir(r'C:\Users\clam\Desktop\HashCode_Pizza\grid_combination')

with open("results.txt", 'w+') as f:
    for each in world:
        msg = "".join(each)
        f.write(msg + "\n")

visited[(13, 135)]

pizza.width

len(visited)


shapes = cell.shapes

for shape in shapes:
    flag = False
    for c in shape.coordinates:
        if c in visited:
            flag = True
            break
    if flag == False:
        print(shape)


























count = {}
for each in pizza.cells_by_index:
    cell = pizza.cells_by_index[each]
    if len(cell.shapes) not in count:
        count[len(cell.shapes)] = 0
    count[len(cell.shapes)] += 1

count = {}
for each in pizza.slice_by_index:
    shape = pizza.slice_by_index[each]
    count[shape.ID] = len(shape.neighboring_shapes)





data = pizza.shape_dim
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

















