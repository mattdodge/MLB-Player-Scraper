MLB-Player-Scraper  
==================  
    
     
     
It's often useful to scrape and parse player projections from various sources (i.e. ESPN, Yahoo, Rotowire, etc). This tool hopes to facilitate that process.

The tool is built on top of the [Scrapy Framework](http://scrapy.org/) for Python. 



## Requirements
```
pip install scrapy unidecode
```



## How do I use the thing?
```
git clone https://github.com/mattdodge/MLB-Player-Scraper mlbScrape
cd mlbScrape
scrapy crawl <spider-name> -o output.csv -t csv
```



## Current Spiders
 - **yahooBatters**  
   Yahoo 2014 Batter Projections (requires Yahoo league ID, username/pass)
 - **yahooPitchers**  
   Yahoo 2014 Pitcher Projections (requires Yahoo league ID, username/pass)
 - **espnBatters**  
   ESPN 2014 Batter Projections
 - **espnPitchers**  
   ESPN 2014 Pitcher Projections
 



## License
Do whatever the hell you want with it.
