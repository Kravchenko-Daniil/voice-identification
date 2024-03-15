import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from parameters import login, password


class RoutToSite:
    def __init__(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=opts)
        self.url = 'https://www.okx.com/ru/account/users'

    def auth(self):
        try:
            self.driver.get(self.url)
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="loginWarp"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[2]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login_email_username_id"]').send_keys(login)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-submit-btn"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="login_phone_password_id"]').send_keys(password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-submit-btn"]').click()
            time.sleep(60)
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
            self.driver.quit()
