from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http.request.form import FormRequest
import scrapy.log
from mlbScrape.items import Batter, Pitcher
from unidecode import unidecode
import urlparse

LEAGUE_ID = "ENTER LEAGUE ID HERE"
YAHOO_USERNAME = "ENTER YAHOO USERNAME HERE"
YAHOO_PASSWORD = "ENTER YAHOO PASSWORD HERE"


class YahooSpider(Spider):
    db_host = "localhost"
    db_user = "root"
    db_passwd = "root"
    db_name = "sports"
    db_table = "mlb_2013_yahoo_proj"

    url_root = ("http://baseball.fantasysports.yahoo.com/b1/%s"
                "/players?status=A&pos=%s&cut_type=33"
                "&stat1=S_PSR&myteam=0&sort=OR&sdir=1")

    start_urls = []

    column_field_mapping = {}

    def parse(self, response):
        if 'Player List' in response.body:
            return self.after_login(response)
        else:
            return [FormRequest.from_response(
                response,
                formdata={'login': YAHOO_USERNAME,
                          'passwd': YAHOO_PASSWORD},
                callback=self.parse_page,
                dont_filter=True,
                dont_click=True)]

    def parse_page(self, response):
        hxs = Selector(response)

        players = hxs.xpath(
            '//div[contains(@class,"players")]/table/tbody/tr')

        for item in self.getPlayerInfo(self.column_field_mapping, players):
            yield item

        next_page = hxs.xpath("//a[text()='Next 25']/@href").extract()

        if len(next_page) > 0:
            self.log("Requesting %s" % next_page[0], scrapy.log.INFO)
            yield Request(
                urlparse.urljoin(response.url, next_page[0]),
                callback=self.parse_page)

    def getPlayerInfo(self, column_field_mapping, players):
        players_arr = []
        for player_row in players:
            player = self.playerTypeCls()

            playerInfoSel = player_row.xpath(
                ".//td[contains(@class, 'player')]").xpath(
                ".//div[contains(@class, 'ysf-player-name')]")

            player['name'] = unidecode(playerInfoSel.xpath(
                ".//a[contains(@class, 'name')]/text()").extract()[0])

            player['team'] = playerInfoSel.xpath(
                ".//span/text()").re(r'(.*) - ')[0]

            player['pos'] = playerInfoSel.xpath(
                ".//span/text()").re(r'- (.*)')[0]

            player['id'] = playerInfoSel.re(
                r"sports.yahoo.com/mlb/players/([0-9]*)")[0]

            player_stats = player_row.xpath(
                ".//td[contains(@class, 'Ta-end')]").xpath(
                ".//*[not(*)]/text()")

            for stat, (col, regex) in column_field_mapping.iteritems():
                try:
                    player[stat] = player_stats[col].re(regex)[0]
                except KeyError:
                    pass
                except IndexError as e:
                    self.log("ERROR DETECTED for %s" % player['name'],
                             scrapy.log.ERROR)
                    self.log(str(e), scrapy.log.ERROR)

            players_arr.append(player)

        return players_arr


class YahooProjBatters(YahooSpider):

    name = "yahooBatters"
    start_urls = [YahooSpider.url_root % (LEAGUE_ID, "B")]
    playerTypeCls = Batter

    column_field_mapping = {
        "rank": (0, r'(.*)'),
        "ab": (3, r'/(.*)'),
        "h": (3, r'/(.*)'),
        "r": (4, r'(.*)'),
        "hr": (5, r'(.*)'),
        "rbi": (6, r'(.*)'),
        "sb": (7, r'(.*)'),
        "avg": (8, r'(.*)')
    }


class YahooProjPitchers(YahooSpider):

    name = "yahooPitchers"
    start_urls = [YahooSpider.url_root % (LEAGUE_ID, "P")]
    playerTypeCls = Pitcher

    column_field_mapping = {
        "rank": (0, r'(.*)'),
        "ip": (3, r'(.*)'),
        "w": (4, r'(.*)'),
        "sv": (5, r'(.*)'),
        "k": (6, r'(.*)'),
        "era": (7, r'(.*)'),
        "whip": (8, r'(.*)')
    }
