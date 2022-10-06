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
if a == 'y':
    print("Input a number: ")
    basewidth = int(input())
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

# print(img_list)   # for debug
for img_name in img_list:
    name = img_name.split('.')
    # sleep(5)
    if len(name) > 2:
        print("Periods cannot be in the name")
        sys.exit(0)
    im = Image.open("./"+MainDir+"/"+WEBPDir+"/"+img_name)
    size = basewidth, basewidth
    new_im = Image.new('RGB', size, (255, 255, 255))
    if basewidth > 0:
        #wpercent = (basewidth/float(im.size[0]))
        #hsize = int((float(im.size[1])*float(wpercent)))
        
        im.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        img_w, img_h = im.size
        bg_w, bg_h = new_im.size
        img_offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        new_im.paste(im, img_offset)
        
        #im = im.resize((basewidth, basewidth), Image.Resampling.LANCZOS)
        Resizename = f"-{basewidth}x"
    #im = remove_transparency(im, (0,0,0))
    new_im.save("./"+MainDir+"/"+CompressedDir+"/"+name[0]+"-Compressed"+Resizename+"."+name[1], quality=quality, optimize=True)
