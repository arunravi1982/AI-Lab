import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


load_dotenv()


llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-5-mini"),
    temperature=0
)


def monitoring_agent(state):

    print("\n[Monitoring Agent] Investigating application health...")

    incident = state["incident_description"]

    prompt = f"""
    You are an IT Monitoring Specialist.

    Your responsibility is to investigate application health.

    Analyze the following incident:

    {incident}

    Use the following simulated monitoring information:

    Payment Service: DOWN
    Authentication Service: UP
    Notification Service: UP

    Provide:

    1. Application health status.
    2. Relevant service findings.
    3. Possible technical observations.

    Do not invent additional monitoring data.

    Keep the response concise and professional.
    """

    response = llm.invoke(prompt)

    return {
        "monitoring_findings": response.content
    }


# Agent 2 – Database Agent

def database_agent(state):

    print("\n[Database Agent] Investigating database availability...")

    incident = state["incident_description"]

    prompt = f"""
    You are a Database Investigation Specialist.

    Your responsibility is to investigate database availability.

    Incident:

    {incident}

    Use the following simulated database information:

    payments_db: UNAVAILABLE
    users_db: AVAILABLE

    Provide:

    1. Database availability status.
    2. Relevant database findings.
    3. Possible technical observations.

    Do not invent additional database information.

    Keep the response concise and professional.
    """

    response = llm.invoke(prompt)

    return {
        "database_findings": response.content
    }


# Agent 3 – Business Impact Agent

def business_impact_agent(state):

    print("\n[Business Impact Agent] Analyzing business impact...")

    incident = state["incident_description"]

    monitoring = state["monitoring_findings"]

    database = state["database_findings"]

    prompt = f"""
    You are a Business Impact Analysis Specialist.

    Your responsibility is to analyze the potential business
    impact of an IT incident.

    Original Incident:
    {incident}

    Monitoring Findings:
    {monitoring}

    Database Findings:
    {database}

    Analyze:

    1. Potential customer impact.
    2. Potential business impact.
    3. Operational priority.
    4. Recommended escalation.

    Do not invent customer counts, financial losses,
    or confirmed impacts that are not provided.

    Clearly distinguish confirmed findings from
    potential impact.

    Keep the response concise and professional.
    """

    response = llm.invoke(prompt)

    return {
        "business_impact": response.content
    }


# Agent 4 – Supervisor Agent

def supervisor_agent(state):

    print("\n[Supervisor Agent] Consolidating investigation results...")

    prompt = f"""
    You are an IT Incident Management Supervisor.

    Your responsibility is to review the findings from
    multiple specialist agents and prepare a final
    incident investigation report.

    Original Incident:
    {state['incident_description']}

    Monitoring Agent Findings:
    {state['monitoring_findings']}

    Database Agent Findings:
    {state['database_findings']}

    Business Impact Findings:
    {state['business_impact']}

    Prepare a professional report with these sections:

    1. Incident Summary
    2. Application Health
    3. Database Health
    4. Business Impact
    5. Possible Root Cause
    6. Recommended Actions
    7. Final Incident Priority

    Important instructions:

    - Use only the information provided.
    - Do not invent facts.
    - Do not claim that the root cause is confirmed
      unless the findings establish it.
    - Clearly identify possible causes as hypotheses.
    - Keep the report structured and professional.
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }
