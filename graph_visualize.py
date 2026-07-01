from backend.agents.graph_agent import agent_graph

try:
    png_bytes = agent_graph.get_graph().draw_mermaid_png()

    with open("agent_graph.png", "wb") as f:
        f.write(png_bytes)

    print("Graph saved as agent_graph.png")

except Exception as e:

    print("PNG generation failed:", e)

    mermaid = agent_graph.get_graph().draw_mermaid()

    print("\nMermaid Diagram:\n")
    print(mermaid)