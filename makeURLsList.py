from ast import While
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy import Selector
import csv
from datetime import datetime




def botInitialization():
    # Initialize the Bot
    chromeOptions = Options()
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    # chromeOptions.add_argument("--headless")
    chromePath = which("D:\Projects\chromedriver_97\chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chromePath, options=chromeOptions)
    driver.maximize_window()
    return driver

driver = botInitialization()

driver.get("https://www.redfin.ca/on/ottawa/filter/property-type=condo,include=sold-6mo")
sleep(2)


while True:

    with open('Data.csv', 'a', newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = ['URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        start = input("Start scraping? (y/n)")

        while True:
            response = Selector(text=driver.page_source)

            listings = response.css("div.flex.flex-wrap > div.HomeCardContainer")
            
            for listing in listings:
                listingURL = listing.css("div.bottomV2 > a::attr(href)").extract_first()
                if listingURL:
                    writer.writerow({'URL': listingURL})
                    print(listingURL)

            try:
                nextPage = driver.find_element_by_css_selector("button[data-rf-test-id='react-data-paginate-next']")
            except:
                break
            if "disabled" in nextPage.get_attribute("class"):
                break
            else:
                driver.execute_script("arguments[0].click();", nextPage)
                sleep(3)
    
    s = input("scrape again? (y/n)")
    if s == "n":
        break