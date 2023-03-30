from logging import getLogger
from selenium.webdriver.common.by import By

from browser.driver.chrome import ChromeDriver

LOGGER = getLogger(__name__)


class Yahoo:
    def __init__(self, driver: ChromeDriver):
        self.driver = driver

    def login(self, username, password, pre_logout=False):
        self.driver.get("https://login.yahoo.co.jp/config/login")
        ss = self.driver.send_keys_if_exist((By.ID, "login_handle"), username)
        if ss[0]:
            self.driver.click((By.XPATH, "//button[text() = '次へ']"))
            self.driver.send_keys((By.ID, "password"), password)
            self.driver.click((By.XPATH, "//button[text() = 'ログイン']"))
        else:
            LOGGER.error(ss[1])
            self.driver.send_keys((By.ID, "username"), username)
            self.driver.click((By.ID, "btnNext"))
            self.driver.send_keys((By.ID, "passwd"), password)
            self.driver.click((By.ID, "btnSubmit"))

    def sell():
        pass
