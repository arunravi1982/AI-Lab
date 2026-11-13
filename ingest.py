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
    ),

    Document(
        page_content="""
        TechNova Product Warranty Policy
1. Warranty PeriodTechNova provides a limited hardware warranty for all eligible products. The specific warranty coverage periods are as follows:
• Smartphones and Tablets: 12 months from the date of original retail purchase.
• Laptops and Desktop Computers: 12 months for the main chassis, motherboard, and processor.
• Accessories (Power adapters, charging cables, standalone docks): 6 months from the date of original retail purchase.
• Consumables (Internal batteries, headphone driver components): 6 months from the date of original retail purchase.
2. Eligible Products
This warranty applies exclusively to original, authentic hardware devices manufactured by TechNova. To be eligible for service under this policy, the product must meet the following criteria:
• The product must have been purchased directly from TechNova’s official online storefront or through an authorized retail partner.
• The product must have its original, legible serial number or IMEI plate completely intact and unaltered.
• The customer must provide a valid proof of purchase (tax invoice or retail receipt) clearly showing the purchase date, product description, and seller details.
3. Warranty Exclusions
The TechNova limited warranty covers defects in materials and manufacturing workmanship under normal, intended use. This warranty does not cover:
• Cosmetic Damage: Scratches, dents, cracks, or broken plastic on ports and outer enclosures resulting from regular wear and tear or accidental drops.
• Environmental or Liquid Damage: Malfunctions caused by exposure to moisture, severe dampness, liquid submersion, sand, dirt, extreme thermal environments, or electrical power surges.
• Unauthorized Modifications: Any device that has been opened, repaired, altered, or modified by a third-party service center not authorized in writing by TechNova.
• Misuse and Abuse: Damage arising from operating the product outside its published technical specifications, physical abuse, or use with non-approved, incompatible third-party accessories.
• Software Issues: Operating system corruption, viruses, malware, or data loss caused by unauthorized software installations or rooting.
4. How to Raise a Warranty Request
If an eligible product develops a hardware defect during its coverage period, customers can initiate a claim through the following steps:
Step 1: Gather Documentation
Prepare your original tax invoice or retail proof of purchase, along with the device serial number or IMEI number.
Step 2: Submit the Claim
• Online Support Portal: Visit the official TechNova Support page, log into your account, navigate to "Your Orders," and select the defective item to generate a Digital Return Merchandise Authorization (RMA) ticket.
• Customer Service Email: Send an email containing your invoice, clear photos or videos of the defect, and a detailed description of the issue to support@technova.com.
Step 3: Device Return and Evaluation
Once the ticket is approved, customer service will provide a shipping label or direct you to the nearest authorized TechNova Walk-In Service Center. Do not ship your product without an approved RMA number, as it will be rejected. TechNova will, at its option, repair the device using new or refurbished parts, or replace it with an equivalent model at no structural cost to the customer.
        """,
        metadata={"source": "product_warranty"}
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
