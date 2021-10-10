from tkinter import *
from tkinter import filedialog


def openFile():
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("CSV files", "*.csv"),
                                                     ("all files", "*.*")))
    pathInput.config(text=filepath)

def findResult():
    print(0)

window = Tk()
window.resizable(width=False, height=False)

framePath = Frame(window)
framePath.pack(fill=BOTH)

titlePath = Label(framePath, text="File path: ")
titlePath.pack(side=LEFT)
pathInput = Label(framePath, text="Please choose a file", width=50)
pathInput.pack(side=LEFT)
buttonChoose = Button(framePath, text="Choose", command=openFile)
buttonChoose.pack(side=LEFT)

frameWords = Frame(window)
frameWords.pack(fill=BOTH)

titleWords = Label(frameWords, text="Words: ")
titleWords.pack(side=LEFT)
wordsInput = Entry(frameWords, text="Please choose a file", width=50)
wordsInput.pack(side=LEFT)
button = Button(frameWords, text="Enter", command=findResult)
button.pack(side=RIGHT)

frameResult = Frame(window)
frameResult.pack(fill=BOTH)
titleResult = Label(frameResult, text="Result")
titleResult.pack(side=LEFT)

childFrameResult = Frame(frameResult)
childFrameResult.pack()

titleSpam = Label(childFrameResult, text="some spam result")
titleSpam.pack()
titleHam = Label(childFrameResult, text="some ham result")
titleHam.pack()

window.mainloop()
