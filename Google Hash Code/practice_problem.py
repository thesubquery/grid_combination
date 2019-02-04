 
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

    def __repr__(self):
        return "This is a {} X {} cells pizza with {} mushrooms and {} tomato. \nThe requirement is minimum {} ingredients of each & max {} cells per slice ".format(
                self.num_rows, self.num_cols, self.num_M, self.num_T, self.min_i, self.max_size)

p = Pizza("medium")
print(p)
