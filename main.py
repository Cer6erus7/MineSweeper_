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
    MINES = 15
    IS_FIRST_CLICK = True
    IS_GAME_OVER = False

    window = tk.Tk()
    image = tk.PhotoImage(file="img.png")
    window.resizable(False, False)
    window.iconphoto(True, image)
    window.title("MineSweeper")

    def __init__(self):
        """
        Instance of class create the buttons that
        were specified in the static variable: ROW, COLUMN and MINES.
        """
        self.buttons = []
        MineSweeper.window.geometry(f"{MineSweeper.COLUMN * 50}x{MineSweeper.ROW * 50}+500+100")

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMN + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title("Settings")
        win_settings.geometry("+635+300")

        row_var = tk.IntVar()
        column_var = tk.IntVar()
        mine_var = tk.IntVar()

        row_entry = tk.Entry(win_settings, textvariable=row_var)
        row_entry.delete(0, tk.END)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=10)
        tk.Label(win_settings, text="Row").grid(row=0, column=0)

        column_entry = tk.Entry(win_settings, textvariable=column_var)
        column_entry.delete(0, tk.END)
        column_entry.insert(0, MineSweeper.COLUMN)
        column_entry.grid(row=1, column=1, padx=20, pady=10)
        tk.Label(win_settings, text="Column").grid(row=1, column=0)

        mine_entry = tk.Entry(win_settings, textvariable=mine_var)
        mine_entry.delete(0, tk.END)
        mine_entry.insert(0, MineSweeper.MINES)
        mine_entry.grid(row=2, column=1, padx=20, pady=10)
        tk.Label(win_settings, text="Mine").grid(row=2, column=0)

        def ok_button():
            MineSweeper.ROW = int(row_var.get())
            MineSweeper.COLUMN = int(column_var.get())
            MineSweeper.MINES = int(mine_var.get())
            self.new_game()

        ok_btn = tk.Button(win_settings, text="OK", command=ok_button)
        ok_btn.grid(row=3, columnspan=2, pady=10)

    def create_widgets(self):
        """
        Arranges buttons and menubar on the window of the game.
        :return: None
        """

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar)
        settings_menu.add_command(label="Restart", command=self.new_game)
        settings_menu.add_command(label="Settings", command=self.create_settings_win)
        settings_menu.add_command(label="Exit", command=self.window.destroy)
        menubar.add_cascade(label="File", menu=settings_menu)

        count = 1
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                btn.number = count
                btn.grid(row=row, column=column, stick="wens")
                count += 1

        for row in range(1, MineSweeper.ROW + 1):
            MineSweeper.window.grid_rowconfigure(row, minsize=50)

        for column in range(1, MineSweeper.COLUMN + 1):
            MineSweeper.window.grid_columnconfigure(column, minsize=50)

    def _open_all_buttons(self):
        """
        Opens every button on the window. Use only for testing.
        :return: None
        """
        for row, i in enumerate(self.buttons):
            for column, j in enumerate(i):
                self.click(j)

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
    def get_mines_places(excluded_number: int):
        """
        Static method. Choose the location of mines by using button's indexes.
        :return: indexes of mines
        """
        indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMN + 1))
        indexes.remove(excluded_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def insert_mines(self, number: int):
        """
        Places mines on the field by using Static method 'get_mines_places'.
        :return: None
        """
        indxes_mines = self.get_mines_places(number)
        print(indxes_mines)
        for row in range(1, MineSweeper.ROW + 1):
            for column in range(1, MineSweeper.COLUMN + 1):
                btn = self.buttons[row][column]
                if btn.number in indxes_mines:
                    btn.is_mine = True

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
        It is a logic for the buttons, that they should show when was clicked
        (Mines or number of mines beside the ceil), and made color for them.
        Show every mine on the field after losing the game.
        :param clicked_button:
        :return: None
        """
        colors = {1: "orange", 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple', 6: "red", 7: 'pink'}

        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_ceil()
            self.print_widgets()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            messagebox.showerror(message="You lost!")

            for row in range(1, MineSweeper.ROW + 1):
                for column in range(1, MineSweeper.COLUMN + 1):
                    btn = self.buttons[row][column]
                    if btn.is_mine:
                        btn.config(text="*")

        elif clicked_button.count_mine != 0:
            clicked_button.config(text=clicked_button.count_mine, disabledforeground=colors[clicked_button.count_mine])
            clicked_button.is_open = True
        else:
            self.breadth_first_search(clicked_button, colors)
        clicked_button.config(state=tk.DISABLED)

    def breadth_first_search(self, btn: MyButton, colors):
        """
        It's width search algorithm that opens every button that doesn't have mine. Take nearbiest button
        to the queue, stops only nearby ceil that have "count of mine" more than 0 and still opens them.
        Method repeats it until the queue won't be empty.
        :param btn:
        :param colors:
        :return: None
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

                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and 1 <= next_btn.y <= MineSweeper.COLUMN and next_btn not in queue:
                            queue.append(next_btn)

    def new_game(self):
        """
        Delete everything from the class and recreate everything to start a new game
        :return:
        """
        [child.destroy() for child in self.window.winfo_children()]
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False
        self.__init__()
        self.create_widgets()

    def start(self):
        """
        Start the game. Every required method was encapsulated in one method!
        :return: None
        """
        self.create_widgets()
        # self._open_all_buttons()
        self.window.mainloop()


if __name__ == "__main__":
    game = MineSweeper()
    game.start()
