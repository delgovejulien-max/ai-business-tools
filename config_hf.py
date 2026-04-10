"""
Hugging Face Spaces Configuration
Uses Groq API (free, fast, open source models)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Groq Configuration (Free API with Mixtral/Gemma)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model options (all free on Groq):
# - mixtral-8x7b-32768 (Fast, best quality)
# - gemma-7b-it (Good quality)
# - llama2-70b-4096 (Powerful)
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

# Ollama fallback (for local development)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")

# LLM Provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # "groq" or "ollama"


def get_llm():
    """
    Get LLM instance based on provider

    Groq: Free API with fast inference
    Ollama: Local inference (for development)
    """
    provider = LLM_PROVIDER.lower()

    if provider == "groq":
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not set. Get free key at: https://console.groq.com"
            )

        from groq import Groq
        return Groq(api_key=GROQ_API_KEY)

    elif provider == "ollama":
        # For local development
        from langchain_ollama import OllamaLLM
        return OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7
        )

    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Use 'groq' or 'ollama'")


def get_llm_response(prompt: str, system_prompt: str = "") -> str:
    """
    Get response from LLM

    Args:
        prompt: User prompt
        system_prompt: System instruction

    Returns:
        LLM response text
    """
    if LLM_PROVIDER.lower() == "groq":
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    else:
        # Ollama
        from langchain_ollama import OllamaLLM

        llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt

        return llm.invoke(full_prompt)


# Test function
if __name__ == "__main__":
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"Model: {GROQ_MODEL if LLM_PROVIDER == 'groq' else OLLAMA_MODEL}")
    print()

    try:
        response = get_llm_response(
            prompt="What is 2+2?",
            system_prompt="You are a helpful assistant. Answer concisely."
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Setup:")
        print("1. Get free Groq key: https://console.groq.com")
        print("2. Set GROQ_API_KEY environment variable")
        print("3. Run again")
