import tkinter as tk
from tkinter import LEFT , RIGHT
from constants import *
from StreamTweets import MyListener , fetchtweet , stop_stream
import threading
from globals import *
from countwordsSHE import mainAnalysis 
import tkinter.filedialog as dialog
import globals


#ob = MyListener()
global hashtagText 
flag =0

class EmotionApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top" , fill = "both" , expand = True)

        container.grid_rowconfigure(0,weight = 1)
        container.grid_columnconfigure(0,weight = 1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo , PageThree , PageFour):

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
        

        button = tk.Button(self, text="Start", 
                            command=lambda: controller.show_frame(PageOne))
        

        #button2 = tk.Button(self, text="Visit Page 2",
        #                    command=lambda: controller.show_frame(PageTwo))

        #label.grid()
        
        
        label.pack(pady=100,padx=10)
        button.pack(pady=20)  #Using pack manager 
        #button2.pack()

#hashtagText=None
class PageOne(tk.Frame , threading.Thread):
    

    def __init__(self, parent, controller):
        global hashtagText , hashtag 
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter the hashtag", font=main_heading , bg = "lightblue")
        label.pack(pady=50,padx=10)
        self.controller = controller

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
                    
        
        hashtagText = tk.Entry(self , font = ("TimesNewRoman" , "16"))
        
        hashtagText.pack(pady = 20 , ipady = 10 )

        button2 = tk.Button(self, text="Stream Tweets",
                            command=self.printhashtag)
        button2.pack(pady = 20)
        label2 = tk.Label(self , text = "OR" , font = sub_heading )
        button3 = tk.Button(self , text = "Upload the JSON file" , font = sub_heading ,bg = "lightblue",
                                        command = self.uploadClick)
        label2.pack(pady =20)

        button3.pack()
        
        button1.pack()

    def uploadClick(self):
        globals.filename = dialog.askopenfilename()
        print(globals.filename)

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

        self.contoller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Streaming!!!", font=main_heading)
        label.pack(pady=10,padx=10)
        button3 = tk.Button(self , text ="Stop streaming" , font = sub_heading,
                            command = self.stopButtonClick)
        button3.pack(pady=20)

        button1 = tk.Button(self, text="Back to Home", font = sub_heading,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack( pady = 20 , padx = 50,side = LEFT)

        button2 = tk.Button(self, text="Page One",font = sub_heading,
                            command=lambda:controller.show_frame(PageOne))
        button2.pack( pady = 20 , padx = 50 , side=LEFT )
        button4 = tk.Button(self ,text = "Start Sentiment analysis",
                            command = lambda:controller.show_frame(PageFour))
        button4.pack(pady =20)
    def printhashtag(self ,hashtagText):
        print(hashtagText.get())

    def stopButtonClick(self):
        stop_stream()
        mainAnalysis()

class PageThree(tk.Frame):

    i=0 
    length = len(adjectives_list)
    def __init__(self, parent, controller):
        
    
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select category of theese top words", font=main_heading)
        label.pack(pady=10,padx=10)
        print(adjectives_list[self.i])

        self.topLabel = tk.Label(self , text =adjectives_list[self.i] , font = sub_heading)
        self.i+=1
        label.pack(pady=20)
        self.topLabel.pack(pady=40)
        

        button1 = tk.Button(self , text ="Positive" , font = sub_heading,
                            command = self.posButtonClick)
        button1.pack( padx = 30 , side=LEFT )

        button2 = tk.Button(self , text ="Negative" , font = sub_heading,
                            command = self.negButtonClick)
        button2.pack( padx = 30,side=LEFT)

        button3 = tk.Button(self , text ="Neutral" , font = sub_heading,
                            command = self.neutralButtonClick)
        button3.pack( padx = 30, side=LEFT )

    def posButtonClick(self):
        if self.i == self.length:
            self.raiseFrame4()
        print(adjectives_list[self.i])
        self.topLabel['text'] = adjectives_list[self.i]
        positive_vocab.append(adjectives_list[self.i])
        if self.i<self.length-1:
            self.i+=1
        

    def negButtonClick(self):
        if self.i == self.length-1:
            self.raiseFrame4()
        print(adjectives_list[self.i])
        self.topLabel['text'] = adjectives_list[self.i]
        negative_vocab.append(adjectives_list[self.i])
        if self.i<self.length-1:
            self.i+=1
        

    def neutralButtonClick(self):
        print(self.i)
        print(self.length)
        if self.i == self.length-1:
            print("Inside")
            self.raiseFrame4()
        print(adjectives_list[self.i])
        self.topLabel['text']=adjectives_list[self.i]
        if self.i<self.length-1:
            self.i+=1
        

    def raiseFrame4(self):
        print("Inside!!!!")
        self.controller.show_frame(PageFour)

        

class PageFour(tk.Frame):

    def __init__(self,parent , controller):

        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self , text ="Enter the word for which sentiment is to be found" , font = mid_heading)
        label1.pack(pady=20)
        self.controller = controller
        self.wordEntry = tk.Entry(self , font = sub_heading)
        self.wordEntry.pack(pady = 20)

        button1 = tk.Button(self , text="Enter" , font = sub_heading,
                                            command = self.semOrientation )
        button1.pack(padx = 20 , side=RIGHT)
        button2 = tk.Button(self,text ="Increase Accuracy method 1" , font = mid_heading,
                                            command = self.accuracyoneClick )
        # button3 = tk.Button(self , text = "Increase accuracy method 2" , font = mid_heading,
        #                                     command = self.accuracytwoclick)
        button2.pack()
        # button3.pack()

    def accuracyoneClick(self):
        self.controller.show_frame(PageFive)


    # def accuracytwoclick(self):
    #     self.controller.show_frame(PageSix)




    def semOrientation(self):
        global semantic_orientation
        word = self.wordEntry.get()
        result = semantic_orientation[word]
        label2 = tk.Label(self , text="Semantic orientation of "+word+str(result))
        label2.pack(pady=30)


class PageFive(tk.Frame):

    def __init__(self , parent  , controller):
        tk.Frame.__init__(self , parent)
        label1 = tk.Label()


if __name__ == "__main__":
    app = EmotionApp()
    app.geometry(str(WIDTH)+'x'+str(HEIGHT))
    app.title("Sentiment Analyser")
    app.mainloop()
