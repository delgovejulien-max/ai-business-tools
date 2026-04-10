#!/bin/bash

# Script rapide pour démarrer le projet LangGraph

echo "================================================"
echo "LANGGRAPH - QUICKSTART"
echo "================================================"
echo ""

# Vérifier si on est dans le bon répertoire
if [ ! -f "config.py" ]; then
    echo "ERROR: Assurez-vous d'être dans le répertoire mon-agent-langgraph"
    exit 1
fi

# Activer l'environnement
echo "[1] Activation de l'environnement virtuel..."
source venv/Scripts/activate

# Vérifier la configuration
echo "[2] Vérification du setup..."
python verify_setup.py

echo ""
echo "================================================"
echo "PRET A DEMARRER!"
echo "================================================"
echo ""
echo "Commandes disponibles:"
echo ""
echo "  python main.py              - Lancer l'agent interactif"
echo "  python agent_simple.py      - Phase 2 (agent simple)"
echo "  python agent_avec_outils.py - Phase 3 (agent + outils)"
echo "  python test_phases.py       - Test de toutes les phases"
echo "  python test_imports.py      - Test des imports"
echo ""
echo "================================================"
