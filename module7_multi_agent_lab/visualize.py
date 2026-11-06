from graph import graph


diagram = graph.get_graph().draw_mermaid()

print(diagram)

with open(
    "multi_agent_workflow.mmd",
    "w",
    encoding="utf-8"
) as file:

    file.write(diagram)

print("\nGraph diagram saved successfully.")