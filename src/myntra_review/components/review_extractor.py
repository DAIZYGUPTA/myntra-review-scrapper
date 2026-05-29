from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

import time
import random
import sys

from src.myntra_review.utils.logger import logger

from src.myntra_review.utils.exception import CustomException

from src.myntra_review.config.config import (
    MAX_REVIEWS_PER_PRODUCT
)


class ReviewExtractor:

    def __init__(self, driver):

        self.driver = driver

    # -----------------------------------
    # LOAD MORE REVIEWS
    # -----------------------------------

    def load_more_reviews(self):

        """
        Clicks 'Load More Reviews'
        multiple times.
        """

        try:

            while True:

                reviews = self.driver.find_elements(
                    By.CLASS_NAME,
                    "user-review-userReviewWrapper"
                )

                logger.info(
                    f"Current reviews loaded: "
                    f"{len(reviews)}"
                )

                # STOP IF LIMIT REACHED
                if len(reviews) >= MAX_REVIEWS_PER_PRODUCT:

                    logger.info(
                        "Reached max review limit"
                    )

                    break

                # SCROLL DOWN
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                time.sleep(
                    random.uniform(2, 4)
                )

                # FIND LOAD MORE BUTTON
                load_more_buttons = (
                    self.driver.find_elements(
                        By.XPATH,
                        "//span[contains(text(),'Load More Reviews')]"
                    )
                )

                if not load_more_buttons:

                    logger.info(
                        "No more review buttons found"
                    )

                    break

                # CLICK BUTTON
                button = load_more_buttons[0]

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                logger.info(
                    "Clicked Load More Reviews"
                )

                time.sleep(
                    random.uniform(3, 5)
                )

        except Exception as e:

            logger.warning(
                f"Load more review issue: {e}"
            )

    # -----------------------------------
    # EXTRACT REVIEWS
    # -----------------------------------

    def extract_reviews(
        self,
        product_url
    ):

        """
        Extracts reviews from product page.
        """

        try:

            logger.info(
                f"Extracting reviews from: "
                f"{product_url}"
            )

            # -----------------------------------
            # LOAD MORE REVIEWS
            # -----------------------------------

            self.load_more_reviews()

            # -----------------------------------
            # GET REVIEW BLOCKS
            # -----------------------------------

            review_blocks = (
                self.driver.find_elements(
                    By.CLASS_NAME,
                    "user-review-userReviewWrapper"
                )
            )

            logger.info(
                f"Total review blocks found: "
                f"{len(review_blocks)}"
            )

            # -----------------------------------
            # NO REVIEWS CASE
            # -----------------------------------

            if len(review_blocks) == 0:

                logger.info(
                    "No reviews found"
                )

                return [
                    {
                        "rating": None,
                        "review_text": "No Reviews",
                        "username": None,
                        "review_date": None
                    }
                ]

            reviews = []

            # -----------------------------------
            # EXTRACT REVIEW DATA
            # -----------------------------------

            for block in review_blocks[
                :MAX_REVIEWS_PER_PRODUCT
            ]:

                try:

                    # RATING
                    try:

                        rating = block.find_element(
                            By.CLASS_NAME,
                            "user-review-starRating"
                        ).text.strip()

                    except:

                        rating = None

                    # REVIEW TEXT
                    try:

                        review_text = (
                            block.find_element(
                                By.CLASS_NAME,
                                "user-review-reviewTextWrapper"
                            ).text.strip()
                        )

                    except:

                        review_text = None

                    # USERNAME + DATE
                    try:

                        footer = block.find_element(
                            By.CLASS_NAME,
                            "user-review-left"
                        )

                        spans = footer.find_elements(
                            By.TAG_NAME,
                            "span"
                        )

                        username = (
                            spans[0].text.strip()
                            if len(spans) > 0
                            else None
                        )

                        review_date = (
                            spans[1].text.strip()
                            if len(spans) > 1
                            else None
                        )

                    except:

                        username = None
                        review_date = None

                    # REVIEW OBJECT
                    review_data = {

                        "rating": rating,

                        "review_text": review_text,

                        "username": username,

                        "review_date": review_date
                    }

                    reviews.append(review_data)

                except Exception as review_error:

                    logger.warning(
                        f"Skipping review due to error: "
                        f"{review_error}"
                    )

                    continue

            logger.info(
                f"Successfully extracted "
                f"{len(reviews)} reviews"
            )

            return reviews

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)