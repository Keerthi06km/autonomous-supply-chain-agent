# Autonomous Supply Chain Decision System using Agentic AI

## Overview

The **Autonomous Supply Chain Decision System** is an Agentic AI-based system designed to automate supply-chain decisions such as inventory monitoring, supplier selection, and reorder decisions.

The system uses multiple specialized agents coordinated through **LangGraph**. Each agent performs a specific task, while the workflow maintains the execution state and routes the task based on inventory conditions. The system also includes **episodic memory** to store previous supply-chain decisions and an **evaluation agent** to verify whether a generated decision is valid.

---

## Problem Statement

Traditional supply-chain systems often require human intervention to monitor inventory, identify suppliers, and decide when and how much stock should be reordered.

This project aims to develop an autonomous decision-making system that can analyze inventory conditions, select an appropriate supplier, generate a reorder decision, evaluate the decision, and store the resulting experience for future use.

---

## Objectives

- Monitor product inventory levels automatically.
- Identify products that require reordering.
- Select suitable suppliers based on reliability and delivery time.
- Determine an appropriate reorder quantity.
- Evaluate generated supply-chain decisions.
- Maintain execution state using LangGraph.
- Store previous decisions using episodic memory.
- Demonstrate planning and multi-agent coordination.

---

## System Architecture

```text
                         User / Request
                              |
                              v
                       +--------------+
                       |    Planner   |
                       |     Agent    |
                       +------+-------+
                              |
                              v
                       +--------------+
                       |  Inventory   |
                       |     Agent    |
                       +------+-------+
                              |
                       Stock Sufficient?
                         /          \
                       YES           NO
                        |             |
                        v             v
                  +----------+   +--------------+
                  | No Action|   |   Supplier   |
                  |          |   |     Agent    |
                  +----+-----+   +------+-------+
                       |                |
                       |                v
                       |        +--------------+
                       |        |   Decision   |
                       |        |     Agent    |
                       |        +------+-------+
                       |               |
                       |               v
                       |        +--------------+
                       |        | Evaluation   |
                       |        |     Agent    |
                       |        +------+-------+
                       |               |
                       +-------+-------+
                               |
                               v
                       +---------------+
                       |    Episodic   |
                       |     Memory    |
                       +-------+-------+
                               |
                               v
                              END
```

---

## Agents

### 1. Planner Agent

Creates an execution plan for the requested product.

Example plan:

```text
check_inventory
evaluate_inventory_status
find_supplier
make_reorder_decision
```

### 2. Inventory Agent

Reads product information and determines whether the current inventory requires reordering.

It considers:

- Current stock
- Reorder level
- Daily demand
- Estimated remaining days of stock

### 3. Supplier Agent

Identifies available suppliers for the product and calculates a supplier score using reliability and delivery time.

### 4. Decision Agent

Generates the final supply-chain decision.

For example:

```text
Decision: REORDER
Product: Laptop
Supplier: QuickTech
Order Quantity: 50
```

### 5. Evaluation Agent

Evaluates the generated decision using multiple checks, including:

- Whether inventory requires a reorder
- Whether a valid supplier exists
- Whether order quantity is valid
- Supplier reliability
- Delivery time

The decision can be classified as:

```text
APPROVED
```

or

```text
REQUIRES_REVIEW
```

### 6. Episodic Memory

Stores previous supply-chain decisions.

Example:

```json
{
  "product_id": "P001",
  "decision": "REORDER",
  "supplier": "QuickTech",
  "order_quantity": 50
}
```

This provides the foundation for future experience-based decision making.

---

## Workflow

The current workflow is implemented using **LangGraph**.

```text
Planner
   |
   v
Inventory
   |
   +---- Stock sufficient ----> No Action
   |                                |
   |                                v
   |                              Memory
   |
   +---- Reorder required ----> Supplier
                                  |
                                  v
                               Decision
                                  |
                                  v
                              Evaluation
                                  |
                                  v
                                Memory
                                  |
                                  v
                                 END
```

---

## Technologies Used

- **Python** — Core programming language
- **LangGraph** — Agent workflow and state orchestration
- **LangChain** — Agentic AI framework support
- **Pandas** — CSV data processing
- **JSON** — Episodic memory storage
- **Virtual Environment (venv)** — Dependency isolation

---

## Project Structure

```text
autonomous-supply-chain-agent/
│
├── agents/
│   ├── inventory_agent.py
│   ├── supplier_agent.py
│   ├── decision_agent.py
│   ├── planner_agent.py
│   ├── evaluation_agent.py
│   └── workflow.py
│
├── data/
│   ├── products.csv
│   └── suppliers.csv
│
├── memory/
│   ├── __init__.py
│   ├── memory_store.py
│   └── episodic_memory.json
│
├── api/
│
├── utils/
│
├── tests/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Sample Scenario

Consider product `P001` (Laptop).

```text
Current Stock = 20
Reorder Level = 50
Daily Demand = 10
```

Since:

```text
20 < 50
```

the system identifies that a reorder is required.

The Supplier Agent evaluates the available suppliers and selects:

```text
Supplier: QuickTech
Reliability: 98%
Delivery: 3 days
```

The Decision Agent recommends:

```text
Decision: REORDER
Order Quantity: 50
```

The Evaluation Agent then verifies the decision and returns:

```text
Evaluation: APPROVED
```

Finally, the decision is stored in episodic memory.

---

## Example Output

```text
===== EXECUTION PLAN =====
['check_inventory',
 'evaluate_inventory_status',
 'find_supplier',
 'make_reorder_decision']

===== INVENTORY RESULT =====
{
    'status': 'reorder_required',
    'product_id': 'P001',
    'product_name': 'Laptop',
    'current_stock': 20,
    'reorder_level': 50,
    'daily_demand': 10,
    'days_remaining': 2.0
}

===== SUPPLIER RESULT =====
{
    'status': 'supplier_found',
    'supplier_id': 'S003',
    'supplier_name': 'QuickTech',
    'price': 46000.0,
    'delivery_days': 3,
    'reliability': 0.98,
    'score': 92.0
}

===== FINAL DECISION =====
{
    'decision': 'REORDER',
    'product': 'Laptop',
    'supplier': 'QuickTech',
    'order_quantity': 50
}

===== EVALUATION RESULT =====
{
    'evaluation': 'APPROVED',
    'valid': True
}
```

---

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install langgraph langchain langchain-openai python-dotenv pandas
```

---

## Running the Project

Make sure the virtual environment is activated:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run:

```powershell
python main.py
```

The product can be changed in `main.py`.

For example:

```python
"product_id": "P001"
```

or:

```python
"product_id": "P002"
```

---

## Current Implementation Status

| Component              | Status    |
| ---------------------- | --------- |
| Project setup          | Completed |
| Product dataset        | Completed |
| Supplier dataset       | Completed |
| Inventory Agent        | Completed |
| Supplier Agent         | Completed |
| Decision Agent         | Completed |
| Planner Agent          | Completed |
| LangGraph workflow     | Completed |
| Conditional routing    | Completed |
| Episodic memory        | Completed |
| Evaluation Agent       | Completed |
| Failure recovery       | Planned   |
| Re-planning            | Planned   |
| API layer              | Planned   |
| Frontend               | Planned   |
| Advanced LLM reasoning | Planned   |

---

## Future Enhancements

The next stages of development will focus on making the system more autonomous and production-oriented:

1. **Failure Recovery**
   - Detect unsuitable or unavailable suppliers.
   - Automatically search for alternatives.

2. **Re-planning**
   - Generate a new execution plan when the original plan fails.

3. **Improved Memory**
   - Retrieve relevant previous decisions.
   - Introduce working, episodic, and semantic memory.

4. **LLM-based Reasoning**
   - Introduce an LLM for more flexible planning and reasoning.

5. **FastAPI Backend**
   - Expose the agent system through REST APIs.

6. **Web Interface**
   - Provide a simple interface for supply-chain analysis.

7. **Database Integration**
   - Move from JSON-based memory to persistent database storage.

---

## Conclusion

The project demonstrates an Agentic AI approach to supply-chain decision making using multiple specialized agents, state-based workflow orchestration, conditional execution, decision evaluation, and episodic memory.

The current implementation establishes the foundation for a more autonomous system capable of planning, coordinating multiple agents, evaluating decisions, learning from previous experiences, and recovering from execution failures.
