
from PIL import Image, ImageOps
import urllib, cStringIO
import sys
from pyfaces_main import pyfaces_get_dist

def faceget(img, xcenter, ycenter, width, filename='test.png'):
    """Download photo at URL, return a square cropped image centered at XCENTER and YCENTER (percent) of size WIDTH (pixels)."""

    # crop photo
    w, h = img.size
    xcoord, ycoord = xcenter * w, ycenter * h
    left = int(xcoord - width/2)
    right = int(xcoord + width/2)
    top = int((ycoord - width/2) * 6 / float(5))
    bottom = int((ycoord + width/2) * 6 / float(5))
    box = (left, top, right, bottom)
    
    cropped = img.crop(box)
    cropped.save(filename)
    
def get_face(url, xcenter, ycenter, fn):
    
    f = cStringIO.StringIO(urllib.urlopen(url).read())
    original_img = Image.open(f)
    w, h = original_img.size
    
    width_to_dist = dict()
    
    
    for width_percent in range(10,100,10):
        filename = fn+str(width_percent)+'.png'
        faceget(original_img, xcenter, ycenter, width_percent*w/float(100), filename)
        img = Image.open(filename)
        
        img = img.resize((125,150))
        img.save(filename)
        dist = pyfaces_get_dist(filename)
        #print width_percent,dist
        width_to_dist[width_percent] = dist
    
    min_width, min_dist = 100, 1
    for width, dist in width_to_dist.iteritems():
        if dist < min_dist:
            min_width = width
            min_dist = dist
    
    img = Image.open(fn+str(min_width)+'.png')
    img.save('max/'+fn+'_'+str(round(min_dist,3))+'.png')
        

#get_face("http://www.uni-regensburg.de/Fakultaeten/phil_Fak_II/Psychologie/Psy_II/beautycheck/english/durchschnittsgesichter/m(01-32)_gr.jpg", .5, .5)
    