# Migration vers Open Source (Ollama + Gemma 3)

## Résumé des changements

Votre projet LangGraph a été migré pour supporter à la fois:
- **Ollama + Gemma 3** (open source local - PAR DÉFAUT)
- **Anthropic Claude** (optionnel, cloud)

## Changements principaux

### 1. Configuration flexible

**Avant**: Seulement Claude via Anthropic
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(api_key=key, model="claude-3-5")
```

**Après**: Support Ollama + Anthropic
```python
from config import get_llm
llm = get_llm()  # Détecte automatiquement
```

### 2. Fichier .env redesigné

```env
# Choix du provider
LLM_PROVIDER=ollama  # ou "anthropic"

# Config Ollama (open source local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:latest

# Config Anthropic (cloud - optionnel)
ANTHROPIC_API_KEY=sk-ant-v0-xxxxx...
```

### 3. Dépendances ajoutées

```
langchain-ollama>=0.1.0  # Support Ollama
ollama>=0.1.0            # Client Ollama
```

## Fichiers modifiés

| Fichier | Changement |
|---------|-----------|
| `config.py` | Nouveau système de provider (Ollama vs Anthropic) |
| `.env` | Configuration pour Ollama |
| `agents/agent.py` | Utilise `get_llm()` au lieu de `ChatAnthropic` |
| `main.py` | Affiche le provider utilisé |
| `requirements.txt` | Ajout dépendances Ollama |

## Fichiers nouveaux

| Fichier | Purpose |
|---------|---------|
| `main_ollama.py` | Version dédiée Ollama (avec vérifications) |
| `start_ollama.sh` | Script bash pour démarrer Ollama |
| `start_ollama.bat` | Script Windows pour démarrer Ollama |
| `OPEN_SOURCE_SETUP.md` | Documentation open source |
| `MIGRATION_GUIDE.md` | Ce fichier |

## Comment ça marche?

### Ordre de décision

```
1. Lire LLM_PROVIDER dans .env
   ├─ Si "ollama"
   │  └─ Créer OllamaLLM
   │     └─ Connecter à OLLAMA_BASE_URL
   │        └─ Utiliser OLLAMA_MODEL
   │
   └─ Si "anthropic"
      └─ Créer ChatAnthropic
         └─ Utiliser ANTHROPIC_API_KEY
```

### Code généralisé

```python
# config.py
def get_llm():
    if LLM_PROVIDER == "ollama":
        return OllamaLLM(model=OLLAMA_MODEL, ...)
    elif LLM_PROVIDER == "anthropic":
        return ChatAnthropic(api_key=ANTHROPIC_API_KEY, ...)
```

```python
# agents/agent.py
llm = get_llm()  # Fonctionne avec les deux!
llm_with_tools = llm.bind_tools(tools)
```

## Basculer entre Ollama et Anthropic

### Passer à Ollama (par défaut)

Modifier `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:latest
```

Puis:
```bash
ollama serve  # Terminal 1
python main.py  # Terminal 2
```

### Passer à Anthropic Claude

Modifier `.env`:
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-v0-xxxxx...
```

Puis:
```bash
python main.py  # Aucun serveur à démarrer
```

## Modèles Ollama populaires

```bash
# Généraliste rapide
ollama pull mistral:latest

# Généraliste puissant
ollama pull llama2:latest

# Codage
ollama pull phind-codellama:latest

# Chat optimisé
ollama pull neural-chat:latest

# Petit et rapide
ollama pull tinyllama:latest
```

Puis mettre à jour `.env`:
```env
OLLAMA_MODEL=mistral:latest
```

## Avantages de chaque provider

### Ollama (Open Source)
✅ Gratuit
✅ Privé (données locales)
✅ Hors-ligne
✅ Changer de modèle facilement
❌ Moins puissant que Claude
❌ Plus lent (sauf GPU)

### Anthropic Claude
✅ Plus puissant
✅ Plus rapide
✅ Mieux pour tâches complexes
❌ Coûts API
❌ Données dans le cloud
❌ Internet requis

## Voir les performances

```python
# config.py retourne le provider utilisé
from config import LLM_PROVIDER
print(f"Using: {LLM_PROVIDER}")  # "ollama" ou "anthropic"
```

## Émettre un problème?

### Ollama ne répond pas
```bash
# Terminal 1
ollama serve

# Terminal 2
curl http://localhost:11434/api/tags
```

### Modèle manquant
```bash
ollama pull gemma3:latest
```

### Performance lente
```bash
# Vérifier l'utilisation GPU
ollama show gemma3:latest

# Utiliser un modèle plus petit
ollama pull mistral:latest  # Plus rapide
```

## Statistiques

**Gemma 3** (modèle par défaut):
- Paramètres: ~9B
- Taille: ~3.3 GB
- Vitesse: 30-60 sec/réponse (CPU), 5-10 sec (GPU)
- Qualité: Très bonne
- Langues: Multilingue (français OK)

## Architecture finale

```
┌─────────────────────────────────────┐
│      main.py (Point d'entrée)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   config.get_llm()                  │
│  (Detect Provider: Ollama/Anthropic)│
└──────┬────────────────────┬─────────┘
       │                    │
  ┌────▼──────┐      ┌──────▼──────┐
  │ OllamaLLM │      │ ChatAnthropic│
  │ (Gemma3)  │      │  (Claude)    │
  └────┬──────┘      └──────┬───────┘
       │                    │
  ┌────▼──────┐      ┌──────▼───────┐
  │Ollama     │      │ Anthropic    │
  │Server     │      │ Cloud API    │
  │localhost  │      │              │
  │:11434     │      │              │
  └───────────┘      └──────────────┘
```

## Prochaines étapes

1. ✅ Code migrépour support Ollama/Anthropic
2. ✅ Dépendances installées
3. ⏳ Gemma 3 en cours de téléchargement (~4%)
4. ▶️ Démarrer Ollama: `ollama serve`
5. ▶️ Lancer l'agent: `python main.py`

## Questions?

Consultez:
- `OPEN_SOURCE_SETUP.md` - Guide d'utilisation Ollama
- `README.md` - Documentation générale
- `.env` - Configuration actuelle

---

**Migration complète vers open source terminée! 🎉**
