def check_service(service_name):
    """Check the health of an application service."""

    services = {
        "payment": "RUNNING",
        "database": "RUNNING",
        "authentication": "WARNING",
        "notification": "RUNNING"
    }

    service_name = service_name.lower()

    if service_name not in services:
        return {
            "service": service_name,
            "status": "NOT_FOUND",
            "message": "Service does not exist."
        }

    return {
        "service": service_name,
        "status": services[service_name],
        "cpu_usage": "42%",
        "memory_usage": "65%"
    }

def check_database(database_name):
    """Check database connectivity."""

    return {
        "database": database_name,
        "status": "CONNECTED",
        "active_connections": 45,
        "response_time": "120 ms"
    }

def get_system_logs(service_name):
    """Retrieve simulated application logs."""

    logs = {
        "payment": [
            "Payment application started successfully.",
            "Payment request processed.",
            "Health check completed."
        ],
        "authentication": [
            "Authentication service started.",
            "Warning: Login response time increased.",
            "Retry attempt detected."
        ],
        "notification": [
            "Notification service started.",
            "Email notification sent successfully."
        ]
    }

    return logs.get(
        service_name.lower(),
        [f"No logs found for {service_name}."]
    )

def check_disk_space(service_name):
    ***Check available disk space***
    return {
        "total_space": "500 GB",
        "used_space": "350 GB",
        "free_space": "150 GB"
    }
