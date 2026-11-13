from langchain.tools import tool


# Simulated application services
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
    """Check whether an application service is UP or DOWN.

    Args:
        service_name: Name of the service, such as payment,
                      authentication, or notification.
    """

    print(f"\n[TOOL EXECUTED] Checking service: {service_name}")

    status = SERVICE_STATUS.get(service_name.lower())

    if status is None:
        return f"Service '{service_name}' was not found."

    return f"Service: {service_name}\nStatus: {status}"


@tool
def check_database(database_name: str) -> str:
    """Check database connectivity and availability.

    Args:
        database_name: Name of the database, such as
                       payments_db or users_db.
    """

    print(f"\n[TOOL EXECUTED] Checking database: {database_name}")

    status = DATABASE_STATUS.get(database_name.lower())

    if status is None:
        return f"Database '{database_name}' was not found."

    return f"Database: {database_name}\nStatus: {status}"


@tool
def get_system_logs(service_name: str) -> str:
    """Retrieve recent application logs for a service.

    Args:
        service_name: Name of the application service.
    """

    print(f"\n[TOOL EXECUTED] Retrieving logs for: {service_name}")

    logs = APPLICATION_LOGS.get(service_name.lower())

    if logs is None:
        return f"No logs found for service '{service_name}'."

    return "\n".join(logs)
