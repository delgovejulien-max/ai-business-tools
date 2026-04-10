"""
CEO Agent avec capacité à créer et gérer une équipe de sous-agents
Architecture LangGraph multi-agent
"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import HumanMessage, AIMessage
from config import get_llm, LLM_PROVIDER

# Importer les outils
from agents.ceo.specialists import list_available_specialists, get_specialist_profile
from agents.ceo.team_manager import (
    hire_team_member,
    fire_team_member,
    view_team,
    delegate_task,
    report_task_completion
)
from agents.ceo.ceo_tools import (
    analyze_business_opportunity,
    create_quarterly_plan,
    make_strategic_decision,
    set_company_vision,
    generate_executive_report
)


class CEOState(TypedDict):
    """État du CEO"""
    messages: list
    team_composition: dict
    current_mission: str
    strategic_decisions: list


def create_ceo_agent():
    """
    Crée un agent CEO autonome capable de:
    - Analyser les opportunités
    - Créer/gérer une équipe de spécialistes
    - Déléguer des tâches
    - Prendre des décisions stratégiques
    - Générer des rapports

    Returns:
        Un graphe LangGraph compilé pour le CEO
    """

    # Récupérer le LLM
    try:
        llm = get_llm()
        print(f"[CEO] Utilisant LLM: {LLM_PROVIDER}")
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du LLM: {str(e)}")

    # Outils disponibles pour le CEO
    ceo_tools = [
        list_available_specialists,
        get_specialist_profile,
        hire_team_member,
        fire_team_member,
        view_team,
        delegate_task,
        report_task_completion,
        analyze_business_opportunity,
        create_quarterly_plan,
        make_strategic_decision,
        set_company_vision,
        generate_executive_report,
    ]

    # Mode Ollama: chat simple
    if LLM_PROVIDER.lower() == "ollama":
        print("[CEO] Mode Ollama: Chat simple (outils limités)")

        def ceo_node(state: CEOState):
            from langchain_core.messages import AIMessage
            response = llm.invoke(state["messages"])
            if isinstance(response, str):
                response = AIMessage(content=response)
            return {"messages": state["messages"] + [response]}

        # Graphe simplifié
        graph_builder = StateGraph(CEOState)
        graph_builder.add_node("ceo", ceo_node)
        graph_builder.add_edge(START, "ceo")
        graph_builder.add_edge("ceo", END)

    else:
        # Mode Anthropic: support complet des outils
        print("[CEO] Mode Anthropic: Chat + Outils complets")

        llm_with_tools = llm.bind_tools(ceo_tools)

        def ceo_node(state: CEOState):
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": state["messages"] + [response]}

        # Nœud pour exécuter les outils
        tool_node = ToolNode(ceo_tools)

        # Construire le graphe complet
        graph_builder = StateGraph(CEOState)
        graph_builder.add_node("ceo", ceo_node)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "ceo")
        graph_builder.add_conditional_edges(
            "ceo",
            tools_condition,
            {
                "tools": "tools",
                "__end__": END
            }
        )
        graph_builder.add_edge("tools", "ceo")

    return graph_builder.compile()


def create_ceo_state() -> CEOState:
    """Crée un état initial pour le CEO"""
    return {
        "messages": [],
        "team_composition": {},
        "current_mission": "",
        "strategic_decisions": []
    }
