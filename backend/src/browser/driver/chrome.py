import os
import shutil
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriver(webdriver.Chrome):
    def __init__(
        self, profile_name="", disable_extensions=True, is_headless=True, is_mobile=False, is_image_no_load=False
    ):
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")  # https://stackoverflow.com/a/26283818/1689770
        options.add_argument("--disable-logging")  # Logger
        # options.add_argument("enable-automation")  # https://stackoverflow.com/a/43840128/1689770
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--no-sandbox")  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument("--disable-infobars")  # https://stackoverflow.com/a/43840128/1689770
        options.add_argument("--disable-dev-shm-usage")  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument("--disable-browser-side-navigation")  # https://stackoverflow.com/a/49123152/1689770
        options.add_argument("--disable-gpu")  # https://stackoverflow.com/questions/51959986
        options.add_argument("--ignore-certificate-errors")  # https://stackoverflow.com/questions/37883759
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--ignore-ssl-errors")  # https://stackoverflow.com/questions/37883759
        options.add_argument("--disable-desktop-notifications")

        # 意味あるのか？？
        options.add_argument('--proxy-server="direct://"')
        options.add_argument("--proxy-bypass-list=*")

        # 画像を読み込まないで軽くする
        if is_image_no_load:
            options.add_argument("--blink-settings=imagesEnabled=false")

        # https://kacchanblog.com/programming/jidoukounyu/selenium-faster
        options.add_argument("--lang=ja")
        options.page_load_strategy = "eager"

        options.add_experimental_option(
            "useAutomationExtension", False
        )  # 拡張機能の自動更新をさせない（アプリ側の自動アップデートとドライバーの互換性によるエラーを回避）

        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        options.add_argument(f"--user-agent={UA}")

        # ログイン後の保存ポップアップを非表示設定
        options.add_experimental_option(
            "prefs", {"credentials_enable_service": False, "profile": {"password_manager_enabled": False}}
        )

        if profile_name != "":
            self.userdata_dir = self.create_userdata(profile_name)
            options.add_argument(f"--user-data-dir={self.userdata_dir}")

        if disable_extensions:
            options.add_argument("--disable-extensions")  # すべての拡張機能を無効にする。ユーザースクリプトも無効にする

        if is_headless:
            options.add_argument("--headless=new")

        if is_mobile:
            mobile_emulation = {"deviceName": "iPhone X"}
            options.add_argument("start-maximized")
            options.add_argument("--auto-open-devtools-for-tabs")
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

        path = ChromeDriverManager().install()
        chrome_service = ChromeService(path)
        chrome_service.creationflags = CREATE_NO_WINDOW

        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # https://stackoverflow.com/questions/41400934/
            "download.default_directory": os.path.join(os.getcwd(), "download"),  # ダウンロード先のフォルダ
            "plugins.always_open_pdf_externally": True,  # PDFをブラウザのビューワーで開かせない
        }
        options.add_experimental_option("prefs", prefs)

        super().__init__(path, chrome_options=options, service=chrome_service)
        self.set_page_load_timeout(30)

        # https://qiita.com/r_ishimori/items/4ed251f0d166d5c9cee1
        self.execute_script(
            "const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;"
        )

        self.timeout = 10

    def create_userdata(self, profile_name):
        userdata_dir = os.path.join(os.getcwd(), "Userdata", profile_name)
        os.makedirs(userdata_dir, exist_ok=True)
        return userdata_dir

    def delete_userdata(self):
        if os.path.isdir(self.userdata_dir):
            shutil.rmtree(self.userdata_dir)

    def quit(self):
        """_summary_
        ドライバを終了する
        """
        super().quit()
        self.session_id = None

    def exist(self):
        """_summary_
        ドライバが存在しているか確認
        Returns:
            bool: 存在していたらTrue
        """
        return self.session_id is not None

    def send_keys(self, locator, value):
        elem = WebDriverWait(self, self.timeout, 2).until(IsLocated(locator=locator))
        elem.send_keys(value)
        return elem

    def click(self, locator):
        elem = WebDriverWait(self, self.timeout).until(IsClickable(locator=locator))
        elem.click()
        return elem


class IsLocated:
    def __init__(self, locator=(), element=None):
        self.locator = locator
        self.element = element

    def __call__(self, driver):
        try:
            ecc = EC.visibility_of_element_located(self.locator)
            return ecc(driver)
        except Exception as e:
            return False


class IsClickable:
    def __init__(self, locator=(), element=None):
        self.locator = locator
        self.element = element

    def __call__(self, driver):
        try:
            ecc = EC.element_to_be_clickable(self.locator)
            return ecc(driver)
        except Exception as e:
            return False
