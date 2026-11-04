import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Step 1: Load environment variables
load_dotenv()

# Step 2: Initialize LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-5-mini"),
    temperature=0
)

# Step 3: Create prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an experienced executive assistant.
        Summarize emails for senior management.
        Focus on decisions, risks, deadlines and responsibilities.

        Analyze the email and provide:

        1. EMAIL PURPOSE:
        Explain why the email was sent.

        2. IMPORTANT DEADLINE:
        List only the important deaflines.

        3. ACTION ITEMS:
        Identify what the recipient needs to do.

        4. SUMMARY:
        Provide a short summary in 3-4 sentences.

        Use only information available in the email.
        Do not invent missing details.
        """
    ),
    (
        "human",
        "Summarize the following email:\n\n{email}"
    )
])

# Step 4: Create output parser
parser = StrOutputParser()

# Step 5: Build LangChain
email_chain = prompt | llm | parser


# Step 6: Execute application
def summarize_email(email):

    result = email_chain.invoke({
        "email": email
    })

    return result


# Step 7: Command-line application
def main():

    print("=" * 55)
    print("          AI EMAIL SUMMARIZER")
    print("             Using LangChain")
    print("=" * 55)

    print("\nPaste your email below.")
    print("Type END on a new line when finished.")

    email_lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        email_lines.append(line)

    email = "\n".join(email_lines)

    if not email.strip():
        print("Please enter an email.")
        return

    print("\nSummarizing email...\n")

    try:

        result = summarize_email(email)

        print("=" * 55)
        print("             EMAIL SUMMARY")
        print("=" * 55)

        print(result)

        print("=" * 55)

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()

