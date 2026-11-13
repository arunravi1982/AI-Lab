from graph import graph


print("=" * 70)

print("       MULTI-AGENT IT INCIDENT INVESTIGATION SYSTEM")

print("=" * 70)


while True:

    print("\nEnter an IT incident description.")

    print("Type 'exit' to close the application.")

    incident = input("\nIncident: ").strip()

    if incident.lower() == "exit":

        print("\nApplication closed.")

        break

    if not incident:

        print("Please enter a valid incident description.")

        continue

    # Initial graph state
    initial_state = {

        "incident_description": incident,

        "monitoring_findings": "",

        "database_findings": "",

        "business_impact": "",

        "final_report": ""

    }

    try:

        print("\nStarting multi-agent investigation...")

        result = graph.invoke(
            initial_state,
            config={
                "recursion_limit": 10
            }
        )
        print("\n========== INDIVIDUAL AGENT FINDINGS ==========")

        print("\nMONITORING AGENT:")
        print(result["monitoring_findings"])    
        print("\nDATABASE AGENT:")
        print(result["database_findings"])
        print("\nBUSINESS IMPACT AGENT:")
        print(result["business_impact"])
        print("\nSUPERVISOR AGENT:")
        print(result["final_report"])     
        print("\n" + "=" * 70)

        print("             FINAL INCIDENT REPORT")

        print("=" * 70)

        print(result["final_report"])

        print("\n" + "=" * 70)

    except Exception as e:

        print("\nAn error occurred:")

        print(str(e))
