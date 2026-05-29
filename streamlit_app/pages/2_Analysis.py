import sys
from pathlib import Path

project_root = (
    Path(__file__).resolve().parents[2]
)

sys.path.append(str(project_root))


import streamlit as st

import pandas as pd
import numpy as np

import plotly.express as px

from textblob import TextBlob

from wordcloud import WordCloud

import matplotlib.pyplot as plt


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "📊 Myntra Review Analytics Dashboard"
)


st.markdown(
    """
    Analyze scraped Myntra reviews
    with intelligent visualizations
    and buyer insights.
    """
)


# -----------------------------------
# CHECK SESSION DATA
# -----------------------------------

if "scraped_df" not in st.session_state:

    st.warning(
        "No scraped dataset found.\n\n"
        "Please scrape products first "
        "from the Scraper page."
    )

    st.stop()


# -----------------------------------
# LOAD DATAFRAME
# -----------------------------------

df = st.session_state["scraped_df"]


# -----------------------------------
# DATA PREVIEW
# -----------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)


# -----------------------------------
# CLEAN DATA
# -----------------------------------

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["product_rating"] = pd.to_numeric(
    df["product_rating"],
    errors="coerce"
)


# -----------------------------------
# KPI SECTION
# -----------------------------------

st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Reviews",
        len(df)
    )

with col2:

    st.metric(
        "Average Rating",
        round(
            df["rating"].mean(),
            2
        )
    )

with col3:

    st.metric(
        "Unique Products",
        df["product_name"].nunique()
    )

with col4:

    st.metric(
        "Unique Brands",
        df["brand"].nunique()
    )


# -----------------------------------
# RATING DISTRIBUTION
# -----------------------------------

st.subheader("⭐ Rating Distribution")

rating_fig = px.histogram(
    df,
    x="rating",
    nbins=5,
    title="Customer Rating Distribution"
)

st.plotly_chart(
    rating_fig,
    use_container_width=True
)


# -----------------------------------
# TOP BRANDS
# -----------------------------------

st.subheader("🏷️ Top Brands")

top_brands = (
    df["brand"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_brands.columns = [
    "Brand",
    "Reviews"
]

brand_fig = px.bar(
    top_brands,
    x="Brand",
    y="Reviews",
    title="Top Reviewed Brands"
)

st.plotly_chart(
    brand_fig,
    use_container_width=True
)


# -----------------------------------
# SENTIMENT ANALYSIS
# -----------------------------------

st.subheader("🧠 Sentiment Analysis")


def get_sentiment(text):

    polarity = TextBlob(
        str(text)
    ).sentiment.polarity

    if polarity > 0:

        return "Positive"

    elif polarity < 0:

        return "Negative"

    else:

        return "Neutral"


df["sentiment"] = df[
    "review_text"
].apply(get_sentiment)


sentiment_counts = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "Sentiment",
    "Count"
]


sentiment_fig = px.pie(
    sentiment_counts,
    names="Sentiment",
    values="Count",
    title="Review Sentiment Distribution"
)

st.plotly_chart(
    sentiment_fig,
    use_container_width=True
)



# -----------------------------------
# AI RECOMMENDATION ENGINE
# -----------------------------------

st.subheader(
    "🧠 AI Shopping Recommendation"
)


# -----------------------------------
# METRICS CALCULATION
# -----------------------------------

avg_rating = df["rating"].mean()

positive_ratio = (

    len(
        df[df["sentiment"] == "Positive"]
    )

    / len(df)

) * 100


negative_ratio = (

    len(
        df[df["sentiment"] == "Negative"]
    )

    / len(df)

) * 100


review_volume = len(df)


# -----------------------------------
# CONFIDENCE SCORE
# -----------------------------------

confidence_score = (

    (avg_rating * 20 * 0.5)

    +

    (positive_ratio * 0.4)

    +

    (min(review_volume, 100) * 0.1)

)

confidence_score = min(
    round(confidence_score, 2),
    100
)


# -----------------------------------
# RECOMMENDATION LOGIC
# -----------------------------------

if confidence_score >= 80:

    recommendation = (
        "🟢 Highly Recommended"
    )

    recommendation_reason = (

        "Customers are highly satisfied "
        "with product quality, comfort "
        "and overall experience."
    )

elif confidence_score >= 65:

    recommendation = (
        "🟡 Recommended"
    )

    recommendation_reason = (

        "Most buyers had a positive "
        "experience with minor concerns."
    )

elif confidence_score >= 50:

    recommendation = (
        "🟠 Mixed Reviews"
    )

    recommendation_reason = (

        "Customer feedback is divided. "
        "Review product details carefully."
    )

else:

    recommendation = (
        "🔴 Not Recommended"
    )

    recommendation_reason = (

        "Many customers reported "
        "negative experiences."
    )



# -----------------------------------
# HERO CARD
# -----------------------------------

# -----------------------------------
# HERO CARD
# -----------------------------------

with st.container():

    st.markdown("---")

    st.subheader(
        "🧠 AI Shopping Recommendation"
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        st.markdown(
            f"""
            # {recommendation}

            ### Confidence Score:
            **{confidence_score}%**

            {recommendation_reason}
            """
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence_score}%"
        )

    st.markdown("---")


# -----------------------------------
# BUYER INSIGHT METRICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⭐ Avg Rating",
        round(avg_rating, 2)
    )

with col2:

    st.metric(
        "😊 Positive Reviews",
        f"{round(positive_ratio, 1)}%"
    )

with col3:

    st.metric(
        "😡 Negative Reviews",
        f"{round(negative_ratio, 1)}%"
    )






# -----------------------------------
# WORD CLOUD
# -----------------------------------

st.subheader("☁️ Review WordCloud")


all_reviews = " ".join(
    df["review_text"]
    .dropna()
    .astype(str)
)


wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(all_reviews)


fig, ax = plt.subplots(
    figsize=(12, 6)
)

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)


# -----------------------------------
# TOP PRODUCTS
# -----------------------------------

st.subheader("🛍️ Top Rated Products")


top_products = (
    df.groupby("product_name")[
        "rating"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)


top_product_fig = px.bar(
    top_products,
    x="product_name",
    y="rating",
    title="Top Rated Products"
)

st.plotly_chart(
    top_product_fig,
    use_container_width=True
)


# -----------------------------------
# BUYER INSIGHTS
# -----------------------------------

st.subheader("🧠 AI Buyer Insights")


positive_reviews = len(
    df[df["sentiment"] == "Positive"]
)

negative_reviews = len(
    df[df["sentiment"] == "Negative"]
)


if positive_reviews > negative_reviews:

    st.success(
        "Most customers are satisfied "
        "with the products."
    )

else:

    st.warning(
        "Products show mixed or "
        "negative customer feedback."
    )


# -----------------------------------
# COMMON REVIEW TERMS
# -----------------------------------

review_text = " ".join(
    df["review_text"]
    .dropna()
    .astype(str)
    .tolist()
).lower()


keywords = [
    "quality",
    "fabric",
    "fit",
    "size",
    "comfortable",
    "delivery",
    "color",
    "soft"
]


keyword_counts = {}

for keyword in keywords:

    keyword_counts[keyword] = (
        review_text.count(keyword)
    )


keyword_df = pd.DataFrame({

    "Keyword": keyword_counts.keys(),

    "Mentions": keyword_counts.values()
})


keyword_fig = px.bar(
    keyword_df,
    x="Keyword",
    y="Mentions",
    title="Common Customer Discussion Topics"
)

st.plotly_chart(
    keyword_fig,
    use_container_width=True
)


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Built by DAIZY using Selenium + Streamlit + NLP"
)