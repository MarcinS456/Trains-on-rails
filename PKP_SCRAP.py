import os
import time
from datetime import date, timedelta

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def wait_for_the_page_to_load():
    time.sleep(2)


def sleep_to_not_stress_server():
    time.sleep(1)

options.headless = False

driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)
actions = ActionChains(driver)

today = date.today().strftime("%d.%m.%y")
yesterday = date.today() + timedelta(days=-1)
yesterday = yesterday.strftime("%d.%m.%y")

Trains = pd.DataFrame()
path = os.getcwd()
cities = pd.read_csv(path + '/cities.csv')
cities_list = cities['City'].to_list()



def count_trains_between_two_cities():
    is_date_today = False
    counter = 0
    while not is_date_today:
        counter = 0
        if check_exists_by_xpath('//tr'):
            trains = driver.find_elements(By.XPATH, '//tr')
            for train in trains:
                txt = train.text
                is_date_today = today in txt
                train_started_yesterday = yesterday in txt
                if not train_started_yesterday and is_date_today:
                    counter = counter + 1
            sleep_to_not_stress_server()
            if check_exists_by_xpath('//a[@class="tp later-connections"]'):
                next_trains = driver.find_element(By.XPATH, '//a[@class="tp later-connections"]')
                next_trains.click()
        else:
            is_date_today = False

    return counter


def load_timetable_page():
    timetable_search_url = 'https://rozklad-pkp.pl/'
    driver.get(timetable_search_url)
    wait_for_the_page_to_load()

    # close popup
    while check_exists_by_xpath('//button[@class=" css-1hy2vtq"]'):
        cookie_button = driver.find_element(By.XPATH, '//button[@class=" css-1hy2vtq"]')
        cookie_button.click()
    wait_for_the_page_to_load()

    # close privacy settings popup
    if check_exists_by_xpath('//div[@class="qc-cmp2-buttons-desktop"]'):
        cookie_button = driver.find_element(By.XPATH, '//div[@class="qc-cmp2-buttons-desktop"]')
        cookie_button.click()
    wait_for_the_page_to_load()


df_idx = 1

for origination in cities_list:
    other_cities = [c for c in cities_list if c != origination]
    print(origination, "->", other_cities)
    for destination in other_cities:
        load_timetable_page()

        print("count", origination, destination, "route")
        orig = driver.find_element(By.XPATH, '//input[@id="from-station"]')
        sleep_to_not_stress_server()

        dest = driver.find_element(By.XPATH, '//input[@id="to-station"]')
        orig.send_keys(origination)
        sleep_to_not_stress_server()
        dest.send_keys(destination)
        sleep_to_not_stress_server()

        depart = driver.find_element(By.XPATH, '//input[@id="hour"]')
        depart.send_keys("00:00")
        sleep_to_not_stress_server()

        direct_train = driver.find_element(By.XPATH, '//div[@class="checkbox3"]')
        ActionChains(driver).move_to_element(direct_train).perform()
        sleep_to_not_stress_server()

        direct_train.click()
        sleep_to_not_stress_server()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        submit = driver.find_element(By.XPATH, '//img[@class="search-icon"]')
        ActionChains(driver).move_to_element(submit).perform()
        sleep_to_not_stress_server()
        submit.click()
        wait_for_the_page_to_load()

        num_connections = count_trains_between_two_cities()
        if num_connections > 0:
            Trains.loc[df_idx, 'Origination'] = origination
            Trains.loc[df_idx, 'Destination'] = destination
            Trains.loc[df_idx, 'daily_trains'] = num_connections
        df_idx = df_idx + 1


driver.quit()
dest_path = os.path.join(path, 'graf.csv')
Trains.to_csv(dest_path, index=False)
