#!/usr/bin/env python
"""
LangGraph Agent Service - Ollama + Gemma 2b
Service interactif 100% open source
"""
from langchain_core.messages import HumanMessage
from agents import create_agent_graph
import sys

def main():
    print("")
    print("=" * 60)
    print("LANGGRAPH AGENT - OLLAMA + GEMMA 2B")
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
    print("SERVICE OPERATIONNEL - PRET A RECEVOIR QUESTIONS")
    print("=" * 60)
    print("")
    print("Commandes:")
    print("  - Posez une question")
    print("  - Tapez 'quit' ou 'exit' pour quitter")
    print("  - Ctrl+C pour arreter")
    print("")

    while True:
        try:
            user_input = input("Vous: ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print("")
            print("Au revoir!")
            break

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Au revoir!")
            break

        if not user_input:
            continue

        print("[AGENT] Reflection...")
        try:
            state = {
                "messages": [HumanMessage(content=user_input)]
            }
            result = graph.invoke(state)
            response = result["messages"][-1].content
            print(f"Agent: {response}")
            print("")
        except Exception as e:
            print(f"[ERR] {str(e)[:100]}")
            print("")

if __name__ == "__main__":
    main()
