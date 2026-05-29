# 🛍️ Myntra Review Scraper & AI Shopping Intelligence

An end-to-end AI-powered shopping intelligence platform built using:

- Selenium
- Streamlit
- NLP
- Plotly
- Python

This project scrapes product reviews from Myntra and generates intelligent buyer insights using sentiment analysis, review mining, visual analytics, and AI-driven recommendation logic.

---

# 🚀 Features

## ✅ Smart Product Search

Users can search products directly using keywords like:

- cotton tshirts
- jeans
- women tops
- oversized hoodies

The scraper automatically:
- navigates Myntra
- searches products
- opens product pages
- extracts reviews

---

# ✅ Dynamic Product Scraping

The scraper handles:

- Infinite scrolling
- Dynamic loading
- Multiple products
- Pagination
- Product metadata extraction

---

# ✅ Review Extraction

Extracts:

- Review text
- Ratings
- Username
- Review date
- Product rating
- Product image
- Brand name
- Product price
- Discount
- Product URL

---

# ✅ AI-Powered Analytics Dashboard

Built with Streamlit.

Dashboard includes:

## 🧠 AI Recommendation Engine

Provides:
- Highly Recommended
- Recommended
- Mixed Reviews
- Not Recommended

based on:
- review sentiment
- average ratings
- review volume
- buyer confidence

---

# ✅ Sentiment Analysis

Classifies reviews into:
- Positive
- Neutral
- Negative

using NLP.

---

# ✅ Buyer Intelligence

Answers practical buyer questions like:

- Is the fabric soft?
- Does it fit properly?
- Is it worth the money?
- Are customers satisfied?

---

# ✅ Pros vs Cons Extraction

Automatically extracts:

### Customers Loved
- soft fabric
- comfortable fit
- premium quality

### Common Complaints
- loose fitting
- thin material
- quality issues

---

# ✅ Fit Intelligence

Detects:
- Oversized fit
- Tight fit
- Perfect fit

from customer reviews.

---

# ✅ Visual Analytics

Interactive charts built with Plotly:

- Rating distribution
- Sentiment breakdown
- Top brands
- Top products
- Fabric insights
- Keyword intelligence
- Product health score

---

# ✅ WordCloud

Generates review word clouds from customer feedback.

---

# 🏗️ Project Structure

```bash
myntra-review-scrapper/
│
├── artifacts/
│
├── logs/
│
├── notebooks/
│
├── src/
│   └── myntra_review/
│       ├── components/
│       │   ├── scraper.py
│       │   ├── search_handler.py
│       │   ├── product_extractor.py
│       │   ├── review_extractor.py
│       │
│       ├── config/
│       │   └── config.py
│       │
│       ├── pipeline/
│       │
│       └── utils/
│           ├── logger.py
│           ├── exception.py
│           ├── browser.py
│
├── streamlit_app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Scraper.py
│       └── 2_Analysis.py
│
├── .env
├── requirements.txt
├── app.py
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd myntra-review-scrapper
```

---

# Create Virtual Environment

```bash
conda create -p venv python=3.11 -y
```

Activate environment:

```bash
conda activate venv/
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Setup `.env`

Create a `.env` file:

```env
HEADLESS=False
MAX_PRODUCTS=5
MAX_REVIEWS_PER_PRODUCT=50
SCROLL_PAUSE_TIME=2
```

---

# ▶️ Run Streamlit App

```bash
streamlit run streamlit_app/Home.py
```

---

# 📊 Workflow

## Step 1
Open Scraper Page

## Step 2
Enter product search query

Example:

```text
cotton tshirts
```

## Step 3
Select number of products

## Step 4
Start scraping

## Step 5
Open Analytics Page

Dashboard automatically generates:
- AI recommendations
- Sentiment analysis
- Product intelligence
- Buyer insights

---

# 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Selenium | Dynamic web scraping |
| Streamlit | Dashboard UI |
| Plotly | Interactive charts |
| TextBlob | NLP sentiment analysis |
| Pandas | Data processing |
| WordCloud | Keyword visualization |
| Python | Core backend |

---

# 🔥 Current Highlights

✅ Modular architecture  
✅ Production-style folder structure  
✅ Logging system  
✅ Exception handling  
✅ Environment variables  
✅ Dynamic scraping  
✅ AI analytics  
✅ Interactive dashboard  
✅ Export functionality  

---

# 🚀 Future Improvements

Planned upgrades:

- OpenAI review summarization
- Fake review detection
- Competitor comparison
- Recommendation engine
- Review clustering
- AI chatbot assistant
- Outfit intelligence
- Personalized shopping insights

---

# 👨‍💻 Author

Built as an AI + Data Engineering + NLP portfolio project.

---

# ⭐ Final Goal

Transform this project from:

```text
simple review scraper
```

into:

```text
AI Shopping Intelligence Platform
```