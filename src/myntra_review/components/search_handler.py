from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import time
import random
import sys

from src.myntra_review.utils.logger import logger

from src.myntra_review.utils.exception import CustomException


class SearchHandler:

    def __init__(self, driver):

        self.driver = driver

    def search_product(self, search_query):

        """
        Searches product on Myntra.
        """

        try:

            logger.info(
                f"Searching for: {search_query}"
            )

            # Open homepage
            self.driver.get(
                "https://www.myntra.com/"
            )

            time.sleep(
                random.uniform(3, 5)
            )

            # Wait for search box
            search_box = WebDriverWait(
                self.driver,
                15
            ).until(

                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "desktop-searchBar"
                    )
                )
            )

            # Clear existing text
            search_box.clear()

            # Type query naturally
            for char in search_query:

                search_box.send_keys(char)

                time.sleep(
                    random.uniform(0.05, 0.15)
                )

            time.sleep(1)

            # Press Enter
            search_box.send_keys(Keys.ENTER)

            logger.info(
                "Search submitted successfully"
            )

            time.sleep(
                random.uniform(4, 6)
            )

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)