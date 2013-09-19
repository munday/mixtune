import pymongo
import urllib2
import urlparse
import re
import datetime
from bs4 import BeautifulSoup
from subprocess import call
import shutil
import os
from os.path import basename
from urlparse import urlsplit
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request
from mutagen.easyid3 import EasyID3
from mp3scrape.items import Mp3ScrapeItem

class BVSpider(CrawlSpider):
    name = 'brooklynvegan'
    start_urls = ['http://brooklynvegan.com']

    rules = [Rule(SgmlLinkExtractor(allow=()), callback='parse_item')]

    def parse_item(self,response):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]
        
        dom = BeautifulSoup(response.body)
        links = dom.find_all(href=re.compile("\.mp3$"))
        items = []
        for link in links:
            if(collection.find_one({'name':link.text,'remote_url':link.get('href')})==None):
                item = Mp3ScrapeItem()
                item['source'] = 'http://brooklynvegan.com'
                item['name'] = link.text
                item['remote_url'] = link.get('href')
                item['date'] = datetime.datetime.utcnow()
                item['local_path'] = download(item['remote_url'],settings['MUSIC_DL_FOLDER'])

                try:
                    audio = EasyID3(item['local_path'])
                    item['id3_title'] = audio['title'][0]
                    item['id3_artist'] = audio['artist'][0]
                    sz = os.path.getsize(item['local_path'])
                    if(item['local_path']!=None):
                        item['local_url'] = item['local_path'].replace(settings['MUSIC_DL_FOLDER'],settings['LOCAL_URL_BASE'])
		        items.append(item)
                except:
                    if(item['local_path']!=None):
                        os.remove(item['local_path'])

                    

        soundcloud_links = dom.find_all(src=re.compile(".*soundcloud\.com"))
        for link in soundcloud_links:
            parsed = urlparse.urlparse(link.get('src'))
            qs = urlparse.parse_qs(parsed.query)
            url = qs['url']
            if(collection.find_one({'name':link.text,'remote_url':str(url[0]) + '/download?client_id=e050a3144b149a981a0579f1eca4b505'})==None):
                item = Mp3ScrapeItem()
                item['name'] = link.text
                item['remote_url'] = str(url[0]) + '/download?client_id=e050a3144b149a981a0579f1eca4b505'
                item['date'] = datetime.datetime.utcnow()
                item['local_path'] = download(item['remote_url'],settings['MUSIC_DL_FOLDER'])
		
                try:
                    audio = EasyID3(item['local_path'])
                    item['id3_title'] = audio['title'][0]
                    item['id3_artist'] = audio['artist'][0]
                    sz = os.path.getsize(item['local_path'])
                    if(item['local_path']!=None):
                        item['local_url'] = item['local_path'].replace(settings['MUSIC_DL_FOLDER'],settings['LOCAL_URL_BASE'])
                        items.append(item)
		except:
                    if(item['local_path']!=None):
                        os.remove(item['local_path'])

        return items

def url2name(url):
    return urllib2.unquote(basename(urlsplit(url)[2]))

def download(url, path = '', localFileName = None):
    try:
        localName = url2name(url)
	headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1' }
        req = urllib2.Request(url, None, headers)
        r = urllib2.urlopen(req)
	sz = long(r.headers["content-length"])
	if(sz > 15728640 or sz < 1048576 ):
		return None

        if r.info().has_key('Content-Disposition'):
            # If the response has Content-Disposition, we take file name from it
            localName = r.info()['Content-Disposition'].split('filename=')[1].split(';')[0]
            localName = localName.replace('"', '').replace("'", "")
            if localName == '':
                localName = 'mp3-' + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        elif r.url != url:
            # if we were redirected, the real file name we take from the final URL
            localName = url2name(r.url)

        if localFileName:
            # we can force to save the file as specified name
            localName = localFileName

        localName = path + localName
        f = open(localName, 'wb')
        shutil.copyfileobj(r, f)
        f.close()
        return localName
    except:
        return None
