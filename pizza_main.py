# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:18:40 2019

@author: CLAM
"""
import gc
gc.collect()


lines = []
with open(r"C:\Users\clam\Desktop\HashCode_Pizza\grid_combination\Google Hash Code\d_big.in", "r") as f:
    lines = f.readlines()        
lines = [ l.replace("\n", "") for l in lines]


height    = len(lines)
width     = len(lines[1])
t_minimum = 4
m_minimum = 4

pizza     = [[lines[i][j] for j in range(width)] for i in range(1, height)]



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
for size in range(8, 12 + 1):
    data[size] = gen_shape(size)
    


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


queue = []

for key in cells.keys():
    for shape in cells[key]:
        queue.append([len(shape), [c for c in shape]])

queue = sorted(queue, reverse=True)
max_size = 0
max_coords = []
total    = len(queue)
while queue:
    record  = queue.pop(0)
    count   = record[0]
    coords  = record[1]
    toCheck = [c2 for c1 in coords for c2 in surroundings[c1]]
    toCheck = list(set(toCheck))
    toCheck = [each for each in toCheck if each not in coords]
    toCheck = sorted(toCheck)
    
    for i in range(len(toCheck)):
        for new_shape in cells[toCheck[i]]:
            size       = len(new_shape)
            new_coords = [new_coord for new_coord in new_shape if new_coord not in coords]
            if len(new_coords) == size:
#                print("{} - {} - {}\t{}".format(i, toCheck[i], size, new_coords))
                coords = coords + new_coords
                count  = len(coords)
                queue.append([count, coords])
                total += 1
                if max_size < count:
                    max_size = count
                    max_coords = [c for c in coords]
                    msg = "{} / {} Max: {}".format(total - len(queue), total, max_size)
                    printProgressBar(total - len(queue), total, suffix = msg)
    queue = sorted(queue, reverse=True)
    
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent      = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar          = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()    
























