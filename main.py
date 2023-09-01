import tkinter as tk
from tkinter import messagebox
from random import shuffle


class MyButton(tk.Button):
    """
    Inheritance of Tkinter's Button. Made coordination for buttons, mines and indexes!
    """
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=0, font='Colibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mine = 0
        self.is_open = False

    def __repr__(self):
        return f"{self.x} {self.y} {self.is_mine} {self.number}"


class MineSweeper:
    """
    This class represent the game MineSweeper. Every method and logic was encapsulated in this class.
    It has several static variable: ROW, COLUMN and MINES. This class create a new tkinter window.
    """
    ROW = 10
    COLUMN = 10
    MINES = 10

    window = tk.Tk()
    image = tk.PhotoImage(file="img.png")
    window.iconphoto(True, image)
    window.geometry("+500+100")
    window.title("MineSweeper")
    for row in range(1, ROW + 1):
        window.grid_rowconfigure(row, minsize=50)
    for column in range(1, COLUMN + 1):
        window.grid_columnconfigure(column, minsize=50)

    def __init__(self):
        """
        Instance of class create the buttons that
        were specified in the static variable: ROW, COLUMN and MINES.
        """
        self.buttons = []

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMN + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        """
        Arranges buttons on the window of the game.
        :return: None
        """
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                btn.grid(row=row, column=column, stick="wens")

    def _open_all_buttons(self):
        """
        Opens every button on the window. Use only for testing.
        :return: None
        """
        for row, i in enumerate(self.buttons):
            for column, j in enumerate(i):
                self.click(j)

    @staticmethod
    def _lose_message():
        return messagebox.showerror(message="You lost!")

    def print_widgets(self):
        """
        Print all info about every button on the window.
        :return: None
        """
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                if btn.is_mine:
                    print("*", end='')
                else:
                    print(btn.count_mine, end='')
            print()

    @staticmethod
    def get_mines_places():
        """
        Static method. Choose the location of mines by using button's indexes.
        :return: indexes of mines
        """
        indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMN + 1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def insert_mines(self):
        """
        Places mines on the field by using Static method 'get_mines_places'.
        :return: None
        """
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
        """
        Count every mine that was placed beside of the button.
        :return: None
        """
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

    def click(self, clicked_button: MyButton):
        """
        Static method. It is a logic for the buttons, that they should show when was clicked
        (Mines or number of mines beside the ceil), and made color for them
        :param clicked_button:
        :return: None
        """
        colors = {1: "orange", 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple', 6: "red", 7: 'pink'}
        print(clicked_button)
        if clicked_button.is_mine:
            clicked_button.config(text="*", disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper._lose_message()
        elif clicked_button.count_mine != 0:
            clicked_button.config(text=clicked_button.count_mine, disabledforeground=colors[clicked_button.count_mine])
            clicked_button.is_open = True
        else:
            self.breadth_first_search(clicked_button, colors)
        clicked_button.config(state=tk.DISABLED)

    def breadth_first_search(self, btn: MyButton, colors):
        """
        It's width search algorithm that opens every button that doesn't have mine. Take nearbiest button
        that leis on south, west, norths, east to the queue, stops only nearby ceil that have "count of mine"
        more than 0 and still opens them. Method repeats it until the queue won't be empty.
        :param btn:
        :param colors:
        :return:
        """
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            if cur_btn.count_mine:
                cur_btn.config(text=cur_btn.count_mine, disabledforeground=colors[cur_btn.count_mine])
            else:
                cur_btn.config(text="")
            cur_btn.is_open = True
            cur_btn.config(state=tk.DISABLED)

            if cur_btn.count_mine == 0:
                x, y = cur_btn.x, cur_btn.y

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if abs(dx-dy) != 1:
                            continue

                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and 1 <= next_btn.y <= MineSweeper.COLUMN and next_btn not in queue:
                            queue.append(next_btn)

    def start(self):
        """
        Start the game. Every required method was encapsulated in one method!
        :return: None
        """
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_ceil()
        self.print_widgets()
        # self._open_all_buttons()
        MineSweeper.window.mainloop()


if __name__ == "__main__":
    game = MineSweeper()
    game.start()
