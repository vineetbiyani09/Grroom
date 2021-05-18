from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(4)

driver.get('https://www.myntra.com/')
driver.maximize_window()

element = driver.find_element(by = By.CLASS_NAME, value = 'desktop-searchBar').send_keys('t-shirt')
search = driver.find_element(by = By.CLASS_NAME, value = 'desktop-submit').click()

h_refs = []
dict_ = dict()
img_link = []
size_lst = []

def link_scrap() :
    global h_refs
    global img_link
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    division = soup.find('div', {'id' : 'desktopSearchResults'})
    results = division.find('ul', {'class' : 'results-base'})
    divs = soup.findAll('div', {'class' : 'product-imageSliderContainer'})
    tags = results.findAll('a')
    for tag in tags :
        h_refs.append(tag.get('href',None))

def scraper() :
    global h_refs
    global img_link
    global h_ref
    global gender
    global dict_
    global product_name
    global product_brand
    global var
    global price
    global mrp
    global size_lst
    global product_link
    global image_link
    product_link = link + h_refs[i]
    driver.get(product_link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    division = soup.find('div', {'class' : 'pdp-description-container'})
    product_name = division.find('h1', {'class' : 'pdp-name'}).text.split()
    var = product_name[0]
    product_name = ' '.join(product_name[1:])
    if var.lower() == 'men' :
        gender = 'M'
    elif var.lower() == 'women' :
        gender = 'F'
    product_brand = division.find('h1', {'class' : 'pdp-title'}).text
    sizes = division.find('div', {'class' : 'size-buttons-size-buttons'})
    buttons = sizes.findAll('button', {'class' : 'size-buttons-size-button-default'})
    for button in buttons :
        availability = button.get('class')
        if availability[0] == 'size-buttons-size-button-disabled' :
            size_lst.append((button.text,'N/A'))
        else :
            size_lst.append((button.text,'A'))
    price = division.find('span', {'class' : 'pdp-price'}).text.replace('\n', '')
    mrp = division.find('span', {'class' : 'pdp-mrp'}).text.replace('\n', '')
    desc = soup.find('div', {'class' : 'pdp-productDescriptorsContainer'})
    detail = desc.find('p', {'class' : 'pdp-product-description-content'}).text
    dict_['product_detail'] = detail
    table = desc.find('div', {'class' : 'index-tableContainer'})
    tables = table.findAll('div', {'class' : 'index-row'})

    for values in tables :
        key = values.find('div', {'class' : 'index-rowKey'}).text
        dict_[key] = values.find('div', {'class' : 'index-rowValue'}).text

x = 0
while x < 50 :
    link_scrap()
    driver.find_element(by = By.CLASS_NAME, value = 'pagination-next').click()
    x += 1
    time.sleep(2)

link = 'https://www.myntra.com/'
gender = ''

for i in range(0, len(h_refs)) :
    scraper()
    print('PRODUCT_NAME:', product_name)
    print('PRODUCT_BRAND:', product_brand)
    print('SIZE:', size_lst)
    print('SELLING_PRICE:', price)
    print('MRP:', mrp)
    print('FOR_GENDER:', gender)
    print('DESCRIPTION:', dict_)
    print('PRODUCT_LINK:', product_link)
    print('\r')
