'''Life class module'''
import numpy

class Life():
    '''Life class'''
    def __init__(self, rows=100, columns=100, population=10):
        self.columns = columns
        self.last_column = self.columns - 1
        self.rows = rows
        self.last_row = self.rows - 1
        self.all = self.rows * self.columns
        self.population = population
        self.A = self.gen_population()
        self.B = numpy.zeros_like(self.A)
        self.C = numpy.zeros_like(self.A)
        self.D = numpy.zeros_like(self.A)
        self.E = numpy.zeros_like(self.A)
        self.cycles = 0
        self.stabilized = False
        self.stabilized_at = -1
    
    def reset(self):
        '''reset life'''
        self.A = self.gen_population()
        self.stabilized = False
        self.cycles = 0
        self.stabilized_at = -1

    def increase_population(self, val=5):
        '''increase population value'''
        if self.cycles == 0:
            self.population += val
            if self.population > 100:
                self.population = 100
            self.reset()

    def decrease_population(self, val=5):
        '''decrease population value'''
        if self.cycles == 0 and self.population > val:
            self.population -= val
            if self.population <= 0:
                self.population = val
            self.reset()

    def gen_population(self):
        '''generates random population'''
        s = self.columns * self.rows
        i = int(s * (self.population / 100))
        X = numpy.array([2]*i+[0]*(s-i), int)
        numpy.random.shuffle(X)
        return X.reshape([self.columns, self.rows])
        
    def next(self):
        '''calculates one cycle of life'''
        numpy.copyto(self.C, self.A)
        self.B = numpy.zeros_like(self.A)

        for i in range(self.A.shape[0]):

            for j in range(self.A.shape[1]):

                col1 = i - 1
                if col1 < 0:
                    col1 = self.last_column
                col2 = i + 1
                if col2 >= self.columns:
                    col2 = 0
                row1 = j - 1
                if row1 < 0:
                    row1 = self.last_row
                row2 = j + 1
                if row2 >= self.rows:
                    row2 = 0
                
                n = 0
                
                if self.A[col1, row1] > 0:
                    n += 1
                if self.A[col1, j] > 0:
                    n += 1
                if self.A[col1, row2] > 0:
                    n += 1
                if self.A[i, row1] > 0:
                    n += 1
                if self.A[i, row2] > 0:
                    n += 1
                if self.A[col2, row1] > 0:
                    n += 1
                if self.A[col2, j] > 0:
                    n += 1
                if self.A[col2, row2] > 0:
                    n += 1
                
                if self.A[i, j] == 0 and n == 3:
                    self.B[i, j] = n
                if self.A[i, j] > 0 and (n > 1 and n < 4):
                    self.B[i, j] = n
        
        self.A = self.B
        self.cycles += 1

        self.D = self.C + self.A
        if not numpy.array_equal(self.D, self.E):
            numpy.copyto(self.E, self.D)
        else:
            self.stabilized = True
            self.stabilized_at = self.cycles-1
