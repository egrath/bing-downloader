#!/usr/bin/python3

from urllib.request import urlopen
from urllib.error import HTTPError
from xml.dom.minidom import parseString
import os


ad=0        # already downloaded
sd=0        # successfully downloaded
fd=0        # failed to download

outputdir="out"
 
# check if the output directory exists and exit if not
if not os.path.isdir(outputdir):
    print("output directory (", os.path.abspath(outputdir), ") does not exist", sep="")
    exit()   

# work through all Bing markets
markets=["US", "AU", "GB", "DE", "JP", "CN", "BR", "NZ", "FR", "CA"]
for market in markets:
    print("Retrieving list of images for", market, ": ", end="")
    try:
        f = urlopen("https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=7&pid=hp&cc=%s" % market, data=None, timeout=4)
        print("OK")
        rawXml = f.read()
        dom_object = parseString(rawXml)
        bases = dom_object.getElementsByTagName("urlBase")
        for b in bases:
            # retrieve images
            sizes = [ "_1920x1080", "_1920x1200" ]
            for size in sizes:
                imageUrl = "https://www.bing.com" + b.firstChild.wholeText + size + ".jpg"
                outputImage = imageUrl.split("=")[1]
            
                # does the image already exist?
                print("    Downloading:", outputImage.ljust(70), end="")
                if not os.path.isfile("out/" + outputImage):
                    try:
                        f = urlopen(imageUrl, data=None, timeout=4)
                        outputFile = open("out/" + outputImage,"wb")
                        outputFile.write(f.read())
                        outputFile.close()
                        print("SUCCESS")
                        sd=sd+1
                    except (HTTPError, IOError) as error:
                        print("ERROR (",error,")",sep="")
                        fd=fd+1
                else:
                    print("ALREADY DOWNLOADED")
                    ad=ad+1
    except Exception as e:
        print("error, was: ", e );

print("Successfully downloaded : ", sd)
print("Already downloaded      : ", ad)
print("Error during download   : ", fd)
