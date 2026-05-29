import sys
from pathlib import Path

# -----------------------------------
# PROJECT ROOT
# -----------------------------------

project_root = (
    Path(__file__).resolve().parents[2]
)

sys.path.append(str(project_root))


# -----------------------------------
# IMPORTS
# -----------------------------------

import streamlit as st

import pandas as pd

import numpy as np

import plotly.express as px

import plotly.graph_objects as go

from textblob import TextBlob

from wordcloud import WordCloud

import matplotlib.pyplot as plt


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Shopping Intelligence",
    page_icon="🧠",
    layout="wide"
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title(
    "🧠 AI-Powered Myntra Shopping Intelligence"
)

st.markdown(
    """
    Smart buyer intelligence dashboard
    powered by NLP + Selenium + Streamlit.
    """
)


# -----------------------------------
# CHECK SESSION STATE
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
# DATA PREVIEW
# -----------------------------------

st.subheader(
    "📄 Dataset Preview"
)

st.dataframe(
    df.head(),
    use_container_width=True
)


# -----------------------------------
# SENTIMENT FUNCTION
# -----------------------------------

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


# -----------------------------------
# APPLY SENTIMENT
# -----------------------------------

df["sentiment"] = df[
    "review_text"
].apply(get_sentiment)


# -----------------------------------
# AI RECOMMENDATION ENGINE
# -----------------------------------

st.subheader(
    "🧠 AI Shopping Recommendation"
)


avg_rating = df["rating"].mean()

review_volume = len(df)


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
        "with quality, comfort and value."
    )

elif confidence_score >= 65:

    recommendation = (
        "🟡 Recommended"
    )

    recommendation_reason = (
        "Most buyers had positive "
        "experiences with minor concerns."
    )

elif confidence_score >= 50:

    recommendation = (
        "🟠 Mixed Reviews"
    )

    recommendation_reason = (
        "Customer opinions are divided."
    )

else:

    recommendation = (
        "🔴 Not Recommended"
    )

    recommendation_reason = (
        "Many users reported "
        "negative experiences."
    )


# -----------------------------------
# HERO SECTION
# -----------------------------------

with st.container():

    st.markdown("---")

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
# KPI METRICS
# -----------------------------------

st.subheader(
    "📌 Key Metrics"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Reviews",
        len(df)
    )

with col2:

    st.metric(
        "Average Rating",
        round(avg_rating, 2)
    )

with col3:

    st.metric(
        "Positive Reviews",
        f"{round(positive_ratio,1)}%"
    )

with col4:

    st.metric(
        "Brands",
        df["brand"].nunique()
    )


# -----------------------------------
# COMBINE ALL REVIEWS
# -----------------------------------

all_reviews = " ".join(

    df["review_text"]
    .dropna()
    .astype(str)
    .tolist()

).lower()


# -----------------------------------
# PROS VS CONS ENGINE
# -----------------------------------

st.subheader(
    "⚖️ Pros vs Cons Analysis"
)


positive_keywords = [

    "soft",
    "comfortable",
    "good",
    "great",
    "perfect",
    "nice",
    "quality",
    "fit",
    "love",
    "awesome",
    "premium",
    "worth"

]


negative_keywords = [

    "bad",
    "poor",
    "tight",
    "loose",
    "worst",
    "fade",
    "small",
    "large",
    "thin",
    "issue",
    "disappointed",
    "cheap"

]


pros = []

cons = []


# -----------------------------------
# EXTRACT PROS
# -----------------------------------

for keyword in positive_keywords:

    count = all_reviews.count(keyword)

    if count > 0:

        pros.append(
            f"{keyword.title()} ({count})"
        )


# -----------------------------------
# EXTRACT CONS
# -----------------------------------

for keyword in negative_keywords:

    count = all_reviews.count(keyword)

    if count > 0:

        cons.append(
            f"{keyword.title()} ({count})"
        )


# -----------------------------------
# DISPLAY
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    st.success(
        "✅ What Customers Loved"
    )

    if pros:

        for item in pros[:10]:

            st.write(f"• {item}")

    else:

        st.write(
            "No strong positives found."
        )


with col2:

    st.error(
        "❌ Common Complaints"
    )

    if cons:

        for item in cons[:10]:

            st.write(f"• {item}")

    else:

        st.write(
            "No major complaints found."
        )


# -----------------------------------
# FIT ANALYSIS
# -----------------------------------

st.subheader(
    "📏 Fit Intelligence"
)


fit_keywords = {

    "Oversized": [
        "oversized",
        "loose"
    ],

    "Perfect Fit": [
        "perfect fit",
        "true size",
        "comfortable fit"
    ],

    "Tight Fit": [
        "tight",
        "small"
    ]
}


fit_results = {}


for category, words in fit_keywords.items():

    total = 0

    for word in words:

        total += all_reviews.count(word)

    fit_results[category] = total


fit_df = pd.DataFrame({

    "Fit": fit_results.keys(),

    "Mentions": fit_results.values()
})


fit_fig = px.bar(

    fit_df,

    x="Fit",

    y="Mentions",

    color="Fit",

    text="Mentions",

    title="Customer Fit Feedback",

    color_discrete_map={

        "Oversized": "orange",

        "Perfect Fit": "green",

        "Tight Fit": "red"
    }
)

fit_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fit_fig,
    use_container_width=True
)


# -----------------------------------
# FABRIC & QUALITY ANALYSIS
# -----------------------------------

st.subheader(
    "🧵 Fabric & Quality Insights"
)


fabric_keywords = [

    "soft",
    "fabric",
    "quality",
    "cotton",
    "comfortable",
    "material",
    "breathable",
    "smooth",
    "premium"

]


fabric_counts = {}


for keyword in fabric_keywords:

    fabric_counts[keyword] = (
        all_reviews.count(keyword)
    )


fabric_df = pd.DataFrame({

    "Keyword": fabric_counts.keys(),

    "Mentions": fabric_counts.values()
})


fabric_fig = px.bar(

    fabric_df,

    x="Keyword",

    y="Mentions",

    color="Mentions",

    text="Mentions",

    title="Fabric Discussion Frequency"
)

fabric_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fabric_fig,
    use_container_width=True
)

# -----------------------------------
# RATING DISTRIBUTION
# -----------------------------------

st.subheader(
    "⭐ Rating Distribution"
)


rating_counts = (

    df["rating"]
    .value_counts()
    .sort_index()
    .reset_index()

)

rating_counts.columns = [

    "Rating",
    "Count"
]


# -----------------------------------
# COLOR MAPPING
# -----------------------------------

rating_color_map = {

    1: "red",
    2: "orange",
    3: "yellow",
    4: "lightgreen",
    5: "green"
}


rating_fig = px.bar(

    rating_counts,

    x="Rating",

    y="Count",

    color="Rating",

    text="Count",

    title="Customer Rating Distribution",

    color_discrete_map=rating_color_map
)

rating_fig.update_traces(
    textposition="outside"
)

rating_fig.update_layout(
    xaxis_title="Stars",
    yaxis_title="Review Count"
)

st.plotly_chart(
    rating_fig,
    use_container_width=True
)


# -----------------------------------
# SENTIMENT ANALYSIS
# -----------------------------------

st.subheader(
    "😊 Sentiment Analysis"
)


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

    title="Review Sentiment Breakdown",

    color="Sentiment",

    color_discrete_map={

        "Positive": "green",

        "Neutral": "yellow",

        "Negative": "red"
    }
)

st.plotly_chart(
    sentiment_fig,
    use_container_width=True
)


# -----------------------------------
# TOP BRANDS
# -----------------------------------

st.subheader(
    "🏷️ Most Reviewed Brands"
)


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

    color="Reviews",

    text="Reviews",

    title="Top Reviewed Brands"
)

brand_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    brand_fig,
    use_container_width=True
)


# -----------------------------------
# TOP PRODUCTS
# -----------------------------------

st.subheader(
    "🛍️ Top Rated Products"
)


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


product_fig = px.bar(

    top_products,

    x="product_name",

    y="rating",

    color="rating",

    text="rating",

    title="Best Rated Products"
)

product_fig.update_traces(
    textposition="outside"
)

product_fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Average Rating"
)

st.plotly_chart(
    product_fig,
    use_container_width=True
)


# -----------------------------------
# COMMON DISCUSSION TOPICS
# -----------------------------------

st.subheader(
    "💬 Customer Discussion Topics"
)


keywords = [

    "quality",
    "fabric",
    "fit",
    "size",
    "comfortable",
    "delivery",
    "color",
    "soft",
    "material",
    "price"

]


keyword_counts = {}


for keyword in keywords:

    keyword_counts[keyword] = (
        all_reviews.count(keyword)
    )


keyword_df = pd.DataFrame({

    "Keyword": keyword_counts.keys(),

    "Mentions": keyword_counts.values()
})


keyword_fig = px.bar(

    keyword_df,

    x="Keyword",

    y="Mentions",

    color="Mentions",

    text="Mentions",

    title="Most Discussed Topics"
)

keyword_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    keyword_fig,
    use_container_width=True
)




# -----------------------------------
# WORD CLOUD
# -----------------------------------

st.subheader(
    "☁️ Review WordCloud"
)


wordcloud = WordCloud(

    width=1400,

    height=600,

    background_color="white"

).generate(all_reviews)


fig, ax = plt.subplots(
    figsize=(16, 7)
)

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)


# -----------------------------------
# BUYER INTELLIGENCE
# -----------------------------------

st.subheader(
    "🛒 Buyer Intelligence"
)


if positive_ratio >= 75:

    st.success(
        """
        Most customers strongly recommend
        these products.

        Buyers are especially happy with:
        - comfort
        - fabric quality
        - overall fit
        """
    )

elif positive_ratio >= 50:

    st.warning(
        """
        Products received mixed feedback.

        Buyers should carefully inspect:
        - fitting
        - size consistency
        - fabric expectations
        """
    )

else:

    st.error(
        """
        Many customers reported
        dissatisfaction.

        Buyers should proceed carefully.
        """
    )


# -----------------------------------
# PRODUCT HEALTH SCORE
# -----------------------------------

st.subheader(
    "📈 Product Health Score"
)


health_score = round(

    (

        avg_rating * 20 * 0.5

        +

        positive_ratio * 0.5

    ),

    2
)


health_fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=health_score,

        title={
            "text": "Overall Product Health"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "darkblue"
            },

            "steps": [

                {
                    "range": [0, 40],
                    "color": "red"
                },

                {
                    "range": [40, 70],
                    "color": "yellow"
                },

                {
                    "range": [70, 100],
                    "color": "green"
                }
            ]
        }
    )
)

st.plotly_chart(
    health_fig,
    use_container_width=True
)


# -----------------------------------
# SMART BUYER QUESTIONS
# -----------------------------------

st.subheader(
    "❓ Questions Buyers Usually Ask"
)


questions = [

    "Is the fabric soft and comfortable?",

    "Does the product fit true to size?",

    "Do customers regret buying it?",

    "Is the material premium quality?",

    "Are there delivery or quality complaints?",

    "Is this product worth the price?"
]


for question in questions:

    st.write(f"• {question}")


# -----------------------------------
# SMART ANSWERS
# -----------------------------------

st.subheader(
    "🤖 AI Answers"
)


if all_reviews.count("soft") > 3:

    st.write(
        "✅ Customers frequently mention "
        "soft and comfortable fabric."
    )

if all_reviews.count("fit") > 3:

    st.write(
        "✅ Fit satisfaction appears "
        "strong among buyers."
    )

if all_reviews.count("quality") > 3:

    st.write(
        "✅ Product quality is discussed "
        "positively in reviews."
    )

if negative_ratio > 25:

    st.write(
        "⚠️ Some users reported "
        "negative experiences."
    )


# -----------------------------------
# RAW DATA EXPANDER
# -----------------------------------

with st.expander(
    "🔍 View Full Dataset"
):

    st.dataframe(
        df,
        use_container_width=True
    )


# -----------------------------------
# DOWNLOAD BUTTONS
# -----------------------------------

st.subheader(
    "⬇️ Download Dataset"
)


csv = df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="Download CSV",

    data=csv,

    file_name="myntra_reviews.csv",

    mime="text/csv"
)


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    """
    Built by DAIZY using

    Selenium + NLP + Streamlit + Plotly
    """
)



