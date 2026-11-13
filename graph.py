import os

from typing import TypedDict, Optional

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt


load_dotenv()

# ------------------------------------------------
# STEP 1: Initialize models
# ------------------------------------------------

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-5-mini"),
    temperature=0
)

embeddings = OpenAIEmbeddings(
    model=os.getenv(
        "EMBEDDING_MODEL",
        "text-embedding-3-small"
    )
)

# ------------------------------------------------
# STEP 2: Connect to existing ChromaDB
# ------------------------------------------------

vectorstore = Chroma(
    collection_name="technova_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# ------------------------------------------------
# STEP 3: Define workflow state
# ------------------------------------------------

class EnterpriseState(TypedDict):
    question: str
    context: str
    answer: str
    requires_approval: bool
    proposed_action: str
    approval_status: str
    approval: Optional[dict]
    final_response: str


# ------------------------------------------------
# STEP 4: Identify sensitive operations
# ------------------------------------------------

APPROVAL_KEYWORDS = [
    "process refund",
    "issue refund",
    "issue compensation",
    "initiate refund",
    "cancel order",
    "delete account",
    "restart production service",
    "execute production change"
]


def requires_human_approval(question: str) -> bool:

    normalized = question.lower()

    return any(
        phrase in normalized
        for phrase in APPROVAL_KEYWORDS
    )


# ------------------------------------------------
# STEP 5: Document retrieval node
# ------------------------------------------------

def retrieve_documents(state: EnterpriseState):

    question = state["question"]

    print("\n[RETRIEVAL NODE]")
    print("Searching enterprise knowledge base...")

    documents = retriever.invoke(question)

    context_parts = []

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "unknown"
        )
    for doc in documents:
        print(
        "Retrieved source:",
        doc.metadata.get("source")
        )
   
        context_parts.append(
            f"Source: {source}\n"
            f"Content: {doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    if not context:
        context = "No relevant documents were retrieved."

    print(f"Documents retrieved: {len(documents)}")

    return {
        "context": context
    }


# ------------------------------------------------
# STEP 6: Generate grounded answer
# ------------------------------------------------

def generate_answer(state: EnterpriseState):

    question = state["question"]
    context = state["context"]

    print("\n[LLM NODE]")
    print("Generating response using retrieved context...")

    prompt = f"""
    You are the TechNova Enterprise Knowledge Assistant.

    Answer the user's question using the retrieved
    company knowledge provided below.

    Rules:
    1. Use the retrieved documents as your evidence.
    2. Do not invent company policies.
    3. If the answer is not available in the documents,
       clearly say that you could not find sufficient
       information.
    4. Mention relevant source names where useful.
    5. Do not claim that any refund, cancellation,
       or other business operation has been executed.
    6. If the user requests a sensitive operation,
       explain the applicable policy and state that
       human approval is required.

    USER QUESTION:
    {question}

    RETRIEVED COMPANY KNOWLEDGE:
    {context}

    Generate a clear and professional response.
    """

    response = llm.invoke(prompt)

    answer = response.content

    requires_approval = requires_human_approval(
        question
    )

    proposed_action = ""

    if requires_approval:
        proposed_action = (
            "Review the requested business operation: "
            + question
        )

    return {
        "answer": answer,
        "requires_approval": requires_approval,
        "proposed_action": proposed_action
    }


# ------------------------------------------------
# STEP 7: Conditional routing
# ------------------------------------------------

def route_after_answer(state: EnterpriseState):

    if state["requires_approval"]:
        return "approval"

    return "complete"


# ------------------------------------------------
# STEP 8: Human approval node
# ------------------------------------------------

def human_approval(state: EnterpriseState):

    print("\n[HUMAN APPROVAL NODE]")
    print("Waiting for authorized human decision...")

    decision = interrupt({
        "message": "Human approval is required.",
        "proposed_action": state["proposed_action"],
        "retrieved_context": state["context"][:1000]
    })

    approved = (
        decision.get("approved", False)
        if isinstance(decision, dict)
        else False
    )

    comments = (
        decision.get("comments", "")
        if isinstance(decision, dict)
        else ""
    )

    return {
        "approval": decision,
        "approval_status": (
            "approved" if approved else "rejected"
        ),
        "final_response": (
            f"Human decision: "
            f"{'APPROVED' if approved else 'REJECTED'}.\n"
            f"Reviewer comments: {comments}"
        )
    }


# ------------------------------------------------
# STEP 9: Simulated business operation
# ------------------------------------------------

def execute_action(state: EnterpriseState):

    print("\n[EXECUTION NODE]")
    print("Human approval received.")

    # This is only a simulation.
    # No real refund or cancellation is performed.

    result = (
        "SIMULATION SUCCESSFUL: The requested "
        "business operation would now be sent to "
        "the authorized backend."
    )

    return {
        "final_response": (
            "The request was approved by the human reviewer.\n"
            + result
        )
    }


# ------------------------------------------------
# STEP 10: Rejection node
# ------------------------------------------------

def reject_action(state: EnterpriseState):

    print("\n[REJECTION NODE]")
    print("Human reviewer rejected the request.")

    return {
        "final_response": (
            "The request was rejected by the human reviewer. "
            "No business operation was executed."
        )
    }


# ------------------------------------------------
# STEP 11: Approval routing
# ------------------------------------------------

def route_after_approval(state: EnterpriseState):

    if state["approval_status"] == "approved":
        return "execute"

    return "reject"


# ------------------------------------------------
# STEP 12: Build LangGraph
# ------------------------------------------------

workflow = StateGraph(EnterpriseState)

workflow.add_node("retrieve", retrieve_documents)
workflow.add_node("generate", generate_answer)
workflow.add_node("approval", human_approval)
workflow.add_node("execute", execute_action)
workflow.add_node("reject", reject_action)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")

workflow.add_conditional_edges(
    "generate",
    route_after_answer,
    {
        "approval": "approval",
        "complete": END
    }
)

workflow.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "execute": "execute",
        "reject": "reject"
    }
)

workflow.add_edge("execute", END)
workflow.add_edge("reject", END)

# ------------------------------------------------
# STEP 13: Compile with checkpointer
# ------------------------------------------------

checkpointer = InMemorySaver()

graph = workflow.compile(
    checkpointer=checkpointer
)

print("Enterprise AI workflow initialized.")