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
import magic
from enum import Enum

class Orientation(Enum):
    """
    Enumerations for image orientation.
    """
    PORTRAIT = 0
    LANDSCAPE = 1


def compress_image(path, image_format, MAX_WIDTH, MAX_HEIGHT):
    """
    Compresses the image in path and replaces the
    uncompressed image with the compressed one.
    """
    
    try:   
        img = Image.open(path)
    except IOError:
        print ("You don't have permissions to open the image!")
        sys.exit()

    (width, height) = img.size
    orientation = Orientation.LANDSCAPE if width >= height else Orientation.PORTRAIT

    # Convert PNG images to RGB to save them as JPEG images
    if image_format == 'PNG':
        img = img.convert('RGB')

    if width > MAX_WIDTH or height > MAX_HEIGHT:
        if orientation == Orientation.LANDSCAPE:
            if width > MAX_WIDTH:
                height = int(round((MAX_WIDTH / float(width)) * height))
                width = MAX_WIDTH
            else:
                width = int(round((MAX_HEIGHT / float(height)) * width))
                height = MAX_HEIGHT
        else:
            if height > MAX_HEIGHT:
                width = int(round((MAX_HEIGHT / float(height)) * width))
                height = MAX_HEIGHT
            else:
                height = int(round((MAX_WIDTH / float(width)) * height))
                width = MAX_WIDTH
        img = img.resize((width, height), Image.ANTIALIAS)

    try:
        img.save(path, format="JPEG", quality=85)
    except PermissionError:
        print ("You don't have permissions to save the image!\nExiting program...")
        sys.exit()


def main():
    """
    Checks if path was given and finds recursively files in directory and 
    its subdirectories.
    """

    if len(sys.argv) <= 1:
        msg = "Give path to folder where images are searched\n"
        msg += "$ python %s <path>" % sys.argv[0]
        sys.exit(msg)

    path = sys.argv[1]
    file_counter = 0
    FILE_TYPES = [
        "image/jpeg",
        "image/png",
    ]

    # Prompt for max resolutions
    while True:
        try:
            MAX_WIDTH = int(input("Enter max width: "))
            MAX_HEIGHT = int(input("Enter max height: "))
            break
        except ValueError:
            print ("Not a valid integer!\nPlease type an integer.")
        except KeyboardInterrupt:
            print ("\nExiting program...")
            sys.exit()

    for filename in glob.iglob(path+'/**', recursive=True):
        if os.path.isdir(filename):
            # Don't try to compress directories
            continue
        else:
            mimetype = magic.from_file(filename, mime=True)
            if mimetype in FILE_TYPES:
                image_format = mimetype.split('/')[1].upper()
                compress_image(filename, image_format, MAX_WIDTH, MAX_HEIGHT)
                print ("Resized image: %s" % (filename))
                file_counter += 1
    print ("%d images were resized!\nDone!" % (file_counter))    


if __name__ == '__main__':
    main()
