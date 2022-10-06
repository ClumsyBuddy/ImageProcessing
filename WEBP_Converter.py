# --cwebp_compressor.py--

# cmd> python cwebp_compressor.py folder-name 80

import sys
from subprocess import call
from glob import glob
from PIL import Image
from time import sleep
import os

#folder-name
path = "./"#sys.argv[1]
#quality of produced .webp images [0-100]
quality = sys.argv[1]

basewidth = 0

MainDir = "ProcessedImages"
JPGDir = "JPG"
WEBPDir = "WEBP"
CompressedDir = "Compressed"

if not os.path.exists("./"+MainDir):
    os.mkdir("./"+MainDir)
if not os.path.exists("./"+MainDir+"/"+JPGDir):
    os.mkdir("./"+MainDir+"/"+JPGDir)
if not os.path.exists("./"+MainDir+"/"+WEBPDir):
    os.mkdir("./"+MainDir+"/"+WEBPDir)
if not os.path.exists("./"+MainDir+"/"+CompressedDir):
    os.mkdir("./"+MainDir+"/"+CompressedDir)

if int(quality) < 0 or int(quality) > 100:
    print("image quality out of range[0-100] ;/:/")
    sys.exit(0)

img_list = []
for img_name in glob(path+'/*'):
    # one can use more image types(bmp,tiff,gif)
    if img_name.endswith(".jpg") or img_name.endswith(".png") or img_name.endswith(".jpeg") or img_name.endswith(".PNG") or img_name.endswith(".tif"):
        # extract images name(image_name.[jpg|png]) from the full path
        img_list.append(img_name.split('\\')[-1])
        

def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        # Need to convert to RGBA if LA format due to a bug in PIL
        alpha = im.convert('RGBA').getchannel("A")
        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        new_im = bg.convert("RGB")
        return new_im
    else:
        return im

# print(img_list)   # for debug
for img_name in img_list:
    name = img_name.split('.')
    print(path+img_name)
    if  name[1] == "tif": #Basically tif files suck and we convert to jpg before converting to webp. 
        im = Image.open(path+img_name)
        im_rgb = remove_transparency(im=im)
        im_rgb.save("./"+MainDir+"/"+JPGDir+"/"+name[0]+"."+"jpg")
        cmd='cwebp \"'+path+'/'+MainDir+"/"+JPGDir+"/"+name[0]+".jpg"+'\" -q '+quality+'  -lossless -m 6 -mt -af -o \"'+path+'/'+MainDir+"/"+WEBPDir+"/"+(img_name.split('.')[0])+'.webp\"'
        call(cmd, shell=False)
    else:
        cmd='cwebp \"'+path+'/'+img_name+'\" -q '+quality+'  -lossless -m 6 -mt -af -o \"'+path+"/"+MainDir+"/"+WEBPDir+'/'+(img_name.split('.')[0])+'.webp\"'
        call(cmd, shell=False)
    # though the chances are very less but be very careful when modifying the below code
    # cmd='cwebp \"'+path+'/'+name[0]+".jpg"+'\" -q '+quality+'  -lossless -m 6 -mt -o \"'+path+'/'+(img_name.split('.')[0])+'.webp\"'
    #cmd='cwebp \"'+path+'/'+img_name+'\" -q '+quality+' -lossless -exact -m 6 -o \"'+path+'/'+(img_name.split('.')[0])+'.webp\"'
    #cmd='cwebp \"'+path+'/'+img_name+'\" -q '+quality+' -o \"'+path+'/'+(img_name.split('.')[0])+'.webp\"'
    # running the above command
    #call(cmd, shell=False)

cmd = "python ImageCompressor.py"
call(cmd, shell=False)

