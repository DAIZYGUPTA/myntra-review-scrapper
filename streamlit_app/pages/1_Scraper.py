import sys
from pathlib import Path

# -----------------------------------
# ADD PROJECT ROOT TO PYTHONPATH
# -----------------------------------

project_root = (
    Path(__file__).resolve().parents[2]
)

sys.path.append(str(project_root))


import streamlit as st

import pandas as pd

from src.myntra_review.components.scraper import (
    MyntraReviewScraper
)

from src.myntra_review.pipeline.exporter import (
    DataExporter
)

from src.myntra_review.utils.logger import (
    logger
)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Myntra Scraper",
    page_icon="🛒",
    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "🛒 Myntra Product Review Scraper"
)

st.markdown(
    """
    Search products dynamically and scrape
    customer reviews directly from Myntra.
    """
)


# -----------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------

st.sidebar.header(
    "⚙️ Scraper Configuration"
)


search_query = st.sidebar.text_input(
    "Enter Product Search",
    placeholder="e.g. cotton tshirt"
)


max_products = st.sidebar.slider(
    "Select Number of Products",
    min_value=1,
    max_value=20,
    value=5
)


scrape_button = st.sidebar.button(
    "🚀 Start Scraping"
)


# -----------------------------------
# MAIN SCRAPING LOGIC
# -----------------------------------

if scrape_button:

    if not search_query.strip():

        st.warning(
            "Please enter a valid search query."
        )

    else:

        scraper = MyntraReviewScraper()

        try:

            # -----------------------------------
            # LOADING SPINNER
            # -----------------------------------

            with st.spinner(
                "Scraping reviews... "
                "Please wait."
            ):

                df = scraper.scrape(
                    search_query=search_query,
                    max_products=max_products
                )

            # -----------------------------------
            # STORE DATAFRAME GLOBALLY
            # -----------------------------------

            st.session_state[
                "scraped_df"
            ] = df

            # -----------------------------------
            # SUCCESS MESSAGE
            # -----------------------------------

            st.success(
                f"Successfully scraped "
                f"{len(df)} reviews!"
            )

            # -----------------------------------
            # KPI METRICS
            # -----------------------------------

            st.subheader(
                "📌 Scraping Summary"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Reviews",
                    len(df)
                )

            with col2:

                st.metric(
                    "Products Scraped",
                    max_products
                )

            with col3:

                avg_rating = round(

                    pd.to_numeric(
                        df["product_rating"],
                        errors="coerce"
                    ).mean(),

                    2
                )

                st.metric(
                    "Average Product Rating",
                    avg_rating
                )

            # -----------------------------------
            # DATA PREVIEW
            # -----------------------------------

            st.subheader(
                "📄 Scraped Dataset Preview"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # -----------------------------------
            # EXPORT FILES
            # -----------------------------------

            exporter = DataExporter()

            csv_path = exporter.export_csv(
                df
            )

            excel_path = (
                exporter.export_excel(df)
            )

            # -----------------------------------
            # DOWNLOAD SECTION
            # -----------------------------------

            st.subheader(
                "⬇️ Download Dataset"
            )

            col1, col2 = st.columns(2)

            with col1:

                with open(
                    csv_path,
                    "rb"
                ) as f:

                    st.download_button(

                        label="Download CSV",

                        data=f,

                        file_name=(
                            "myntra_reviews.csv"
                        ),

                        mime="text/csv"
                    )

            with col2:

                with open(
                    excel_path,
                    "rb"
                ) as f:

                    st.download_button(

                        label="Download Excel",

                        data=f,

                        file_name=(
                            "myntra_reviews.xlsx"
                        ),

                        mime=(
                            "application/"
                            "vnd.openxmlformats-"
                            "officedocument."
                            "spreadsheetml.sheet"
                        )
                    )

            # -----------------------------------
            # ANALYTICS READY MESSAGE
            # -----------------------------------

            st.info(
                "Dataset is now available "
                "inside the Analytics page."
            )

        except Exception as e:

            logger.error(e)

            st.error(
                f"Error occurred: {e}"
            )

        finally:

            scraper.close()


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    """Built by DAIZY 
     
    using Selenium + Streamlit"""
)