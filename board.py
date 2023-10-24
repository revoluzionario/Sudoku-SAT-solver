import math
from pysat.formula import CNF

# Index helper function
def index(i, j, v, n):
    modulo = n**2 + 1
    return (modulo**2)*i + modulo*j + v

def decode(number, n):
    modulo = n**2 + 1
    v = number % modulo
    j = ((number - v)//modulo) % modulo
    i = number//(modulo**2)
    return i, j, v

# Product encoding helper
def at_most_one_encoding(maxVar: int, list_of_vars: list):
    formula = CNF()
    n = list_of_vars.__len__()
    if n <= 4:
        for i in range(0, n):
            for j in range(i+1, n):
                formula.append([-list_of_vars[i], -list_of_vars[j]])
        return formula
    p = math.ceil(math.sqrt(n))
    q = math.ceil(n/p)
    startVar = maxVar + 1
    
    xItr = 0
    for pvar in range(startVar, startVar+p):
        for qvar in range(startVar+p, startVar+p+q):
            formula.append([-list_of_vars[xItr], pvar])
            formula.append([-list_of_vars[xItr], qvar])
            xItr+=1
            if (xItr > list_of_vars.__len__() - 1):
                break
        if (xItr > list_of_vars.__len__() - 1):
            break
    formula.extend(at_most_one_encoding(formula.nv, [_p for _p in range(startVar, startVar+p)]))
    formula.extend(at_most_one_encoding(formula.nv, [_q for _q in range(startVar+p, startVar+p+q)]))
    return formula
    
class Board:
    def __init__(self, rawData: list[list[int]]):
        self.board = rawData
        self.size = rawData.__len__()
        self.boxSize = int(math.sqrt(self.size))
        self.clues = self.generateAssumption()
        self.product_encoding = self.productEncoding()
        self.binomial_encoding = self.binomialEncoding()
        self.solution = list()

    def checkValid(self):
        valid = True
        for i in range(0, self.size):
            if self.board[i].__len__ != self.size:
                valid = False
                break
        return valid
    
    def generateAssumption(self):
        clues = list()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    clues.append(index(i+1, j+1, self.board[i][j], self.boxSize))
        return clues

    def productEncoding(self):
        long_formula = CNF()
        # At lease one value in a cell.
        clause = list()
        for i in range(self.size):
            for j in range(self.size):
                for v in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()
        
        # Make sure that every value appear at least once in a row.
        for i in range(self.size):
            for v in range(self.size):
                for j in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()

        # Make sure that every value appear at least once in a column.
        for j in range(self.size):
            for v in range(self.size):
                for i in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()
        # Make sure that every value appear at least once in a n x n box.
        for v in range(self.size):
            for i in range(0, self.size, self.boxSize):
                for j in range(0, self.size, self.boxSize):
                    for k in range(self.boxSize):
                        for m in range(self.boxSize):
                            clause.append(index(i+k+1, j+m+1, v+1, self.boxSize))
                    long_formula.append(clause)
                    clause.clear()
        
        # Make sure that every value appear at most once in a cell.
        cell_literals_list = list()
        for i in range(self.size):
            for j in range(self.size):
                for v in range(self.size):
                    cell_literals_list.append(index(i+1, j+1, v+1, self.boxSize))
                amo_cell = at_most_one_encoding(long_formula.nv, cell_literals_list)
                long_formula.extend(amo_cell)
                cell_literals_list.clear()

        # Make sure that every value appear at most once in a row.
        row_literals_list = list()
        for i in range(self.size):
            for v in range(self.size):
                for j in range(self.size):
                    row_literals_list.append(index(i+1, j+1, v+1, self.boxSize))
                amo_row = at_most_one_encoding(long_formula.nv, row_literals_list)
                long_formula.extend(amo_row)
                row_literals_list.clear()

        # Make sure that every value appear at most once in a column.
        column_literals_list = list()
        for j in range(self.size):
            for v in range(self.size):
                for i in range(self.size):
                    column_literals_list.append(index(i+1, j+1, v+1, self.boxSize))
                amo_column = at_most_one_encoding(long_formula.nv, column_literals_list)
                long_formula.extend(amo_column)
                column_literals_list.clear()

        # Make sure that every value appear at most once in a n x n box.
        box_literals_list = list()
        for v in range(self.size):
            for i in range(0, self.size, self.boxSize):
                for j in range(0, self.size, self.boxSize):
                    for k in range(self.boxSize):
                        for m in range(self.boxSize):
                            box_literals_list.append(index(i+k+1, j+m+1, v+1, self.boxSize))
                    amo_box = at_most_one_encoding(long_formula.nv, box_literals_list)
                    long_formula.extend(amo_box)
                    box_literals_list.clear()

        return long_formula
    
    def binomialEncoding(self):
        long_formula = CNF()
        clause = list()

        # Precise one value in one cell.
        for i in range(self.size):
            for j in range(self.size):
                for v in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()

        for i in range(self.size):
            for j in range(self.size):
                for v in range(self.size):
                    for k in range(v+1, self.size):
                        long_formula.append([-index(i+1, j+1, v+1, self.boxSize), -index(i+1, j+1, k+1, self.boxSize)])

        # Make sure that every value appear precisely once in a row.
        
        for i in range(self.size):
            for v in range(self.size):
                for j in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()

        for i in range(self.size):
            for v in range(self.size):
                for j in range(self.size):
                    for k in range(j+1, self.size):
                        long_formula.append([-index(i+1, j+1, v+1, self.boxSize), -index(i+1, k+1, v+1, self.boxSize)])

        # Make sure that every value appear precisely once in a column.
        for j in range(self.size):
            for v in range(self.size):
                for i in range(self.size):
                    clause.append(index(i+1, j+1, v+1, self.boxSize))
                long_formula.append(clause)
                clause.clear()

        for j in range(self.size):
            for v in range(self.size):
                for i in range(self.size):
                    for k in range(i+1, self.size):
                        long_formula.append([-index(i+1, j+1, v+1, self.boxSize), -index(k+1, j+1, v+1, self.boxSize)])

        # Make sure that every value appear precisely once in a n x n box.
        for v in range(self.size):
            for i in range(0, self.size, self.boxSize):
                for j in range(0, self.size, self.boxSize):
                    for k in range(self.boxSize):
                        for m in range(self.boxSize):
                            clause.append(index(i+k+1, j+m+1, v+1, self.boxSize))
                    long_formula.append(clause)
                    clause.clear()
        
        for v in range(self.size):
            for i in range(0, self.size, self.boxSize):
                for j in range(0, self.size, self.boxSize):
                    for k in range(self.boxSize):
                        for m in range(self.boxSize):
                            for p in range(m+1, self.boxSize):
                                long_formula.append([-index(i+k+1, j+m+1, v+1, self.boxSize), -index(i+k+1, j+p+1, v+1, self.boxSize)])
                            for q in range(k+1, self.boxSize):
                                for r in range(self.boxSize):
                                    long_formula.append([-index(i+k+1, j+m+1, v+1, self.boxSize), -index(i+q+1, j+r+1, v+1, self.boxSize)])

        return long_formula
    
    def generateResultFromSolution(self):
        complete = [[0 for i in range(self.size)] for j in range(self.size)]
        if self.solution is not None:
            for i in range(0, index(self.size,self.size,self.size, self.boxSize)):
                if self.solution[i] > 0:
                    x_index, y_index, value = decode(self.solution[i], self.boxSize)
                    complete[x_index-1][y_index-1] = value
        return complete
        
