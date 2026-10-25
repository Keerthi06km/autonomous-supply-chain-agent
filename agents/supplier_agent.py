import pandas as pd


def supplier_agent(product_id):
    suppliers = pd.read_csv("data/suppliers.csv")

    product_suppliers = suppliers[
        suppliers["product_id"] == product_id
    ]

    if product_suppliers.empty:
        return {
            "status": "error",
            "message": "No suppliers found"
        }

    # Rank suppliers using price, delivery time and reliability
    product_suppliers = product_suppliers.copy()

    product_suppliers["score"] = (
        product_suppliers["reliability"] * 100
        - product_suppliers["delivery_days"] * 2
    )

    best_supplier = product_suppliers.sort_values(
        by="score",
        ascending=False
    ).iloc[0]

    return {
        "status": "supplier_found",
        "supplier_id": best_supplier["supplier_id"],
        "supplier_name": best_supplier["supplier_name"],
        "price": float(best_supplier["price"]),
        "delivery_days": int(best_supplier["delivery_days"]),
        "reliability": float(best_supplier["reliability"]),
        "score": round(float(best_supplier["score"]), 2)
    }