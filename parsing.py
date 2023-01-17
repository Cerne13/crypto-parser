import random

from selenium import webdriver
from selenium.webdriver.common.by import By

from threading import Thread
import datetime
import time

# from main import *
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
#
# import schedule
# import requests
# from pyvirtualdisplay import Display
# import os
# import subprocess


# os.chmod('/usr/local/bin/chromedriver', 755)
# display = Display(visible=0, size=(1024, 768))
# display.start()

def start_driver():
    options = webdriver.ChromeOptions()

    # options.add_argument('headless')
    # options.add_argument("enable-automation")
    # options.add_argument("--dns-prefetch-disable")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--profile-directory=Default")

    browser = webdriver.Chrome(options=options)
    return browser


# TODO: FOR TEST ONLY! Ask what the func should return
def get_random():
    return random.randint(1, 10)


def check_all():
    data = {}

    # TODO: ask why we print an empty obj
    print(data)

    def check_tronscan(driver):
        url = 'https://tronscan.org/#/token20/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
        driver.get(url)
        print(driver)

        check_url_success = driver.current_url
        print(f'Url successfully got: {str(check_url_success)}')

        time.sleep(5)

        check_page_available = driver.find_element(By.CSS_SELECTOR, '.logo').get_attribute('class')
        print(f"{'Page successfully got' if check_page_available else 'Error: parsing blocked'}")

        for i in range(20):
            try:
                amount_temp = driver.find_element(By.CLASS_NAME, 'ant-table-tbody')
                print(amount_temp)

                amount = driver.find_element(by=By.XPATH,
                                             value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[1]/span").text
                time_trans = driver.find_element(by=By.XPATH,
                                                 value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[4]/span/div/div").text
                '''try:
                    from_trans = driver.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[5]/div/span/div/div/span/div/a/div").text
                except:
                    from_trans = driver.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[5]/div/span/span/a/div").text
                to_trans = driver.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[6]/div/span/div/div/span/div/a/div").text
                '''
                hash = driver.find_element(by=By.XPATH,
                                           value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[7]/div/div/span/a/div/div[1]").text
                hash2 = driver.find_element(by=By.XPATH,
                                            value=f"/html/body/div[1]/div[2]/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[7]/div/div/span/a/div/div[2]").text
                hash += hash2
                amount = "$" + amount
                time_trans = time_trans.split(" ")[0]
                time_trans = str(datetime.datetime.now() - datetime.timedelta(seconds=int(time_trans)))
                time_trans = time_trans.split(" ")[1].split(".")[0].split(":")[0] + ":" + \
                             time_trans.split(" ")[1].split(".")[0].split(":")[1]
                changer = get_random()

                data_transaction = {
                    "amount": amount,
                    "time_trans": time_trans,
                    "hash": hash,
                    "birz": "TRON",
                    "changer": changer
                }

                data[len(data) + 1] = data_transaction
                print(data_transaction)
            except Exception as a:
                print(a)
                continue

    def check_blockchain(driver):
        url = "https://www.blockchain.com/btc/unconfirmed-transactions"
        driver.get(url)
        time.sleep(1)
        for i in range(50):
            try:
                hash = driver.find_element(by=By.XPATH,
                                           value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[1]/div[2]/a").text
                time_trans = driver.find_element(by=By.XPATH,
                                                 value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[2]/div[2]/span").text
                amount = driver.find_element(by=By.XPATH,
                                             value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[4]/div[2]/span").text
                changer = get_random()

                data_transaction = {
                    "amount": amount,
                    "time_trans": time_trans,
                    "hash": hash,
                    "birz": "BLOCK",
                    "changer": changer
                }
                data[len(data) + 1] = data_transaction
            except:
                continue

    def check_etherscan(driver):
        url = "https://etherscan.io/txs"
        driver.get(url)
        driver.save_screenshot('ether.png')
        time.sleep(1)
        for i in range(50):
            try:
                hash = driver.find_element(by=By.XPATH,
                                           value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[2]/span/a").text
                time_trans = driver.find_element(by=By.XPATH,
                                                 value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[6]/span").text
                amount = driver.find_element(by=By.XPATH,
                                             value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[10]").text
                time_trans = time_trans.split(" ")[0]
                time_trans = str(datetime.datetime.now() - datetime.timedelta(seconds=int(time_trans)))
                time_trans = time_trans.split(" ")[1].split(".")[0].split(":")[0] + ":" + \
                             time_trans.split(" ")[1].split(".")[0].split(":")[1]
                changer = get_random()

                data_transaction = {
                    "amount": amount,
                    "time_trans": time_trans,
                    "hash": hash,
                    "birz": "ETH",
                    "changer": changer
                }
                data[len(data) + 1] = data_transaction
            except Exception as a:
                print(a)

    driver = start_driver()

    # TODO: why do we start ether twice?
    # check_etherscan(driver)

    try:
        check_tronscan(driver)
        driver.quit()
        time.sleep(30)

        # driver = start_driver()
        # check_blockchain(driver)
        # driver.quit()
        # time.sleep(20)
        #
        # driver = start_driver()
        # check_etherscan(driver)
    except:
        driver.quit()
    finally:
        driver.quit()
        print(data)

        # TODO: create token save
        # save_new_token(data)


def start_parsing():
    thread = Thread(target=check_all)
    thread.start()
check_all()
