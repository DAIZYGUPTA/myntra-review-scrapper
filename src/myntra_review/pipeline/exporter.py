import pandas as pd

import os

from datetime import datetime

import sys

from src.myntra_review.utils.logger import logger

from src.myntra_review.utils.exception import CustomException


class DataExporter:

    def __init__(self):

        self.output_dir = "artifacts"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def generate_filename(self, prefix):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return f"{prefix}_{timestamp}"

    def export_csv(self, df):

        try:

            filename = self.generate_filename(
                "myntra_reviews"
            )

            filepath = os.path.join(
                self.output_dir,
                f"{filename}.csv"
            )

            df.to_csv(
                filepath,
                index=False
            )

            logger.info(
                f"CSV exported to {filepath}"
            )

            return filepath

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)

    def export_excel(self, df):

        try:

            filename = self.generate_filename(
                "myntra_reviews"
            )

            filepath = os.path.join(
                self.output_dir,
                f"{filename}.xlsx"
            )

            df.to_excel(
                filepath,
                index=False
            )

            logger.info(
                f"Excel exported to {filepath}"
            )

            return filepath

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)