"""
Created on Sunday 2021-04-25

@author Ethan Tran

to do:
- its functional poggers, prolly some undiscovered bugs left to discover ;-;
- convert this to classes so an interface file can be implemented
"""
import config
import requests
import selenium
from selenium import webdriver
import os
import time
import io
import cv2
import numpy as np
import matplotlib.pyplot as plt

#returns chrome webdriver
def getWebDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome(executable_path = config.driverPath, options = options)
    return wd

#scroll through image page
def scroll(wd: webdriver):
    wd.execute_script("window.scrollTo(0, document.documentElement.scrollTop || document.body.scrollTop);")


"""
creates .txt file to record image urls that have been scraped for specific query
@param {string} search query
@param {set} set of scraped URLs 
"""
def urlLogs(query:str, URLs:set):
    with open(f"log{query}.txt", "a+") as f:
        for url in URLs:
            f.write(url + "\n")

"""
returns set with elements present in URLs but not in log files (remove duplicate urls in URLs compared to log file)
@param: {string} query
@param: {set} set of scraped URLs
"""
def checkDuplicates(query:str, URLs:set):
    try:
        with open(f"log{query}.txt", 'r+') as f:
            lines = f.read().splitlines() #read all lines and remove \n
            return  set(URLs) - set(lines) #returns set of strings found in URLs and not in lines
    #file doesn't exist (new query)
    except Exception as e:
        f = open(f"log{query}.txt", 'x')
        return URLs
"""
returns set of image urls from google
@param: {string} search term
@param: {number} number of URLS to obtain
@param: {webdriver} selenium webdriver
@param: {number} keeping track of what image urls have been returned - when user wants more images
"""
def getImgURL(query:str, numURL:int, wd:webdriver):
    wd.get(config.searchURL.format(q = query))

    imgURLs = set()
    imageCount = 0
    resultStart = 0

    if(numURL < 0):
        print("Error please enter a valid integer")

    while imageCount < numURL:
        scroll(wd)

        #get list of image thumbnails
        thumbnailList = wd.find_elements_by_css_selector("img.Q4LuWd")
        numThumbnail = len(thumbnailList)
        print(f"Found: {numThumbnail} search results. Extracting links from {resultStart}:{numThumbnail}")

        for thumbnail in thumbnailList[resultStart:numThumbnail]:
            try:
                #click thumbnail to get image behind it
                thumbnail.click()
                #print("click")
                time.sleep(config.timeToSleep)
            except Exception:
                print(f"Error in clicking thumbnail")
                continue
        
            #get image URLs
            images = wd.find_elements_by_css_selector('img.n3VNCb') 
            for image in images:
                #check if the image has attriubte 'src' and check that it also has 'http'
                if image.get_attribute('src') and 'http' in image.get_attribute('src'): 
                    imgURLs.add(image.get_attribute('src'))
            
            #print(imgURLs)
            #check duplicates
            imgURLs = checkDuplicates(query, imgURLs)
            imageCount = len(imgURLs)

            if len(imgURLs) >= numURL:
                print(f"Done! Found: {imageCount} image links")
                urlLogs(query, imgURLs)
                break

            #else, continue (for loop goes again)
        
        #if there are not enough images in the page, load more images (only hapens with huge amounts of images, > 50)
        #or if you run the program enough times with the same query
        else: 
            print("Found:", len(imgURLs), "image links, looking for", numURL - len(imgURLs), "more...")
            time.sleep(5)
            return
            loadMoreButton = wd.find_element_by_css_selector(".mye4qd")
            if loadMoreButton:
                wd.execute_script("document.querySelector('.mye4qd').click();") #click load more button
            
            resultStart = len(thumbnailList)
    
    return imgURLs

"""
returns array of image contents from url
@param {set} image url set
"""
def getImage(URLs:set):
    
    imageContents = []
    for url in URLs:
        try:
            imageContent = requests.get(url).content #get payload in raw bytes
            imageContents.append(imageContent)
        except Exception as e:
            print(f"ERROR - Could not get {url} - {e}")
    
    return imageContents

"""
displays images using MatplotLib
@param {bytes array} array of image content bytes
"""
def displayImages(imageContents):
    for imageContent in imageContents:
        #sometimes there are errors, skip that image
        try:
            imageStream = io.BytesIO(imageContent) #creates in-memory buffer, allows file-like operations to be performed on it
            image = cv2.imdecode(np.frombuffer(imageStream.read(), np.uint8), 1) #reads data from memory cache and decodes into image format
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert BGR to RBG
            plt.imshow(image)
            plt.xticks([]), plt.yticks([])  #hide tick values on X and Y axis
            plt.show()
        except Exception as e:
            print(e)
            continue


#main function for testing
def main():
    wd = getWebDriver()

    test = getImgURL("cat", 2, wd)
    imageContent = getImage(test)
    displayImages(imageContent)

    wd.quit()

if __name__ == "__main__":
    main()