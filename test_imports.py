"""
Test des imports - Verifie que le code peut etre charge sans cle API
"""
import sys

def test_module(module_name, description):
    """Teste l'import d'un module"""
    try:
        __import__(module_name)
        print("[OK]   {} - {}".format(module_name.ljust(25), description))
        return True
    except Exception as e:
        print("[ERR]  {} - {} ({})".format(module_name.ljust(25), description, str(e)[:30]))
        return False

def main():
    print("\n[TEST] Import des modules du projet\n")

    tests = [
        ("config", "Configuration"),
        ("tools.weather", "Outil: Meteo"),
        ("tools.calculator", "Outil: Calculatrice"),
        ("tools", "Package outils"),
        ("agents.agent", "Agent LangGraph"),
    ]

    print("=" * 70)
    results = []
    for module, desc in tests:
        results.append(test_module(module, desc))

    print("=" * 70)

    passed = sum(results)
    total = len(results)

    print("\nResultat: {}/{} tests passes".format(passed, total))

    if passed == total:
        print("\nSUCCESS! Tous les modules se chargent correctement.")
        print("\nVous pouvez maintenant:")
        print("  1. Configurer votre ANTHROPIC_API_KEY dans .env")
        print("  2. Lancer: python main.py")
        return 0
    else:
        print("\nERROR! Il y a des problemes d'import.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
