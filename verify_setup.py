"""
Script de vérification du setup LangGraph
Verifie que tout est installe correctement sans avoir besoin d'une cle API
"""
import sys
import os

def check_imports():
    """Verifie que tous les imports fonctionnent"""
    print("\n" + "=" * 60)
    print("[CHECK] VERIFICATION DES IMPORTS")
    print("=" * 60 + "\n")

    tests = [
        ("langgraph", "LangGraph"),
        ("langchain_anthropic", "Langchain-Anthropic"),
        ("langchain_core", "Langchain-Core"),
        ("dotenv", "Python-dotenv"),
    ]

    all_passed = True

    for module, name in tests:
        try:
            __import__(module)
            print("[OK]   {} - Installe".format(name.ljust(25)))
        except ImportError as e:
            print("[ERR]  {} - MANQUANT".format(name.ljust(25)))
            all_passed = False

    return all_passed

def check_env_file():
    """Verifie que le fichier .env existe et est configure"""
    print("\n" + "=" * 60)
    print("[CHECK] VERIFICATION DE LA CONFIGURATION")
    print("=" * 60 + "\n")

    if os.path.exists(".env"):
        print("[OK]   Fichier .env trouve")

        with open(".env", "r") as f:
            content = f.read()

        if "ANTHROPIC_API_KEY=" in content:
            if "your_api_key_here" in content or content.strip().endswith("="):
                print("[WARN] ANTHROPIC_API_KEY pas configuree (valeur vide ou placeholder)")
                return False
            else:
                print("[OK]   ANTHROPIC_API_KEY configuree")
                return True
        else:
            print("[ERR]  ANTHROPIC_API_KEY manquante dans .env")
            return False
    else:
        print("[ERR]  Fichier .env manquant")
        return False

def check_structure():
    """Verifie que la structure des dossiers est correcte"""
    print("\n" + "=" * 60)
    print("[CHECK] VERIFICATION DE LA STRUCTURE")
    print("=" * 60 + "\n")

    files = [
        ("config.py", "Configuration"),
        ("agent_simple.py", "Phase 2 - Agent Simple"),
        ("agent_avec_outils.py", "Phase 3 - Agent avec Outils"),
        ("main.py", "Point d'entree"),
        ("test_phases.py", "Script de test"),
    ]

    folders = [
        ("tools", "Dossier des outils"),
        ("agents", "Dossier des agents"),
    ]

    all_passed = True

    print("[FILES] Fichiers:")
    for file, desc in files:
        if os.path.exists(file):
            print("  [OK]   {} - {}".format(file.ljust(25), desc))
        else:
            print("  [ERR]  {} - {} (MANQUANT)".format(file.ljust(25), desc))
            all_passed = False

    print("\n[DIRS]  Dossiers:")
    for folder, desc in folders:
        if os.path.isdir(folder):
            print("  [OK]   {} - {}".format(folder.ljust(25), desc))
        else:
            print("  [ERR]  {} - {} (MANQUANT)".format(folder.ljust(25), desc))
            all_passed = False

    return all_passed

def main():
    """Lance toutes les verifications"""
    print("\n" + "SETUP LANGGRAPH - VERIFICATION COMPLETE\n")

    import_ok = check_imports()
    env_ok = check_env_file()
    struct_ok = check_structure()

    print("\n" + "=" * 60)
    print("[RESUME] RESULTAT")
    print("=" * 60)

    if import_ok:
        print("[OK]   Tous les imports sont OK")
    else:
        print("[ERR]  Il manque des dependances - lancez: pip install -r requirements.txt")

    if env_ok:
        print("[OK]   Configuration API OK")
    else:
        print("[WARN] Mettez a jour .env avec votre ANTHROPIC_API_KEY")

    if struct_ok:
        print("[OK]   Structure du projet OK")
    else:
        print("[ERR]  La structure du projet est incomplete")

    print("\n" + "=" * 60)
    if import_ok and struct_ok:
        if env_ok:
            print("SUCCESS! Setup complet - Pret a utiliser!")
            print("\nCommandes disponibles:")
            print("  python main.py              # Lancer l'agent interactif")
            print("  python agent_simple.py      # Tester Phase 2")
            print("  python agent_avec_outils.py # Tester Phase 3")
            print("  python test_phases.py       # Tester toutes les phases")
        else:
            print("ALMOST DONE! Setup presque complet - Il faut configurer la cle API")
            print("\nEtapes:")
            print("  1. Ouvrez le fichier .env")
            print("  2. Remplacez 'your_api_key_here' par votre cle Anthropic")
            print("  3. Relancez python main.py")
    else:
        print("ERROR! Le setup n'est pas complet")
        sys.exit(1)

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
