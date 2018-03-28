import tkinter as tk
from constants import *
from StreamTweets import *
import threading

LARGE_FONT = ("Verdana" , 25)

#ob = MyListener()
global hashtagText 

class EmotionApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top" , fill = "both" , expand = True)

        container.grid_rowconfigure(0,weight = 1)
        container.grid_columnconfigure(0,weight = 1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    
    def show_frame(self,cont):

        frame =  self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self , parent , controller):
        tk.Frame.__init__(self,parent,bg="lightblue")
        label = tk.Label(self, text="Sentiment Analyser", font=main_heading)
        label.pack(pady=100,padx=10)

        button = tk.Button(self, text="Start", 
                            command=lambda: controller.show_frame(PageOne))
        button.pack(pady=20)

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

#hashtagText=None
class PageOne(tk.Frame , threading.Thread):


    def __init__(self, parent, controller):
        global hashtagText , hashtag 
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter the hashtag", font=LARGE_FONT , bg = "lightblue")
        label.pack(pady=100,padx=10)
        self.controller = controller

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
                    
        
        hashtagText = tk.Entry(self , font = ("TimesNewRoman" , "16"))
        
        hashtagText.pack(pady = 20 , ipady = 10 )

        button2 = tk.Button(self, text="Stream Tweets",
                            command=self.printhashtag)
        button2.pack(pady = 20)
        button1.pack()

    def printhashtag(self ):
        self.controller.show_frame(PageTwo)
        global hashtagText
        hashtag = (hashtagText.get())
        self.streamFunc(hashtag)
    
    def streamFunc(self , hashtag):
        
        fetchtweet(hashtag)
        


class PageTwo(tk.Frame ):

    def __init__(self, parent, controller):
        global hashtagText
        hashtag = hashtagText.get()

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Streaming!!!", font=main_heading)
        label.pack(pady=10,padx=10)
        button3 = tk.Button(self , text ="Stop streaming" , font = sub_heading,
                            command = self.stopButtonClick)
        button3.pack(pady=20)

        button1 = tk.Button(self, text="Back to Home", font = sub_heading,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=self.printhashtag(hashtagText))
        button2.pack()
    def printhashtag(self ,hashtagText):
        print(hashtagText.get())

    def stopButtonClick(self):
        stop_stream()



if __name__ == "__main__":
    app = EmotionApp()
    app.geometry(str(WIDTH)+'x'+str(HEIGHT))
    app.mainloop()
