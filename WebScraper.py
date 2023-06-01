from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


"""
Add functionality for multiple websites:
AutoTrader
Motors
CarGuru
CarZoo
Parkers
CarWow
AA
CarSupermarket
BigMotoringWorld
"""

url = "https://www.autotrader.co.uk/car-search?postcode=SW1A 0AA"

#Setup driver
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#issues with Selenium's implicit wait when using Chrome so using Python time.sleep to load in all components instead
driver.get(url)
driver.maximize_window()
time.sleep(3)
pageNum = 1

while driver.find_element(By.XPATH, "//a[@direction='next']").get_attribute("data-testid") != "pagination-disabled":
    carPrice = driver.find_elements(By.XPATH, "//div[@data-testid='advertCard']/div/div/section/section/div/p/span/span")
    carModel = driver.find_elements(By.XPATH, "//a[@data-testid='search-listing-title']/h3")
    carMileage = driver.find_elements(By.XPATH, "//div[@data-testid='advertCard']/div/div/section/section/ul/li[3]")
    zipTest = list(zip(carPrice, carModel, carMileage))
    print(f"------------------ PAGE NUMBER: {pageNum} ---------------")
    for price, model, mileage in zip(carPrice, carModel, carMileage):
        print(f"Found a {model.text} which costs {price.text} with a mileage of {mileage.text[:-6]}")
    driver.find_element(By.XPATH, "//main[@id='content']/article/div[2]/div[2]/a[@direction='next']").click()
    time.sleep(3)
    pageNum += 1
    
driver.close()