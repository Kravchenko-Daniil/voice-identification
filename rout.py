import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

from parameters import login, password


class RoutToSite:
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--allow-profiles-outside-user-dir")
        options.add_argument("--enable-profile-shortcut-manager")
        options.add_argument(r"user-data-dir=Cookies")
        options.add_argument("--profile-directory=Profile 1")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(15)
        self.driver.implicitly_wait(15)

        # self.url = "https://www.binance.com/ru/my/wallet/account/overview"
        self.url = "https://www.okx.com/account/users"

    def auth(self):
        try:
            self.driver.get(self.url)
            time.sleep(10)

            # time.sleep(2)
            # self.driver.find_element(
            #     By.XPATH,
            #     '//*[@id="loginWarp"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[2]',
            # ).click()
            # time.sleep(1)
            # self.driver.find_element(
            #     By.XPATH, '//*[@id="login_email_username_id"]'
            # ).send_keys(login)
            # time.sleep(1)
            # self.driver.find_element(By.XPATH, '//*[@id="login-submit-btn"]').click()
            # time.sleep(2)
            # self.driver.find_element(
            #     By.XPATH, '//*[@id="login_phone_password_id"]'
            # ).send_keys(password)
            # time.sleep(1)
            # self.driver.find_element(By.XPATH, '//*[@id="login-submit-btn"]').click()

            print("Congratulations, you are logged in")
        except Exception as e:
            print(e)


RoutToSite().auth()
