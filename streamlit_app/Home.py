import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

sys.path.append(str(project_root))

import streamlit as st


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Myntra Review Scraper",
    page_icon="🛍️",
    layout="wide"
)


# -----------------------------------
# HERO SECTION
# -----------------------------------

st.title("🛍️ Myntra Review Scraper & Analytics")

st.markdown(
    """
    A complete end-to-end web scraping and analytics platform
    for Myntra product reviews using:

    - Selenium
    - Python
    - Streamlit
    - Pandas
    - NLP
    - Data Visualization
    """
)


# -----------------------------------
# FEATURES
# -----------------------------------

st.header("🚀 Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### Scraping Features

        ✅ Dynamic product search

        ✅ Automated Myntra search handling

        ✅ Infinite scrolling support

        ✅ Multi-product scraping

        ✅ Product review extraction

        ✅ CSV & Excel export

        ✅ Modular architecture
        """
    )

with col2:

    st.markdown(
        """
        ### Analytics Features

        ✅ Sentiment analysis

        ✅ Rating distributions

        ✅ Wordcloud visualization

        ✅ Review insights

        ✅ Brand-level analysis

        ✅ Product-level comparison

        ✅ Interactive charts
        """
    )


# -----------------------------------
# WORKFLOW
# -----------------------------------

st.header("⚙️ Application Workflow")

st.markdown(
    """
    ```text
    User Search
        ↓
    Selenium Automation
        ↓
    Myntra Product Extraction
        ↓
    Review Scraping
        ↓
    Dataset Generation
        ↓
    Analytics Dashboard
    ```
    """
)


# -----------------------------------
# PROJECT STRUCTURE
# -----------------------------------

st.header("📁 Project Architecture")

st.code(
    """
project/
│
├── app.py
│
├── streamlit_app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Scraper.py
│       └── 2_Analysis.py
│
├── src/
│   └── myntra_review/
│       ├── components/
│       ├── pipeline/
│       ├── utils/
│       └── config/
│
├── artifacts/
│
├── logs/
│
└── requirements.txt
    """,
    language="text"
)


# -----------------------------------
# HOW TO USE
# -----------------------------------

st.header("📌 How To Use")

st.markdown(
    """
    1. Open the **Scraper Page**
    2. Enter product search query
    3. Select number of products
    4. Start scraping
    5. Download dataset
    6. Open Analytics Dashboard
    """
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.success(
    "Select a page above."
)



# -----------------------------------
# FOOTER
# -----------------------------------


st.markdown(
    "<div style='text-align:center; color:#888; font-size:14px;'>"
    "Built by <b>Daizy</b> using Python, Selenium & Streamlit"
    "</div>",
    unsafe_allow_html=True
)

#st.markdown("---")

#st.caption(
#    "Built by Daizy using Python, Selenium & Streamlit"
#)