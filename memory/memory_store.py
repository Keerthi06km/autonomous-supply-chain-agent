import json
from pathlib import Path


MEMORY_FILE = Path("memory/episodic_memory.json")


def save_memory(memory):
    """
    Save an agent experience to episodic memory.
    """

    MEMORY_FILE.parent.mkdir(exist_ok=True)

    memories = []

    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as file:
            memories = json.load(file)

    memories.append(memory)

    with open(MEMORY_FILE, "w") as file:
        json.dump(memories, file, indent=4)


def load_memory():
    """
    Load all previous agent experiences.
    """

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def get_product_history(product_id):
    """
    Retrieve previous decisions for a specific product.
    """

    memories = load_memory()

    return [
        memory
        for memory in memories
        if memory.get("product_id") == product_id
    ]