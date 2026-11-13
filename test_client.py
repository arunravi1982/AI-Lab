import requests
import json


BASE_URL = "http://127.0.0.1:8000"


def print_response(response):

    print("\nHTTP Status:", response.status_code)

    try:

        print(
            json.dumps(
                response.json(),
                indent=4
            )
        )

    except ValueError:

        print(response.text)


# -----------------------------------------
# TEST 1: HEALTH CHECK
# -----------------------------------------

print("\nTEST 1: HEALTH CHECK")

response = requests.get(
    f"{BASE_URL}/health",
    timeout=15
)

print_response(response)


# -----------------------------------------
# TEST 2: AVAILABLE SERVICES
# -----------------------------------------

print("\nTEST 2: AVAILABLE SERVICES")

response = requests.get(
    f"{BASE_URL}/services",
    timeout=15
)

print_response(response)


# -----------------------------------------
# TEST 3: INVESTIGATE PAYMENT SERVICE
# -----------------------------------------

print("\nTEST 3: PAYMENT SERVICE INVESTIGATION")

payload = {

    "services": ["payment"],

    "question": (
        "Investigate the payment service "
        "and explain why it is experiencing issues."
    )

}

response = requests.post(

    f"{BASE_URL}/agent/investigate",

    json=payload,

    timeout=120

)

print_response(response)


# -----------------------------------------
# TEST 4: INVESTIGATE MULTIPLE SERVICES
# -----------------------------------------

print("\nTEST 4: MULTIPLE SERVICE INVESTIGATION")

payload = {

    "services": [
        "payment",
        "authentication",
        "notification",
        "database"
    ],

    "question": (
        "Analyze the health of all services "
        "and identify potential operational risks."
    )

}

response = requests.post(

    f"{BASE_URL}/agent/investigate",

    json=payload,

    timeout=120

)

print_response(response)


# -----------------------------------------
# TEST 5: INVALID SERVICE
# -----------------------------------------

print("\nTEST 5: INVALID SERVICE")

payload = {

    "services": ["unknown-service"],

    "question": "Check the service health."

}

response = requests.post(

    f"{BASE_URL}/agent/investigate",

    json=payload,

    timeout=30

)

print_response(response)


# -----------------------------------------
# TEST 6: PERFORMANCE METRICS
# -----------------------------------------

print("\nTEST 6: PERFORMANCE METRICS")

response = requests.get(
    f"{BASE_URL}/metrics",
    timeout=15
)

print_response(response)
