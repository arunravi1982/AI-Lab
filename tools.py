from langchain.tools import tool


# Simulated service status
SERVICE_STATUS = {
    "payment": "DOWN",
    "authentication": "UP",
    "notification": "UP"
}


# Simulated database status
DATABASE_STATUS = {
    "payments_db": "UNAVAILABLE",
    "users_db": "AVAILABLE"
}


# Simulated application logs
APPLICATION_LOGS = {
    "payment": [
        "ERROR: Unable to establish database connection",
        "ERROR: Database connection timeout",
        "ERROR: Payment transaction processing failed"
    ],
    "authentication": [
        "INFO: Authentication service started",
        "INFO: Login requests processed successfully"
    ]
}


@tool
def check_service(service_name: str) -> str:
    """Check whether an IT application service is UP or DOWN."""

    print(f"\n[TOOL EXECUTED] Checking service: {service_name}")

    status = SERVICE_STATUS.get(service_name.lower())

    if status is None:
        return f"Service {service_name} was not found."

    return f"{service_name} service status: {status}"


@tool
def check_database(database_name: str) -> str:
    """Check whether an IT database is available or unavailable."""

    print(f"\n[TOOL EXECUTED] Checking database: {database_name}")

    status = DATABASE_STATUS.get(database_name.lower())

    if status is None:
        return f"Database {database_name} was not found."

    return f"{database_name} database status: {status}"


@tool
def get_system_logs(service_name: str) -> str:
    """Retrieve recent application logs for an IT service."""

    print(f"\n[TOOL EXECUTED] Retrieving logs for: {service_name}")

    logs = APPLICATION_LOGS.get(service_name.lower())

    if logs is None:
        return f"No logs found for {service_name}."

    return "\n".join(logs)


tools = [
    check_service,
    check_database,
    get_system_logs
]