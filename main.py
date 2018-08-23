# main.py
import os
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

USERNAME = os.environ.get("NETFLIX_USER")
PASSWORD = os.environ.get("NETFLIX_PASS")
URL = "https://www.netflix.com/browse/my-list"
REGEX = r"https://www.netflix.com/watch/(.*?)\?tctx"

def login(browser):
    print(browser.current_url)
    try:
        username_field = browser.find_element_by_id('id_userLoginId')
        username_field.send_keys(USERNAME)
        password_field = browser.find_element_by_id("id_password")
        password_field.send_keys(PASSWORD)
    except:
        username_field = browser.find_element_by_id('email')
        username_field.send_keys(USERNAME)
        password_field = browser.find_element_by_id("password")
        password_field.send_keys(PASSWORD)
    login_button = browser.find_element_by_class_name('login-button')
    login_button.click()

def profileselect(browser):
    print(browser.current_url)
    try:
        profile_button = browser.find_element_by_class_name('profile-icon')
        profile_button.click()
    except:
        pass

def get_favorites(browser):
    items = []
    print(browser.find_elements_by_class_name('ptrack-content'))
    for elem in browser.find_elements_by_class_name('ptrack-content'):
        item = {
            'title': elem.find_element_by_class_name('slider-refocus').get_attribute('aria-label'),
            'viewlink': elem.find_element_by_class_name('slider-refocus').get_attribute('href')
        }
        item['id'] = re.search(REGEX, item['viewlink']).group(1)
        item['infolink'] = f"https://www.netflix.com/title/{item['id']}"
        items.append(item)
    pd.DataFrame(items).to_csv('output/items.csv', index=False)

def set_favorites(browser):
    df = pd.read_csv('output/items.csv')
    for elem in df['infolink']:
        print(f"Adding {elem}")
        try:
            browser.get(elem)
            list_button = browser.find_elements_by_class_name('nf-icon-button')[-1]
            time.sleep(1)
            list_button.click()
        except:
            print("FAILED")

def main():
    # browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
    browser = webdriver.Chrome()
    print("Running Netflix Selenium")
    browser.get(URL)
    login(browser)
    profileselect(browser)
    
    set_favorites(browser)
    
    # get_favorites(browser)
    
    browser.quit()
    
if __name__ == "__main__":
    main()
