def planner_agent(product_id):
    """
    Creates an execution plan for a supply-chain decision.
    """

    return {
        "product_id": product_id,
        "plan": [
            "check_inventory",
            "evaluate_inventory_status",
            "find_supplier",
            "make_reorder_decision"
        ]
    }