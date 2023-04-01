from selenium.webdriver.common.by import By

from browser.driver.chrome import ChromeDriver
from config import Config
from model.models import AmazonProduct
from util import normalize_money


class Amazon:
    def __init__(self, driver: ChromeDriver):
        self.driver = driver

    def login(self, username, password):
        self.driver.get(
            "https://www.amazon.co.jp/ap/signin?_encoding=UTF8&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"
        )

        # 過去にログインしたことがある
        if not self.driver.find_xpath('//input[@id = "ap_password"]'):
            self.driver.send_keys((By.ID, "ap_email"), username)
            self.driver.click((By.ID, "continue"))

        self.driver.send_keys((By.ID, "ap_password"), password)
        self.driver.click((By.ID, "signInSubmit"))

    def get_product_data(self, asin) -> AmazonProduct:
        self.driver.get(f"https://www.amazon.co.jp/dp/{asin}")
        product = AmazonProduct(asin)

        # 通常注文を選択
        is_click = self.driver.click_if_exist(
            "//div[@id = 'newAccordionCaption_feature_div']", timeout=Config.TIMEOUT_lv2
        )
        if is_click:
            elem_for_wait = self.driver.find_xpath_if_exist("//input[@id = 'add-to-cart-button']")
            if not elem_for_wait:
                raise Exception("通常の注文を選択できませんでした")

        # タイトル
        product.title = self.driver.find_xpath("//span[@id='productTitle']").text

        # 価格
        price_text = self.driver.find_xpath("//div[@id='corePrice_feature_div']").text
        product.price = normalize_money(price_text)

        # 画像
        img_thumb_list = self.driver.finds_xpath("//*[@id='altImages']/ul/li[contains(@class,'imageThumbnail')]")
        for img_thumb in img_thumb_list:
            img_thumb.click()

        product.img_list = [
            e.get_attribute("src") for e in self.driver.finds_xpath("//div[@id='main-image-container']/ul/li/*//img")
        ]

        # 説明
        product.desc = self.driver.find_xpath("//div[@id='feature-bullets']").text

        # 在庫
        product.stock = self.driver.find_xpath("//div[@id='availability']/span[1]").text

        return product
