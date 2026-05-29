from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from src.myntra_review.config.config import HEADLESS

from src.myntra_review.utils.logger import logger

from src.myntra_review.utils.exception import CustomException

import sys


class BrowserManager:

    def __init__(self):

        self.options = Options()

        self.options.add_argument("--start-maximized")

        self.options.add_argument("--disable-notifications")

        self.options.add_argument("--disable-popup-blocking")

        self.options.add_argument("--disable-blink-features=AutomationControlled")

        self.options.add_argument("--no-sandbox")

        self.options.add_argument("--disable-dev-shm-usage")

        self.options.add_argument(
            "user-agent=Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )

        if HEADLESS == "True":

            self.options.add_argument("--headless=new")

    def get_driver(self):

        try:

            logger.info("Initializing Chrome Driver")

            service = Service(
                ChromeDriverManager().install()
            )

            driver = webdriver.Chrome(
                service=service,
                options=self.options
            )

            logger.info("Chrome Driver Initialized")

            return driver

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)