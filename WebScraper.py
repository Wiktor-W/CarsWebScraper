from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

import cv2
import imutils
import pytesseract


"""
TODO:

Implement filters in url retrieved i.e. model name, price etc

Maybe implement a GUI for specifying filters

Think of a name..

Calculate a hash value of all the cars' details and use that as an id value for the car.
Any cars with new id values will get added to the overall list when 

Set of hash values assigned to CarAd objects which contain the overall details for the ad
Whenever a new ad is scanned its hash is calculated and added to the set. If it already exists then the set
will ignore it, if it is new then it will be added in.

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

def getAutoTraderCars():
    while True:
        carPrice = driver.find_elements(By.XPATH, "//div[@data-testid='advertCard']/div/div/section/section/div/p/span/span")
        carModel = driver.find_elements(By.XPATH, "//a[@data-testid='search-listing-title']/h3")
        carMileage = driver.find_elements(By.XPATH, "//div[@data-testid='advertCard']/div/div/section/section/ul/li[3]")
        adUrl = driver.find_elements(By.XPATH, "//a[@data-testid='search-listing-title']")
        regYear = driver.find_elements(By.XPATH, "//ul[@data-testid='search-listing-specs']/li[1]")
        zipTest = list(zip(carPrice, carModel, carMileage))
        print(f"------------------ PAGE NUMBER: {pageNum} ---------------")
        for price, model, mileage, url, regYear in zip(carPrice, carModel, carMileage, adUrl, regYear):
            print(f"Found a {model.text} which costs {price.text} with a mileage of {mileage.text[:-6]} registered in {regYear.text[:-9]}")
            carAds.write(f"{model.text}, {price.text.replace(',', '').replace('£','')}, {url.get_attribute('href')}, {mileage.text.replace(',','')[:-6]}, {regYear.text[:-9]}\n")
        driver.find_element(By.XPATH, "//main[@id='content']/article/div[2]/div[2]/a[@direction='next']").click()
        time.sleep(3)
        pageNum += 1
        if len(driver.find_elements(By.XPATH, "//a[@direction='next']")) == 0:
            break

def getNumberPlate():
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
    testImage = cv2.imread('TestPhotos\BlackVauxCorsa.jpg')
    resizedTestImage = imutils.resize(testImage, width=500)
    greyscaleTestImage = cv2.cvtColor(resizedTestImage, cv2.COLOR_BGR2GRAY)
    reducedNoiseGreyscale = cv2.bilateralFilter(greyscaleTestImage, 11, 17, 17)
    imageEdges = cv2.Canny(reducedNoiseGreyscale, 30, 200)
    cv2.imshow("Vauxhall Corsa", imageEdges)
    contours, new = cv2.findContours(imageEdges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = resizedTestImage.copy()
    cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
    cv2.imshow("img1", img1)
    contours = sorted(contours, key= cv2.contourArea, reverse= True)[:4]

    img2 = resizedTestImage.copy()

    cv2.drawContours(img2, contours, -1, (0,255,0), 3)
    cv2.imshow("Top 5 contours", img2)

    screenCount = None
    idx = 0
    
    for contour in contours:
        contour_perimiter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.18 * contour_perimiter, True)

        if len(approx) == 4:
            screenCount = approx

            x, y, w, h = cv2.boundingRect(contour)
            new_img = resizedTestImage [y: y + h, x: x + w]

            cv2.imwrite('./' + str(idx)+ '.png', new_img)
            idx += 1
            break

    cv2.drawContours(resizedTestImage, [screenCount], -1, (0, 255, 0), 3)
    cv2.imshow("License plate detected!", resizedTestImage)
    cv2.waitKey(0)
    text = pytesseract.image_to_string()

def getCarPhotos():
    return ""

def buildUrl(filters):
    url = "https://www.autotrader.co.uk/car-search?"
    for item in filters:
        url += item + "&"
    postcode = "SW1A 0AA"
    url += postcode
    #?make=<makeName>
    #?model=<modelName>
    #&price-from
    #&price-to
    #&year-from
    #&year-to
    #minimum-mileage
    #maximum-mileage
    #transmission
    #fuel-type
    #insuranceGroup=03U...50U
    #exclude-writeoff-categories=on
    return url

url = buildUrl(["postcode=TW119RJ", "price-to=5000", "maximum-mileage=60000", "transmission=Manual", "fuel-type=Petrol", "insuranceGroup=10U", "exclude-writeoff-categories=on", "year-from=2011"])

#Setup driver
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#issues with Selenium's implicit wait when using Chrome so using Python time.sleep to load in all components instead
driver.get(url)
driver.maximize_window()
time.sleep(3)
pageNum = 1
carAds = open("F:\carAds.csv", "w")
carAds.truncate(0)
carAds.write("Car brand + mode, car price, url, car mileage, registration year\n")

#getAutoTraderCars()
getNumberPlate()


    
driver.close()
carAds.close()