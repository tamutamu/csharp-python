class YahooAuction:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password, pre_logout):
        self.driver.get("https://login.yahoo.co.jp/config/login")
