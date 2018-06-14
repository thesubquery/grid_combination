# Generate all possible shapes
import copy
def gen_shapes(n):
    directions = {
        0 : [ -1,  0 ], #up
        1 : [ +1,  0 ], #down
        2 : [  0, -1 ], #left
        3 : [  0, +1 ] #right
    }    
    init = [[[0, 0]]]
    for step in range(n-1):
        new_list = []
        for shape in range(0, len(init)):
            for point in range(0, len(init[shape])):
                new_point = init[shape][point]
                for d in range(0, 4):
                    actual = copy.deepcopy(init[shape])
                    x = new_point[0] + directions[d][0]
                    y = new_point[1] + directions[d][1]
                    found = False
                    for each_point in actual:
                        if each_point == [x, y]:
                            found = True
                    if found == False:
                        actual.append([x, y])
                        new_list.append(actual)
        init = copy.deepcopy(new_list)
    return init


def unique_shapes(shape):
    
    list_of_shapes_in_strings = []
    
    # For each list of grid cells or shape
    for i in range(len(shape)):
        min_x = shape[i][0][0]
        min_y = shape[i][0][1]
        # For each grid cell in the shape
        new_string = ""
        for j in range(len(shape[i])):
            new_x = shape[i][j][0]
            new_y = shape[i][j][1]
            
            if new_x < min_x:
                min_x = new_x
            if new_y < min_y:
                min_y = new_y
                    
        for j in range(len(shape[i])):
            shape[i][j][0] -= min_x
            shape[i][j][1] -= min_y
                
        shape[i].sort()
        for j in range(len(shape[i])):
            new_string += str(shape[i][j][0]) + "," + str(shape[i][j][1]) + ","            

        list_of_shapes_in_strings.append(new_string)
    
    new_list = list(set(list_of_shapes_in_strings))
    new_list.sort()
    new_shape_list = []
    for i in range(len(new_list)):
        new_shape = []
        shape_coord = new_list[i].split(sep=",")
        shape_coord.pop()
        for j in range(0, len(shape_coord), 2):
            x = int(shape_coord[j])
            y = int(shape_coord[j+1])
            new_shape.append([x, y])
        new_shape_list.append(new_shape)
            
    
    return new_shape_list

def gen_world(x, y):
    l = [ ['   ' for i in range(y)] for j in range(x)]
    return l 


def display_shapes(shape, offset=False):
    world_offset = len(shape[0])
    grid_offset = 0
    if offset:
        grid_offset = world_offset
        world_offset *= 2
    for i in range(len(shape)):
        world = gen_world(world_offset, world_offset)
        for t in range(len(shape[i])):
            
            x1 = shape[i][t][0] + grid_offset
            y1 = shape[i][t][1] + grid_offset
            
            world[x1][y1] = '[]'
        for t in range(len(world)):
            row = ""
            for r in range(len(world[t])):
                row += world[t][r]
            print(row)
        print('\n')
         
def write_to_file(shape, filename= "test.txt", offset=False):
    with open(filename, "a") as f:
        f.write("***********************")
        f.write("\n")
        f.write("******Shape :**********")
        f.write("\n")
        f.write("***********************")
        f.write("\n")
        world_offset = len(shape[0])
        grid_offset = 0
        if offset:
            grid_offset = world_offset
            world_offset *= 2
        for i in range(len(shape)):
            world = gen_world(world_offset, world_offset)
            for t in range(len(shape[i])):
                
                x1 = shape[i][t][0] + grid_offset
                y1 = shape[i][t][1] + grid_offset
                
                world[x1][y1] = '[]'
            for t in range(len(world)):
                row = ""
                for r in range(len(world[t])):
                    row += world[t][r]
                f.write(row) #print(row)
                f.write("\n")
            f.write("\n") #print('\n')
        f.write("***********************")
        f.write("\n")
results = []
shapes = []
for i in range(1, 9):
    shapes.append(unique_shapes(gen_shapes(i)))
    results.append(len(shapes[i-1]))

#for i in range(len(shapes)):
#    display_shapes(shapes[i])
#    
