import pandas as pd


def inventory_agent(product_id):
    products = pd.read_csv("data/products.csv")

    product = products[products["product_id"] == product_id]

    if product.empty:
        return {
            "status": "error",
            "message": "Product not found"
        }

    product = product.iloc[0]

    current_stock = product["current_stock"]
    reorder_level = product["reorder_level"]
    daily_demand = product["daily_demand"]

    if current_stock <= reorder_level:
        days_remaining = current_stock / daily_demand

        return {
            "status": "reorder_required",
            "product_id": product_id,
            "product_name": product["product_name"],
            "current_stock": int(current_stock),
            "reorder_level": int(reorder_level),
            "daily_demand": int(daily_demand),
            "days_remaining": float(round(days_remaining, 2))
        }

    return {
        "status": "stock_sufficient",
        "product_id": product_id,
        "product_name": product["product_name"],
        "current_stock": int(current_stock),
        "reorder_level": int(reorder_level)
    }