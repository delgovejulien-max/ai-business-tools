"""Agent principal avec outils - Support Ollama et Anthropic"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict
from config import get_llm, LLM_PROVIDER
from tools import get_weather, calculate

# État de l'agent
class AgentState(TypedDict):
    messages: list

def create_agent_graph():
    """
    Crée et retourne le graphe LangGraph compilé.
    Support Ollama (open source local) et Anthropic (cloud).

    Returns:
        Un graphe LangGraph compilé et prêt à utiliser
    """
    # Récupérer le LLM configuré
    try:
        llm = get_llm()
        print(f"[LLM] Utilisant: {LLM_PROVIDER}")
    except Exception as e:
        raise ValueError(
            f"Erreur lors du chargement du LLM: {str(e)}\n"
            f"Vérifiez votre configuration .env et que le serveur Ollama est actif."
        )

    # Configuration des outils selon le provider
    tools = [get_weather, calculate]

    # Ollama n'a pas le support complet bind_tools comme Claude
    # On utilise une approche simplifiée pour Ollama
    if LLM_PROVIDER.lower() == "ollama":
        # Pour Ollama: chat simple sans outils complexes
        # Ollama peut répondre à des questions mais pas utiliser les outils
        print("[INFO] Ollama: Support chat (outils limités)")

        def agent_node(state: AgentState):
            # Simple invoke sans outils
            from langchain_core.messages import AIMessage
            response = llm.invoke(state["messages"])
            # Ollama retourne une string, pas un AIMessage
            if isinstance(response, str):
                response = AIMessage(content=response)
            return {"messages": state["messages"] + [response]}

        # Construire le graphe simplifié pour Ollama
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("agent", agent_node)
        graph_builder.add_edge(START, "agent")
        graph_builder.add_edge("agent", END)

    else:
        # Pour Anthropic Claude: support complet des outils
        print("[INFO] Anthropic: Support chat + outils")
        llm_with_tools = llm.bind_tools(tools)

        def agent_node(state: AgentState):
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": state["messages"] + [response]}

        # Nœud tools
        tool_node = ToolNode(tools)

        # Construire le graphe complet pour Claude
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("agent", agent_node)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                "__end__": END
            }
        )
        graph_builder.add_edge("tools", "agent")

    return graph_builder.compile()
