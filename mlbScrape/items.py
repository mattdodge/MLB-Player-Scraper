# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Player(Item):
    """Overall player attributes (not specific to position)"""
    name = Field()
    pos = Field()
    team = Field()
    id = Field()
    rank = Field()

    # Some stats that everyone has
    games = Field()


class Pitcher(Player):
    starts = Field()
    ip = Field()
    bb = Field()
    k = Field()
    w = Field()
    sv = Field()
    hd = Field()
    era = Field()
    whip = Field()
    k_per_9 = Field()


class Batter(Player):
    ab = Field()
    r = Field()
    hr = Field()
    rbi = Field()
    bb = Field()
    k = Field()
    sb = Field()
    avg = Field()
    obp = Field()
    slg = Field()
