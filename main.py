import tkinter as tk
from random import shuffle


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=0, font='Colibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mine = 0

    def __repr__(self):
        return f"{self.x} {self.y} {self.is_mine} {self.number}"


class MineSweeper:
    ROW = 10
    COLUMN = 5
    MINES = 25

    window = tk.Tk()
    image = tk.PhotoImage(file="img.png")
    window.iconphoto(True, image)
    window.geometry("+500+100")
    for row in range(1, ROW + 1):
        window.grid_rowconfigure(row, minsize=50)
    for column in range(1, COLUMN + 1):
        window.grid_columnconfigure(column, minsize=50)

    def __init__(self):
        self.buttons = []
        self.field = tk.StringVar()

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMN + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                btn.grid(row=row, column=column, stick="wens")

    def open_all_buttons(self):
        for row, i in enumerate(self.buttons):
            for column, j in enumerate(i):
                self.click(j)

    def print_widgets(self):
        for row_btn in self.buttons:
            print(row_btn)

    @staticmethod
    def get_mines_places():
        indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMN + 1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def insert_mines(self):
        indxes_mines = self.get_mines_places()
        print(indxes_mines)
        count = 1
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                btn.number = count
                if btn.number in indxes_mines:
                    btn.is_mine = True
                count += 1

    def count_mines_in_ceil(self):
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                mines = 0
                if btn.is_mine is False:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[row+row_dx][column+col_dx]
                            if neighbour.is_mine:
                                mines += 1
                btn.count_mine = mines

    @staticmethod
    def click(clicked_button: MyButton):
        print(clicked_button)
        if clicked_button.is_mine:
            clicked_button.config(text="*", disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.count_mine, disabledforeground='black')
        clicked_button.config(state=tk.DISABLED)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_ceil()
        self.print_widgets()
        self.open_all_buttons()
        MineSweeper.window.mainloop()


if __name__ == "__main__":
    game = MineSweeper()
    game.start()
