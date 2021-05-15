"""
Created on Saturday 2021-05-08

@author Ethan Tran

to do:
- its functional poggers
"""
import webscraping

wd = webscraping.getWebDriver()

#driver function
def main():
    query = input("Enter your search query: ")
    numURL = int(input("Enter number of images desired: "))
    imgURLs = webscraping.getImgURL(query, numURL, wd)
    imageContent = webscraping.getImage(imgURLs)
    webscraping.displayImages(imageContent)
    
    message = "Do you want to continue? y/n: "
    cont = prompt(message)
    if cont == True:
        main()
    else:
        print("Until next time")
        wd.quit()

"""
Determines if user enters a valid input. return True if it's a confirmation, False if it's a refusal
@param: {string} prompt message
"""
def prompt(message):
    val = input(message)
    val.lower()
    if val == "y":
        return True
    elif val == "n":
        return False
    else:
        print("Error, please type a valid input") 
        prompt(message) 

if __name__ == "__main__":
    main()