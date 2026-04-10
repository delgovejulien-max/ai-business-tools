#!/bin/bash

# Script pour démarrer Ollama avec Gemma 3

echo "=========================================="
echo "DEMARRAGE OLLAMA + GEMMA 3"
echo "=========================================="
echo ""

# Vérifier que Ollama est installé
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama n'est pas installé"
    echo "Téléchargez-le sur: https://ollama.ai/download"
    exit 1
fi

echo "[1] Vérification de Gemma 3..."
ollama list | grep -q gemma3

if [ $? -ne 0 ]; then
    echo "[DOWNLOAD] Gemma 3 non trouvé - Téléchargement..."
    ollama pull gemma3:latest

    if [ $? -ne 0 ]; then
        echo "ERROR: Erreur lors du téléchargement de Gemma 3"
        exit 1
    fi
fi

echo "[OK] Gemma 3 trouvé"
echo ""
echo "[2] Démarrage du serveur Ollama..."
echo "     URL: http://localhost:11434"
echo "     Modèle: Gemma 3"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

ollama serve
