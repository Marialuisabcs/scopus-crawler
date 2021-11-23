import os
import sys
import time
from typing import Union

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crawler.xpath import XPath


class ScopusCitationBot:
    """Bot that uses Scopus database via browser to download csv with the cited by data"""
    driver: Union[FirefoxDriver]
    download_dir: str
    proxy: str

    def __init__(self, driver, download_dir, search_string: str, homepage: str = 'https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/index.php?'):
        """
        :param driver: selenium driver with a configured profile
        :param download_dir: directory where the files will be downloaded
        """
        self.driver = driver
        self.download_dir = download_dir
        self.driver.get(homepage)
        self.search_string = search_string

    def start_session(self):
        """Must be executed after the user started a scopus session"""
        # since the scopus page is opened on another window, we need to switch
        # to the other window
        self.driver.switch_to.window(window_name=self.driver.window_handles[1])
        self.proxy = self.driver.current_url.split('/search')[0]
        with open(f'{self.download_dir}/scopus.csv', 'w') as f:
            f.write('\n')

    def get_url(self, year):
        encoded_search_string = self.search_string.replace(' ', '+')
        url = f'https://www-scopus.ez51.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&nlo=&nlr=&nls=&sid=ee1f9e9f5ce79f0c36e51ea488394230&sot=b&sdt=cl&cluster=scopubyr%2c%22{year}%22%2ct&sl=31&s=TITLE-ABS-KEY%28{encoded_search_string}%29&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=973f0ce7e5ed7db95f978310df6b4303'
        self.driver.get(url)

    def wait_until_clickable(self, xpath: str, timeout: int = 20):
        """Waits until the xpath element is clickable on the actual page, given a timeout
        :param xpath: xpath of the element to be waited
        :param timeout: time to wait for the element
        """
        WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(
            (By.XPATH, xpath))).click()

    def get_number_citations(self) -> int:
        """Gets the number of citations on the actual page
        :return: number of citations
        """
        number_citations = 0
        try:
            self.driver.find_element_by_xpath(XPath.NO_CITATIONS)

        except NoSuchElementException:
            self.wait_until_clickable(XPath.NUMBER_CITATIONS, 20)
            number_citations = int(
                self.driver.find_element_by_xpath(XPath.NUMBER_CITATIONS).text.replace(',', ''))

        return number_citations

    def wait_download(self, file_id):
        """Waits until the download is finished"""
        while not os.path.exists(f'{self.download_dir}/scopus({file_id}).csv'):
            time.sleep(1)

    def click(self, xpath: str):
        """Tries to close any popups before clicking the given xpath element
        :param xpath: xpath of the element to be clicked
        """
        try:
            self.driver.find_element_by_xpath(XPath.CLOSE_POPUP).click()

        except NoSuchElementException:
            pass

        self.driver.find_element_by_xpath(xpath).click()

    def export_csv_with_abstracts(self, file_id: int):
        self.wait_until_clickable(XPath.PAGE)
        self.wait_until_clickable(XPath.SELECT_ALL)

        try:
            self.click(XPath.DIRECT_EXPORT)

        except NoSuchElementException:
            self.click(XPath.EXPORT)

            self.click(XPath.UNCHECK_INFOS)

            self.click(XPath.CHECK_TITLE)
            self.click(XPath.CHECK_ABSTRACT)

            self.click(XPath.CSV_FORMAT)
            self.click(XPath.DOWNLOAD)

        try:
            self.wait_until_clickable(XPath.ONLY_2000_RESULTS)
            self.click(XPath.ONLY_2000_RESULTS)
            self.click(XPath.ONLY_2000_RESULTS_EXPORT)

        except NoSuchElementException:
            pass

        except TimeoutException:
            self.wait_download(file_id)
            return True

        self.wait_download(file_id)

        return True

    def end_session(self):
        """Closes the browser driver"""
        self.driver.quit()
