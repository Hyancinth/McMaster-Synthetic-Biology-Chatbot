import webscraping
import tkinter as Tk
from tkinter import*
def search(self):
    wd = webscraping.getWebDriver()
    query = queryEntry.get()
    numURL = numURLEntry.get()
    webscraping.getImgURL(query, numURL, wd)

class Window(Frame):
#Defines the settings of the master widget upon initialization 
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
    def init_window(self):
        self.master.title("Image Scraper")
        self.pack(fill = BOTH, expand = 1)  

        queryLabel = Label(text = "Enter image search query")
        queryLabel.pack(fill = BOTH)
        queryEntry = Entry()
        queryEntry.pack(fill = BOTH)

        numURLLabel = Label(text = "Enter number of images to be searched")
        numURLLabel.pack(fill = BOTH, expand = True)
        numURLEntry = Entry()
        numURLEntry.pack(fill = BOTH, expand = True)

        searchBtn = Button(self, text = "Search", command=lambda : search)
        searchBtn.pack(fill = BOTH, expand = True, side = BOTTOM)


root = Tk()
app = Window(root)
root.mainloop()