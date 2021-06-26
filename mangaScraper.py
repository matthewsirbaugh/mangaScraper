"""
Developed by Matthew Sirbaugh

This script saves all pages of a manga given a specific URL into a pdf

Future updates should include a way to automate the rest of the script so that you
only need to specify the url and the program will generate the name of the pdf.
Once integrated into a flask app, the pdf will also be deleted locally. 

"""
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from PIL import Image
import requests
import shutil
import lxml
import PIL
import os
import re

imgList = []
UrlList = []
pdfList = []

url = "https://mangafast.net/shingeki-no-kyojin-before-the-fall-chapter-1/"
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")

currentDirectory = os.getcwd() #get current working directory
directoryName = "Shingeki No Kyojin - Before The Fall" #name of new directory
path = os.path.join(currentDirectory, directoryName) #join current path and new directory
os.mkdir(path) #make the directory

imgs = soup.findAll("img", {"title": re.compile(r"Shingeki No Kyojin Before The Fall Chapter 1 Page")})

for img in imgs:
    imgUrl = img['src']
    UrlList.append(imgUrl) #list of Urls
    filename = imgUrl.split('/')[-1] #file name (.jpg)
    imgPath = path + '/' + filename #path to image
    imgList.append(imgPath) #final location of images


def download(url, images): #gets images and saves them to previously generated directory
    response = requests.get(url, stream = True)
    if response.status_code == 200:
        response.raw.decode_content = True
        img = Image.open(response.raw)
        img.save(images) 
        print('Success')
    else:
        print('Failure.')

with ThreadPoolExecutor(max_workers=8) as executor: #multithreading to speed up downloads
    executor.map(download, UrlList, imgList)

for images in imgList: #generates list of Image objects
    thisImage = Image.open(images)
    pdfList.append(thisImage)

newList = pdfList[1:] #ensures the last page is not saved first due to implementation of PIL
#print(pdfList[0])
pdfList[0].save(directoryName + '.pdf',save_all=True, append_images=newList) #saves images as single pdf

try:
    shutil.rmtree(path) #removes the generated directory and all images
except OSError as e:
    print("Error: %s : %s" % (path, e.strerror))

print("End")
