"""
Specialists disponibles que le CEO peut recruter
Chaque spécialiste est un agent autonome dans son domaine
"""
from typing import TypedDict
from langchain_core.tools import tool

class SpecialistProfile(TypedDict):
    """Profil d'un spécialiste"""
    name: str
    role: str
    description: str
    skills: list
    expertise_level: str

# Catalogue des spécialistes disponibles
AVAILABLE_SPECIALISTS = {
    "marketing": SpecialistProfile(
        name="Marketing Expert",
        role="CMO",
        description="Expert en stratégie marketing, brand, acquisition clients",
        skills=["strategie_marketing", "brand_positioning", "customer_acquisition", "analytics"],
        expertise_level="EXPERT"
    ),

    "technology": SpecialistProfile(
        name="Technology Expert",
        role="CTO",
        description="Expert en architecture tech, scalabilité, infrastructure",
        skills=["architecture", "scalabilite", "infrastructure", "security", "devops"],
        expertise_level="EXPERT"
    ),

    "finance": SpecialistProfile(
        name="Finance Expert",
        role="CFO",
        description="Expert en finance, budgets, stratégie financière",
        skills=["budgeting", "forecasting", "cost_analysis", "investment_strategy"],
        expertise_level="EXPERT"
    ),

    "operations": SpecialistProfile(
        name="Operations Expert",
        role="COO",
        description="Expert en opérations, processus, efficacité",
        skills=["process_optimization", "resource_management", "efficiency", "logistics"],
        expertise_level="EXPERT"
    ),

    "product": SpecialistProfile(
        name="Product Expert",
        role="CPO",
        description="Expert en product management, roadmap, user experience",
        skills=["product_strategy", "user_research", "roadmap", "feature_prioritization"],
        expertise_level="EXPERT"
    ),

    "analytics": SpecialistProfile(
        name="Analytics Expert",
        role="Chief Data Officer",
        description="Expert en data analytics, insights, reporting",
        skills=["data_analysis", "reporting", "dashboards", "predictive_analytics"],
        expertise_level="EXPERT"
    ),
}

class TeamMember(TypedDict):
    """Membre de l'équipe recruté"""
    id: str
    role: str
    name: str
    status: str
    hired_at: str
    tasks_completed: int

@tool
def list_available_specialists() -> dict:
    """
    Liste tous les spécialistes disponibles que le CEO peut recruter

    Returns:
        Dict avec tous les spécialistes disponibles
    """
    return {
        name: {
            "role": profile["role"],
            "description": profile["description"],
            "skills": profile["skills"]
        }
        for name, profile in AVAILABLE_SPECIALISTS.items()
    }

@tool
def get_specialist_profile(role: str) -> dict:
    """
    Obtient le profil détaillé d'un spécialiste

    Args:
        role: Le rôle du spécialiste (marketing, technology, finance, operations, product, analytics)

    Returns:
        Profil détaillé du spécialiste
    """
    if role.lower() not in AVAILABLE_SPECIALISTS:
        return {"error": f"Specialist role '{role}' not found. Available: {list(AVAILABLE_SPECIALISTS.keys())}"}

    profile = AVAILABLE_SPECIALISTS[role.lower()]
    return {
        "name": profile["name"],
        "role": profile["role"],
        "description": profile["description"],
        "skills": profile["skills"],
        "expertise_level": profile["expertise_level"]
    }
