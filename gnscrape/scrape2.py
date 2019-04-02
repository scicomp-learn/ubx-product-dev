from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib3, sys, certifi, re, pandas as pd, os

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
url = 'https://m.gadgetsnow.com/mobile-phones'

# Create new Firefox session
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--test-type')
options.binary_location = "D:/documents/feedloop/learn-py-02/chromedriver.exe"
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(30)

def connectsoup(url):
    # Handling any error in GET request
    response = http.request('GET',url)
    assert(response.status == 200), "Unable to contact successfully : "+ url
    return response

def preparesoup(url):
    # Handling any error in parsing
    try:
        soup = bs(connectsoup(url).data, "html.parser").find(attrs={"class":"gadget_list"})
        # print(soup)
        return soup
    except AssertionError as error:
        print(error)

def detectelement(url,xpath):
    driver.get(url)
    try:
        elem = driver.find_element_by_xpath(xpath)
        elem.click()
    except:
        print("Element is unable to find")
        pass

def scrapeGadName(url,array_sub):
    # Generate several request based on array of subdirectory
    result =  []
    for sub in array_sub:
        page = url +'/'+ sub
        soup = preparesoup(page)
        try:
            gadName = soup.find_all(attrs={"class":"gadName"})
            if len(gadName) < 1: 
                print(page+' has no content')
            else:
                for name in gadName: result.append(name.getText())
            detectelement(page,'//*[@id="c_wdt_gadget_filters_1"]/a')
        except:
            pass
    return result

gadgetName = scrapeGadName(url,['Samsung','Nokia','Apple'])