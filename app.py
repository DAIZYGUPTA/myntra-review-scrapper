from src.myntra_review.components.scraper import (
    MyntraReviewScraper
)

from src.myntra_review.pipeline.exporter import (
    DataExporter
)

from src.myntra_review.utils.logger import logger


def main():

    logger.info(
        "Application Started"
    )

    scraper = MyntraReviewScraper()

    try:

        # -----------------------------------
        # USER INPUTS
        # -----------------------------------

        search_query = input(
            "\nEnter product search query: "
        )

        max_products = int(
            input(
                "Enter number of products to scrape: "
            )
        )

        # -----------------------------------
        # SCRAPING
        # -----------------------------------

        df = scraper.scrape(
            search_query=search_query,
            max_products=max_products
        )

        # -----------------------------------
        # DATA PREVIEW
        # -----------------------------------

        print("\nDataset Preview:\n")

        print(df.head())

        print(
            f"\nTotal Reviews Scraped: "
            f"{len(df)}"
        )

        # -----------------------------------
        # EXPORTING
        # -----------------------------------

        exporter = DataExporter()

        csv_path = exporter.export_csv(df)

        excel_path = exporter.export_excel(df)

        # -----------------------------------
        # SUCCESS OUTPUT
        # -----------------------------------

        print(
            f"\nCSV Saved: {csv_path}"
        )

        print(
            f"Excel Saved: {excel_path}"
        )

    except Exception as e:

        logger.error(e)

        print(f"\nError: {e}")

    finally:

        scraper.close()

        logger.info(
            "Application Finished"
        )


if __name__ == "__main__":

    main()