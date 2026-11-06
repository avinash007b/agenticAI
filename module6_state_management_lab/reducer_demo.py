from typing import Annotated
from typing_extensions import TypedDict

from operator import add

from langgraph.graph import StateGraph, START, END


# Define state
class State(TypedDict):
    findings: Annotated[list[str], add]


# First node
def first_finding(state):

    return {
        "findings": [
            "Payment service is unavailable"
        ]
    }


# Second node
def second_finding(state):

    return {
        "findings": [
            "Database connection failed"
        ]
    }


# Build graph
builder = StateGraph(State)

builder.add_node("first", first_finding)
builder.add_node("second", second_finding)

builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

graph = builder.compile()


# Execute graph
result = graph.invoke({
    "findings": []
})


print("\nFinal Findings:")

for finding in result["findings"]:
    print("-", finding)