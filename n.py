from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename

print("Opening file selection prompt...")
file_path = askopenfilename()

root = Tk()
root.title("Args")

def printvars():
    args = [mode.get(), npic.get(), nrdm.get(), nbyt.get(), nrep.get()]
    print(args)
    root.destroy()

# window.geometry("700x400")

mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight = 1, pad=30)
mainframe.columnconfigure(1, weight = 1, pad=30)
mainframe.columnconfigure(2, weight = 1, pad=30)
mainframe.rowconfigure(0, weight = 1, pad=20)
mainframe.rowconfigure(2, weight = 1, pad=20)
mainframe.rowconfigure(4, weight = 1, pad=20)
mainframe.pack(pady = 50, padx = 50)

choices = {'change', 'reverse', 'repeat', 'remove', 'zero', 'insert', 'replace', 'move'}
mode = StringVar(root)
mode.set("change") # default value

modeMenu = OptionMenu(mainframe, mode, *choices)
Label(mainframe, text="Choose a mode").grid(sticky='w', row = 1, column = 0)
modeMenu.grid(sticky=('w','n'), row = 2, column = 0)

Label(mainframe, text="How many pictures to generate?", anchor='w').grid(sticky='w', row = 1, column = 1)
npic = Entry(mainframe, width=20)
npic.grid(sticky=('w','n'), row = 2, column = 1)
npic.insert(0, "1")

Label(mainframe, text="How many random changes?", anchor='w').grid(sticky='w', row = 1, column = 2)
nrdm = Entry(mainframe, width=20)
nrdm.grid(sticky=('w','n'), row = 2, column = 2)

Label(mainframe, text="How many bytes to change each change?", anchor='w').grid(sticky='w', row = 3, column = 0)
nbyt = Entry(mainframe, width=20)
nbyt.grid(sticky=('w','n'), row = 4, column = 0)

Label(mainframe, text="How many bytes to repeat?", anchor='w').grid(sticky='w', row = 3, column = 1)
nrep = Entry(mainframe, width=20)
nrep.grid(sticky=('w','n'), row = 4, column = 1)

Button(mainframe, text='ADD',bd=10,command=printvars).grid(row = 5, column = 1)

# Label(text='Mode').place(x=50, y=30)

root.mainloop()