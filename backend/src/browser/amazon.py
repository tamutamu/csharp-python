from selenium.webdriver.common.by import By


class Amazon:
    def __init__(self, driver):
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

    def get_product_data(self, asin):
        pass
