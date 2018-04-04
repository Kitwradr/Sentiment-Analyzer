# from tkinter import *

# root = Tk()

# w = Label(root, text="red", bg="red", fg="white")
# w.pack(padx=5, pady=20)
# w = Label(root, text="green", bg="green", fg="black")
# w.pack(padx=5, pady=50, side=LEFT)
# w = Label(root, text="blue", bg="blue", fg="white")
# # w.pack(padx=5, pady=20, side=LEFT)
# w.place(x = 20 , y = 30 , width = 120 , height =25)

# mainloop()

#----------------------------------------------

from tkinter import Tk
import tkinter.filedialog as a

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = a.askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)