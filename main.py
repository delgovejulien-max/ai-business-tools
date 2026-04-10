"""
Point d'entrée principal du projet LangGraph
Support: Ollama (open source) + Anthropic Claude
"""
from langchain_core.messages import HumanMessage
from agents import create_agent_graph
from config import LLM_PROVIDER
import sys

def main():
    """Lance l'agent interactif"""
    # Créer le graphe
    try:
        graph = create_agent_graph()
    except Exception as e:
        print(f"Erreur lors du chargement: {str(e)}")
        sys.exit(1)

    print("=" * 60)
    print("AGENT LANGGRAPH - {}".format(LLM_PROVIDER.upper()))
    print("=" * 60)
    print("\nCommandes disponibles:")
    print("  - Posez une question à l'agent")
    print("  - Tapez 'quit' ou 'exit' pour quitter")
    print("\nExemples de questions:")
    print("  - 'Quel est la météo à Paris?'")
    print("  - 'Calcule 12 * 5 + 100'")
    print("  - 'Quelle est la météo à Lyon et à Marseille?'")
    print("=" * 60 + "\n")

    while True:
        # Obtenir l'entrée utilisateur
        try:
            user_input = input("Vous: ").strip()
        except EOFError:
            # Gestion Ctrl+D
            break
        except KeyboardInterrupt:
            # Gestion Ctrl+C
            print("\nAu revoir!")
            break

        # Vérifier les commandes de sortie
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Au revoir!")
            break

        if not user_input:
            continue

        # Exécuter l'agent
        try:
            initial_state = {
                "messages": [HumanMessage(content=user_input)]
            }

            result = graph.invoke(initial_state)

            # Afficher la réponse
            print(f"\n🤖 Agent: {result['messages'][-1].content}\n")

        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}\n")

if __name__ == "__main__":
    main()
