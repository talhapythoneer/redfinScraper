from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy import Selector
import csv
from datetime import datetime
import html2text
from twocaptcha import TwoCaptcha


apiKey = ""

solver = TwoCaptcha(apiKey)

h = html2text.HTML2Text()
h.ignore_links = True

def solveCaptcha(driver):
    siteKey = driver.find_element_by_css_selector("div.g-recaptcha").get_attribute("data-sitekey")

    result = solver.recaptcha(
        sitekey=siteKey,
        url=driver.current_url,
    )

    code = result["code"]

    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = '%s';" % code)

    submit = driver.find_element_by_css_selector("input[type='submit']")

    driver.execute_script("arguments[0].click();", submit)

    return driver



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


# read csv file
def readCsv(fileName):
    with open(fileName, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


URLs = readCsv("Data.csv")[1:]
listings = [url[0] for url in URLs]


driver = botInitialization()

driver.get("https://www.redfin.ca/login-v2")

emailInput = driver.find_element_by_css_selector("input[name='emailInput']")
emailInput.send_keys("talhairfan778@gmail.com")

passwordInput = driver.find_element_by_css_selector("input[name='passwordInput']")
passwordInput.send_keys("Dxdiag778")

submit = driver.find_element_by_css_selector("button[type='submit']")
submit.click()

sleep(5)

# listings = ['/on/ottawa/101-Richmond-Rd-K1Z-0A6/unit-221/home/148755533']

with open('Data_redfin.csv', 'a', newline='', encoding="utf-8-sig") as csvfile:
    fieldnames = [
        "Address", "Year Built", "Community", "Management Company", "Fee includes", "Amenities", "Condo Fee",
        "Beds", "Baths", "SqFt", "Price", "Link",
        'AgentName', 'AgentPhone', "AgentEmail", "Status" , "EstPrice", "Time on Redfin", "MLS#", "PropertyType","Descriptiopn",
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    for i, listingURL in enumerate(listings):
        print(str(i + 1) + " --> ", end="")
        print("https://www.redfin.com" + listingURL)
        while True:
            try:
                driver.get("https://www.redfin.com" + listingURL)
                # sleep(1)
                break
            except:
                continue

        response = Selector(text=driver.page_source)

        testCaptcha = response.css("div#txt > p::text").extract_first()
        if testCaptcha:
            if "Oops" in testCaptcha:
                solveCaptcha(driver)
                print("Captcha Solved...")

                driver.get("https://www.redfin.com" + listingURL)
                response = Selector(text=driver.page_source)

        else:
            pass
        
        try:
            address = response.css("h1.homeAddress").extract()[0]
        except:
            driver.get("https://www.redfin.com" + listingURL)
            sleep(2)
            response = Selector(text=driver.page_source)

        address = h.handle(address)
        address = address.replace("*", "")
        address = address.replace("\n", "").replace("#", "").strip()

        price = response.css("div.beds-section:nth-of-type(1) > div::text").extract_first()
        beds = response.css("div.beds-section:nth-of-type(2) > div::text").extract_first()
        baths = response.css("div.baths-section > div::text").extract_first()
        area = response.css("div.sqft-section > span::text").extract_first()

        # print([price, beds, baths, area])

        estPrice = response.css("div[data-rf-test-id='key-detail-estimate'] > span::text").extract_first()

        description = response.css("p.text-base > span::text").extract_first()

        agentName = ""
        agentPhone = ""
        agentEmail = ""

        agentData = response.css("div.blockedContactBox")
        if agentData:
            agentName = agentData[0].css("div.font-weight-bold::text").extract_first()
            contactInfo = agentData[0].css("div.padding-top-medium > div > a::attr(href)").extract()
            for c in contactInfo:
                if "tel" in c:
                    agentPhone = c.split(":")[-1]
                if "mailto" in c:
                    agentEmail = c.split(":")[-1]

        if not agentName:
            agentName = response.css("div.agent-basic-details > span > span::text").extract_first()
        

        details = response.css("div.keyDetail.font-weight-roman.font-size-base").extract()
        detailsEx = []
        for d in details:
            detailsEx.append(h.handle(d))
        
        mls = ""
        timeOnR = ""
        status = ""
        propertyType = ""
        yearBuilt = ""
        community = ""
        for d in detailsEx:
            if "Property Type" in d:
                propertyType = d.replace("Property Type", "").replace("*", "").replace(":", "").strip()
            if "MLS" in d:
                mls = d.split("#")[-1].replace("*", "").strip()
            if "Time on Redfin" in d:
                timeOnR = d.replace("Time on Redfin", "").replace("*", "").strip()
            if "Status" in d:
                status = d.replace("Status", "").replace("*", "").strip()
            if "Year Built" in d:
                yearBuilt = d.replace("Year Built", "").replace("*", "").strip()
            if "Community" in d:
                community = d.replace("Community", "").replace("*", "").strip()
        


        details = response.css("li.entryItem > span").extract()
        managementCompany = ""
        feeIncludes = ""
        amenities = ""
        condoFee = ""
        for detail in details:
            detailText = h.handle(detail).replace("*", "").strip()
            if "Management Company" in detailText:
                managementCompany = detailText.split(":")[-1].strip()
            if "Fee Includes" in detailText:
                feeIncludes = detailText.split(":")[-1].strip().replace("\n", ", ").strip()
            if "Amenities" in detailText:
                amenities = detailText.split(":")[-1].strip().replace("\n", ", ").strip()
            if "Condo Fee:" in detailText:
                condoFee = detailText.split(":")[-1].strip()

        
        writer.writerow({
            "Year Built": yearBuilt, 
            "Community": community, 
            "Management Company":managementCompany, 
            "Fee includes":feeIncludes, 
            "Amenities":amenities, 
            "Condo Fee":condoFee,
            'AgentName': agentName,
            'AgentPhone': agentPhone,
            "AgentEmail": agentEmail,
            "Status": status,
            "PropertyType": propertyType,
            "Address": address,
            "Beds": beds,
            "Baths": baths,
            "SqFt": area,
            "Price": price,
            "EstPrice": estPrice,
            "Time on Redfin": timeOnR,
            "MLS#": mls,
            "Link": "https://www.redfin.com" + listingURL,
            "Descriptiopn": description,
        })