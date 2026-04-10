"""
Phase 3 : Agent avec outils (tools)
L'agent peut utiliser des outils pour faire des choses (appeler des APIs, calculer, etc)
"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from typing import TypedDict
from config import ANTHROPIC_API_KEY, MODEL

# === ÉTAPE 1 : DÉFINIR VOS OUTILS ===
@tool
def get_weather(location: str) -> str:
    """Récupère la météo pour une localisation donnée."""
    weather_data = {
        "Paris": "Ensoleillé, 18°C",
        "Lyon": "Nuageux, 15°C",
        "Marseille": "Ensoleillé, 22°C",
        "Toulouse": "Pluie, 16°C"
    }
    return weather_data.get(location, "Localisation inconnue")

@tool
def calculate(expression: str) -> str:
    """Calcule une expression mathématique simple."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Erreur dans le calcul: {str(e)}"

# Lister les outils disponibles
tools = [get_weather, calculate]

# === ÉTAPE 2 : ÉTAT DE L'AGENT ===
class AgentState(TypedDict):
    messages: list

# === ÉTAPE 3 : INITIALISER CLAUDE AVEC LES OUTILS ===
llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model=MODEL)
llm_with_tools = llm.bind_tools(tools)

# === ÉTAPE 4 : NŒUD AGENT (appelle Claude avec tools) ===
def agent_node(state: AgentState):
    """L'agent appelle Claude, qui peut utiliser les outils"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# === ÉTAPE 5 : NŒUD TOOLS (exécute les outils) ===
tool_node = ToolNode(tools)

# === ÉTAPE 6 : CONSTRUIRE LE GRAPHE ===
graph_builder = StateGraph(AgentState)

# Ajouter les nœuds
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)

# Connecter : START -> agent -> (condition: tools ou END?)
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    tools_condition,  # Si Claude veut utiliser un outil
    {
        "tools": "tools",
        "__end__": END
    }
)
# tools -> agent (boucle : réexécute après avoir utilisé un outil)
graph_builder.add_edge("tools", "agent")

# Compiler
graph = graph_builder.compile()

# === ÉTAPE 7 : TESTER ===
if __name__ == "__main__":
    initial_state = {
        "messages": [HumanMessage(content="Quel est la météo à Paris? Et calcule 12 * 5")]
    }

    result = graph.invoke(initial_state)

    print("\n=== CONVERSATION ===")
    for msg in result["messages"]:
        if hasattr(msg, 'content'):
            print(f"{msg.__class__.__name__}: {msg.content}")
        elif hasattr(msg, 'tool_calls'):
            print(f"{msg.__class__.__name__}: Tool calls: {msg.tool_calls}")
        else:
            print(f"{msg.__class__.__name__}: {msg}")
