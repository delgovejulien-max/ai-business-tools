# 🤖 Projet LangGraph - Agent IA Interactif

Un projet progressif pour apprendre LangGraph avec Claude en partant de zéro jusqu'à une architecture réaliste.

## 📁 Structure du projet

```
mon-agent-langgraph/
├── .env                    # Clé API Claude (à remplir)
├── config.py              # Configuration centralisée
├── requirements.txt       # Dépendances Python
├── main.py               # Point d'entrée principal
│
├── agent_simple.py       # PHASE 2: Premier agent (avant outils)
├── agent_avec_outils.py  # PHASE 3: Agent avec outils
│
├── tools/                # PHASE 4: Architecture modulaire
│   ├── __init__.py
│   ├── weather.py       # Outil: météo
│   └── calculator.py    # Outil: calcul mathématique
│
└── agents/
    ├── __init__.py
    └── agent.py         # Logique du graphe LangGraph
```

## 🚀 Installation rapide

### 1️⃣ Configurer l'environnement

```bash
# Activez votre environnement virtuel (Windows)
venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt
```

### 2️⃣ Configurez votre clé API

Éditez le fichier `.env` et remplacez `your_api_key_here` par votre vraie clé API Anthropic:

```env
ANTHROPIC_API_KEY=sk-ant-v0-xxxxxxxxxxxx
```

## 🎯 Phases d'apprentissage

### Phase 2: Agent simple
Fichier: `agent_simple.py`

```bash
python agent_simple.py
```

✅ L'agent appelle juste Claude, pas de boucle réflexion/action.

### Phase 3: Agent avec outils
Fichier: `agent_avec_outils.py`

```bash
python agent_avec_outils.py
```

✅ L'agent peut maintenant utiliser des outils (météo, calcul).
- Claude décide s'il faut utiliser un outil
- L'agent exécute l'outil
- Claude synthétise avec le résultat

### Phase 4: Architecture modulaire
Fichier: `main.py`

```bash
python main.py
```

✅ Interface interactive, code organisé en modules:
- `config.py` - Configuration
- `tools/` - Les outils
- `agents/` - Logique de l'agent

## 📝 Exemples de questions

```
Quel est la météo à Paris?
Calcule 12 * 5 + 100
Quelle est la météo à Lyon et Marseille?
Quel est le résultat de (100 + 50) * 2?
```

## 🛠️ Pour aller plus loin

### Ajouter un nouvel outil

1. Créez un fichier dans `tools/` (ex: `tools/search.py`)
2. Définissez votre outil avec `@tool`
3. Importez-le dans `tools/__init__.py`
4. Ajoutez-le à la liste `tools` dans `agents/agent.py`

Exemple:
```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Recherche sur le web"""
    # Votre implémentation
    return "résultats..."
```

### Ajouter de la mémoire persistent

Étendez `AgentState` pour stocker des informations:

```python
class AgentState(TypedDict):
    messages: list
    memory: dict  # Nouvelle: mémoire persistante
    conversation_id: str
```

### Workflows multi-étapes

Ajoutez des nœuds supplémentaires dans le graphe:

```python
graph_builder.add_node("analyse", analyse_node)
graph_builder.add_node("decision", decision_node)
graph_builder.add_edge("agent", "analyse")
graph_builder.add_edge("analyse", "decision")
```

## 🐛 Dépannage

### Erreur: "ANTHROPIC_API_KEY not found"
→ Vérifiez que le fichier `.env` existe et contient votre clé API

### Erreur: "Module not found"
→ Installez les dépendances: `pip install -r requirements.txt`

### L'agent met longtemps à répondre
→ C'est normal! Claude appelle l'API Anthropic. Vérifiez votre connexion.

## 📚 Ressources

- [Documentation LangGraph](https://langchain-ai.github.io/langgraph/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [LangChain Documentation](https://python.langchain.com/)

## 📄 Licence

Libre d'usage pour l'apprentissage
