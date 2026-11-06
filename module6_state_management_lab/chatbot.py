import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from state import AgentState


# Load environment variables
load_dotenv()


# Initialize the language model
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-5-mini"),
    temperature=0
)


# Define chatbot node
def chatbot(state: AgentState):

    # Get previous conversation messages
    messages = state["messages"]

    # Generate response using conversation history
    response = llm.invoke(messages)

    # Return new AI message
    return {
        "messages": [response]
    }


# Create graph builder
builder = StateGraph(AgentState)


# Register chatbot node
builder.add_node("chatbot", chatbot)


# Define graph execution flow
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


# Create in-memory checkpointer
checkpointer = InMemorySaver()


# Compile graph with checkpointing
graph = builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "employee-101"
    }
}

snapshot = graph.get_state(config)

print("Current State:")
print(snapshot.values)


print("\nCheckpoint History:")

for checkpoint in graph.get_state_history(config):

    print("\nCheckpoint ID:")
    print(checkpoint.config["configurable"]["checkpoint_id"])

    print("Messages:")
    print(checkpoint.values.get("messages", []))