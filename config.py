import os
from dotenv import load_dotenv

load_dotenv()

# Configuration API - Support multiple modeles
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" ou "anthropic"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("MODEL", "gemma:2b")

# Configuration Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")

# Note: Validation du provider est faite au runtime quand le model est necessaire
# Cela permet de charger le module pour les tests et verifications

def get_llm():
    """
    Retourne une instance du LLM configuré
    Support: Ollama (open source) ou Anthropic Claude
    """
    provider = LLM_PROVIDER.lower()

    if provider == "ollama":
        from langchain_ollama import OllamaLLM
        return OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7
        )

    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured in .env")
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model=MODEL)

    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Use 'ollama' or 'anthropic'")
