
from PIL import Image
import urllib, cStringIO
import sys

def faceget(url, xcenter, ycenter, width=50):
    """Download photo at URL, return a square cropped image centered at XCENTER and YCENTER (percent) of size WIDTH (pixels)."""
    
    f = cStringIO.StringIO(urllib.urlopen(url).read())
    img = Image.open(f)
    #img.show()
    
    # crop photo
    w, h = img.size
    xcoord, ycoord = xcenter * w, ycenter * h
    left = int(xcoord - width/2)
    right = int(xcoord + width/2)
    top = int(ycoord - width/2)
    bottom = int(ycoord + width/2)
    box = (left, top, right, bottom)
    
    cropped = img.crop(box)
    cropped.save("test.png")
    


#faceget("http://www.statesymbolsusa.org/IMAGES/Kentucky/squirrel-gray.jpg", .5, .5)
    