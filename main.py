# main.py
import os
import re
import pandas as pd
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser

parser = ArgumentParser(description='Get or set "My List" from Netflix account provided to script')
parser.add_argument('--action',help='provide "set" to update Netflix My List from csv or "get" to download data to csv')
parser.add_argument('--account', help='Netflix account to be used with script')

args = parser.parse_args()

ACTION=args.action

print(os.environ)
if "NETFLIX_USER" and "NETFLIX_PASS" not in os.environ:
    print("Please set environment variables for NETFLIX_USER AND NETFLIX_PASS")
    sys.exit(0)

USERNAME = os.environ["NETFLIX_USER"]
PASSWORD = os.environ["NETFLIX_PASS"]
ACCOUNT = args.account
URL = "https://www.netflix.com/browse/my-list"
REGEX = r"https://www.netflix.com/watch/(.*?)\?tctx"


def login(browser):
    print("logging in...")
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


def profileselect(browser, account):
    print("profile select")
    print(browser.current_url)
    try:
        time.sleep(2)
        profile_button = browser.find_element_by_xpath(f"//span[@class='profile-name' and contains(text(),'{account}')]")
        profile_button.click()
    except Exception as e:
        print(e)
        pass


def get_favorites(browser):
    print("get favourites..")
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
    print("setting favourites")
    df = pd.read_csv('output/items.csv')
    for elem in df['infolink']:
        print(f"Adding {elem}")
        try:
            browser.get(elem)
            list_button = browser.find_elements_by_class_name('nf-icon-button')[-1]
            time.sleep(1)
            list_button.click()
        except Exception as e:
            print("Failed", e)


def main():
    # browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome("/path/to/your/chromedriver", options=chrome_options)
    print("Running Netflix Selenium")
    browser.get(URL)
    login(browser)
    profileselect(browser, ACCOUNT)

    if ACTION == "set":
        set_favorites(browser)
    else:
        get_favorites(browser)

    browser.quit()


if __name__ == "__main__":
    main()
