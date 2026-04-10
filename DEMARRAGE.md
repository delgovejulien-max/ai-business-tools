# 🚀 DÉMARRAGE RAPIDE - LANGGRAPH

## ✅ Setup complété!

L'environnement et toutes les dépendances sont installés.

### Vérification rapide
```bash
cd "C:\Users\JulienDelgove\OneDrive - 797579778\Documents\Claude\mon-agent-langgraph"
source venv/Scripts/activate
python test_imports.py
python verify_setup.py
```

---

## 📋 CONFIGURATION FINALE (3 minutes)

### 1️⃣ Ouvrir le fichier `.env`

```bash
# Windows PowerShell
notepad .env

# Ou avec votre editeur prefere
```

### 2️⃣ Remplacer la cle API

Cherchez cette ligne:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Remplacez par votre vraie cle (depuis https://console.anthropic.com/):
```
ANTHROPIC_API_KEY=sk-ant-v0-xxxxxxxxxxxxxxxxxxxxx
```

### 3️⃣ Sauvegarder et c'est prêt!

---

## 🎯 LANCER L'AGENT

```bash
# S'assurer que l'environnement est activé
source venv/Scripts/activate

# Lancer l'agent interactif
python main.py
```

### Exemples de questions

```
Vous: Quel est la météo à Paris?
Agent: La météo à Paris est Ensoleillé, 18°C

Vous: Calcule 12 * 5 + 100
Agent: Le résultat est 160

Vous: Quelle est la météo à Lyon et Marseille?
Agent: ...utilise l'outil 2 fois...

Vous: quit
```

---

## 📚 PHASES D'APPRENTISSAGE

### Phase 2: Agent simple (sans outils)
```bash
python agent_simple.py
```
L'agent appelle juste Claude.

### Phase 3: Agent avec outils
```bash
python agent_avec_outils.py
```
L'agent peut utiliser des outils (météo, calcul).

### Phase 4: Architecture modulaire (PRINCIPALE)
```bash
python main.py
```
Interface interactive avec code bien organisé.

### Test de toutes les phases
```bash
python test_phases.py all
```

---

## 🛠️ AJOUTER UN NOUVEL OUTIL

### Étape 1: Créer le fichier `tools/mon_outil.py`

```python
from langchain_core.tools import tool

@tool
def mon_outil(param: str) -> str:
    """Description de ce que fait l'outil."""
    # Votre logique ici
    return "résultat"
```

### Étape 2: L'importer dans `tools/__init__.py`

```python
from .mon_outil import mon_outil
__all__ = ["get_weather", "calculate", "mon_outil"]
```

### Étape 3: L'ajouter dans `agents/agent.py`

```python
from tools import get_weather, calculate, mon_outil

tools = [get_weather, calculate, mon_outil]  # <-- Ajouter ici
```

C'est tout! L'agent peut maintenant utiliser votre outil.

---

## 📊 STRUCTURE DU PROJET

```
mon-agent-langgraph/
├── venv/                    # Environnement Python
├── .env                     # Clés API (gitignore)
├── config.py               # Configuration centralisée
│
├── main.py                 # POINT D'ENTRÉE PRINCIPAL
├── agent_simple.py         # Phase 2
├── agent_avec_outils.py    # Phase 3
│
├── tools/                  # Outils réutilisables
│   ├── weather.py
│   ├── calculator.py
│   └── (ajouter vos outils ici)
│
└── agents/                 # Logique des agents
    └── agent.py           # Graphe LangGraph
```

---

## 🔍 VÉRIFICATION

```bash
# Vérifier les imports
python test_imports.py

# Vérifier la structure complète
python verify_setup.py

# Tester l'agent (avec clé API)
python main.py
```

---

## ❓ PROBLÈMES COURANTS

### "ANTHROPIC_API_KEY not configured"
→ Votre .env n'a pas de clé valide
→ Mettez à jour .env et relancez

### "Module not found"
→ Activez l'environnement: `source venv/Scripts/activate`
→ Réinstallez les dépendances: `pip install -r requirements.txt`

### "Connection error" à l'execution
→ Vérifiez votre connexion internet
→ Vérifiez que votre clé API est valide

---

## 📚 RESSOURCES

- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Anthropic Claude**: https://docs.anthropic.com/
- **LangChain**: https://python.langchain.com/

---

## 🎉 VOUS ÊTES PRÊT!

1. Configurez votre clé API dans `.env`
2. Lancez `python main.py`
3. Posez une question à l'agent
4. Regardez-le utiliser ses outils!

Bon apprentissage! 🚀
