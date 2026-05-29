import pandas as pd

import sys
import time
import random

from src.myntra_review.utils.logger import logger

from src.myntra_review.utils.exception import (
    CustomException
)

from src.myntra_review.utils.browser import (
    BrowserManager
)

from src.myntra_review.components.search_handler import (
    SearchHandler
)

from src.myntra_review.components.product_extractor import (
    ProductExtractor
)

from src.myntra_review.components.review_extractor import (
    ReviewExtractor
)


class MyntraReviewScraper:

    def __init__(self):

        logger.info(
            "Initializing MyntraReviewScraper"
        )

        self.driver = (
            BrowserManager().get_driver()
        )

    # -----------------------------------
    # MAIN SCRAPE WORKFLOW
    # -----------------------------------

    def scrape(
        self,
        search_query,
        max_products
    ):

        try:

            logger.info(
                "Starting scraping workflow"
            )

            # -----------------------------------
            # SEARCH PRODUCT
            # -----------------------------------

            search_handler = SearchHandler(
                self.driver
            )

            search_handler.search_product(
                search_query
            )

            # -----------------------------------
            # EXTRACT PRODUCTS
            # -----------------------------------

            product_extractor = (
                ProductExtractor(
                    self.driver,
                    max_products
                )
            )

            products = (
                product_extractor.extract_products()
            )

            logger.info(
                f"Collected "
                f"{len(products)} products"
            )

            all_reviews = []

            # -----------------------------------
            # ITERATE PRODUCTS
            # -----------------------------------

            for index, product in enumerate(products):

                try:

                    logger.info(
                        f"Processing product "
                        f"{index + 1}"
                    )

                    product_url = product[
                        "product_url"
                    ]

                    self.driver.get(product_url)

                    time.sleep(
                        random.uniform(3, 5)
                    )

                    # -----------------------------------
                    # EXTRACT REVIEWS
                    # -----------------------------------

                    review_extractor = (
                        ReviewExtractor(
                            self.driver
                        )
                    )

                    reviews = (
                        review_extractor
                        .extract_reviews(
                            product_url=product_url
                        )
                    )

                    logger.info(
                        f"Collected "
                        f"{len(reviews)} reviews"
                    )

                    # -----------------------------------
                    # NO REVIEW CASE
                    # -----------------------------------

                    if not reviews:

                        logger.warning(
                            "No reviews found "
                            "for this product"
                        )

                        reviews = [
                            {
                                "rating": None,

                                "review_text":
                                "No Reviews",

                                "username": None,

                                "review_date": None
                            }
                        ]

                    # -----------------------------------
                    # MERGE PRODUCT METADATA
                    # -----------------------------------

                    for review in reviews:

                        review["brand"] = (
                            product.get(
                                "brand"
                            )
                        )

                        review["product_name"] = (
                            product.get(
                                "product_name"
                            )
                        )

                        review["price"] = (
                            product.get(
                                "price"
                            )
                        )

                        review["original_price"] = (
                            product.get(
                                "original_price"
                            )
                        )

                        review["discount"] = (
                            product.get(
                                "discount"
                            )
                        )

                        review["product_rating"] = (
                            product.get(
                                "rating"
                            )
                        )

                        review["product_image"] = (
                            product.get(
                                "image_url"
                            )
                        )

                        review["product_url"] = (
                            product.get(
                                "product_url"
                            )
                        )

                        all_reviews.append(
                            review
                        )

                except Exception as product_error:

                    logger.warning(
                        f"Skipping product "
                        f"due to error: "
                        f"{product_error}"
                    )

                    continue

            # -----------------------------------
            # CREATE DATAFRAME
            # -----------------------------------

            df = pd.DataFrame(
                all_reviews
            )

            logger.info(
                f"Final dataset shape: "
                f"{df.shape}"
            )

            logger.info(
                "Scraping completed "
                "successfully"
            )

            return df

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)

    # -----------------------------------
    # CLOSE DRIVER
    # -----------------------------------

    def close(self):

        try:

            self.driver.quit()

            logger.info(
                "Browser closed successfully"
            )

        except Exception as e:

            logger.warning(e)
            