import pandas as pd
import os

def load_all_datasets():
    # Ambil direktori absolut dari file ini (utils/load_data.py)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_DIR = os.path.join(BASE_DIR, "dataset")

    def load(file_name):
        return pd.read_csv(os.path.join(DATASET_DIR, file_name))
    
    def load_xlsx(file_name):
        return pd.read_excel(os.path.join(DATASET_DIR, file_name))

    closed_deals = load("closed_deals_dataset.csv")
    customers = load("customers_dataset.csv")
    geolocation = load("geolocation_dataset.csv")
    marketing_leads = load("marketing_qualified_leads_dataset.csv")
    order_items = load("order_items_dataset.csv")
    order_payments = load("order_payments_dataset.csv")
    order_reviews = load("order_reviews_dataset.csv")
    orders = load("orders_dataset.csv")
    product_category_translation = load("product_category_name_translation.csv")
    products = load("products_dataset.csv")
    sellers = load("sellers_dataset.csv")
    topics = load_xlsx("review_translated_topic.xlsx")

    return {
        "closed_deals": closed_deals,
        "customers": customers,
        "geolocation": geolocation,
        "marketing_leads": marketing_leads,
        "order_items": order_items,
        "order_payments": order_payments,
        "order_reviews": order_reviews,
        "orders": orders,
        "product_category_translation": product_category_translation,
        "products": products,
        "sellers": sellers,
        "topics":topics
    }
