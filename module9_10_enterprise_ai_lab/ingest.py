from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DB_DIRECTORY = "./chroma_db"

# ------------------------------------------------
# STEP 1: Create enterprise knowledge documents
# ------------------------------------------------

documents = [
    Document(
        page_content="""
        TechNova Refund Policy

        Customers can request a refund within 7 days
        of receiving their product.

        Products must be returned in their original
        condition with all accessories and packaging.

        Damaged products are eligible for a refund
        after verification by the support team.

        Refunds must be reviewed by an authorized
        support manager before processing.

        Refunds are normally processed within
        5 to 7 business days after approval.
        """,
        metadata={"source": "refund_policy"}
    ),

    Document(
        page_content="""
        TechNova Product Return Policy

        Customers can request a product return within
        7 days of delivery.

        The product must be unused and returned
        with original packaging.

        Products damaged during delivery should be
        reported to customer support.

        The support team must verify the damage
        before recommending a refund or replacement.
        """,
        metadata={"source": "return_policy"}
    ),

    Document(
        page_content="""
        TechNova Shipping Policy

        Standard delivery normally takes 3 to 5
        business days.

        Express delivery normally takes 1 to 2
        business days.

        Customers can contact support if an order
        has not been delivered within the expected
        delivery window.

        Delivery delays should be investigated
        before offering compensation.
        """,
        metadata={"source": "shipping_policy"}
    ),

    Document(
        page_content="""
        TechNova Payment Troubleshooting Guide

        If a payment fails, customers should first
        verify the payment method and available balance.

        A failed payment should not automatically
        result in a duplicate payment attempt.

        Payment transaction IDs should be collected
        for investigation.

        If the payment amount was deducted but the
        order was not confirmed, the support team
        should investigate the transaction status.

        Escalate unresolved payment issues to the
        payment operations team.
        """,
        metadata={"source": "payment_troubleshooting"}
    ),

    Document(
        page_content="""
        TechNova Customer Support Escalation Policy

        Customer complaints involving financial loss
        should be escalated to the support manager.

        Product damage complaints should be reviewed
        by the product support team.

        Unresolved payment issues should be escalated
        to payment operations.

        Any refund or cancellation requiring an
        account-level change must be reviewed by an
        authorized employee before execution.
        """,
        metadata={"source": "support_escalation"}
    )
]

# ------------------------------------------------
# STEP 2: Split documents into chunks
# ------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)

chunks = splitter.split_documents(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Document chunks created: {len(chunks)}")

# ------------------------------------------------
# STEP 3: Generate embeddings
# ------------------------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# ------------------------------------------------
# STEP 4: Store vectors in ChromaDB
# ------------------------------------------------

vectorstore = Chroma(
    collection_name="technova_knowledge",
    embedding_function=embeddings,
    persist_directory=DB_DIRECTORY
)

# Stable IDs make repeated ingestion update the
# same records instead of creating duplicate chunks.
ids = [f"technova-chunk-{i}" for i in range(len(chunks))]

vectorstore.add_documents(
    documents=chunks,
    ids=ids
)

print("\nKnowledge base successfully indexed!")

print("Vector database location:", DB_DIRECTORY)