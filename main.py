from gui import Window
import logic


class Application:
    def __init__(self):
        self.logic = logic.SudokuLogic()
        self.window = Window((1200, 800), self.logic)

    def run(self) -> None:
        self.window.mainloop()


app = Application()

app.run()
