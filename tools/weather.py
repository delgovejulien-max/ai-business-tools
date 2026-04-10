"""Outil : Récupération de la météo"""
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Récupère la météo pour une localisation donnée.

    Args:
        location: La ville pour laquelle récupérer la météo

    Returns:
        La météo actuelle
    """
    weather_data = {
        "Paris": "Ensoleillé, 18°C",
        "Lyon": "Nuageux, 15°C",
        "Marseille": "Ensoleillé, 22°C",
        "Toulouse": "Pluie, 16°C",
        "Bordeaux": "Partiellement nuageux, 17°C"
    }
    return weather_data.get(location, f"Désolé, je n'ai pas les données météo pour {location}")
