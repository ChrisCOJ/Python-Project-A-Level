from tkinter import *
import tkinter as tk
import math
from PIL import ImageTk, Image

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# GUI INTERFACE FOR THE ACTUAL BOARD GAME

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=6, columns=6, size=92, color="blue"):
        # size is the size of a square, in pixels
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=2, width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)




    def addpiece(self, name, image, row, column):
        # Add a piece to the playing board
        self.canvas.create_image(0, 0, image=image, tags=name, anchor="c")
        self.placepiece(name, row, column)



    def placepiece(self, name, row, column):
        # Place a piece at the given row/column
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)


    def refresh(self, event):
        # Redraw the board, possibly in response to window being resized
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color
        for row in range(1):
            for col in range(6):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for col in range(1):
            for row in range(6):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for row in range(5,6):
            for col in range(6):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for col in range(5, 6):
            for row in range(6):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for col in range(1):
            for row in range(1):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="red", tags="start/end_square")
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
            self.canvas.tag_raise(name)


    def movePiece(self, name):
        self.pos = self.canvas.coords('player1')
        self.pos2 = self.canvas.coords('player2')
        if name == "player1":
            x = (self.pos[1]-math.floor(self.size/2))/self.size
            y = (self.pos[0]-math.floor(self.size/2))/self.size
            if x >= -1 and x < 1 and y >= -1 and y <4.85:
                y += 1
            elif y >= 4.85 and y < 5 and x >= -1 and x < 5:
                x += 1
            elif x == 5 and y <= 6 and y > -0.15:
                y -= 1
            elif y >= -1 and y < 1 and x <=6 and x > -1:
                x -= 1
            print(self.pos)
            print("x: ", x, "\n", "y: ", y)
            self.placepiece(name, x, y)
        elif name == "player2":
            x = (self.pos2[1] - math.floor(self.size / 2)) / self.size
            y = (self.pos2[0] - math.floor(self.size / 2)) / self.size
            if x >= -1 and x < 1 and y >= -1 and y < 4.85:
                y += 1
            elif y >= 4.85 and y < 6 and x >= -1 and x < 5:
                x += 1
            elif x == 5 and y <= 6 and y > 1:
                y -= 1
            elif y >= 0 and y < 1 and x <= 5 and x > 0:
                x -= 1
            print(self.pos2)
            print("x2: ", x, "\n", "y2: ", y)
            self.placepiece(name, x, y)




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Quiz


def check(letter, view):
    global label3, index, letter_pos
    if(letter == correctLetter[letter_pos]):
        label3 = Label(view, text="Correct!")
        board.movePiece("player2")
    else:
        label3 = Label(view, text="Wrong!")
    label3.grid()
    view.after(400, lambda *args: unpackView())
    index += 2
    letter_pos += 1
    button_a.config(state=tk.DISABLED)
    button_b.config(state=tk.DISABLED)
    button_c.config(state=tk.DISABLED)
    button_d.config(state=tk.DISABLED)


def getView():
    global label2, button_a, button_b, button_c, button_d
    newWindow_label.grid_forget()
    label2 = Label(newWindow, text=questions[index])
    button_a = Button(newWindow, text=questions[index + 1][0], command=lambda *args: check("A", newWindow))
    button_b = Button(newWindow, text=questions[index + 1][1], command=lambda *args: check("B", newWindow))
    button_c = Button(newWindow, text=questions[index + 1][2], command=lambda *args: check("C", newWindow))
    button_d = Button(newWindow, text=questions[index + 1][3], command=lambda *args: check("D", newWindow))

    label2.grid()
    button_a.grid()
    button_b.grid()
    button_c.grid()
    button_d.grid()



def unpackView():
    label2.grid_forget()
    label3.grid_forget()
    button_a.grid_forget()
    button_b.grid_forget()
    button_c.grid_forget()
    button_d.grid_forget()
    if index != 40:
        getView()
    elif index == 40:
        winner_label = Label(newWindow, text="YOU'VE WON!!!")
        winner_label.pack()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def currency():
    pass




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def abilityShopDesign():
    global shop
    shop = Toplevel(window)
    shop.title("Shop")
    shop.geometry("400x400")
    for x in range(20):
        shop.grid_columnconfigure(x, weight=1)
        shop.grid_rowconfigure(x, weight=1)
    offensive_label = Label(shop, text="OFFENSIVE ABILITIES")
    offensive_label.grid(row=1, column=1)
    offensive_stasis = Button(shop, text="Stasis")
    offensive_stasis.config(height=4, width=14)
    offensive_stasis.grid(row=2, column=1)
    offensive_cost = Label(shop, text="$80")
    offensive_cost.grid(row=3, column=1)


    defensive_label = Label(shop, text="DEFENSIVE ABILITIES")
    defensive_label.grid(row=1, column=10)
    defensive_shield = Button(shop, text="Shield")
    defensive_shield.config(height=4, width=14)
    defensive_shield.grid(row=2, column=10)
    defensive_cost = Label(shop, text="$80")
    defensive_cost.grid(row=3, column=10)


    support_label = Label(shop, text="SUPPORT ABILITIES")
    support_label.grid(row=1, column=19)
    support_moneyBoost = Button(shop, text="MoneyBoost")
    support_moneyBoost.config(height=4, width=14)
    support_moneyBoost.grid(row=2, column=19)
    support_cost = Label(shop, text="$80")
    support_cost.grid(row=3, column=19)


    shopButton.config(state=tk.DISABLED)
    shop.protocol("WM_DELETE_WINDOW", closeShop)



def closeShop():
    shop.destroy()
    shopButton.config(state=tk.NORMAL)




def startBoard():
    global shopButton
    start_button.grid_forget()
    label.grid_forget()
    cgButton.grid_forget()
    jgButton.grid_forget()
    quitButton.grid_forget()
    window.title("Board Game")
    board.pack(side="top", fill="both", expand=True, padx=4, pady=4)

    img = Image.open("images/Player1.png")
    img = img.resize((20, 20), Image.ANTIALIAS)
    player1 = ImageTk.PhotoImage(img)

    secondImg = Image.open("images/Player2.png")
    secondImg = secondImg.resize((20, 20), Image.ANTIALIAS)
    player2 = ImageTk.PhotoImage(secondImg)

    board.addpiece("player1", player1, 0, 0 - 0.15)
    board.addpiece("player2", player2, 0, 0 + 0.15)
    shopButton = Button(window, text="Ability_Shop", command=abilityShopDesign)
    shopButton.pack(side="top")

    getView()
    window.mainloop()




def quitBoard():
    def Destroy():
        q.destroy()
        window.destroy()
    q = tk.Tk()
    q.geometry("361x50")
    for x in range(20):
        window.grid_columnconfigure(x, weight=1)
        window.grid_rowconfigure(x, weight=1)
    label1 = Label(q, text="Are you sure you want to exit?")
    label1.config(font=("Calibri", 12))
    label1.grid(row=0, column=10)
    buttonYes = Button(q, text="YES", height=1, width=10, command=Destroy)
    buttonYes.grid(row=20, column=0)
    buttonNo = Button(q, text="NO", height=1, width=10, command=q.destroy)
    buttonNo.grid(row=20, column=20)
    q.mainloop()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


questions = []
file = open("questions.txt", "r")
line = file.readline()
correctLetter = []
while(line != ""):
    questionString = line
    answers = []
    for i in range (4):
        answers.append(file.readline())
    questions.append(questionString)
    questions.append(answers)
    letter = file.readline()[0]
    correctLetter.append(letter)
    line = file.readline()
file.close()
index = 0
letter_pos = 0



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------






if __name__ == "__main__":

    window = tk.Tk()
    window.geometry("574x600")
    window.title("Main Menu")
    board = GameBoard(window)

    newWindow = Toplevel(window)
    newWindow.title("Questions")


    for x in range(20):
        window.grid_columnconfigure(x, weight=1)
        window.grid_rowconfigure(x, weight=1)

    ''''''
    newWindow_label = Label(newWindow, text="Question Window")
    newWindow_label.config(font=("Calibri", 17))
    newWindow_label.grid(row=6, column=14)


    label = Label(window, text="Multiple Choice Board Game!")
    label.config(font=("Calibri", 17))
    label.grid(row=6, column=14)

    ''''''

    start_button = tk.Button(window, text="Start", height=3, width=20, command=startBoard)
    start_button.grid(row=14, column=14)

    cgButton = Button(window, text="Create Game", height=3, width=20)
    cgButton.grid(row=16, column=14)

    jgButton = Button(window, text="Join Game", height=3, width=20)
    jgButton.grid(row=18, column=14)

    quitButton = Button(window, text="Quit", height=3, width=15, command=quitBoard)
    quitButton.grid(row=18, column=19)

    # shopButton = Button(window, text="Ability_Shop", command=abilityShop)
    # shopButton.grid(row=10, column=10)
    ''''''
    window.mainloop()

