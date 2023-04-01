from glob import glob
from logging import getLogger
import os
import shutil
from time import sleep
from selenium.webdriver.common.by import By

from browser.driver.chrome import ChromeDriver
from model.models import AmazonProduct
from util.request_util import FileDownloader

LOGGER = getLogger(__name__)


class Yahoo:
    def __init__(self, driver: ChromeDriver):
        self.driver = driver

    def login(self, user_id, password, pre_logout=False):
        self.driver.get("https://login.yahoo.co.jp/config/login")
        sleep(1)
        pattern1 = self.driver.send_keys_if_exist((By.ID, "login_handle"), user_id)

        if pattern1[0]:
            self.driver.click((By.XPATH, "//button[text() = '次へ']"))
            self.driver.send_keys((By.ID, "password"), password)
            self.driver.click((By.XPATH, "//button[text() = 'ログイン']"))
        else:
            self.driver.send_keys((By.ID, "username"), user_id)
            self.driver.click((By.ID, "btnNext"))
            self.driver.send_keys((By.ID, "passwd"), password)
            self.driver.click((By.ID, "btnSubmit"))


class YahooAuction(Yahoo):
    def new_sell(self, product: AmazonProduct):
        self.driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")

        # 画像
        self.upload_image(product)

        # タイトル
        self.driver.send_keys((By.ID, "fleaTitleForm"), product.title[:60])

        # カテゴリ
        self.select_category(product)

        # 説明
        self.driver.switch_to_iframe((By.ID, "rteEditorComposition0"))
        self.driver.send_keys((By.XPATH, "//body"), product.desc)

    def upload_image(self, product: AmazonProduct):
        save_dir = os.path.abspath("./_images/")
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)

        FileDownloader.download_files(product.img_list, save_dir)
        img_list = glob(os.path.abspath("./_images/*"))
        for file_path in img_list:
            LOGGER.info(file_path)
            self.driver.find_element(By.ID, "selectFile").send_keys(file_path)

        # アップロードを待つ
        self.driver.wait_xpath("//label[@for='selectFile']", len(img_list))

    def select_category(self, product: AmazonProduct):
        self.driver.click((By.ID, "acMdCateChange"))
        self.driver.click((By.XPATH, "//a[div[contains(text(), 'キーワードから選択する')]]"))
        self.driver.send_keys((By.ID, "category-search-keyword"), product.title)
        # 検索ボタン押下
        self.driver.click((By.XPATH, "//input[@type = 'submit' and @name = 'submit' and contains(@value, '検')]"))
        # 検索結果の１番目を選択
        self.driver.click((By.XPATH, "(//input[@type = 'radio' and @name = 'category'])[1]"))

        self.driver.click((By.ID, "search_category_submit"))
