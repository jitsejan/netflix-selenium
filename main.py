# main.py
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

USERNAME = os.environ.get("NETFLIX_USER")
PASSWORD = os.environ.get("NETFLIX_PASS")
URL = "https://www.netflix.com/browse/my-list"
REGEX = r"https://www.netflix.com/watch/(.*?)\?tctx"

def main():
    browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
    print("Running Netflix Selenium")
    browser.get(URL)
    print(browser.current_url)
    try:
        print("Try")
        username_field = browser.find_element_by_id('id_userLoginId')
        print(username_field)
        username_field.send_keys(USERNAME)
        password_field = browser.find_element_by_id("id_password")
        print(password_field)
        password_field.send_keys(PASSWORD)
    except:
        print("Except")
        username_field = browser.find_element_by_id('email')
        print(username_field)
        username_field.send_keys(USERNAME)
        password_field = browser.find_element_by_id("password")
        print(password_field)
        password_field.send_keys(PASSWORD)
    login_button = browser.find_element_by_class_name('login-button')
    login_button.click()
    print(browser.current_url)
    try:
        profile_button = browser.find_element_by_class_name('profile-icon')
        profile_button.click()
    except:
        pass
    items = []
    print(browser.find_elements_by_class_name('ptrack-content'))
    for elem in browser.find_elements_by_class_name('ptrack-content'):
        item = {
            'title': elem.find_element_by_class_name('slider-refocus').get_attribute('aria-label'),
            'viewlink': elem.find_element_by_class_name('slider-refocus').get_attribute('href')
        }
        item['id'] = re.search(REGEX, item['viewlink']).group(1)
        item['infolink'] = f"https://www.netflix.com/title/{item['id']}"
        print(item)
        items.append(item)
    pd.DataFrame(items).to_csv('/app/output/items.csv', index=False)
    browser.quit()
    
if __name__ == "__main__":
    main()
