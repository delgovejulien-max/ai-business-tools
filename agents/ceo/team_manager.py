"""
Gestionnaire d'équipe pour le CEO
Gère l'embauche, le déploiement et le management des sous-agents
"""
import json
from datetime import datetime
from typing import Optional, Dict, List
from langchain_core.tools import tool
from agents.ceo.specialists import AVAILABLE_SPECIALISTS, TeamMember

class TeamManager:
    """Gère l'équipe du CEO"""

    def __init__(self):
        self.team: Dict[str, TeamMember] = {}
        self.team_counter = 0
        self.tasks_assigned = 0

    def hire_specialist(self, specialist_role: str) -> Dict:
        """
        Embauche un spécialiste

        Args:
            specialist_role: Le rôle du spécialiste à embaucher

        Returns:
            Infos du nouveau membre de l'équipe
        """
        specialist_role = specialist_role.lower()

        if specialist_role not in AVAILABLE_SPECIALISTS:
            return {"error": f"Specialist role '{specialist_role}' not available"}

        if specialist_role in self.team:
            return {"error": f"Already have a {specialist_role} specialist in the team"}

        profile = AVAILABLE_SPECIALISTS[specialist_role]
        self.team_counter += 1

        member: TeamMember = {
            "id": f"agent_{specialist_role}_{self.team_counter}",
            "role": specialist_role,
            "name": profile["name"],
            "status": "ACTIVE",
            "hired_at": datetime.now().isoformat(),
            "tasks_completed": 0
        }

        self.team[specialist_role] = member
        return {
            "status": "hired",
            "member": member,
            "message": f"Welcome to the team, {profile['name']}!"
        }

    def fire_specialist(self, specialist_role: str) -> Dict:
        """
        Licencie un spécialiste

        Args:
            specialist_role: Le rôle du spécialiste à licencier

        Returns:
            Confirmaton du licenciement
        """
        specialist_role = specialist_role.lower()

        if specialist_role not in self.team:
            return {"error": f"No {specialist_role} specialist in the team"}

        member = self.team.pop(specialist_role)
        return {
            "status": "fired",
            "message": f"{member['name']} has left the company",
            "tasks_completed": member["tasks_completed"]
        }

    def get_team(self) -> Dict:
        """Obtient la composition actuelle de l'équipe"""
        return {
            "total_members": len(self.team),
            "members": list(self.team.values()),
            "available_roles": [
                role for role in AVAILABLE_SPECIALISTS.keys()
                if role not in self.team
            ]
        }

    def assign_task(self, specialist_role: str, task: str) -> Dict:
        """
        Assigne une tâche à un spécialiste

        Args:
            specialist_role: Le rôle du spécialiste
            task: Description de la tâche

        Returns:
            Confirmation d'assignation
        """
        specialist_role = specialist_role.lower()

        if specialist_role not in self.team:
            return {"error": f"No {specialist_role} specialist in the team"}

        member = self.team[specialist_role]
        self.tasks_assigned += 1

        return {
            "status": "assigned",
            "task_id": f"task_{self.tasks_assigned}",
            "assigned_to": member["name"],
            "task": task,
            "message": f"Task assigned to {member['name']}"
        }

    def complete_task(self, specialist_role: str) -> Dict:
        """
        Marque une tâche comme complétée

        Args:
            specialist_role: Le rôle du spécialiste

        Returns:
            Confirmation de complétion
        """
        specialist_role = specialist_role.lower()

        if specialist_role not in self.team:
            return {"error": f"No {specialist_role} specialist in the team"}

        member = self.team[specialist_role]
        member["tasks_completed"] += 1

        return {
            "status": "completed",
            "member": member["name"],
            "total_tasks": member["tasks_completed"]
        }


# Instance globale du gestionnaire d'équipe
_team_manager = TeamManager()


@tool
def hire_team_member(specialist_role: str) -> dict:
    """
    Embauche un nouveau membre de l'équipe

    Args:
        specialist_role: Le rôle du spécialiste (marketing, technology, finance, operations, product, analytics)

    Returns:
        Infos du nouveau membre embauché
    """
    return _team_manager.hire_specialist(specialist_role)


@tool
def fire_team_member(specialist_role: str) -> dict:
    """
    Licencie un membre de l'équipe

    Args:
        specialist_role: Le rôle du spécialiste à licencier

    Returns:
        Confirmation du licenciement
    """
    return _team_manager.fire_specialist(specialist_role)


@tool
def view_team() -> dict:
    """
    Affiche la composition de l'équipe actuelle

    Returns:
        Liste des membres de l'équipe et postes disponibles
    """
    return _team_manager.get_team()


@tool
def delegate_task(specialist_role: str, task_description: str) -> dict:
    """
    Assigne une tâche à un spécialiste de l'équipe

    Args:
        specialist_role: Le rôle du spécialiste (marketing, technology, finance, etc.)
        task_description: Description détaillée de la tâche

    Returns:
        Confirmation d'assignation
    """
    return _team_manager.assign_task(specialist_role, task_description)


@tool
def report_task_completion(specialist_role: str) -> dict:
    """
    Rapporte la complétion d'une tâche

    Args:
        specialist_role: Le rôle du spécialiste qui a complété la tâche

    Returns:
        Confirmation de complétion
    """
    return _team_manager.complete_task(specialist_role)
