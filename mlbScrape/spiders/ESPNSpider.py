from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import scrapy.log
from mlbScrape.items import Batter, Pitcher
from unidecode import unidecode
import urlparse

MAX_PAGES = 50


class ESPNSpider(Spider):
    url_root = ("http://games.espn.go.com/flb/tools/projections?"
                "display=alt&slotCategoryGroup=%s")

    start_urls = []

    column_field_mapping = {}

    pages_parsed = 1

    def parse(self, response):
        hxs = Selector(response)

        players = hxs.xpath(
            '//div[contains(@class,"games-fullcol")]/table')

        for item in self.getPlayerInfo(self.column_field_mapping, players):
            yield item

        next_page = hxs.xpath("//a[text()='NEXT']/@href").extract()

        if len(next_page) > 0 and self.pages_parsed < MAX_PAGES:
            self.log("Requesting %s" % next_page[0], scrapy.log.INFO)
            self.pages_parsed += 1
            yield Request(
                urlparse.urljoin(response.url, next_page[0]),
                callback=self.parse)

    def getPlayerInfo(self, column_field_mapping, players):
        players_arr = []
        for player_row in players:
            player = self.playerTypeCls()

            playerInfoSel = player_row.xpath(
                ".//span[contains(@class, 'subheadPlayerNameLink')]/nobr")

            player['name'] = unidecode(playerInfoSel.xpath(
                ".//a/text()").extract()[0])

            player['rank'] = player_row.re(r"/players/full/([0-9]*).png")[0]

            player['team'] = playerInfoSel.xpath("./text()").re(
                r', ([^ ]*) ')[0]

            player['pos'] = playerInfoSel.xpath("./text()").re(
                r', [^ ]* (.*)')[0]

            player['id'] = playerInfoSel.re(r"playerid=\"([0-9]*)\"")[0]

            player_stats = player_row.xpath(
                ".//tr[contains(@class, 'tableBody')][%s]" % (
                    self.table_row, )).xpath(
                ".//td[contains(@class, 'playertableStat')]/text()")

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


class ESPNBatters(ESPNSpider):

    name = "espnBatters2014"
    start_urls = [ESPNSpider.url_root % ("1",)]
    playerTypeCls = Batter
    table_row = 1

    column_field_mapping = {
        "ab": (0, r'(.*)'),
        "r": (1, r'(.*)'),
        "hr": (2, r'(.*)'),
        "rbi": (3, r'(.*)'),
        "bb": (4, r'(.*)'),
        "k": (5, r'(.*)'),
        "sb": (6, r'(.*)'),
        "avg": (7, r'(.*)'),
        "obp": (8, r'(.*)'),
        "slg": (9, r'(.*)')
    }


class ESPNPitchers(ESPNSpider):

    name = "espnPitchers2014"
    start_urls = [ESPNSpider.url_root % ("2",)]
    playerTypeCls = Pitcher
    table_row = 1

    column_field_mapping = {
        "games": (0, r'(.*)'),
        "starts": (1, r'(.*)'),
        "ip": (2, r'(.*)'),
        "bb": (3, r'(.*)'),
        "k": (4, r'(.*)'),
        "w": (5, r'(.*)'),
        "sv": (6, r'(.*)'),
        "hd": (7, r'(.*)'),
        "era": (8, r'(.*)'),
        "whip": (9, r'(.*)'),
        "k_per_9": (10, r'(.*)')
    }


class ESPNProjBatters(ESPNBatters):

    name = "espnBatters"
    table_row = 2


class ESPNProjPitchers(ESPNPitchers):

    name = "espnPitchers"
    table_row = 2
