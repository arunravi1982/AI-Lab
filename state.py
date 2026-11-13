from typing_extensions import TypedDict

class IncidentState(TypedDict):

    incident_description: str

    monitoring_findings: str

    database_findings: str

    business_impact: str

    final_report: str
