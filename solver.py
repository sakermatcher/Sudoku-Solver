from math import *
import PySimpleGUI as sg
from sudokus.hard import * #Change 'base' to the sudoku you want to open

sg.theme('Dark Green')
start= True
timeout= 0

def complexCrunch(gy, gx, n):
    global sudoku, missing
    boxChar = [[['False','False','False'],['False','False','False'],['False','False','False']], [['False','False','False'],['False','False','False'],['False','False','False']]]
    boxChar.append(boxChar)
    for y in range(3):
        for x in range(3):
            if f"{gy}{gx}{y}{x}" in list(missing.keys()) and str(n) in missing[f"{gy}{gx}{y}{x}"]:
                boxChar[0][y][x] = 'True'
                boxChar[1][x][y] = 'True'
    for box in range(2):
        for i in range(3):
            if 'True' in boxChar[box][i] :
                boxChar[box][i] = 'True'
            else:
                boxChar[box][i] = 'False'
        if boxChar[box].count('True') == 1:
            if box == 0:
                return 'h'+str(boxChar[box].index('True'))
            else:
                return 'v'+str(boxChar[box].index('True'))
    return 'f0'

def generateLayout(start=False):#Generate the first layout
    global sudoku, sudokuL
    font = ("Arial", 30, 'bold')
    sudokuL = []#Starting Layout (sudoku converted to GUI)
    for y in range (9):
        sudokuL.append([])

    for gy in range(3):#g stands for group
        for gx in range (3):#group x
            for y in range(3):#Inside group y
                for x in range(3):#Inside y x
                    if sudoku[gy][gx][y][x] == '0':#Test if there is no value set in that cell
                        if start:
                            sudokuL[gy*3 + y].append( sg.Input(size=(2), justification='center', key=f"{gy*3 + y}{gx*3 + x}", font=font) ) #Convert gy,y to a general y
                        else:
                            sudokuL[gy*3 + y].append( sg.Text('  ',p=((20, 20), (10,10)), justification='center', key=f"{gy*3 + y}{gx*3 + x}", font=font, text_color='orange') )
                    else: 
                        if start: 
                            sudokuL[gy*3 + y].append( sg.Input(str(sudoku[gy][gx][y][x]),size=(2), justification='center', key=f"{gy*3 + y}{gx*3 + x}", font=font) )
                        else:
                            sudokuL[gy*3 + y].append( sg.Text(str(sudoku[gy][gx][y][x]),p=((20, 20), (10,10)), justification='center', key=f"{gy*3 + y}{gx*3 + x}", font=font) )
    for y in range(9):#Place Vertical type(li)nes
        for x in [3, 7]:
            sudokuL[y].insert(x, sg.VSeparator())

    for y in [3, 7]:#Place Horizontal type(li)nes
        sudokuL.insert(y, [sg.HorizontalSeparator()])
    if start:
        sudokuL.append([sg.Button('SOLVE', key= 'solve'), sg.Button('SAVE TO FILE', key= 'save'), sg.Text('Save As:'), sg.Input('new', key='new', size=(10, 5))])
    else:
        sudokuL.append([sg.Button('METHOD 1', key='start1'), sg.Button('METHOD 2', key='start2')])
    sudokuL.append([sg.Text(key='warn')])

    return sudokuL

def saveToSudoku():
    global sudoku, values
    for gy in range(3):
        for gx in range(3):
            for y in range(3):
                for x in range(3):
                    if values[f"{gy*3 + y}{gx*3 + x}"] != '':
                        sudoku[gy][gx][y][x] = values[f"{gy*3 + y}{gx*3 + x}"]
                    else:
                        sudoku[gy][gx][y][x] = '0'

def possibilities(gy, gx, y, x, poss, vh):
    global sudoku, missing
    li=[]
    #Check if its affected by something and discard that as a possibitype(li)ty
    print(vh)
    if vh != 'v':

        if type(poss) == type(li):
            for row in range(3):#Check row
                for affected in sudoku[int(gy)][int(row)][int(y)]:
                    if row == gx:
                        break
                    if affected in poss:
                        poss.remove(affected)
        else:
            for row in range(3):#Check row
                for affected in range(3):
                    if row == gx:
                        break
                    if f"{gy}{row}{y}{affected}" in list(missing.keys()) and poss in missing[f"{gy}{row}{y}{affected}"]:
                        missing[f"{gy}{row}{y}{affected}"].remove(poss)

    if vh != 'h':
        if type(poss) == type(li):
            for col in range(3):#Check column
                for iy in range(3):
                    if col == gy:
                        break
                    if sudoku[col][int(gx)][iy][int(x)] in poss:
                        poss.remove(sudoku[col][int(gx)][iy][int(x)])
        else:
            for col in range(3):#Check column
                for iy in range(3):
                    if col == gy:
                        break
                    if f"{col}{gx}{iy}{x}" in list(missing.keys()) and poss in missing[f"{col}{gx}{iy}{x}"]:
                        missing[f"{col}{gx}{iy}{x}"].remove(poss)

    if vh == '':
        if type(poss) == type(li):
            for boxy in range(3):#Check box
                for boxx in range(3):
                    if sudoku[int(gy)][int(gx)][boxy][boxx] in poss:
                        poss.remove(sudoku[int(gy)][int(gx)][boxy][boxx])
        else:
            for boxy in range(3):#Check box
                for boxx in range(3):
                    if f"{gy}{gx}{boxy}{boxx}" in list(missing.keys()) and poss in missing[f"{gy}{gx}{boxy}{boxx}"]:
                        missing[f"{gy}{gx}{boxy}{boxx}"].remove(poss)

    return poss

def crunch():
    global sudoku, missing, window, values, events, timeout
    for i in list(missing.keys()):
        gy= i[0]
        gx= i[1]
        y= i[2]
        x= i[3]
        if len(missing[i]) == 1:
            sudoku [int(gy)][int(gx)][int(y)][int(x)] = missing[i][0]
            window[f"{int(gy)*3 + int(y)}{int(gx)*3 + int(x)}"].update(missing[i][0])
            window.read(timeout= timeout)
            possibilities(gy, gx, y, x, missing[i][0],'')
            missing.pop(i)
            return True

    for gy in range(3):#g stands for group
        for gx in range (3):#group x
            count = {}
            for y in range(3):#Inside group y
                for x in range(3):#Inside y x
                    if f"{gy}{gx}{y}{x}" in list(missing.keys()):#Check if slice is missing
                        for i in missing[f"{gy}{gx}{y}{x}"]: #Go thru all the possibilities
                            if i in list(count.keys()): #Check if there is already a count on that number
                                count[i] += 1# If there is add one
                            else:
                                count[i] = 1 #If there is none create it
            if 1 in list(count.values()):#Check if there is a blank in a box that is the only one that can be that number
                for i in list(count.keys()):#Find which number it is that only 1 blank can have
                    if count[i] == 1:
                        for y in range(3):
                            for x in range(3):#Find which blank the number is referring to
                                if f"{gy}{gx}{y}{x}" in list(missing.keys()) and i in missing[f"{gy}{gx}{y}{x}"]:

                                    sudoku [gy][gx][y][x] = i
                                    print(i)
                                    window[f"{gy*3 + y}{gx*3 + x}"].update(i)
                                    window.read(timeout= timeout)
                                    possibilities(gy, gx, y, x, i, '')
                                    missing.pop(f"{gy}{gx}{y}{x}")
                                    return True

    for gy in range (3):
        for gx in range(3): 
            for i in range(1, 10):
                cc = complexCrunch(gy, gx, i)
                if cc[0]== 'h':
                    possibilities(gy,gx,cc[1], 0, str(i), 'h')
                elif cc[1] == 'v':
                    possibilities(gy,gx,0,cc[1], str(i), 'v')

    if len(missing)== 0:     
        return False
    else:
        return True
                                
def solve():
    global window, sudoku, sudokuL, event, values, missing, timeout
    saveToSudoku()
    orgSudoku = sudoku.copy()
    window.close()
    generateLayout()
    window = sg.Window('SUDOKU SOLVER', sudokuL)
    while True:
        missing= {}
        sudoku= orgSudoku.copy()
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                exit()
            if event in ['start1', 'start2', 'compare']:
                window.close()
                generateLayout()
                window = sg.Window('SUDOKU SOLVER', sudokuL)
                window.read(timeout=0)
                break
        #Make Dictionary with missing numbers
        if event in ['start1', 'compare']:
            for gy in range(3):
                for gx in range(3):
                    for y in range(3):
                        for x in range(3):
                            if sudoku [gy][gx][y][x] == '0':
                                missing[f"{gy}{gx}{y}{x}"] = possibilities(gy, gx, y, x, ['1','2','3','4','5','6','7','8','9'], '')
            #Crunch numbrers down
            c= True
            while c:
                c = crunch()
        if event in ['start2', 'compare']:
        


            window.read(timeout= timeout)

while True:

    if start:
        window = sg.Window('SUDOKU SOLVER', generateLayout(True))

    while start:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            exit()
        if event == 'solve':
            solve()
            
        if event == 'save':
            if values['new'] == 'base': 
                window['warn'].update('file name "base" cant be used')
            else:
                with open(f"sudokus/{values['new']}.py", 'w+')as new:
                    saveToSudoku()
                    new.write(f"sudoku = {sudoku}")