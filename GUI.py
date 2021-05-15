"""
Created on Sunday 2021-05-01

@author Ethan Tran

to do:
- its functional poggers, prolly some undiscovered bugs left to discover ;-;
- fix the bug where the GUI would have to be closed to show the next image (if > 1 images are requested)
- convert to class implmentation (if not too lazy) 
"""
import tkinter as tk
import webscraping

wd = webscraping.getWebDriver()

def search():
    query = queryEntry.get()
    numURL = int(numURLEntry.get())
    imgURLs = webscraping.getImgURL(query, numURL, wd)
    display(imgURLs)

def display(imgURLs):
    imageContent = webscraping.getImage(imgURLs)
    webscraping.displayImages(imageContent)

def close():
    wd.quit()
    window.destroy()

window = tk.Tk()
window.title("Image Scraper")
window.resizable(width=False, height=False)


frame = tk.Frame(master=window)
queryEntry = tk.Entry(master=frame)
queryLabel = tk.Label(master=frame, text="Enter image search query")

numURLEntry = tk.Entry(master=frame)
numURLLabel = tk.Label(master=frame, text="Enter number of images")

queryLabel.grid(row=0, column=0, sticky="e")
numURLLabel.grid(row=1, column=0, sticky="e")

queryEntry.grid(row=0, column=1, sticky="w")
numURLEntry.grid(row=1, column=1, sticky="w")

searchBtn = tk.Button(master=window, text="Search", command= search)

quitBtn = tk.Button(master = window, text = "Quit", command =close)

frame.grid(row=0, column=0, padx=10)
searchBtn.grid(row=0, column=1, pady=10)
quitBtn.grid(row = 1, column =1, pady = 10)

window.mainloop()