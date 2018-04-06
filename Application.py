import tkinter as tk
from tkinter import *
from constants import *
from StreamTweets import MyListener , fetchtweet , stop_stream
import threading
from globals import *
from countwordsSHE import *
import tkinter.filedialog as dialog
import globals as g
from PIL import ImageTk as itk
from PIL import Image


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

        for F in (StartPage, PageOne, PageTwo , PageThree , PageFour , PageFive , PageSix):

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
    
        label = tk.Label(self, text="Sentiment Analyser", font=main_heading , bg = "lightblue")
        

        button = tk.Button(self, text="Start", font = mid_heading,
                            command=lambda: controller.show_frame(PageOne) )

        img = Image.open('senti.png')
        
        #resized = img.resize((600 , 300))
        pimg = itk.PhotoImage(img)
        imgLabel = tk.Label(self , image = pimg)
        imgLabel.image = pimg
        
        
        label.pack(pady=75,padx=10)
        button.pack(pady=20  , ipadx = 60)  #Using pack manager 
        imgLabel.pack(pady = 50)
        

class PageOne(tk.Frame , threading.Thread):
    

    def __init__(self, parent, controller):
        global hashtagText , hashtag 
        tk.Frame.__init__(self, parent , bg = "LightSteelBlue2")
        img1 = Image.open('bird.jpg')
        
        resized = img1.resize((900 , 280))
        img = itk.PhotoImage(resized)
        panel = tk.Label(self, image = img)
        panel.image = img
        panel.place(x=20 , y = 25)

        label = tk.Label(self, text="Enter the hashtag", font=main_heading , bg = "lightblue")
        label.pack(pady=50,padx=10)
        self.controller = controller

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
                    
        
        hashtagText = tk.Entry(self , font = ("TimesNewRoman" , "16"))
        
        hashtagText.pack(pady = 20 , ipady = 10 )

        button2 = tk.Button(self, text="Stream Tweets",font = sub_heading , 
                            command=self.printhashtag)
            
        button2.pack(pady = 20)
        label2 = tk.Label(self , text = "OR" , font = sub_heading )
        label2.pack(pady =20)
        button3 = tk.Button(self , text = "Upload the JSON file" , font = sub_heading ,bg = "aquamarine2",
                                        command = self.uploadClick)
        

        button4 = tk.Button(self , text = "DONE" , font = sub_heading , 
                                            command = self.doneClick )
        button4.place(x=700 , y= 440 , width = 120 , height = 25)

        button3.pack(pady = 50)
        
        button1.pack(pady = 40)

    def doneClick(self):
        labelAl = tk.Label(self , text = "Algorithm is running..." , font = mid_heading,
                                                        bg = "LightSteelBlue2" )
        labelAl.place(x=375 , y = 450 , width = 300 , height = 50 )
        mainAnalysis()
        if g.filename is not '':

            self.controller.show_frame(PageFour)
        

    def uploadClick(self):
        g.uploaded = True
        g.filename = dialog.askopenfilename()
        print(g.filename)

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
        tk.Frame.__init__(self, parent , bg = "papaya whip")
        self.controller = controller
        label = tk.Label(self, text="Streaming!!!", font=main_heading , bg = "papaya whip")
        label.pack(pady=10,padx=10)

        button3 = tk.Button(self , text ="Stop streaming" , font = sub_heading,
                            command = self.stopButtonClick)
        button3.pack(pady=20)

        button1 = tk.Button(self, text="Back to Home", font = sub_heading,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack( pady = 20 , padx = 200,side = LEFT)

        button2 = tk.Button(self, text="Page One",font = sub_heading,
                            command=lambda:controller.show_frame(PageOne))
        button2.pack( pady = 20 , padx = 100 , side=LEFT )
        button4 = tk.Button(self ,text = "Start Sentiment analysis", font = sub_heading,
                            command = self.startClick)
        button4.place(x = 350 , y = 200 , height=25 , width = 300)

    def startClick(self):
        labelAl = tk.Label(self , text = "Algorithm is running..." , font = sub_heading , bg = "papaya whip")
        labelAl.place(x=370 , y = 230 , width = 300 , height = 50 )
        mainAnalysis()
        self.controller.show_frame(PageFour)



    def printhashtag(self ,hashtagText):
        print(hashtagText.get())

    def stopButtonClick(self):
        numTweet = tk.Label(self , text = "Number of tweets streamed:"+str(g.tweetnum) , font = mid_heading , 
                                                                    bg = "bisque")
        numTweet.place(x = 250 , y = 150 , width = 500 , height = 25)
        stop_stream()

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

        tk.Frame.__init__(self, parent , bg = "LightGoldenrod1")
        #print(semantic_orientation)
        button3 = tk.Button(self,text = "View top Tweets" , font = sub_heading,
                                            command = self.topClick)
        button3.place(x = 100 , y = 500)
        button3 = tk.Button(self,text = "View top positive words" , font = sub_heading)
        button3.place( x = 350 , y = 500)
        button3 = tk.Button(self,text = "View top negative words" , font = sub_heading)
        button3.place( x = 700 , y =500)

        label1 = tk.Label(self , text ="Enter the word for which sentiment is to be found" , font = mid_heading)
        label1.pack(pady=20)
        self.controller = controller
        self.wordEntry = tk.Entry(self , font = sub_heading)
        self.wordEntry.pack(pady = 20)

        button1 = tk.Button(self , text="Enter" , font = sub_heading,
                                            command = self.semOrientation )
        button1.pack(pady = 20 )
        button2 = tk.Button(self,text ="Increase Accuracy\n Method 1" , font = min_heading,
                                            command = self.accuracyoneClick )
        # button3 = tk.Button(self , text = "Increase accuracy method 2" , font = mid_heading,
        #                                     command = self.accuracytwoclick)
        button2.place(x=700 , y = 150 , width = 210, height = 45)
        # button3.pack()

    def topClick(self):
        self.controller.show_frame(PageSix)

    def accuracyoneClick(self):
        self.controller.show_frame(PageFive)


    # def accuracytwoclick(self):
    #     self.controller.show_frame(PageSix)

    def semOrientation(self):
        global semantic_orientation
        word = self.wordEntry.get()
        result = semantic_orientation[word]
        label2 = tk.Label(self , text="Semantic orientation of "+word+": "+str(result) , font = min_heading_bold,
                                                                        bg = "goldenrod1")
        # if(result>0):
        #     label2['text'] = "Semantic orientation of "+word+": "+str(result) + '😃'
        # else:
        #     label2['text'] = "Semantic orientation of "+word+": "+str(result) + '🙁'

        label2.pack(pady=30)


class PageFive(tk.Frame):
    i=0

    def __init__(self , parent  , controller):
       
        tk.Frame.__init__(self , parent , bg ="SeaGreen2")
        print(g.toptweets)
        topList = g.toptweets[:6]
        print(topList)
        qlabel = tk.Label(self , text = "Enter the positive or negative words in these tweets" , 
                                                            font = sub_heading)
        qlabel.pack(pady = 20)

        self.tLabel = tk.Label(self , text = g.toptweets[self.i] , font = sub_heading)
        self.i+=1
        self.tLabel.pack(pady  = 20 , ipady = 15)
        self.word = tk.Entry(self , font = min_heading)
        self.word.pack(pady = 50 , ipady = 15)
        self.controller = controller
        button1 = tk.Button(self , text = "Positive" , font = min_heading_bold , 
                            command = self.posButtonClick )
        button1.place(x = 350 , y = 350 , width = 120 , height = 25)
        button2 = tk.Button(self , text = "Negative" , font = min_heading_bold , 
                            command = self.negButtonClick )
        button2.place(x = 550 , y = 350 , width = 120 , height = 25)
        button3 = tk.Button(self , text = "NEXT" , font = sub_heading,
                        command = self.nextClick)
        button3.place(x = 425 , y = 400 , width = 150 , height = 30)

    def nextClick(self):
        if(self.i <=5):
            tempstr =  g.toptweets[self.i]
            char_list = [tempstr[j] for j in range(len(tempstr)) if ord(tempstr[j]) in range(65536)]
            tempstr = ''
            for  j in char_list:
                tempstr+=j
            
            self.tLabel['text'] = tempstr
            self.i+=1
        if(self.i == 6 ):
            dLabel = tk.Label(self , text = "Running modified algorithm..." , font = sub_heading)
            dLabel.pack(pady = 20)
            mainAnalysis()
            self.controller.show_frame(PageFour)
            dLabel.destroy()

    
    def posButtonClick(self):
        global positive_vocab
        
        positive_vocab.append(self.word.get())
        print(positive_vocab)
        self.word.delete(0,END)
        



    def negButtonClick(self):
        global negative_vocab
        
        print(self.word.get())
        negative_vocab.append(self.word.get())
        print(negative_vocab)
        self.word.delete(0,END)
        




class PageSix(tk.Frame):
    i=0

    def __init__(self,parent , controller):
        tk.Frame.__init__(self , parent , bg = 'thistle2')
        self.controller = controller
        self.tLabel = tk.Label(self , text = g.toptweets[self.i] , font = sub_heading , bg = 'thistle2')
        self.i+=1
        self.tLabel.pack(pady = 20)
        button3 = tk.Button(self , text = "NEXT" , font = sub_heading,
                        command = self.nextClick)
        button3.pack(pady = 30)

    def nextClick(self):
        if(self.i <=10):
            tempstr =  g.toptweets[self.i]
            char_list = [tempstr[j] for j in range(len(tempstr)) if ord(tempstr[j]) in range(65536)]
            tempstr = ''
            for  j in char_list:
                tempstr+=j
            
            self.tLabel['text'] = tempstr
            self.i+=1
        if(self.i == 11 ):
            self.controller.show_frame(PageFour)




if __name__ == "__main__":
    app = EmotionApp()
    app.geometry(str(WIDTH)+'x'+str(HEIGHT))
    app.title("Sentiment Analyzer")
    app.mainloop()
