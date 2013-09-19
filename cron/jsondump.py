#!/usr/bin/python

import pymongo
import json
from bson import json_util
from datetime import date
import codecs

connection = pymongo.Connection('localhost', 27017)
db = connection['music']
collection = db['mp3s']
songs = []
m3u = []

for song in collection.find().sort("date",-1).limit(30):
    songs.append(song)
    m3u.append([song['remote_url'],song["id3_title"],song["id3_artist"]])
    	
out = json.dumps(songs, sort_keys=True, indent=4, default=json_util.default)
today = date.today()

with codecs.open("/www/hacks.so/playlists/songs-" + today.isoformat() + ".json", "w", "utf-8-sig") as text_file:
    text_file.write(out)

with codecs.open("/www/hacks.so/playlists/playlist-" + today.isoformat() + ".m3u", "w", "utf-8-sig") as text_file:
    text_file.write("#EXTM3U" + '\n\n')
    for url in m3u:
        text_file.write("#EXTINF:, " + url[2]  + " - " + url[1] + '\n')
        text_file.write(url[0]+'\n')

