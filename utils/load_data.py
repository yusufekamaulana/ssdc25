import pandas as pd

def load_all_datasets():
    closed_deals = pd.read_csv("E-commerce/closed_deals_dataset.csv")
    customers = pd.read_csv("E-commerce/customers_dataset.csv")
    geolocation = pd.read_csv("E-commerce/geolocation_dataset.csv")
    marketing_leads = pd.read_csv("E-commerce/marketing_qualified_leads_dataset.csv")
    order_items = pd.read_csv("E-commerce/order_items_dataset.csv")
    order_payments = pd.read_csv("E-commerce/order_payments_dataset.csv")
    order_reviews = pd.read_csv("E-commerce/order_reviews_dataset.csv")
    orders = pd.read_csv("E-commerce/orders_dataset.csv")
    product_category_translation = pd.read_csv("E-commerce/product_category_name_translation.csv")
    products = pd.read_csv("E-commerce/products_dataset.csv")
    sellers = pd.read_csv("E-commerce/sellers_dataset.csv")
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
        "sellers": sellers
    }