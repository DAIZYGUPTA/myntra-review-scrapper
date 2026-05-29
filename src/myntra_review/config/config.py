from dotenv import load_dotenv
import os

load_dotenv()
# -----------------------------------
# SELENIUM SETTINGS
# -----------------------------------

HEADLESS = os.getenv("HEADLESS")

# -----------------------------------
# PRODUCT SETTINGS
# -----------------------------------

MAX_PRODUCTS = int(
    os.getenv("MAX_PRODUCTS")
)

# -----------------------------------
# SCROLL SETTINGS
# -----------------------------------

SCROLL_PAUSE_TIME = int(
    os.getenv("SCROLL_PAUSE_TIME")
)

# -----------------------------------
# REVIEW SETTINGS
# -----------------------------------

MAX_REVIEWS_PER_PRODUCT = int(
    os.getenv("MAX_REVIEWS_PER_PRODUCT")
)