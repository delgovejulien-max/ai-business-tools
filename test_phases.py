"""
Script de test pour comparer les 3 phases
Utile pour voir l'évolution de la complexité
"""
import sys
from langchain_core.messages import HumanMessage

def test_phase_2():
    """Test de Phase 2: Agent simple"""
    print("\n" + "=" * 60)
    print("📌 PHASE 2: Agent Simple (sans outils)")
    print("=" * 60)

    from agent_simple import graph

    initial_state = {
        "messages": [HumanMessage(content="Dis-moi une blague courte")]
    }

    result = graph.invoke(initial_state)
    print("\n✅ Réponse:")
    print(result["messages"][-1].content)

def test_phase_3():
    """Test de Phase 3: Agent avec outils"""
    print("\n" + "=" * 60)
    print("📌 PHASE 3: Agent avec Outils")
    print("=" * 60)

    from agent_avec_outils import graph

    initial_state = {
        "messages": [HumanMessage(content="Quelle est la météo à Paris? Et calcule 25 * 4")]
    }

    result = graph.invoke(initial_state)
    print("\n✅ Réponse:")
    print(result["messages"][-1].content)

def test_phase_4():
    """Test de Phase 4: Architecture modulaire"""
    print("\n" + "=" * 60)
    print("📌 PHASE 4: Architecture Modulaire")
    print("=" * 60)

    from agents import create_agent_graph

    graph = create_agent_graph()
    initial_state = {
        "messages": [HumanMessage(content="Quel est la météo à Marseille?")]
    }

    result = graph.invoke(initial_state)
    print("\n✅ Réponse:")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    print("\n🚀 TESTS DES PHASES LANGGRAPH\n")

    # Demander quelle phase tester
    if len(sys.argv) > 1:
        phase = sys.argv[1]
    else:
        print("Quelle phase voulez-vous tester?")
        print("  1) Phase 2 (agent simple)")
        print("  2) Phase 3 (agent avec outils)")
        print("  3) Phase 4 (architecture modulaire)")
        print("  all) Toutes les phases\n")

        phase = input("Entrez votre choix (1/2/3/all): ").strip()

    try:
        if phase == "1":
            test_phase_2()
        elif phase == "2":
            test_phase_3()
        elif phase == "3":
            test_phase_4()
        elif phase == "all":
            test_phase_2()
            test_phase_3()
            test_phase_4()
        else:
            print("❌ Choix invalide")
            sys.exit(1)

        print("\n✨ Test terminé!\n")

    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        print("\nAssurez-vous que:")
        print("  - pip install -r requirements.txt ✓")
        print("  - .env contient votre ANTHROPIC_API_KEY ✓")
        sys.exit(1)
