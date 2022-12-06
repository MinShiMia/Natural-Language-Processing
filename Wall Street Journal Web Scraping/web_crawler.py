from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from customized_logging import CustomizedLogger
from timeout import TimeOutException, TimeOut, TestFuncForTimeOut

logger = CustomizedLogger.get_file_and_stream_logger(__name__)


class WebCrawler:
    year = None
    month = None
    url = None
    user1 = "user account / registered email address"
    pass1 = "your wsj membership password"
    driver = None
    max_tries_for_finding_items = 50

    day = 0
    order = 0
    retries = {}
    max_retries = 30

    def __init__(self, year, month, day, order, max_retries=30):
        self.year = year
        self.month = month
        self.url = f'https://www.wsj.com/news/archive/{self.year}/{self.month}'
        self.day = day
        self.order = order
        self.max_retries = max_retries
    
    def main_entry(self):
        try:
            self.driver = self.get_driver_for_chrome()
            self.open_homepage_and_sign_in()
            self.try_to_download()
        except Exception as exc:
            logger.exception("web driver exception: %s", str(exc))
            try:
                TimeOut.timeout_func(logger, self.driver.quit)
            except TimeOutException:
                logger.warning("chrome failed to quit")
                pass
            self.driver = self.get_driver_for_chrome()
            self.open_homepage_and_sign_in()
            self.main_entry()

    def try_to_download(self):
        logger.info("try to download from day %d, order %d", self.day, self.order)
        try:
            self.download_articles_for_one_month()
        except TimeOutException as exc:
            logger.exception("time out")
            logger.exception("day: %d, order: %d", exc.day, exc.order)
            logger.info("===============================\n")
            logger.info("retrying")
            count = self.retries.get((exc.day, exc.order), 0)
            if count < self.max_retries:
                self.retries[(exc.day, exc.order)] = count + 1
                self.try_to_download()
            else:
                self.order = self.order + 1
                self.try_to_download()

    def download_articles_for_one_month(self):
        try:
            TimeOut.timeout_func(logger, self.driver.get, [self.url, ])
        except TimeOutException:
            try:
                TimeOut.timeout_func(logger, self.driver.quit)
            except TimeOutException:
                logger.warning("chrome failed to quit")
                pass
            self.driver = self.get_driver_for_chrome()
            self.open_homepage_and_sign_in()
        time.sleep(2)
        list_of_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="WSJTheme--day-link--19pByDpZ "][@href]')))
        time.sleep(2)

        logger.info("list_of_items size: %d \n", len(list_of_items))

        start_day = self.day
        for day in range(start_day, len(list_of_items)):
            self.day = day
            file_name = f"wsj_articles_{self.year}_{self.month}_{day}.csv"
            with open(file_name, 'a+', encoding='utf-8', newline='') as csv_file:
                logger.info("download articles to %s", file_name)
                self.__download_articles_for_one_day(csv_file)
                self.order = 0

    def __download_articles_for_one_day(self, csv_file):
        logger.info("downloading for day: %d \n", self.day)
        list_of_items = None
        try:
            time.sleep(2)
            list_of_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="WSJTheme--day-link--19pByDpZ "][@href]')))
            time.sleep(2)

        except Exception as exc:
            logger.exception("exception: %s", exc.__traceback__)

        try:
            TimeOut.timeout_func(logger, list_of_items[self.day].click)
            # tested: when time out, the program can retry with no error
            # TimeOut.timeout_func(logger, TestFuncForTimeOut.loop)
        except TimeOutException as exc:
            exc.day = self.day
            exc.order = self.order
            raise exc

        time.sleep(1.5)

        list_of_item = self.__find_list_of_item()

        logger.info("Length of list_of_item is: %d \n", len(list_of_item))

        time.sleep(2)
        start_order = self.order

        for order in range(start_order, len(list_of_item)):
            self.order = order
            self.__go_to_article_and_save_to_csv_file(csv_file)
        self.driver.back()

    def __go_to_article_and_save_to_csv_file(self, csv_file):
        logger.info("======================================= \n", )
        logger.info("downloading for article: %d \n", self.order)

        list_of_item = self.__find_list_of_item()

        try:
            logger.info("Trying to click the following web element: %s", str(list_of_item[self.order]))

            # TimeOut.timeout_click(list_of_item[order])
            TimeOut.timeout_func(logger, list_of_item[self.order].click)
            # TimeOut.timeout_func(logger, TestFuncForTimeOut.loop)
            time.sleep(1)
            logger.info("Clicking the following web element: %s", str(list_of_item[self.order]))

            article_dict = self.__parse_article_from_page()

            writer = csv.writer(csv_file)
            writer.writerow(article_dict.values())
            csv_file.flush()
            TimeOut.timeout_func(logger, self.driver.back)
        except TimeOutException as exc:
            exc.day = self.day
            exc.order = self.order
            raise exc

        except Exception as exc:
            logger.info("Failed to click on: %s", str(list_of_item[self.order]))
            logger.exception("exception: %s", exc.__traceback__)
            return

    def __find_list_of_item(self):
        for _ in range(self.max_tries_for_finding_items):
            try:
                list_of_item = self.driver.find_elements(By.XPATH,
                                                    './/h2[@class="WSJTheme--headline--unZqjb45 reset '
                                                    'WSJTheme--heading-standard-s--2eMU4jl4 WSJTheme--standard--2eOdD903 '
                                                    'typography--serif-display--ZXeuhS5E WSJTheme--small--2f09SjbK "]//a['
                                                    '@href]')
                logger.info("trying to get list_of_item")
                logger.debug("list_of_item: %s", str(list_of_item))
                if list_of_item:
                    return list_of_item
            except WebDriverException:
                logger.exception("save_article_to_csv_file exception")
        exc = TimeOutException("finding list_of_item error")
        exc.order = self.order
        exc.day = self.day
        raise exc

    def __parse_article_from_page(self):
        article_dict = {}
        try:
            article_string = ''
            text1 = self.driver.find_elements(By.XPATH, ".//section[@class='css-1ducvg2-Container e1d75se20']//p")
            for ele in text1:
                article_string += ele.text
        except (NoSuchElementException, StaleElementReferenceException) as exc:
            logger.exception("article_string exception: %s", exc.__traceback__)
            article_string = ''
            pass
        logger.info("article content size: %d", len(article_string))
        logger.info("article preview: %s", article_string[:30])

        try:
            headline1 = self.driver.find_element(By.XPATH, './/h1[@class="css-1lvqw7f-StyledHeadline e1ipbpvp0"]')
            article_headline = headline1.text
        except (NoSuchElementException, StaleElementReferenceException) as exc:
            logger.exception("headline1 exception: %s", exc.__traceback__)
            article_headline = ''
            pass
        logger.info("article_headline size: %d", len(article_headline))
        logger.info("article_headline: %s", article_headline[:30])

        try:
            headline2 = self.driver.find_element(By.XPATH, './/h2[@class="css-mosdo-Dek-Dek e1jnru6p0"]')
            article_subheadline = headline2.text
        except (NoSuchElementException, StaleElementReferenceException) as exc:
            logger.exception("headline2 exception: %s", exc.__traceback__)
            article_subheadline = ''
            pass

        logger.info("article_subheadline size: %d", len(article_subheadline))
        logger.info("article_subheadline: %s", article_subheadline[:30])

        try:
            time1 = self.driver.find_element(By.XPATH, ".//time[@class='css-a8mttu-Timestamp-Timestamp emlnvus0']")
            article_published_date = time1.text
        except (NoSuchElementException, StaleElementReferenceException) as exc:
            logger.exception("time1 exception: %s", exc.__traceback__)
            article_published_date = ''
            pass
        logger.info("article_published_date size: %d", len(article_published_date))
        logger.info("article_published_date: %s", article_published_date[:30])

        article_dict['article_body_text'] = article_string
        article_dict['article_headline'] = article_headline
        article_dict['article_subheadline'] = article_subheadline
        article_dict['article_published_date'] = article_published_date
        logger.info("=====> article_dict: %s", str(article_dict))
        return article_dict

    def get_driver_for_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def open_homepage_and_sign_in(self):
        logger.info("homepage: %s", self.url)
        self.driver.get(self.url)
        sign_in_link = self.driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_link.click()
        self.__sign_in()

    def __sign_in(self):
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'username')))
        username.send_keys(self.user1)
        submit_button = self.driver.find_element(
            By.XPATH, ".//button[@type='button'][@class='solid-button continue-submit new-design']"
        )
        submit_button.click()
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'password-login-password')))
        password.send_keys(self.pass1)
        submit_button = self.driver.find_element(
            By.XPATH, ".//button[@type='submit'][@class='solid-button new-design basic-login-submit']"
        )
        submit_button.click()
