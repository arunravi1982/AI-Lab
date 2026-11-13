import logging
from langchain.tools import tool
from langfuse import observe
import time
import urllib.request
import psutil

logger = logging.getLogger(__name__)

SERVICES = {
    "payment-service": {
        "status": "DOWN",
        "cpu": 95,
        "memory": 88,
        "response_time": 15000
    },
    "authentication-service": {
        "status": "UP",
        "cpu": 35,
        "memory": 42,
        "response_time": 120
    },
    "notification-service": {
        "status": "UP",
        "cpu": 48,
        "memory": 55,
        "response_time": 250
    }
}

start_time = time.perf_counter()

# Execute your operation here

end_time = time.perf_counter()

latency = (end_time - start_time) * 1000

print(f"Execution time: {latency:.2f} ms")


INCIDENTS = {
    "INC1001": {
        "service": "payment-service",
        "priority": "P1",
        "status": "OPEN",
        "description": "Payment transactions failing"
    },
    "INC1002": {
        "service": "authentication-service",
        "priority": "P3",
        "status": "RESOLVED",
        "description": "Intermittent login failures"
    }
}


@tool
@observe(
    name="check_service_status",
    as_type="tool",
    capture_input=False,
    capture_output=False
)
def check_service_status(service_name: str) -> str:
    """Check the health and resource metrics of an IT service."""

    try:
        service_name = service_name.lower().strip()

        if service_name == "timeout-demo":
            raise TimeoutError("Simulated monitoring timeout")

        if service_name not in SERVICES:
            return f"Service {service_name} was not found."

        data = SERVICES[service_name]

        logger.info("Service health check completed: %s", service_name)

        return (
            f"Service: {service_name}\n"
            f"Status: {data['status']}\n"
            f"CPU: {data['cpu']}%\n"
            f"Memory: {data['memory']}%\n"
            f"Response time: {data['response_time']} ms"
        )

    except TimeoutError as error:
        logger.error("Monitoring timeout: %s", error)
        return "ERROR: Monitoring request timed out."

    except Exception:
        logger.exception("Unexpected service monitoring failure")
        return "ERROR: Unable to retrieve service information."


@tool
@observe(
    name="get_system_logs",
    as_type="tool",
    capture_input=False,
    capture_output=False
)
def get_system_logs(service_name: str) -> str:
    """Retrieve recent simulated application logs for a service."""

    logs = {
        "payment-service": [
            "ERROR: Database connection failed",
            "ERROR: Payment transaction timeout",
            "WARN: Connection pool exhausted",
            "ERROR: Unable to process transaction"
        ],
        "authentication-service": [
            "INFO: Authentication service started",
            "INFO: Login request processed",
            "INFO: Token validation successful"
        ],
        "notification-service": [
            "INFO: Notification service started",
            "INFO: Message delivery successful"
        ]
    }

    service_name = service_name.lower().strip()

    if service_name not in logs:
        return f"No logs available for {service_name}."

    logger.info("System logs retrieved for %s", service_name)

    return "\n".join(logs[service_name])


@tool
@observe(
    name="get_incident_details",
    as_type="tool",
    capture_input=False,
    capture_output=False
)
def get_incident_details(incident_id: str) -> str:
    """Retrieve details of a simulated IT incident."""

    incident_id = incident_id.upper().strip()

    if incident_id not in INCIDENTS:
        return f"Incident {incident_id} was not found."

    data = INCIDENTS[incident_id]

    logger.info("Incident retrieved: %s", incident_id)

    return (
        f"Incident ID: {incident_id}\n"
        f"Service: {data['service']}\n"
        f"Priority: {data['priority']}\n"
        f"Status: {data['status']}\n"
        f"Description: {data['description']}"
    )
def get_resource_metrics(
    target_url: str = "http://localhost:8000/health", disk_path: str = "/"
) -> dict:
    """Retrieves system resource utilization (CPU, memory, disk) and endpoint response time.

    Args:
        target_url: The endpoint URL to ping for measuring response time.
        disk_path: The filesystem path to check disk utilization (use 'C:\\' on
          Windows).

    Returns:
        A dictionary containing CPU, memory, disk percentages, and response time
        in ms.
    """
    # 1. CPU Utilization (measured over a 0.5-second interval for accuracy)
    cpu_util = psutil.cpu_percent(interval=0.5)

    # 2. Memory Utilization
    memory_util = psutil.virtual_memory().percent

    # 3. Disk Utilization
    disk_util = psutil.disk_usage(disk_path).percent

    # 4. Response Time (measured in milliseconds)
    start_time = time.perf_counter()
    try:
        with urllib.request.urlopen(target_url, timeout=5) as response:
            response.read()
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    except Exception as e:
        response_time_ms = f"Error: {str(e)}"

    return {
        "cpu_utilization_percent": cpu_util,
        "memory_utilization_percent": memory_util,
        "disk_utilization_percent": disk_util,
        "response_time_ms": response_time_ms,
    }


tools = [
    check_service_status,
    get_system_logs,
    get_incident_details,
    get_resource_metrics
]
ALLOWED_TOOLS = {
    "check_service_status",
    "get_system_logs",
    "get_incident_details",
    "get_resource_metrics"
}
def retry_operation(operation, max_attempts=3):

    for attempt in range(max_attempts):

        try:
            return operation()

        except TimeoutError:

            if attempt == max_attempts - 1:
                raise

            time.sleep(2 ** attempt)
