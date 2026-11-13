test_cases = [
    {
        "query": "Check payment-service health",
        "expected_tool": "check_service_status"
    },
    {
        "query": "Retrieve payment-service logs",
        "expected_tool": "get_system_logs"
    },
    {
        "query": "Get incident INC1001",
        "expected_tool": "get_incident_details"
    }
]