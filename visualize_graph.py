#!/usr/bin/env python
"""
Visualize the LangGraph architecture
"""
from agents import create_agent_graph
import sys

def visualize():
    print("")
    print("=" * 60)
    print("VISUALISATION DU GRAPHE LANGGRAPH")
    print("=" * 60)
    print("")

    try:
        graph = create_agent_graph()
        print("[OK] Graphe chargé avec succès")
    except Exception as e:
        print(f"[ERR] {str(e)}")
        sys.exit(1)

    print("")
    print("=" * 60)
    print("STRUCTURE DU GRAPHE")
    print("=" * 60)
    print("")

    # Afficher les nœuds
    print("NOEUDS:")
    if hasattr(graph, 'nodes'):
        for node_name in graph.nodes:
            print(f"  • {node_name}")
    else:
        print("  (Nœuds non disponibles directement)")

    print("")

    # Afficher le diagramme ASCII
    print("=" * 60)
    print("ARCHITECTURE VISUELLE")
    print("=" * 60)
    print("")

    from config import LLM_PROVIDER

    if LLM_PROVIDER.lower() == "ollama":
        print("MODE: OLLAMA (Chat simple)")
        print("")
        print("    START")
        print("      |")
        print("   [AGENT] (Ollama LLM)")
        print("      |")
        print("     END")
        print("")
        print("Pas de noeud tools car Ollama ne supporte pas bind_tools()")
    else:
        print("MODE: ANTHROPIC (Chat + Tools)")
        print("")
        print("    START")
        print("      |")
        print("   [AGENT] (Claude LLM avec outils)")
        print("    |   |")
        print("  tools end")
        print("    |")
        print(" [TOOLS] (Weather, Calculator)")
        print("    |")
        print("  [AGENT] (retour)")
        print("    |")
        print("   END")

    print("")
    print("=" * 60)
    print("CONFIGURATION ACTIVE")
    print("=" * 60)
    print("")
    print(f"Provider: {LLM_PROVIDER}")
    print(f"Graphe compilé: {type(graph).__name__}")
    print("")

if __name__ == "__main__":
    visualize()
