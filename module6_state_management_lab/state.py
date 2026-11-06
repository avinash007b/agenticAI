from langgraph.graph import MessagesState


class AgentState(MessagesState):
    issue_category: str