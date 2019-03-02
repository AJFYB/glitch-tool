import argparse
import random
import sys
import re
import math

# dependency for file selection
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from os import path

def writeFile(fileByteList, fileNum, iteration, bytesTochange, seed):
    filename, extension = path.splitext(args.infile)

    # Used due to difference between / and \ in file paths
    split_by = ""
    if "/" in filename: split_by = "/" 
    else: split_by = "\\"

    filename = filename.split(split_by)[-1]

    print(filename)
    outPath = f"{args.outdir}{filename}_m={args.mode}_b={bytesTochange}_s={seed}_n={fileNum}_i={iteration}{extension}"

    if (not args.quiet):
        print("Writing file to " + outPath)
    open(outPath, "wb").write(bytes(fileByteList))

def messWithFile(originalByteList, iterations, bytesToChange, repeatWidth, fileNum):
    newByteList = [b for b in originalByteList]
    iteration = 1
    seed = args.seed or random.randrange(sys.maxsize)
    random.seed(seed)
    for i in range(iterations):
        iteration = i+1
        if (args.mode == "repeat"):
            newByteList = repeatBytes(newByteList, bytesToChange, repeatWidth)
        else:
            newByteList = transforms[args.mode](newByteList, bytesToChange)
        if (args.output_iterations > 0 and iteration%args.output_iterations == 0):
            writeFile(newByteList, fileNum, iteration, bytesToChange, seed)
    writeFile(newByteList, fileNum, iteration, bytesToChange, seed)
        
# Transforms

def changeBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = [random.randint(0, 255) for i in range(bytesToChange)]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def reverseBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange][::-1]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def repeatBytes(byteList, bytesToChange, repeatWidth):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = []
    for i in range(math.ceil(bytesToChange/repeatWidth)):
        chunk.extend(byteList[pos:pos+repeatWidth])
    byteList[pos:pos+bytesToChange] = chunk[:bytesToChange]
    return byteList

def removeBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    byteList[pos:pos+bytesToChange] = []
    return byteList

def zeroBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    byteList[pos:pos+bytesToChange] = [0] * bytesToChange
    return byteList

def insertBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList))
    chunk = [random.randint(0, 255) for i in range(bytesToChange)]
    byteList[pos:pos] = chunk
    return byteList

def replaceBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange]
    old = random.randint(0, 255)
    new = random.randint(0, 255)
    chunk = [new if b == old else b for b in chunk]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def moveBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange]
    byteList[pos:pos+bytesToChange] = []
    newPos = random.randint(0, len(byteList))
    byteList[newPos:newPos] = chunk
    return byteList

def main():
    # Do stuff to arguments
    if (not args.infile):
        print("Error: No input file specified")
        return False
    if (not path.isfile(args.infile)):
        print("Error: Input file not found")
        return False
    if (not args.mode):
        print("Error: No mode specified")
        return False
    if (not (args.mode in transforms)):
        print("Error: Invalid mode")
        return False
    minChanges = 1
    maxChanges = 1
    if (args.changes and re.match(r"[0-9]+-[0-9]+", args.changes)):
        parts = args.changes.split("-")
        minChanges = int(parts[0])
        maxChanges = int(parts[1])
    elif (args.changes):
        minChanges = int(args.changes)
        maxChanges = int(args.changes)
    minBytes = 1
    maxBytes = 1
    if (args.bytes and re.match(r"[0-9]+-[0-9]+", args.bytes)):
        parts = args.bytes.split("-")
        minBytes = int(parts[0])
        maxBytes = int(parts[1])
    elif (args.bytes):
        minBytes = int(args.bytes)
        maxBytes = int(args.bytes)
    minRepeating = 1
    maxRepeating = 1
    if (args.repeat_width and re.match(r"[0-9]+-[0-9]+", args.repeat_width)):
        parts = args.repeat_width.split("-")
        minRepeating = int(parts[0])
        maxRepeating = int(parts[1])
    elif (args.repeat_width):
        minRepeating = int(args.repeat_width)
        maxRepeating = int(args.repeat_width)
    # Let the glitching commense!
    originalByteList = list(open(args.infile, "rb").read())
    for i in range(args.amount):
        iterations = random.randint(minChanges, maxChanges)
        bytesToChange = random.randint(minBytes, maxBytes)
        repeatWidth = random.randint(minRepeating, maxRepeating)
        messWithFile(originalByteList, iterations, bytesToChange, repeatWidth, i+1)
    if (not args.quiet):
        print("Finished writing files")


# Constants
transforms = {
    "change": changeBytes,
    "reverse": reverseBytes,
    "repeat": repeatBytes,
    "remove": removeBytes,
    "zero": zeroBytes,
    "insert": insertBytes,
    "replace": replaceBytes,
    "move": moveBytes
}

# Setup argparser
parser = argparse.ArgumentParser(description="Do terrible things to data.")

# Required arguments
a = Tk()
a.withdraw()
print("Opening file selection prompt...")
file_path = filedialog.askopenfilename()

# GUI for option selection
root = Tk()
root.title("Args")

# def printvars():
#     args = [mode.get(), npic.get(), nrdm.get(), nbyt.get(), nrep.get()]
#     print(args)
#     root.destroy()

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

Button(mainframe, text='ADD',bd=10,command=root.quit).grid(row = 5, column = 1)
root.mainloop()

# def cont():
parser.add_argument("-m", "--mode", default=mode.get(), help="File change mode")
parser.add_argument("-i", "--infile", default=file_path, help="Input folder")

# defaulting
vals = [npic.get(), nrdm.get(), nbyt.get(), nrep.get()]
print(vals)
npic = int(vals[0])
for v in range(1,3):
    if vals[v] is '' : vals[v] = None
nrdm = vals[1]
nbyt = vals[1]
nrep = vals[1]

# Optional arguments
parser.add_argument("-o", "--outdir", default="./", help="Output folder")
parser.add_argument("-s", "--seed", type=int, help="Seed to use for random")
parser.add_argument("-a", "--amount", type=int, default=npic, help="Amount of new files to create")
parser.add_argument("-c", "--changes", default=nrdm, help="Amount of random changes. Can be in a range, like '1-10'.")
parser.add_argument("-b", "--bytes", default=nbyt, help="Amount of bytes to change each change. Can be in a range, like '1-10'.")
parser.add_argument("-r", "--repeat-width", default=nrep, help="Amount of bytes to repeat. Can be in a range, like '1-10'.")
parser.add_argument("-q", "--quiet", default=False, action="store_true", help="Surpress logging")
parser.add_argument("--output-iterations", type=int, default=0, help="How many iterations between outputs")

# args init
args = parser.parse_args()
print(args)

# args["infile"] = file_path

main()

# Label(text='Mode').place(x=50, y=30)