from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import urllib3, sys, certifi, re, pandas as pd, os, time

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
url = 'https://www.gadgetsnow.com/mobile-phones'

# Create new Firefox session
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=chrome_options, executable_path='D:/documents/chromedriver.exe')
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

def checkelement(xpath):
    print('Checking element : '+xpath)
    target = driver.find_elements_by_xpath(xpath)
    if len(target) >= 1:
        isExist = True
        print('Found')
    else:
        isExist = False
        print('Not Found')
    return isExist, target

def checkseemore():
    loadingExist, loading = checkelement('//*[@id="gadget_loading"]')
    if loadingExist :
        print('Still loading... Wait for 3 sec')
        time.sleep(3)
        checkseemore()
    loadbtnExist, loadbtn = checkelement('//*[@id="load_more"]')
    if loadbtnExist :
        print('Clicking')
        # loadbtn[0].click()
        driver.execute_script("arguments[0].click();", loadbtn[0])
        print('Element clicked')
        checkseemore()
    else :
        print('Click stopped')

def openselenium(url):
    driver.get(url)
    print('Page opened...')
    checkseemore()

def scrapeGadName(url,array_sub):
    # Generate several request based on array of subdirectory
    result =  []
    resultName = pd.Series()
    for sub in array_sub:
        page = url +'/'+ sub
        try:
            openselenium(page)
            name = driver.find_elements_by_class_name('gadName')
            for i in name:
                result.append(i.text)
            if resultName.size < 1:
                resultName = pd.Series(result)
        except Exception as e:
            print(e)
        driver.quit()
    return resultName

def gn_to_csv(filename,data):
    # filename = os.path.join('data/gadgetsnow/raw', 'gn_raw_phone.csv')
    print(f'- Saving data to {filename}..')
    try:
        data.transpose().to_csv(
            filename, index=False
        )
    except Exception as error:
        print(f'Error while saving: {error}')
    else:
        print(f'- [DONE] Saved in {filename}')

gadgetName = scrapeGadName(url,['filters/brand=Inco%7CIvvo%7CK-Tel'])
gn_to_csv('gn_raw_phone.csv',gadgetName)
print(gadgetName)