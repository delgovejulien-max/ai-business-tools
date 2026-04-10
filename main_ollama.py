"""
Point d'entrée principal avec Gemma 3 (Open Source via Ollama)
Solution 100% open source et locale
"""
from langchain_core.messages import HumanMessage
from agents import create_agent_graph
from config import LLM_PROVIDER, OLLAMA_MODEL, OLLAMA_BASE_URL
import sys

def check_ollama():
    """Vérifie que Ollama est disponible"""
    if LLM_PROVIDER.lower() != "ollama":
        return True  # Skip check for non-Ollama providers

    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"Erreur de connexion à Ollama: {e}")
        return False

def main():
    """Lance l'agent interactif avec Gemma 3"""

    # Vérifier Ollama
    if LLM_PROVIDER.lower() == "ollama":
        print("\n[CHECK] Vérification de Ollama...")
        if not check_ollama():
            print(f"[ERR]  Ollama n'est pas disponible sur {OLLAMA_BASE_URL}")
            print("\nSolutions:")
            print("  1. Démarrer Ollama: ollama serve")
            print("  2. Télécharger le modèle: ollama pull gemma3:latest")
            print("  3. Vérifier la configuration dans .env")
            sys.exit(1)
        print(f"[OK]   Ollama connecté - Modèle: {OLLAMA_MODEL}")

    # Créer le graphe
    print("[LOAD] Chargement du graphe LangGraph...")
    try:
        graph = create_agent_graph()
        print("[OK]   Graphe chargé avec succès")
    except Exception as e:
        print(f"[ERR]  Erreur lors du chargement du graphe: {str(e)}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("AGENT LANGGRAPH - GEMMA 3 (OPEN SOURCE)")
    print("=" * 60)
    print(f"Provider: {LLM_PROVIDER.upper()}")
    if LLM_PROVIDER.lower() == "ollama":
        print(f"Modèle: {OLLAMA_MODEL}")
        print(f"URL: {OLLAMA_BASE_URL}")
    print("\nCommandes:")
    print("  - Posez une question à l'agent")
    print("  - Tapez 'quit' ou 'exit' pour quitter")
    print("\nExemples:")
    print("  - 'Quel est la météo à Paris?'")
    print("  - 'Calcule 12 * 5 + 100'")
    print("  - 'Donne-moi la météo à Lyon et Marseille'")
    print("=" * 60 + "\n")

    while True:
        # Obtenir l'entrée utilisateur
        try:
            user_input = input("Vous: ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
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
            print("\n[AGENT] Réflexion en cours...")
            initial_state = {
                "messages": [HumanMessage(content=user_input)]
            }

            result = graph.invoke(initial_state)

            # Afficher la réponse
            response = result['messages'][-1].content
            print(f"\nAgent: {response}\n")

        except Exception as e:
            print(f"\n[ERR]  Erreur: {str(e)}\n")

if __name__ == "__main__":
    main()
