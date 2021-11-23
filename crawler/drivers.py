import os
from pathlib import Path

from selenium import webdriver
import geckodriver_autoinstaller


class Drivers:
    @staticmethod
    def firefox(download_dir: str) -> webdriver.Firefox:
        # geckodriver_autoinstaller.install()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', download_dir)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

        path = Path.cwd() / 'geckodriver.exe'
        driver = webdriver.Firefox(firefox_profile=profile, service_log_path=os.path.devnull, executable_path=path)

        return driver
