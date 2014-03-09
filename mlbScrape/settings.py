# Scrapy settings for mlbScrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mlbScrape'

SPIDER_MODULES = ['mlbScrape.spiders']
NEWSPIDER_MODULE = 'mlbScrape.spiders'

# Unfortunately, we have to spoof the user agent...yahoo won't work otherwise
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'
