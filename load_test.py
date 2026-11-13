import requests
import time

from concurrent.futures import ThreadPoolExecutor


BASE_URL = "http://127.0.0.1:8000"

NUMBER_OF_REQUESTS = 5

MAX_WORKERS = 3


def send_request(request_number):

    payload = {

        "services": [
            "payment",
            "authentication"
        ],

        "question": (
            f"Analyze the health of the services. "
            f"Request number {request_number}."
        )

    }

    start_time = time.perf_counter()

    try:

        response = requests.post(

            f"{BASE_URL}/agent/investigate",

            json=payload,

            timeout=120

        )

        elapsed = time.perf_counter() - start_time

        return {

            "request": request_number,

            "status_code": response.status_code,

            "time_seconds": round(elapsed, 2)

        }

    except requests.RequestException as error:

        return {

            "request": request_number,

            "error": str(error)

        }


print("\nStarting load test...")

print("Total requests:", NUMBER_OF_REQUESTS)

print("Concurrent client workers:", MAX_WORKERS)


overall_start = time.perf_counter()


with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:

    results = list(
        executor.map(
            send_request,
            range(1, NUMBER_OF_REQUESTS + 1)
        )
    )


overall_time = time.perf_counter() - overall_start


print("\nLOAD TEST RESULTS")

for result in results:

    print(result)


print("\nTotal execution time:", round(
    overall_time, 2
), "seconds")


successful = [

    result

    for result in results

    if result.get("status_code") == 200

]

print(
    "\nSuccessful requests:",
    len(successful)
)

print(
    "Failed requests:",
    NUMBER_OF_REQUESTS - len(successful)
)
