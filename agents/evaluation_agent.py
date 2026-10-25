def evaluation_agent(inventory_result, supplier_result, decision_result):
    """
    Evaluates whether the supply-chain decision is valid.
    """

    checks = []

    # Check 1: Inventory
    if inventory_result.get("status") == "reorder_required":
        checks.append("Inventory requires reorder")
    else:
        checks.append("Inventory does not require reorder")

    # Check 2: Supplier
    if supplier_result.get("status") == "supplier_found":
        checks.append("Valid supplier found")
    else:
        checks.append("No valid supplier found")

    # Check 3: Order quantity
    order_quantity = decision_result.get("order_quantity", 0)

    if order_quantity > 0:
        checks.append("Order quantity is valid")
    else:
        checks.append("Order quantity is invalid")

    # Check 4: Supplier reliability
    reliability = supplier_result.get("reliability", 0)

    if reliability >= 0.90:
        checks.append("Supplier reliability is acceptable")
    else:
        checks.append("Supplier reliability is low")

    # Check 5: Delivery time
    delivery_days = supplier_result.get("delivery_days", 999)

    if delivery_days <= 7:
        checks.append("Delivery time is acceptable")
    else:
        checks.append("Delivery time is too long")

    # Overall evaluation
    valid = (
        inventory_result.get("status") == "reorder_required"
        and supplier_result.get("status") == "supplier_found"
        and order_quantity > 0
        and reliability >= 0.90
        and delivery_days <= 7
    )

    if valid:
        evaluation = "APPROVED"
    else:
        evaluation = "REQUIRES_REVIEW"

    return {
        "evaluation": evaluation,
        "valid": valid,
        "checks": checks
    }