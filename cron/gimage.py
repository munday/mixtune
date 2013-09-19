#!/usr/bin/python

import json
import os
import time
import requests
import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError

def getCovers(path):

  BASE_PATH = path # os.path.join(path, query)

  for filename in os.listdir(BASE_PATH):
    getImage(filename.split('.')[0],BASE_PATH,filename.split('.')[0])

 
def getImage(query, path, name):

  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + ' cover&start=%d&rsz=4&imgsz=xxlarge'
 
  BASE_PATH = path # os.path.join(path, query)
 
  if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)
 
  start = 0 # Google's start query string parameter for pagination.
  while start < 60: # Google will only return a max of 56 results.
    r = requests.get(BASE_URL % start)
    for image_info in json.loads(r.text)['responseData']['results']:
      url = image_info['unescapedUrl']
      try:
        image_r = requests.get(url)
 
        # Remove file-system path characters from name.
        title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '')
 
        file = open(os.path.join(BASE_PATH, '%s.jpg') % name, 'w')
        try:
          Image.open(StringIO(image_r.content)).save(file, 'JPEG')
          return file
        except IOError, e:
          # Throw away some gifs...blegh.
          print 'could not save %s' % url
          continue
        finally:
          file.close()
      except ConnectionError, e:
        print 'could not download %s' % url
        continue

    print start
    start += 4 # 4 images per page.
 
    # Be nice to Google and they'll be nice back :)
    time.sleep(1.5)
 
# Example use
getCovers('/www/hacks.so/albumart')
