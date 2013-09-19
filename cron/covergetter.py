#!/usr/bin/python

import json
import os
import time
import requests
import Image
from gimage import getImage
from StringIO import StringIO
from requests.exceptions import ConnectionError
 
def getCovers(path):

  BASE_PATH = path # os.path.join(path, query)

  for filename in os.listdir(BASE_PATH):
    getImage(filename.split('.')[0],os.path.join(BASE_PATH,filename),filename.split('.')[0] 
 
# Example use
#getCovers('/www/hacks.so/albumart')
