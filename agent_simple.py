"""
Phase 2 : Agent simple qui appelle Claude
"""
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from typing import TypedDict
from config import ANTHROPIC_API_KEY, MODEL

# 1️⃣ DÉFINIR L'ÉTAT (la "mémoire" de l'agent)
class AgentState(TypedDict):
    messages: list  # Historique des messages

# 2️⃣ INITIALISER CLAUDE
llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model=MODEL)

# 3️⃣ CRÉER LE NÔD PRINCIPAL (ce que fait l'agent)
def agent_node(state: AgentState):
    """Le cerveau de l'agent - appelle Claude"""
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# 4️⃣ CONSTRUIRE LE GRAPHE
graph_builder = StateGraph(AgentState)

# Ajouter le nœud
graph_builder.add_node("agent", agent_node)

# Connecter le flux : START -> agent -> END
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

# Compiler le graphe
graph = graph_builder.compile()

# 5️⃣ TESTER L'AGENT
if __name__ == "__main__":
    # Créer un message d'entrée
    initial_state = {
        "messages": [HumanMessage(content="Quel est la capitale de la France?")]
    }

    # Exécuter l'agent
    result = graph.invoke(initial_state)

    # Afficher la réponse
    print("\n=== RÉPONSE DE L'AGENT ===")
    print(result["messages"][-1].content)
