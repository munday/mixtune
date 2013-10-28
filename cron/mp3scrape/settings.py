# Scrapy settings for mp3scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'mixtune'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['mp3scrape.spiders']
NEWSPIDER_MODULE = 'mp3scrape.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'mp3scrape.pipelines.MongoDBStorage',
]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "music"
MONGODB_COLLECTION = "mp3s"

LOG_FILE = "scrapy.log"
DEPTH_LIMIT=1
DOWNLOAD_DELAY = 2
MUSIC_DL_FOLDER = "/mnt/music/"
LOCAL_URL_BASE = "/music/"
