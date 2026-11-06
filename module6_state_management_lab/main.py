from chatbot import graph


# Create a conversation thread
thread_id = "employee-101"


# Configuration for the conversation
config = {
    "configurable": {
        "thread_id": thread_id
    }
}


print("=" * 60)
print("       LANGGRAPH CONVERSATIONAL AI ASSISTANT")
print("=" * 60)

print("\nWelcome to the IT Support Assistant!")

print("\nCommands:")
print("  /state  - View current conversation state")
print("  /new    - Start a new conversation")
print("  /exit   - Exit application")

print("\nStart chatting with the assistant.")


while True:

    user_input = input("\nYou: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "/exit":

        print("\nAssistant: Goodbye!")
        break

    elif user_input.lower() == "/new":

        thread_id = input(
            "Enter a new conversation ID: "
        ).strip()

        if not thread_id:
            print("Please provide a valid conversation ID.")
            continue

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        print(
            f"\nStarted new conversation: {thread_id}"
        )

        continue

    elif user_input.lower() == "/state":

        snapshot = graph.get_state(config)

        print("\n--- CURRENT GRAPH STATE ---")

        if snapshot.values:

            for message in snapshot.values.get(
                "messages", []
            ):

                print(
                    f"\n{message.type.upper()}: "
                    f"{message.content}"
                )

        else:

            print("No saved conversation state.")

        continue

    try:

        result = graph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config
        )

        # Get the latest AI response
        response = result["messages"][-1]

        print("\nAssistant:")
        print(response.content)

    except Exception as e:

        print("\nAn error occurred:")
        print(str(e))