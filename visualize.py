from graph import graph


diagram = graph.get_graph().draw_mermaid()

print(diagram)

with open(
    "multi_agent_workflow.mmd",
    "w",
    encoding="utf-8"
) as file:

    file.write(diagram)

print("\nGraph diagram saved successfully.")

from termaid import render_rich
mermaid_graph = """
graph TD;
        __start__:::first
        monitoring_agent(monitoring_agent)
        database_agent(database_agent)
        business_impact_agent(business_impact_agent)
        supervisor_agent(supervisor_agent)
        __end__:::last
        __start__ --> monitoring_agent;
        business_impact_agent --> supervisor_agent;
        database_agent --> business_impact_agent;
        monitoring_agent --> database_agent;
        supervisor_agent --> __end__;
     """
print(render_rich(mermaid_graph,theme="neon"))