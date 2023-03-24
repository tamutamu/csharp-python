import os
import shutil
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriver(webdriver.Chrome):
    def __init__(self, profile_name="", disable_extensions=True, is_headless=True, is_mobile=False):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")  # https://stackoverflow.com/a/26283818/1689770
        options.add_argument("--disable-logging")  # Logger
        options.add_argument("enable-automation")  # https://stackoverflow.com/a/43840128/1689770
        options.add_argument("--no-sandbox")  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument("--disable-infobars")  # https://stackoverflow.com/a/43840128/1689770
        options.add_argument("--disable-dev-shm-usage")  # https://stackoverflow.com/a/50725918/1689770
        options.add_argument("--disable-browser-side-navigation")  # https://stackoverflow.com/a/49123152/1689770
        options.add_argument("--disable-gpu")  # https://stackoverflow.com/questions/51959986
        options.add_argument("--ignore-certificate-errors")  # https://stackoverflow.com/questions/37883759
        options.add_argument("--ignore-ssl-errors")  # https://stackoverflow.com/questions/37883759

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
