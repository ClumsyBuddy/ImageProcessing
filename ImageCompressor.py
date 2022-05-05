import os
import sys
from glob import glob
from PIL import Image

cols = 25
lines = 10
os.system(f'mode con: cols={cols} lines={lines}')

#folder-name
path = "./"#sys.argv[1]

size = 0
print("Change Size? y or n")
a = input()
if a == 'y':
    print("Input a number: ")
    size = int(input())
print("Quality: ")
quality = input()

if int(quality) < 0 or int(quality) > 100:
    print("image quality out of range[0-100] ;/:/")
    sys.exit(0)

img_list = []
for img_name in glob(path+'/*'):
    # one can use more image types(bmp,tiff,gif)
    if img_name.endswith(".webp"):
        # extract images name(image_name.[jpg|png]) from the full path
        img_list.append(img_name.split('\\')[-1])

# print(img_list)   # for debug
for img_name in img_list:
    name = img_name.split('.')
    if len(name) > 2:
        print("Periods cannot be in the name")
        sys.exit(0)
    im = Image.open(path+img_name)
    if size > 0:
        im = im.resize((size, size), Image.ANTIALIAS)
    im.save(name[0]+"-Compressed."+name[1], quality=quality, optimize=True)
