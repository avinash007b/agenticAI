import logging
from langchain.tools import tool
from langfuse import observe

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


tools = [
    check_service_status,
    get_system_logs,
    get_incident_details
]