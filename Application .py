import tkinter

class hashtag_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column =0 , row = 0 , sticky = 'EW')

        button = tkinter.Button(self,text = u"OK")
        button.grid(column=1 , row=0)

        label = tkinter.Label(self , anchor = "w" , fg="white" , bg="blue")
        label.grid(column=0 , row=1 , columnspan=2 , sticky='EW')


        self.grid_columnconfigure(0,weight=1)

if  __name__  == "__main__":
    app=hashtag_tk(None)
    app.title('Sentiment analyser')
    app.mainloop()#looping indefiniitely waiting for button driven events

