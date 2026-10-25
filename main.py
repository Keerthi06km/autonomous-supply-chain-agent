from agents.workflow import app


# ==========================================
# Initial State
# ==========================================

initial_state = {
    "product_id": "P001",
    "plan": [],
    "current_step": "",
    "inventory_result": {},
    "supplier_result": {},
    "decision_result": {},
    "evaluation_result": {}
}


# ==========================================
# Run Agent Workflow
# ==========================================

result = app.invoke(initial_state)


# ==========================================
# Display Results
# ==========================================

print("\n==========================================")
print("       AUTONOMOUS SUPPLY CHAIN AGENT")
print("==========================================")


print("\n===== EXECUTION PLAN =====")
print(result["plan"])


print("\n===== CURRENT STEP =====")
print(result["current_step"])


print("\n===== INVENTORY RESULT =====")
print(result["inventory_result"])


print("\n===== SUPPLIER RESULT =====")
print(result["supplier_result"])


print("\n===== FINAL DECISION =====")
print(result["decision_result"])


print("\n===== EVALUATION RESULT =====")
print(result["evaluation_result"])


print("\n==========================================")
print("             WORKFLOW COMPLETE")
print("==========================================")