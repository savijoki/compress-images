#!/usr/bin/python3
#
# Compression script that finds images inside given directory
# and its subdirectories.
#
# User has to have read/write permissions in order to compress
# images.
# 
# 
# Usage:
# 
# $ python3 main.py <path-to-directory>
# 


import os
import re
import glob
import sys
from PIL import Image


def compress_image(path):
    """
    Compresses the image in path and replaces the
    uncompressed image with the compressed one.
    
    TODO:
        - If the user doesn't have permissions to read/write file, handle
          this exception properly
        - Handle png image compression as well
        - Prompt user for max resolutions
    """
    img = Image.open(path)
    
    MAX_WIDTH = 960
    MAX_HEIGHT = 1080
    (width, height) = img.size

    if width > MAX_WIDTH or height > MAX_HEIGHT:
        if width > height:
            if width > MAX_WIDTH:
                height = int(round((MAX_WIDTH / float(width)) * height))
                width = MAX_WIDTH
        else:
            if height > MAX_HEIGHT:
                width = int(round((MAX_HEIGHT / float(height)) * width))
                height = MAX_HEIGHT
        img = img.resize((width, height), Image.ANTIALIAS)

    img.save(path, format="JPEG", quality=85)


def main():
    """
    Checks if path was given and finds recursively files in directory and 
    its subdirectories.

    TODO: 
        - Check if file is an image
    """

    if len(sys.argv) <= 1:
        msg = "Give path to folder where images are searched\n"
        msg += "$ python %s <path>" % sys.argv[0]
        sys.exit(msg)

    path = sys.argv[1]
    file_counter = 0

    for filename in glob.iglob(path+'/**', recursive=True):
        if os.path.isdir(filename):
            # Don't try to compress directories
            continue
        else:
            compress_image(filename)
            print ("Resized image %s" % (path))
            file_counter += 1

    print ("%d images were resized" % (file_counter))    

if __name__ == '__main__':
    main()
