# Open Source LLM Setup - Gemma 3 via Ollama

## Qu'est-ce qu'on a fait?

Migration du projet vers une **solution 100% open source et locale**:
- ❌ Plus besoin de clé API Anthropic
- ✅ Gemma 3 (Google) - gratuit et open source
- ✅ Exécuté localement via Ollama
- ✅ Données restent sur votre machine

## Architecture

```
LangGraph Agent
      ↓
  Config (supports Ollama + Anthropic)
      ↓
   OllamaLLM
      ↓
Ollama Server (localhost:11434)
      ↓
   Gemma 3
```

## Pré-requis

### 1. Ollama installé ✅
```bash
ollama --version
```

### 2. Gemma 3 téléchargé
```bash
ollama pull gemma3:latest
```

Le modèle est ~3.3 GB. Temps de téléchargement: 5-10 min selon connexion.

## Configuration

### .env

Le fichier `.env` est déjà configuré pour Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:latest
```

Pour passer à Claude, changez:
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-v0-xxxxx...
```

## Utilisation

### 1. Démarrer Ollama

Terminal 1:
```bash
ollama serve
```

### 2. Lancer l'agent

Terminal 2:
```bash
cd mon-agent-langgraph
source venv/Scripts/activate
python main.py
```

### 3. Poser une question

```
Vous: Quel est la météo à Paris?
Agent: [Gemma 3 répond...]

Vous: Calcule 12 * 5 + 100
Agent: [Utilise l'outil calcul...]
```

## Modèles alternatifs

Vous pouvez utiliser d'autres modèles Ollama:

```bash
# Mistral (petit, rapide)
ollama pull mistral

# Llama 2 (populaire)
ollama pull llama2

# Neural Chat
ollama pull neural-chat

# Phind Codellama
ollama pull phind-codellama
```

Puis mettez à jour `.env`:
```env
OLLAMA_MODEL=mistral:latest
```

## Performance

Sur votre machine:
- **CPU**: ~30-60 secondes par réponse
- **GPU (NVIDIA)**: ~5-10 secondes
- **Apple Silicon**: ~3-5 secondes

Pour utiliser GPU:
```bash
# NVIDIA CUDA
ollama pull gemma3:latest  # Utilise GPU auto

# AMD Radeon
# Voir: https://github.com/ollama/ollama/blob/main/docs/linux.md
```

## Avantages de cette approche

✅ **Gratuit** - Pas de frais API
✅ **Privé** - Données locales
✅ **Hors-ligne** - Fonctionne sans internet
✅ **Flexible** - Changez de modèle facilement
✅ **Extensible** - Ajouter d'autres outils

## Limitations

⚠️ **Moins puissant** que Claude 3 (mais bon!)
⚠️ **Plus lent** sans GPU
⚠️ **Moins de tokens** dans le contexte
⚠️ **Moins précis** sur certaines tâches

## Comparaison Ollama vs Anthropic

| Aspect | Ollama | Anthropic |
|--------|--------|-----------|
| Coût | Gratuit | Payant |
| Modèle | Gemma 3 | Claude 3.5 |
| Vitesse | Moyenne | Rapide |
| Qualité | Bonne | Excellente |
| Privé | Oui | Non |
| Hors-ligne | Oui | Non |
| GPU support | Oui | N/A |

## Scripts utiles

### Démarrer Ollama et l'agent ensemble

`start_all.sh`:
```bash
#!/bin/bash
echo "Démarrage de Ollama..."
ollama serve &

sleep 5

echo "Démarrage de l'agent..."
cd mon-agent-langgraph
source venv/Scripts/activate
python main.py
```

### Vérifier l'installation

```bash
# Vérifier Ollama
ollama list

# Vérifier le modèle
ollama pull gemma3:latest

# Tester une réponse
ollama run gemma3:latest "Qui es-tu?"
```

## Troubleshooting

### "Connection refused"
```bash
# Ollama n'est pas actif
# Solution: Démarrer Ollama dans un autre terminal
ollama serve
```

### "Model not found"
```bash
# Gemma 3 n'est pas téléchargé
ollama pull gemma3:latest
```

### Performances lentes
```bash
# 1. Vérifier l'utilisation GPU
ollama show gemma3:latest

# 2. Libérer de la RAM
# Fermer les autres applications

# 3. Utiliser un modèle plus petit
ollama pull mistral:latest
# Puis mettre à jour .env: OLLAMA_MODEL=mistral:latest
```

## Prochaines étapes

1. ✅ Ollama installé
2. ⏳ Gemma 3 en téléchargement (~4% - 2 min restantes)
3. ▶️ Démarrer Ollama: `ollama serve`
4. ▶️ Lancer l'agent: `python main.py`
5. ▶️ Poser une question!

## Documentation

- Ollama: https://ollama.ai
- Gemma: https://ai.google.dev/gemma
- LangChain Ollama: https://python.langchain.com/docs/integrations/llms/ollama

---

**Solution 100% open source! 🎉**
