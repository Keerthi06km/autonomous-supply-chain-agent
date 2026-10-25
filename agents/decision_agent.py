def decision_agent(inventory_result, supplier_result):

    if inventory_result["status"] != "reorder_required":
        return {
            "decision": "NO_ACTION",
            "reason": "Current inventory is sufficient."
        }

    product_name = inventory_result["product_name"]
    current_stock = inventory_result["current_stock"]
    daily_demand = inventory_result["daily_demand"]

    # Maintain approximately 7 days of stock
    target_stock = daily_demand * 7
    order_quantity = target_stock - current_stock

    if order_quantity < 0:
        order_quantity = 0

    return {
        "decision": "REORDER",
        "product": product_name,
        "supplier": supplier_result["supplier_name"],
        "order_quantity": int(order_quantity),
        "price_per_unit": supplier_result["price"],
        "delivery_days": supplier_result["delivery_days"],
        "reason": (
            f"Stock is low. Current stock is {current_stock} units "
            f"while daily demand is {daily_demand} units."
        )
    }