import requests 
from langchain.tools import tool

@tool
def get_product_details(product_id: int) -> dict:
    """Retrieve product information from Fake Store API."""
    if product_id <= 0:
        return {"error": "Product ID must be greater than zero."}

    url = f"https://fakestoreapi.com/products/{product_id}"

    try:
        response = requests.get(url, timeout=20)
        print(f"\n[DEBUG] Product API Status: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict) or not data:
            return {"error": f"Product {product_id} was not found."}

        return {
            "product_id": data.get("id"),
            "title": data.get("title"),
            "price": data.get("price"),
            "description": data.get("description"),
            "category": data.get("category"),
            "image": data.get("image"),
            "rating": data.get("rating"),
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

@tool
def get_user_details(user_id: int) -> dict:
    """
    Retrieve sample customer information using a user ID.
    """

    try:

        url = (
            f"https://jsonplaceholder.typicode.com/users/{user_id}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data:

            return {
                "error": "Customer not found"
            }

        return {

            "user_id": data["id"],

            "name": data["name"],

            "email": data["email"],

            "company": data["company"]["name"],

            "city": data["address"]["city"]

        }

    except requests.RequestException as e:

        return {
            "error": str(e)
        }

@tool
def get_post_details(post_id: int) -> dict:
    """
    Retrieve sample post information from JSONPlaceholder.
    """

    try:

        url = (
            f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data:

            return {
                "error": "Post not found"
            }

        return {

            "post_id": data["id"],

            "user_id": data["userId"],

            "title": data["title"],

            "body": data["body"]

        }

    except requests.RequestException as e:

        return {
            "error": str(e)
        }

@tool
def compare_product_prices(
    product_id_1: int,
    product_id_2: int
) -> dict:
    """
    Retrieve two products and compare their prices.
    """

    try:

        url1 = (
            f"https://fakestoreapi.com/products/{product_id_1}"
        )

        url2 = (
            f"https://fakestoreapi.com/products/{product_id_2}"
        )

        response1 = requests.get(
            url1,
            timeout=10
        )

        response2 = requests.get(
            url2,
            timeout=10
        )

        response1.raise_for_status()

        response2.raise_for_status()

        product1 = response1.json()

        product2 = response2.json()

        if not product1 or not product2:

            return {
                "error": "One or both products were not found"
            }

        price1 = float(product1["price"])

        price2 = float(product2["price"])

        return {

            "product_1": product1["title"],

            "price_1": price1,

            "product_2": product2["title"],

            "price_2": price2,

            "difference": round(abs(price1 - price2), 2),

            "lower_priced_product": (
                product1["title"]
                if price1 < price2
                else product2["title"]
                if price2 < price1
                else "Both products have the same price"
            )

        }

    except requests.RequestException as e:

        return {
            "error": str(e)
        }

tools = [

    get_product_details,

    get_user_details,

    get_post_details,

    compare_product_prices

]
    