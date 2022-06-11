#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 11:25:42 2022

@author: cassandrapate
"""
import numpy as np
import pandas as pd
import time
from datetime import datetime
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ### INFO ###
# Chrome: Version 102.0.5005.61
# ChromeDriver 102.0.5005.61

# ### USER INFO ###
# Items Still needed:
user_zipcode = 19147
item_list = [['sektion base cabinet frame white', '302 653 86', '30x24x30'],
             ['sektion wall top cabinet frame white', '202 655 13', '36x24x20'],
             ['sektion base cabinet frame white', '002 65 458', '18x14 3/4x40'],
             ['sektion base cabinet frame white', '502 655 02', '47x26x30'],
             ['bodarp cover panel gray green', '604 355 99', '36x96']]

# ### SCRIPTS ###
# Change Zipcode
# button class='pip-zip-in__button' | class='pip-link-button'
def changezip(current_zipcode, user_zipcode):
    # Click thru to Enter Zipcode field
    current_zipcode.click()
    time.sleep(1)
    driver.find_element(By.XPATH, ".//*[@class='pip-link-button ']").click()
    time.sleep(1)
    # Enter new zipcode
    zipcode_field = driver.find_element(By.XPATH, ".//*[@id='zip']").send_keys(user_zipcode)
    # Submit New Zipcode
    driver.find_element(By.XPATH, ".//*[@class='geo-ingka-btn geo-ingka-btn--primary update-button']").click()
    time.sleep(2)
    # Close popup
    closebutton_class ='pip-btn pip-btn--small pip-btn--icon-primary-inverse pip-modal-header__close'
    driver.find_element(By.XPATH, ".//*[@class='{}']".format(closebutton_class)).click()
    time.sleep(2)
    
def send_message(text):
    # Using ikea_kitchen_bot
    ## Enter you info here ##
    botfather_token = 'NuMb3R5:LETTERS'
    user_id = '@yourtelegramhandle' #Can also use UserID from @userinfobot
    ## --- ##
    
    url = f'https://api.telegram.org/bot{botfather_token}/sendMessage'
    params = {
       "chat_id": user_id,
       "text": text}
    resp = requests.get(url, params=params)
    # Throw an exception if Telegram API fails
    resp.raise_for_status()
    

# ### WEBSITE ###
# Set up Chromium:
s=Service('/Users/AmbitiousDonut/chromedriver')
options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless")
driver = webdriver.Chrome(service=s, options=options)

# ### CHECK AVAILABILITY ###
# unavailable_class = 'pip-status pip-status--red pip-status--small'
base_url = 'https://www.ikea.com/us/en/p/'
for item in item_list:
    # Load website
    ikea_url = base_url + item[0].replace(" ", "-") + '-' + item[1].replace(" ", "")
    driver.get(ikea_url)
    time.sleep(3)
    
    # Check zipcode for delivery
    current_zipcode = driver.find_element(By.XPATH, ".//*[@class='pip-zip-in__button-link']")
    if user_zipcode != int(current_zipcode.text):
        changezip(current_zipcode, user_zipcode)
    
    # Check if avilable for delivery
    available_class = 'pip-status pip-status--green pip-status--small'
    if driver.find_elements(By.XPATH, ".//*[@class='{}']".format(available_class)):
        print('{} - {} ({}) is AVAILABLE for Delivery to {} as of {}'.format(item[0],
                                                                             item[2],
                                                                             item[1].replace(' ', '.'),
                                                                             user_zipcode,
                                                                             datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        send_message('{} - {} ({}) is AVAILABLE for Delivery to {} as of {}'.format(item[0],
                                                                        item[2],
                                                                        item[1].replace(' ', '.'),
                                                                        user_zipcode,
                                                                        datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        send_message('Visit {} for more information'.format(base_url + item[0].replace(" ", "-") + '-' + item[1].replace(" ", "")))
        
    #else:
    #    print('{} - {} ({}) is UNAVILABLE for Delivery to {}'.format(item[0], item[2], 
    #                                                                item[1].replace(' ', '.'),
    #                                                                user_zipcode))
    
    time.sleep(5)
# terminates driver session and closes all windows
driver.quit()
