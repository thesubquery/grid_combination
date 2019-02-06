 
"""

The file consists of:
● one line containing the following natural numbers separated by single spaces:
    ○ R (1 ≤ R ≤ 1000) i s the number of rows,
    ○ C (1 ≤ C ≤ 1000) is the number of columns,
    ○ L (1 ≤ L ≤ 1000) i s the minimum number of each ingredient cells in a slice,
    ○ H (1 ≤ H ≤ 1000) i s the maximum total number of cells of a slice
● R lines describing the rows of the pizza (one row after another). Each of these lines contains C
characters describing the ingredients in the cells of the row (one cell after another). Each character
is either ‘M’ (for mushroom) or ‘T’ (for tomato).

Input  = R, C , L ,H

Goal : The goal is to cut correct slices out of the pizza maximizing the total number of cells in all slices.

"""
import copy

class Pizza:
    def __init__(self, file_size = "example"):
        self.file_size = file_size
        self.num_rows  = 1
        self.num_cols  = 1
        self.min_i     = 1
        self.max_size  = 1
        self.num_T     = 0
        self.num_M     = 0
        self.lines     = None
        self.pizza     = None
        self.load_data()
    
    def load_data(self):
        input_files = {
                "example" : "a_example.in",
                "small"   : "b_small.in",
                "medium"  : "c_medium.in",
                "big"     : "d_big.in"
                }
        
        with open(input_files[self.file_size], "r") as f:
            lines = f.readlines()        
        self.lines = [ l.replace("\n", "") for l in lines]

        requirments = self.lines[0]
        rows, columns, minimum_i, max_size = [int(x) for x in requirments.split(" ")]
        self.num_rows = rows
        self.num_cols = columns
        self.min_i    = minimum_i
        self.max_size = max_size
        self.pizza = [ [ cell for cell in line ] for line in self.lines[1:]]
        self.num_T = sum([r.count("T") for r in self.pizza])
        self.num_M = self.num_rows * self.num_cols - self.num_T

    def shapes(self):
        shapes = {}
        for each in range(self.min_i * 2 , self.max_size + 1 ):
            
            shapes[each] = Pizza.get_shape(each)
        return shapes
    def __repr__(self):
        return "This is a {} X {} cells pizza with {} mushrooms and {} tomato. \nThe requirement is minimum {} ingredients of each & max {} cells per slice ".format(
                self.num_rows, self.num_cols, self.num_M, self.num_T, self.min_i, self.max_size)
    
    @staticmethod
    def get_shape(size = 5 ):
        combinations = []
        for i in range(1, size+1):
            for j in range(1, size+1):
                if i * j == size :
                    combinations.append((i,j))
        data = {}
        for each in combinations:
            base = []
            for i in range(0, each[0]): 
                for j in range(0, each[1]): 
                    base.append((i,j))    
            data[each] = base
        return data
    
#    def empty_area(self):
#        area = []
#        for r in range(self.num_row):
#            for c in range(self.num_col):
#                

class Shape:
    def __init__(self, position, id_no = None , x = None, y = None):
        self.id_no    = id_no
        self.position = position
        self.size     = len(position)
        self.x        = x 
        self.y        = y
        self.flag     = False
    def __repr__(self):
        return "Shape ID {} - size of {} ".format(self.id_no, self.size)
    
    def __eq__(self, other):
        if self.id_no == other.id_no:
            if self.position == other.position:
                return True
        return False
    
    def placed(self):
        self.flag = True
    
    def copy(self, id_no, x, y):
        new_position = []
        for each in self.position:
            new_x = each[0] + x
            new_y = each[1] + y
            new_position.append((new_x, new_y))
            
        new_shape = Shape(new_position, id_no, x, y)
        
        return new_shape
#    def __del__(self):
#        print("deleted Shape ID {}".format(self.id_no))

        
        
        
class Cell:
    def __init__(self, x = None, y = None, ing_type = "T"):
        self.x            = x 
        self.y            = y
        self.id_no        = "{}_{}".format(x,y)
        self.type         = ing_type
        self.num_slices   = 0
        self.valid_cell   = True
        self.linked_cells = []
        self.shape_list   = {}
        self.actual_slice = None
        
    def reload(self):
        self.num_slices = len(self.shape_list)
        if self.actual_slice:
            self.valid_cell = False
            self.num_slices = 0
            
        if self.num_slices == 0:
            self.valid_cell = False

    def add_poss_slice(self, p_slice, s):
        if s.id_no not in self.shape_list:
            self.shape_list[s.id_no] = s 
            for c in p_slice:
                position = (c.x, c.y)
                self.add_linked_list(position)
                c.add_linked_list((self.x , self.y))
            self.reload()
    
    def check_cell(self):
        return self.valid_cell
    
    def add_linked_list(self, other_location):
        if other_location not in self.linked_cells:
            self.linked_cells.append(other_location)
    
    def __eq__(self, other):
        return self.id_no == other.id_no
    
    def __repr__(self):
        return "Cell at ({},{}) - contains number of possible slices : {}".format(self.x, self.y, self.num_slices)
    
    def _apply_slice(self, s):
        delete_shapes = list(self.shape_list.keys()) 
        delete_shapes = [ e for e in delete_shapes if e != s.id_no]
        self.actual_slice = s
        self.shape_list = {s.id_no : s}  
        self.reload()
        return delete_shapes
    
    def del_shape(self, s_id_no):
        if s_id_no in self.shape_list:
            del self.shape_list[s_id_no]
            self.reload()

        
    def copy(self):
        new_cell = Cell(self.x, self.y, self.type)
        new_cell.valid_cell = copy.deepcopy(self.valid_cell)
        new_cell.shape_list   = { e : self.shape_list[e] for e in self.shape_list}
        new_cell.linked_cells = [ c for c in self.linked_cells]

        new_cell.num_slices   = self.num_slices
        
        new_cell.actual_slice = self.actual_slice
        return new_cell
    
class World:
    def __init__(self, file_size = "example", world = False):
        self.file_size = file_size
        self.num_rows  = 1
        self.num_cols  = 1
        self.min_i     = 1
        self.max_size  = 1
        self.num_T     = 0
        self.num_M     = 0
        self.lines     = None
        self.pizza     = None
        self.world     = None
        
        self.shapes          = {}
        self.available_cells = {}
        self.taken = []
        if world == False:
            self.load_data()
     
    def copy(self):
        new_world = World(world = True) 
        new_world.num_rows = self.num_rows
        new_world.num_cols = self.num_cols
        new_world.min_i    = self.min_i
        new_world.max_size = self.max_size
        new_world.num_T    = self.num_T
        new_world.num_M    = self.num_M
        new_world.pizza    = copy.deepcopy(self.pizza)
        new_world.world    = {}
        
        new_world.shapes          = copy.deepcopy(self.shapes)
        new_world.available_cells = copy.deepcopy(self.available_cells)
        new_world.taken    = [e for e in self.taken]
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                new_world.world[(r,c)] = self.world[(r,c)]

        return new_world
    
    def load_data(self):
        input_files = {
                "example" : "a_example.in",
                "small"   : "b_small.in",
                "medium"  : "c_medium.in",
                "big"     : "d_big.in"
                }
        
        with open(input_files[self.file_size], "r") as f:
            lines = f.readlines()        
        self.lines    = [ l.replace("\n", "") for l in lines]

        requirments   = self.lines[0]
        rows, columns, minimum_i, max_size = [int(x) for x in requirments.split(" ")]
        self.num_rows = rows
        self.num_cols = columns
        self.min_i    = minimum_i
        self.max_size = max_size
        self.pizza    = [ [ cell for cell in line ] for line in self.lines[1:]]
        self.num_T    = sum([r.count("T") for r in self.pizza])
        self.num_M    = self.num_rows * self.num_cols - self.num_T
        self.load_cells()
        self.load_shapes()
    
    def load_cells(self):
        self.world = {}
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                cell_type         = self.pizza[r][c]
                cell              = Cell(r,c, cell_type)
                self.world[(r,c)] = cell
                self.available_cells[(r,c)] = 1
                
    def load_shapes(self):
        shapes = []
        for each in range(self.min_i * 2 , self.max_size + 1 ):
            combinations = World.get_shape(each)
            for shape in combinations:
                x , y = shape
                c = combinations[shape]
                s = Shape(c, x , y)
                shapes.append(s)
        self.fit_shapes(shapes)
    
    def fit_shapes(self, shapes):
        shape_count = 1
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                for s in shapes:
                    fitted ,combination = self.fit_cells(r,c,s)
                    if fitted: 
                        new_s = s.copy(shape_count, r, c )
                        self.shapes[shape_count] = new_s
                        shape_count += 1
                        for slices_cell in combination:
                            sc = self.world[(slices_cell.x,slices_cell.y)]
                            sc.add_poss_slice(combination, new_s)

    def fit_cells(self, x, y, s):
        # X Y are coordinates 
        # S is the shape object
        fitted = False
        temp_dict = {"T" : [] , "M" : []}
        for delta in s.position:
            new_x = x + delta[0]
            new_y = y + delta[1]
            if (0 <= new_x < self.num_rows) & (0 <= new_y < self.num_cols):
                ing_type = self.pizza[new_x][new_y]
                temp_dict[ing_type].append((new_x,new_y))
        count_t = len(temp_dict["T"])
        count_m = len(temp_dict["M"])
        combination = []
        #this is a valid shape
        if (count_t + count_m) == s.size: 
            if (count_m >= self.min_i) & (count_t >= self.min_i):
                fitted = True
                
                for each in temp_dict["T"]:
                    c_x , c_y  = each
                    other_cell = self.world[(c_x,c_y)]
                    combination.append(other_cell)
                for each in temp_dict["M"]:
                    c_x , c_y  = each
                    other_cell = self.world[(c_x,c_y)]
                    combination.append(other_cell)

        return fitted, combination
    
    def get_percentage(self, filled = False, print_flag = True):
        available_count = 0
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                cell = self.world[(r,c)]
                if cell.valid_cell:
                    available_count += 1
        if filled == False:
            percentage = (available_count/(self.num_rows * self.num_cols))* 100
            if print_flag:
                print("Percentage of the cell that is available: {0:.2f}%".format(percentage))
        else:
            available_count = len(self.taken)
            percentage = (available_count/(self.num_rows * self.num_cols))* 100
            if print_flag:
                print("Percentage of the cell that is filled : {0:.2f}%".format(percentage))
        return percentage

    def __repr__(self):
         return "This is a {} X {} cells pizza with {} mushrooms and {} tomato. \nThe requirement is minimum {} ingredients of each & max {} cells per slice ".format(
                self.num_rows, self.num_cols, self.num_M, self.num_T, self.min_i, self.max_size)
       
    def _valid_shape(self, s):
        locations = s.position
        count = 0 
        for each in locations:
            x, y = each 
            if (self.pizza[x][y] == "T") or (self.pizza[x][y] == "M"):
                count +=1 
                
        if count == len(locations):
            return True
        else:
            return False
#    def print_pizza(self):
#        for r in range(self.num_rows):
#            
    def apply_slice(self, s):
        w = self.copy()
        
        if w._valid_shape(s):
            for each in s.position:
                x, y = each 
                w.pizza[x][y] = s.id_no
                c = w.world[(x,y)]
                shape_to_delete = c._apply_slice(s)
                for e_id in shape_to_delete :
                    if e_id in w.shapes:
                        e = w.shapes[e_id]
                        for p in e.position:
                            other_cell = w.world[p]
                            other_cell.del_shape(s.id_no)
                    
                        del w.shapes[e_id]
                
                w.taken.append((x,y))
                
                del w.available_cells[(x,y)]
                
        else:
            for p in s.position:
                cell = w.world[p]
                cell.del_shape(s.id_no)
            if s.id_no in w.shapes:
                del w.shapes[s.id_no]
            
        return w 
            
    @staticmethod
    def get_shape(size = 5 ):
        combinations = []
        for i in range(1, size+1):
            for j in range(1, size+1):
                if i * j == size :
                    combinations.append((i,j))
        data = {}
        for each in combinations:
            base = []
            for i in range(0, each[0]): 
                for j in range(0, each[1]): 
                    base.append((i,j))    
            data[each] = base
        return data
        
#        
#p = Pizza("big")
#print(p)

w = World("small")
print(w)
#
w.get_percentage()
#
##class Player:
import numpy as np 
#chosen_shapes = np.random.choice([ i for i in range(1, 150)] , 10)
#
new_w = w.copy()
prev_A = new_w.get_percentage(filled = True)
sorted_list = sorted(new_w.world.keys() , key = lambda k : w.world[k].num_slices)
chosen_shape = list(new_w.world[sorted_list[0]].shape_list.keys())[0]
found = False
while found == False:
    if len(new_w.shapes) > 0:
        
        
        new_w = new_w.apply_slice(new_w.shapes[chosen_shape])
    
        A = new_w.get_percentage(filled = True, print_flag = True)
        new_w.get_percentage(filled = False, print_flag = True)
        if A == 100 :
            found = True
        if len(new_w.shapes) > 0 :
            chosen_shape = np.random.choice(list(new_w.shapes.keys()), 1)[0]
    else:
        found = True
#        new_w = w.copy()
#        print("This is a new one \n\t",)
#        prev_A = new_w.get_percentage(filled = True)
new_w.get_percentage(filled = True, print_flag = True)
#for each in new_w.pizza:
#    print(each)
#
#world = {}
#for i in range(p.num_rows):
#    for j in range(p.num_cols):
#        world[(i,j)] = {}
#        for s in shapes.values():
#            for shape in s.values():
#                count = {"T": 0 , "M" :0, "valid":0, "cells" : [] }
#                for each in shape:
#                    new_x = i + each[0]
#                    new_y = i + each[1]
#                    if (0<= new_x < p.num_rows) & (0 <= new_y < p.num_cols):
#                        count[p.pizza[new_x][new_y]] += 1
#                        count['cells'].append((new_x, new_y))
#                        count['valid'] += 1
#                if count['valid'] == len(shape):
#                    if (count["T"] >= p.min_i) & (count["M"] >= p.min_i):
#                        for c in count['cells'] :
#                            if c not in world[(i,j)]:
#                                world[(i,j)][c] = 0
#                            world[(i,j)][c] += 1
#world        
