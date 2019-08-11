import tkinter as tk

#Macros
HEIGHT = 500
WIDTH = 600
#Start of main loop
root = tk.Tk()

#Creating a new canvas inside the root using macros for dimensions
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#Creating a new frame
frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

#Creating a second frame for the board
boardFrame = tk.Frame(frame, bg='black', bd = '4')
boardFrame.place(relx=0.15, rely=0.06, relwidth = 0.7, relheight = 0.85)

#Title Label
label = tk.Label(frame, text="Sudoku Solver", bg='yellow', font = ("Calibri 24"))
label.place(relx=0.3, rely = 0, relwidth=0.4, relheight=0.06)

#Creating two 9x9 arrays, one for the entries and one for the StringVars
entries = [[None for i in range(9)] for j in range(9)]
stringVars = [[None for i in range(9)] for j in range(9)]
emptyBoard = [[0 for i in range(9)] for j in range(9)]

#New method of creating squares
for row in range(9):
    for col in range(9):
        stringVar = tk.StringVar()
        stringVars[row][col] = (stringVar)
        entries[row][col] = (tk.Entry(boardFrame, width='1', font = ("Calibri 24"), textvariable = stringVar))
        entries[row][col].place(relx=((col * 0.11) + (col//3 * 0.01)), rely = ((row * 0.11) + (row//3 * 0.01)), relwidth = 0.1)

#Function to display the solved board in the GUI
def displayBoard(board):
    for i in range(9):
        for j in range(9):
            stringVars[i][j].set(str(board[i][j]))
            entries[i][j].config(state='readonly')

#Converts users text input to an integer. Checks for invalid input
def convertString(s):
    try: 
        num = int(s)
        if((num <= 9) and (num >= 1)):
            return s
        return 0
    except ValueError:
        return 0

#Fills the board with the numbers entered by the user.
def fillBoard():
    board = emptyBoard
    for i in range(9):
        for j in range(9):
            board[i][j] = int(convertString(entries[i][j].get()))
    return board

#Resets the text entries so that a new sudoku can be solved.
def resetBoard():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state='normal')
            stringVars[i][j].set("")

# Proivides main functionality. Recursively solves sudoku
def solve(board):
    #Base case of solved board when no squares are empty
    find = findEmpty(board)
    if not find:
        return True
    else:
        row, col = find

    for num in range(1,10):
        if valid(board, num, (row, col)):
            board[row][col] = num

            #Base case returning True
            if solve(board):
                return True
            
            #If the number was invalid, square is reset and next value is tested
            board[row][col] = 0

    #Notifies previous call of invalid number
    return False

#Checks if a proposed move would be valid for the current board.
def valid(board, num, pos):
    #Check row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    
    #Check column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    #Check subsquare
    cornerX = pos[1] // 3
    cornerY = pos[0] // 3

    for i in range(cornerY * 3, cornerY * 3 + 3):
        for j in range(cornerX * 3, cornerX * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    
    return True

#Finds the next empty square in the board
def findEmpty(board):
    for i in range(9):
        for j in range(9):
            if(board[i][j] == 0):
                return (i, j) #row, col
    return None

# This is the main solver function. It takes string input from the
# user and returns a solved sudoku.
def mainSolver():
    sudokuBoard = fillBoard()
    solve(sudokuBoard)
    displayBoard(sudokuBoard)

# Solve, reset and quit buttons for GUI. Buttons need to be created after the
# functions they call have been declared.
solveButton = tk.Button(frame, text="Solve", bg='green', font = ("Calibri 24"), command = mainSolver)
solveButton.place(relx=0.26, rely=0.918, relwidth=0.15, relheight = 0.075)

resetButton = tk.Button(frame, text="Reset", bg='orange', font = ("Calibri 24"), command = resetBoard)
resetButton.place(relx=0.425,rely=0.918, relwidth =0.15, relheight = 0.075)

quitButton = tk.Button(frame, text="Quit", bg='red',font = ("Calibri 24"), command = root.destroy)
quitButton.place(relx=0.59, rely=0.918, relwidth = 0.15, relheight = 0.075)

root.mainloop()