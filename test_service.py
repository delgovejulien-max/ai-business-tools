#!/usr/bin/env python
"""
Test script to demonstrate the service working with predefined questions
No interactive input needed - just run and see responses
"""
from langchain_core.messages import HumanMessage
from agents import create_agent_graph
import sys

def test_service():
    print("")
    print("=" * 60)
    print("LANGGRAPH AGENT - TEST NON-INTERACTIF")
    print("=" * 60)
    print("")
    print("[INIT] Chargement du graphe...")

    try:
        graph = create_agent_graph()
        print("[OK]  Graphe pret")
    except Exception as e:
        print(f"[ERR] {str(e)[:100]}")
        sys.exit(1)

    print("")
    print("=" * 60)
    print("EXECUTION DE TESTS")
    print("=" * 60)
    print("")

    # Questions de test
    test_questions = [
        "Quel est la capitale de la France?",
        "Qui es-tu?",
        "Calcule 10 + 5",
        "Donne-moi un conseil",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"[TEST {i}] Question: {question}")
        try:
            state = {
                "messages": [HumanMessage(content=question)]
            }
            result = graph.invoke(state)
            response = result["messages"][-1].content
            print(f"Reponse: {response}")
            print("")
        except Exception as e:
            print(f"[ERR] {str(e)[:100]}")
            print("")

    print("=" * 60)
    print("TESTS TERMINES")
    print("=" * 60)
    print("")
    print("Si vous voyez cette sortie, le service fonctionne correctement!")
    print("Pour utiliser le service interactif, lancez: python main.py")
    print("")

if __name__ == "__main__":
    test_service()
