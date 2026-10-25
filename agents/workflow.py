from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent
from agents.inventory_agent import inventory_agent
from agents.supplier_agent import supplier_agent
from agents.decision_agent import decision_agent
from agents.evaluation_agent import evaluation_agent

from memory.memory_store import save_memory


# ==========================================
# Supply Chain State
# ==========================================

class SupplyChainState(TypedDict):
    product_id: str
    plan: list
    current_step: str
    inventory_result: dict
    supplier_result: dict
    decision_result: dict
    evaluation_result: dict


# ==========================================
# Planner Node
# ==========================================

def planner_node(state: SupplyChainState):

    result = planner_agent(state["product_id"])

    return {
        "plan": result["plan"],
        "current_step": "check_inventory"
    }


# ==========================================
# Inventory Node
# ==========================================

def inventory_node(state: SupplyChainState):

    result = inventory_agent(state["product_id"])

    return {
        "inventory_result": result,
        "current_step": "evaluate_inventory_status"
    }


# ==========================================
# Inventory Conditional Check
# ==========================================

def check_inventory(state: SupplyChainState):

    if state["inventory_result"]["status"] == "reorder_required":
        return "supplier"

    return "no_action"


# ==========================================
# Supplier Node
# ==========================================

def supplier_node(state: SupplyChainState):

    result = supplier_agent(state["product_id"])

    return {
        "supplier_result": result,
        "current_step": "make_reorder_decision"
    }


# ==========================================
# Decision Node
# ==========================================

def decision_node(state: SupplyChainState):

    result = decision_agent(
        state["inventory_result"],
        state["supplier_result"]
    )

    return {
        "decision_result": result,
        "current_step": "evaluate_decision"
    }


# ==========================================
# Evaluation Node
# ==========================================

def evaluation_node(state: SupplyChainState):

    result = evaluation_agent(
        state["inventory_result"],
        state["supplier_result"],
        state["decision_result"]
    )

    return {
        "evaluation_result": result,
        "current_step": "save_memory"
    }


# ==========================================
# No Action Node
# ==========================================

def no_action_node(state: SupplyChainState):

    result = {
        "decision": "NO_ACTION",
        "reason": "Inventory level is sufficient."
    }

    return {
        "decision_result": result,
        "evaluation_result": {
            "evaluation": "NOT_REQUIRED",
            "valid": True,
            "checks": [
                "Inventory level is sufficient",
                "No reorder required"
            ]
        },
        "current_step": "save_memory"
    }


# ==========================================
# Memory Node
# ==========================================

def memory_node(state: SupplyChainState):

    decision = state["decision_result"]

    memory = {
        "product_id": state["product_id"],
        "decision": decision.get("decision"),
        "supplier": decision.get("supplier"),
        "order_quantity": decision.get("order_quantity")
    }

    save_memory(memory)

    return {
        "current_step": "completed"
    }


# ==========================================
# Build LangGraph
# ==========================================

graph = StateGraph(SupplyChainState)


# Add nodes
graph.add_node("planner", planner_node)
graph.add_node("inventory", inventory_node)
graph.add_node("supplier", supplier_node)
graph.add_node("decision", decision_node)
graph.add_node("evaluation", evaluation_node)
graph.add_node("no_action", no_action_node)
graph.add_node("memory", memory_node)


# Entry point
graph.set_entry_point("planner")


# Planner → Inventory
graph.add_edge("planner", "inventory")


# Inventory → Conditional Routing
graph.add_conditional_edges(
    "inventory",
    check_inventory,
    {
        "supplier": "supplier",
        "no_action": "no_action"
    }
)


# Supplier → Decision
graph.add_edge("supplier", "decision")


# Decision → Evaluation
graph.add_edge("decision", "evaluation")


# Evaluation → Memory
graph.add_edge("evaluation", "memory")


# No Action → Memory
graph.add_edge("no_action", "memory")


# Memory → End
graph.add_edge("memory", END)


# Compile workflow
app = graph.compile()