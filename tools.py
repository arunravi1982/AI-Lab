from langchain.tools import tool

# Simulated order database
ORDERS = {
    "ORD101": {
        "customer": "Rahul",
        "product": "Laptop",
        "amount": 65000,
        "status": "Shipped"
    },

    "ORD102": {
        "customer": "Priya",
        "product": "Mobile Phone",
        "amount": 25000,
        "status": "Processing"
    },

    "ORD103": {
        "customer": "Amit",
        "product": "Headphones",
        "amount": 3000,
        "status": "Delivered"
    }
}

PRODUCTS = {
    "ORD101": "Laptop, 16GB RAM, 512GB SSD",
    "ORD102": "Mobile Phone, 8GB RAM, 128GB storage",
    "ORD103": "Headphones, Wireless Bluetooth headphones"
}

# Simulated delivery information
DELIVERY = {
    "ORD101": "Delayed. Expected delivery in 2 days.",
    "ORD102": "Order is being prepared for dispatch.",
    "ORD103": "Successfully delivered yesterday."
}


@tool
def check_order(order_id: str) -> str:
    """Check order information using the customer's order ID."""

    order = ORDERS.get(order_id)

    if not order:
        return "Order not found."

    return str(order)

@tool
def check_product(order_id: str) -> str:
    """Check product information using the customer's order ID."""

    product = PRODUCTS.get(order_id)

    if not product:
        return "Product not found."

    return str(product)

@tool
def check_delivery(order_id: str) -> str:
    """Check delivery or shipping status using the order ID."""

    status = DELIVERY.get(order_id)

    if not status:
        return "Delivery information not available."

    return status


@tool
def check_refund_policy() -> str:
    """Retrieve the company's refund policy."""

    return """
    Refund Policy:

    1. Customers can request a refund for eligible orders.
    2. Delivered products can be returned within 7 days.
    3. Orders that have not been delivered can be reviewed
       for cancellation and refund.
    4. Refund approval is subject to verification.
    5. Refunds are processed within 5-7 business days
       after approval.
    """


# Register tools
tools = [
    check_order,
    check_product,
    check_delivery,
    check_refund_policy
]
