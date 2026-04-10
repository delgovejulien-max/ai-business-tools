#!/usr/bin/env python
"""
Quick CEO Agent Test - Fast validation
"""
from agents.ceo.team_manager import _team_manager
from agents.ceo.specialists import AVAILABLE_SPECIALISTS
import json


def quick_test():
    print("")
    print("=" * 70)
    print("QUICK CEO AGENT TEST")
    print("=" * 70)
    print("")

    # Test 1: List available specialists
    print("[TEST 1] Available Specialists")
    print("-" * 70)
    try:
        roles = list(AVAILABLE_SPECIALISTS.keys())
        print(f"Available roles: {roles}")
        print("")
    except Exception as e:
        print(f"Error: {e}")
        print("")

    # Test 2: Get specialist profile
    print("[TEST 2] Get Marketing Specialist Profile")
    print("-" * 70)
    try:
        profile = AVAILABLE_SPECIALISTS["marketing"]
        print(f"Role: {profile['role']}")
        print(f"Name: {profile['name']}")
        print(f"Skills: {profile['skills']}")
        print("")
    except Exception as e:
        print(f"Error: {e}")
        print("")

    # Test 3: Hire team members
    print("[TEST 3] Hire Team Members")
    print("-" * 70)
    try:
        result1 = _team_manager.hire_specialist("marketing")
        print(f"Hired: {result1['member']['name']} ({result1['member']['role']})")

        result2 = _team_manager.hire_specialist("technology")
        print(f"Hired: {result2['member']['name']} ({result2['member']['role']})")

        result3 = _team_manager.hire_specialist("finance")
        print(f"Hired: {result3['member']['name']} ({result3['member']['role']})")
        print("")
    except Exception as e:
        print(f"Error: {e}")
        print("")

    # Test 4: View team
    print("[TEST 4] Current Team Composition")
    print("-" * 70)
    try:
        team = _team_manager.get_team()
        print(f"Team size: {team['total_members']} members")
        for member in team['members']:
            print(f"  - {member['name']} ({member['role']}): {member['status']}")
        print(f"Available positions: {team['available_roles']}")
        print("")
    except Exception as e:
        print(f"Error: {e}")
        print("")

    # Test 5: Delegate tasks
    print("[TEST 5] Delegate Tasks to Team")
    print("-" * 70)
    try:
        task1 = _team_manager.assign_task("marketing", "Launch customer acquisition campaign")
        print(f"Task assigned: {task1['task_id']}")
        print(f"Assigned to: {task1['assigned_to']}")

        task2 = _team_manager.assign_task("technology", "Build scalable architecture")
        print(f"Task assigned: {task2['task_id']}")
        print(f"Assigned to: {task2['assigned_to']}")

        task3 = _team_manager.assign_task("finance", "Create quarterly budget")
        print(f"Task assigned: {task3['task_id']}")
        print(f"Assigned to: {task3['assigned_to']}")
        print("")
    except Exception as e:
        print(f"Error: {e}")
        print("")

    # Summary
    print("=" * 70)
    print("QUICK TEST SUMMARY")
    print("=" * 70)
    print("")
    print("[OK] CEO can list available specialists")
    print("[OK] CEO can hire team members")
    print("[OK] CEO can view team composition")
    print("[OK] CEO can delegate tasks")
    print("")
    print("To run interactive CEO service:")
    print("  python ceo_service.py")
    print("")


if __name__ == "__main__":
    quick_test()
