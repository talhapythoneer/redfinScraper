# redfinScraper
This scraper is built to scrape [Redfin](https://www.redfin.com) which is a Captcha protected website. It's built in python using following libraries:
- Scrapy
- Selenium
- twocaptcha
- html2text

Ok so there are two scripts for this.
1) makeURLsList.py
This script is used to generate a list of URLs you want to target. You start the bot, make a search
and input anything when it asks 'Start scraping? (y/n)' it will start scraping the URLs and a Data.csv file will be generated.

2) redfinScraperBot.py
This will scrape the URLs that are in the Data.csv form the previous step.


Note that you would need 2captcha api(which is paid). And put the API key on line no. 12 before starting the final scrape because if the captcha appears the bot would break.

Thanks & Regards
TalhaPythoneer
