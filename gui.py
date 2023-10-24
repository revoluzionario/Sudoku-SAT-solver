import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import *
from logic import *

class Window(tk.Tk):
    def __init__(self, size: tuple, logic: SudokuLogic):
        super().__init__()
        self.size = size
        self.logic = logic
        self.createWindow()

    
    def createWindow(self):
        width, height = self.size
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Sudoku SAT-Solver")
        self.canvasframe = CanvasFrame(self, self.logic)
        self.optionframe = OptionFrame(self, self.canvasframe, self.logic)
        self.optionframe.grid(column=1, row=0,sticky=(N, S, E, W))
        self.canvasframe.grid(column=0, row=0, sticky=(N, S, E, W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        


class CanvasFrame(tk.Frame):
    def __init__(self, master, logic) -> None:
        super().__init__(master, relief="solid")
        self.buildFrame()
        self.logic = logic

    def buildFrame(self):
        self.h = Scrollbar(self, orient=HORIZONTAL)
        self.v = Scrollbar(self, orient=VERTICAL)
        self.boardArea = Canvas(self, bg='white', xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.boardArea.grid(column=0,row=0, sticky=(N, S, E, W))
        self.h["command"]=self.boardArea.xview
        self.v["command"]=self.boardArea.yview
        self.h.grid(column=0,row=1,sticky=EW)
        self.v.grid(column=1, row=0, sticky=NS)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def drawCanvas(self):
        canvas_size = 30 * self.logic.board.size
        self.boardArea.delete("all")
        self.boardArea["scrollregion"] = (0,0, canvas_size if canvas_size > 800 else 800, canvas_size if canvas_size > 800 else 800)
        for i in range(self.logic.board.size + 1):
            if i % self.logic.board.boxSize == 0:
                self.boardArea.create_line(i * 30, 0, i * 30, 30 * self.logic.board.size, width=3,tags="line")
            else:
                self.boardArea.create_line(i * 30, 0, i * 30, 30 * self.logic.board.size, tags="line")

        for j in range(self.logic.board.size + 1):
            if j % self.logic.board.boxSize == 0:
                self.boardArea.create_line(0, j * 30, 30 * self.logic.board.size, j * 30, width=3, tags="line")
            else:
                self.boardArea.create_line(0, j * 30, 30 * self.logic.board.size, j * 30, tags="line")
        
        for i in range(self.logic.board.size):
            for j in range(self.logic.board.size):
                if (self.logic.board.board[i][j] != 0):
                    self.boardArea.create_text(i * 30 + 15, j * 30 + 15, text = self.logic.board.board[i][j].__str__(), font=("Arial", 20), tags="number")
        pass

    def redrawCanvas(self):
        self.boardArea.delete("number")
        for i in range(self.logic.board.size):
            for j in range(self.logic.board.size):
                if (self.logic.board.board[i][j] != 0):
                    self.boardArea.create_text(i * 30 + 15, j * 30 + 15, text = self.logic.board.board[i][j].__str__(), font=("Arial", 20), tags="number")
        pass

class OptionFrame(tk.Frame):
    def __init__(self, master, canvas, logic) -> None:
        super().__init__(master, borderwidth=5, relief='flat')
        self.logic = logic
        self.noVarsIndex = tk.StringVar(value="NaN")
        self.noClausesIndex = tk.StringVar(value="NaN")
        self.solveTimeIndex = tk.StringVar(value="NaN")
        self.directoryIndex = tk.StringVar(value="None")
        self.sizeIndex = tk.StringVar(value="NaN")
        self.grid_propagate(0)
        width, height = master.size
        self["width"]=width/3
        self["height"]=height
        self.buildFrame()
        self.canvas = canvas
 

    def buildFrame(self):
        s = ttk.Style()
        s.configure('.', font=('Arial', 12))
        self.option_add("*TCombobox*Listbox*Font", ('Arial', 12))
        encodingLabel = ttk.Label(self, text="Choose encoding option")
        encodingOptionList = ["Binomial encoding", "Product encoding"]
        encodingOption = ttk.Combobox(self, justify='center', values=encodingOptionList, state="readonly",font=("Arial",12))
        encodingOption.set(self.logic.encodingType)
        encodingOption.bind("<<ComboboxSelected>>", lambda _: self.logic.encodingTypeChange(encodingOption.get()))

        solverLabel = ttk.Label(self, text="Choose SAT Solver")
        solverOptionList = ["Minisat22", "Cadical153", "Glucose42"]
        solverOption = ttk.Combobox(self, justify='center', values=solverOptionList, state="readonly", font=("Arial",12))
        solverOption.set(self.logic.solverName)
        solverOption.bind("<<ComboboxSelected>>", lambda _: self.logic.solverOptionChange(solverOption.get()))

        noVarsLabel = ttk.Label(self, text="No. of vars:")
        noClausesLabel = ttk.Label(self, text="No. of clauses:")
        solveTimeLabel = ttk.Label(self, text="Solve time:")
        dirLabel = ttk.Label(self, text="Directory:")
        sizeLabel = ttk.Label(self, text="Size:")

        noVars_val = ttk.Label(self, textvariable=self.noVarsIndex)
        noClauses_val = ttk.Label(self, textvariable=self.noClausesIndex)
        solveTime_val = ttk.Label(self, textvariable=self.solveTimeIndex)
        dir_val = tk.Message(self, textvariable=self.directoryIndex, font= ('Arial', 11), aspect=250)
        size_val = ttk.Label(self, textvariable=self.sizeIndex)

        solveButton = ttk.Button(self, text="Solve", command=self.solve)
        importButton = ttk.Button(self, text="Import", command=self.select_file)
        exportButton = ttk.Button(self, text="Export", command=self.export)
        exitButton = ttk.Button(self, text="Exit", command=exit)

        solverLabel.grid(column=0, columnspan=2, row=0)
        solverOption.grid(column=0, columnspan=2, row=1,sticky=(E, W))
        encodingLabel.grid(column=0, columnspan=2, row=2)
        encodingOption.grid(column=0, columnspan=2, row=3, sticky=(E, W))

        sizeLabel.grid(column=0, row=4, sticky=(N, S, E, W))
        noVarsLabel.grid(column=0, row=5, sticky=(N, S, E, W))
        noClausesLabel.grid(column=0, row=6, sticky=(N, S, E, W))
        solveTimeLabel.grid(column=0, row=7, sticky=(N, S, E, W))
        dirLabel.grid(column=0, row=8, sticky=(E, W))

        size_val.grid(column=1, row=4, sticky=(N,S))
        noVars_val.grid(column=1, row=5, sticky=(N,S))
        noClauses_val.grid(column=1, row=6, sticky=(N,S))
        solveTime_val.grid(column=1, row=7, sticky=(N,S))
        dir_val.grid(column=1, row=8, sticky=(N,S,E,W))

        importButton.grid(column=0, row=9,sticky=(E, W))
        solveButton.grid(column=1, row=9,sticky=(E, W))
        exportButton.grid(column=0, row=10,sticky=(E, W))
        exitButton.grid(column=1, row=10,sticky=(E, W))
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        

    def updateStatisticsDisplay(self):
        time, novars, noclauses = self.logic.export_stats() 
        self.solveTimeIndex.set(f"{time}")
        self.noClausesIndex.set(f"{noclauses}")
        self.noVarsIndex.set(f"{novars}")
        pass

    def updateInitialInfo(self):
        dir, size = self.logic.export_initialInfo()
        self.directoryIndex.set(f"{dir}")
        self.sizeIndex.set(f"{size} x {size}")
        pass

    def select_file(self):
        filetypes = (
            ('text files', '*.txt'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/home/hoangle/Documents',
            filetypes=filetypes)

        tk.messagebox.showinfo(title='Selected File', message=filename)
        self.logic.fileDir = filename
        self.logic.readFile()
        self.updateInitialInfo()
        self.canvas.drawCanvas()

    def solve(self):
        self.logic._solve()
        self.updateStatisticsDisplay()
        self.canvas.redrawCanvas()

    def export(logic):
        pass
