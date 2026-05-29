from selenium.webdriver.common.by import By

import time
import random
import sys

from src.myntra_review.utils.logger import logger
from src.myntra_review.utils.exception import CustomException
from src.myntra_review.config.config import (
    SCROLL_PAUSE_TIME,
    
)


class ProductExtractor:

    def __init__(self, driver, max_products):

        self.driver = driver
        self.max_products = max_products

    def scroll_to_bottom(self):

        """
        Scrolls dynamically until all products are loaded.
        """

        try:

            logger.info("Starting page scrolling")

            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            while True:

                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                time.sleep(
                    random.uniform(
                        2,
                        SCROLL_PAUSE_TIME
                    )
                )

                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:

                    logger.info("Reached end of page")
                    break

                last_height = new_height

            logger.info("Scrolling completed successfully")

        except Exception as e:

            logger.error(f"Error during scrolling: {e}")

            raise CustomException(e, sys)

    def get_product_cards(self):

        """
        Returns all product card elements.
        """

        try:

            products = self.driver.find_elements(
                By.CSS_SELECTOR,
                "li.product-base"
            )

            logger.info(
                f"Found {len(products)} product cards"
            )

            return products

        except Exception as e:

            logger.error(f"Error finding product cards: {e}")

            raise CustomException(e, sys)

    def safe_find_text(self, parent, by, selector):

        """
        Safely extracts text from element.
        """

        try:

            return parent.find_element(
                by,
                selector
            ).text.strip()

        except:

            return None

    def safe_find_attribute(
        self,
        parent,
        by,
        selector,
        attribute
    ):

        """
        Safely extracts attribute from element.
        """

        try:

            return parent.find_element(
                by,
                selector
            ).get_attribute(attribute)

        except:

            return None

    def extract_products(self):

        """
        Main product extraction pipeline.
        """

        try:

            logger.info("Starting product extraction")

            self.scroll_to_bottom()

            product_cards = self.get_product_cards()

            all_products = []

            seen_links = set()

            for product in product_cards:

                try:

                    brand = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "h3.product-brand"
                    )

                    product_name = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "h4.product-product"
                    )

                    price = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "span.product-discountedPrice"
                    )

                    original_price = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "span.product-strike"
                    )

                    discount = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "span.product-discountPercentage"
                    )

                    rating = self.safe_find_text(
                        product,
                        By.CSS_SELECTOR,
                        "div.product-ratingsContainer span"
                    )

                    product_url = self.safe_find_attribute(
                        product,
                        By.TAG_NAME,
                        "a",
                        "href"
                    )

                    image_url = self.safe_find_attribute(
                        product,
                        By.CSS_SELECTOR,
                        "img.img-responsive",
                        "src"
                    )

                    # Skip invalid links
                    if not product_url:

                        continue

                    # Deduplication
                    if product_url in seen_links:

                        continue

                    seen_links.add(product_url)

                    product_data = {

                        "brand": brand,

                        "product_name": product_name,

                        "price": price,

                        "original_price": original_price,

                        "discount": discount,

                        "rating": rating,

                        "product_url": product_url,

                        "image_url": image_url
                    }

                    all_products.append(product_data)

                    logger.info(
                        f"Extracted product: {product_name}"
                    )

                    # Limit products
                    if len(all_products) >= self.max_products:

                        logger.info(
                            f"Reached max_products limit: "
                            f"{self.max_products}"
                        )

                        break

                except Exception as product_error:

                    logger.warning(
                        f"Skipping product due to error: {product_error}"
                    )

                    continue

            logger.info(
                f"Successfully extracted {len(all_products)} products"
            )

            return all_products

        except Exception as e:

            logger.error(f"Product extraction failed: {e}")

            raise CustomException(e, sys)