import pandas as pd
from datetime import date, timedelta
import selenium
import networkx as nx
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver
import time
#from PIL import Image
import io
import requests
#from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

options = Options()

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)
actions = ActionChains(driver)

today=date.today().strftime("%d.%m.%y")
yesterday=date.today()+timedelta(days=-1)
yesterday=yesterday.strftime("%d.%m.%y")

Trains=pd.DataFrame()
counter=0
print('Start')
cities=pd.read_csv('I:/cities2.csv')
cities_list = cities['City'].to_list()
i=1
for origination in cities_list:
    for destination in cities_list:
        if origination!=destination:
            check_date = 0
            search_url = 'https://rozklad-pkp.pl/'
            driver.get(search_url)
            time.sleep(2)
            while check_exists_by_xpath('//button[@class=" css-1hy2vtq"]') == True:
                cookie_button = driver.find_element(By.XPATH, '//button[@class=" css-1hy2vtq"]')
                cookie_button.click()
            time.sleep(2)
            print("liczę "+origination+" "+destination)
            orig = driver.find_element(By.XPATH, '//input[@id="from-station"]')
            time.sleep(1)
            dest= driver.find_element(By.XPATH, '//input[@id="to-station"]')
            orig.send_keys(origination+"-")
            time.sleep(1)
            dest.send_keys(destination+"-")
            time.sleep(2)
            depart = driver.find_element(By.XPATH, '//input[@id="hour"]')
            depart.send_keys("00:00")
            time.sleep(2)
            direct_train = driver.find_element(By.XPATH, '//div[@class="checkbox3"]')
            direct_train.click()
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            submit = driver.find_element(By.XPATH, '//img[@class="search-icon"]')
            ActionChains(driver).move_to_element(submit).perform()
            time.sleep(1)
            submit.click()
            time.sleep(2)

            while check_date!=-1:
                counter = 0
                if check_exists_by_xpath('//tr'):
                    trains = driver.find_elements(By.XPATH, '//tr')
                    for train in trains:
                        txt=train.text
                        check_date=txt.find(today)
                        check_yesterday=txt.find(yesterday)
                        if (check_yesterday==-1 and check_date!=-1):
                            counter=counter+1
                            #print(counter)
                    time.sleep(1)
                    if check_exists_by_xpath('//a[@class="tp later-connections"]'):
                        next_trains = driver.find_element(By.XPATH, '//a[@class="tp later-connections"]')
                        next_trains.click()
                else: check_date=-1
            if counter>0:
                Trains.loc[i,'Origination']=origination
                Trains.loc[i,'Destination']=destination
                Trains.loc[i,'daily_trains']=counter
            i=i+1

print(Trains)
Trains.to_csv('I:/testowy_graf.csv', index=False)


