from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import traceback
import logging
import time
import requests
import numpy as np
import psycopg2 as ps
import random
from datetime import datetime
import pytz
import os

def get_selenium_driver():
    print("INFO: Get Selenium driver")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def get_environment_variables():
    print("INFO: Get env variables")

    id = '1'
    email = 'energyair1@gmail.com'
    password = 'ub6tfiqasFCHeuWLZX88'

    userdata = [id, email, password]
    print("INFO: " + str(userdata))
    return userdata


def login_game(driver, userdata):
    print("INFO: Login game")
    try:
        id = userdata[0]
        email = userdata[1]
        password = userdata[2]

        driver.get('https://energy.ch/login')
        time.sleep(random.randint(2, 3))

        # login zu onelog
        driver.find_element(By.XPATH, "//div[contains(@class, 'button__StyledButton-b078nx-0 eNhQeC')]").click()

        time.sleep(random.randint(10, 15))

        # accept cookies if needed
        try:
            accept_cookie = driver.find_element(By.XPATH, "//button[contains(@id, 'onetrust-accept-btn-handler')]")
            accept_cookie.click()
        except:
            accept_cookie = False

        # write email
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
        time.sleep(random.randint(2, 3))
        driver.find_element(By.XPATH, "//button[contains(@id, 'first-step-continue-btn')]").click()

        # write password
        time.sleep(random.randint(2, 3))
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
        time.sleep(random.randint(1, 2))

        # click login button
        driver.find_element(By.XPATH, "//button[contains(@id, 'native-login-btn')]").click()

        time.sleep(random.randint(5, 6))

        driver.get('https://energy.ch/api/authorize?redirect_page=%2Fschlaumeier')
    except Exception as e:
        logging.error(traceback.format_exc())
        print("ALERT: Script error trying to log in on bot, retrying")
        driver.quit()
        exit()

def main() -> None:

    userdata = get_environment_variables()
    driver = get_selenium_driver()
    login_game(driver, userdata)


if __name__ == '__main__':
    main()