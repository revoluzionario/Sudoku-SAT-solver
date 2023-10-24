import board
import sudoSolver

class SudokuLogic:
    def __init__(self, option = ["Minisat22", "Binomial encoding", ""]) -> None:
        self.solverName, self.encodingType, self.fileDir = option
        self.sudoSolver = sudoSolver.sudoSolver(self.solverName)
        self.statistics = []
        self.board = None
        self.result = []
        
    def readFile(self):
        with open(self.fileDir, 'r') as file:
            rawData = list()
            data = file.read().strip('\n')
            rawText = data.split("\n")
            for rows in rawText:
                try:
                    rawData.append([int(x) for x in rows.split(" ")])
                except ValueError:
                    # Handle the case where the string cannot be converted to an integer
                    print("Invalid input:", rows)
        self.board = board.Board(rawData)

    def _solve(self):
        solution = None
        time = None
        novars = None
        noclauses = None
        if self.encodingType == "Binomial encoding":
            solution, time, novars, noclauses = self.sudoSolver._solve(
                self.board.binomial_encoding, self.board.clues
            )
        elif self.encodingType == "Product encoding":
            solution, time, novars, noclauses = self.sudoSolver._solve(
                self.board.product_encoding, self.board.clues
            )
        self.board.solution = solution
        self.board.board = self.board.generateResultFromSolution()
        self.statistics =[time, novars, noclauses]
        self.result = self.board.board
    
    def encodingTypeChange(self, encodingType):
        self.encodingType = encodingType
    
    def solverOptionChange(self, solverName):
        self.solverName = solverName
        self.sudoSolver.name = self.solverName

    def export_stats(self):
        return self.statistics
    
    def export_board(self):
        return self.result
    
    def export_initialInfo(self):
        return self.fileDir, self.board.size