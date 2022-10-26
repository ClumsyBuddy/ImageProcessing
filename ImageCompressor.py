from email.mime import base
import os
import sys
from glob import glob
from PIL import Image
from time import sleep


cols = 25
lines = 10
os.system(f'mode con: cols={cols} lines={lines}')

#folder-name
path = "./"#sys.argv[1]

basewidth = 0
Resizename = ""

MainDir = "ProcessedImages"
WEBPDir = "WEBP"
CompressedDir = "Compressed"

print("Change Size? y or n")
a = input()
AspectRatio = False

if a == 'y':
    print("Input a number: ")
    basewidth = int(input())
    print("Keep Aspect Ratio?")
    if input() == "y":
        AspectRatio = True
    
print("Quality: ")
quality = input()

if int(quality) < 0 or int(quality) > 100:
    print("image quality out of range[0-100] ;/:/")
    sys.exit(0)

img_list = []
for img_name in glob("./"+MainDir+"/"+WEBPDir+'/*'):
    # one can use more image types(bmp,tiff,gif)
    if img_name.endswith(".webp"): #or img_name.endswith(".JPG") or img_name.endswith(".png"):
        # extract images name(image_name.[jpg|png]) from the full path
        img_list.append(img_name.split('\\')[-1])

def has_transparency(img): #This checks if the image has the transparency header, then checks its mode.
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

# print(img_list)   # for debug
for img_name in img_list:
    name = img_name.split('.')
    # sleep(5)
    if len(name) > 2:
        print("Periods cannot be in the name")
        sys.exit(0)
    im = Image.open("./"+MainDir+"/"+WEBPDir+"/"+img_name)
    size = im.size
    if basewidth > 0: #If we are changing the width and height we enter this if statement
        size = basewidth, basewidth
        if AspectRatio == True:
            wpercent = (basewidth/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            size = basewidth, hsize
        
        new_im = Image.new('RGBA', size, "WHITE") #We create a new Image with a white background
        im.thumbnail(size=size, resample=Image.Resampling.LANCZOS) #We add antialiasing, probably need to move this around

        img_w, img_h = im.size #get the size of the previous image
        bg_w, bg_h = new_im.size #get the size of the new white background image
        img_offset = (0,0)
        if basewidth > img_w:
            im = im.resize(size)
        else:
            img_offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2) #Find offset to fit old image into new image
        
        if has_transparency(im): #Check if the image has transparency, if it does then use a image mask
            new_im.paste(im, img_offset, im)
        else:
            new_im.paste(im, img_offset)

        Resizename = f"-{basewidth}x" 
        new_im.convert("RGB").save("./"+MainDir+"/"+CompressedDir+"/"+name[0]+"-Compressed"+Resizename+"."+name[1], quality=quality, optimize=True)
    else:
        im.thumbnail(size=im.size, resample=Image.Resampling.LANCZOS)
        new_image = Image.new("RGBA", im.size, "WHITE") # Create a white rgba background
        if has_transparency(im):
            new_image.paste(im, (0, 0), im) # Paste the image on the background. Go to the links given below for details.
        else:
            new_image.paste(im, (0, 0))

        new_image.convert("RGB").save("./"+MainDir+"/"+CompressedDir+"/"+name[0]+"-Compressed"+"."+name[1], quality=quality, optimize=True)
