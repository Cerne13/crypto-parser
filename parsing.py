import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from threading import Thread
import datetime
import time

from fake_useragent import UserAgent


# os.chmod('/usr/local/bin/chromedriver', 755)
# display = Display(visible=0, size=(1024, 768))
# display.start()

def start_driver():
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--profile-directory=Default")

    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Chrome(options=options)
    return browser


def get_random():
    return random.randint(1, 10)


def get_current_date():
    """
    :return:
    current date, current month, current year
    """
    curr_datetime = datetime.date.today()

    curr_date = curr_datetime.day
    curr_month = curr_datetime.month
    curr_year = curr_datetime.year

    return curr_date, curr_month, curr_year


def create_data_transaction(amount, time_trans, hash_, currency):
    date = get_current_date()
    return {
        "amount": amount,
        "time_trans": time_trans,
        "day_trans": date[0],
        "month_trans": date[1],
        "year_trans": date[2],
        "hash": hash_,
        "birz": currency,
        "changer": get_random(),
    }


def check_all():
    data = {}
    print(data if data else "The data object is empty yet")

    def check_tronscan(driver):
        url = 'https://tronscan.org/#/token20/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
        driver.get(url)

        check_url_success = driver.current_url
        print(f'Url successfully got: {str(check_url_success)}')

        time.sleep(10)

        check_page_elems_available = driver.find_element(By.CSS_SELECTOR, '.csv-wrap').get_attribute('class')
        print(f"{'Page successfully got' if check_page_elems_available else 'Error: parsing blocked'}")

        for i in range(20):
            try:
                amount = driver.find_element(
                    By.XPATH,
                    f'//*[@id="popupContainer"]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{i + 1}]/td[1]/span/span'
                ).text
                amount = "$" + amount

                time_trans = driver.find_element(
                    By.XPATH,
                    f'//*[@id="popupContainer"]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{i + 1}]/td[4]/span/div/div'
                ).text
                time_trans = time_trans.split(" ")[0]
                time_trans = str(datetime.datetime.now() - datetime.timedelta(seconds=int(time_trans)))
                time_trans = time_trans.split(" ")[1].split(".")[0].split(":")[0] + ":" + \
                             time_trans.split(" ")[1].split(".")[0].split(":")[1]

                tron_hash = driver.find_element(
                    By.XPATH,
                    f'//*[@id="popupContainer"]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{i + 1}]/td[7]/div/div/span/a/div/div[1]'
                ).text
                hash2 = driver.find_element(
                    By.XPATH,
                    f'//*[@id="popupContainer"]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{i + 1}]/td[7]/div/div/span/a/div/div[2]'
                ).text
                tron_hash += hash2

                data_transaction = create_data_transaction(amount, time_trans, tron_hash, "TRON")
                data[len(data) + 1] = data_transaction
            except Exception as e:
                print(e)
                continue

    def check_etherscan(driver):
        url = "https://etherscan.io/txs"
        driver.get(url)
        # driver.save_screenshot('ether.png')
        time.sleep(1)
        for i in range(50):
            try:
                eth_hash = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[2]/span/a"
                ).text

                time_trans = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[6]/span"
                ).text
                time_trans = time_trans.split(" ")[0]
                time_trans = str(datetime.datetime.now() - datetime.timedelta(seconds=int(time_trans)))
                time_trans = time_trans.split(" ")[1].split(".")[0].split(":")[0] + ":" + \
                             time_trans.split(" ")[1].split(".")[0].split(":")[1]

                amount = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{i + 1}]/td[10]"
                ).text

                data_transaction = create_data_transaction(amount, time_trans, eth_hash, "ETH")
                data[len(data) + 1] = data_transaction
            except Exception as e:
                print(e)
                continue

    def check_blockchain(driver):
        # We will go to mempool if we access unconfirmed transactions page directly.
        # So we need to navigate from here
        # target_url = "https://www.blockchain.com/btc/unconfirmed-transactions"
        initial_url = 'https://www.blockchain.com/explorer?currency=BTC&stat=transactions'

        driver.get(initial_url)
        time.sleep(1)

        # Won't scrape unless button to target page is in view
        driver.execute_script("window.scrollTo(0, 650)")

        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-18ep7w8-5.sc-18ep7w8-7.rKfqM.fLbSjJ button:last-child')
        button.click()

        time.sleep(2)

        for i in range(50):
            try:
                btc_hash = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[1]/div[2]/a"
                ).text
                time_trans = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[2]/div[2]/span"
                ).text
                amount = driver.find_element(
                    by=By.XPATH,
                    value=f"/html/body/div[1]/div[4]/div[2]/div/div/div[2]/div/div[{i + 2}]/div[4]/div[2]/span"
                ).text

                data_transaction = create_data_transaction(amount, time_trans, btc_hash, "BLOCK")
                data[len(data) + 1] = data_transaction
            except Exception as e:
                print(e)
                continue

    def run_checks(*funcs):
        try:
            for func in funcs:
                driver = start_driver()
                func(driver)
                driver.quit()

        except Exception as e:
            print(e)
            driver.quit()
        finally:
            print(data)

        # TODO: create token save
        # save_new_token(data)

    run_checks(
        check_tronscan,
        check_etherscan,
        check_blockchain
    )


def start_parsing():
    thread = Thread(target=check_all)
    thread.start()


check_all()
