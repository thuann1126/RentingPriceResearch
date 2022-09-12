import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests

FORM_URl = 'https://forms.gle/x9uv8Np2nN3Lz8d68'
RENTING_SITE_URL = 'https://www.zillow.com/toronto-on/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A43.91797954739979%2C%22east%22%3A-79.28040995083141%2C%22south%22%3A43.52396044712701%2C%22west%22%3A-79.70338358364391%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A792680%2C%22regionType%22%3A6%7D%5D%7D'
LINK_MISSING_PATTERN = 'https://www.zillow.com/homedetails/'
CHROME_DRIVER_PATH = 'C:\Development\chromedriver.exe'
all_links =[]
all_prices =[]
all_addresses= []
property_dictionary = []

# Request header
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9'
}

# Get the Renting website's information
property_information = requests.get(RENTING_SITE_URL, headers=header)

soup = BeautifulSoup(property_information.text, 'html.parser')

#Get all the address
all_addresses_elements = soup.select('.property-card-link address')
all_addresses = [address.get_text().split(" | ")[-1] for address in all_addresses_elements]
print(all_addresses)

#Get all the prices
all_prices_elements = soup.select('.property-card-data div span')
all_prices = [price.get_text().split("+")[0]  if '$' in price.text else '' for price in all_prices_elements]
print(all_prices)

#Get all the links
all_links_elements = soup.select('.property-card-data a')
for link in all_links_elements:
    href = str(link['href'])
    if LINK_MISSING_PATTERN not in href:
        href = LINK_MISSING_PATTERN + href[3:]
    all_links.append(href)
print(all_links)

#Connect with google sheet
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

#Fill data to the form
for i in range(len(all_addresses)):
    driver.get(FORM_URl)
    time.sleep(1)
    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_input.send_keys(all_addresses[i])
    time.sleep(1)
    price_input.send_keys(all_prices[i])
    time.sleep(1)
    link_input.send_keys(all_links[i])
    time.sleep(1)
    submit_button.click()
    time.sleep(1)
driver.quit()



