#!/usr/bin/env python
"""
CEO Agent Scenarios - Demonstrating real-world use cases
Shows how to use the CEO agent programmatically
"""
import sys
from datetime import datetime
from agents.ceo.team_manager import _team_manager
from agents.ceo.specialists import AVAILABLE_SPECIALISTS


def print_section(title):
    """Pretty print section header"""
    print(f"\n{'=' * 70}")
    print(f"{title.center(70)}")
    print(f"{'=' * 70}\n")


def scenario_startup():
    """SCENARIO 1: Startup CEO building their first team"""
    print_section("SCENARIO 1: Startup CEO - Building First Team")

    print("CEO: Our startup just got funded! Time to build the core team.")
    print("")

    # Step 1: List available roles
    print("[CEO ACTION] Reviewing available specialist roles...")
    roles = list(AVAILABLE_SPECIALISTS.keys())
    print(f"Available positions: {', '.join(roles)}")
    print("")

    # Step 2: Hire core team
    print("[CEO DECISION] Building core team for MVP launch...")
    core_team = ["marketing", "technology", "product"]

    for role in core_team:
        result = _team_manager.hire_specialist(role)
        print(f"[+] Hired {result['member']['name']} as {result['member']['role']}")

    print("")

    # Step 3: View team
    team = _team_manager.get_team()
    print(f"Current team size: {team['total_members']} members")
    print(f"Available to hire: {', '.join(team['available_roles'])}")
    print("")

    # Step 4: Initial task assignment
    print("[CEO COMMAND] Assigning initial tasks...")
    tasks = [
        ("product", "Define MVP features and roadmap"),
        ("technology", "Set up development infrastructure"),
        ("marketing", "Plan go-to-market strategy"),
    ]

    for role, task in tasks:
        result = _team_manager.assign_task(role, task)
        print(f"  > {result['assigned_to']}: {task}")

    print("\n[STATUS] Team ready for MVP launch!")


def scenario_scaling():
    """SCENARIO 2: Scaling company - Hiring additional specialists"""
    print_section("SCENARIO 2: Growth Phase - Scaling Operations")

    # Reset for new scenario
    _team_manager.team = {}
    _team_manager.team_counter = 0

    print("CEO: Product is gaining traction! We need to scale fast.")
    print("")

    # Hire for growth
    growth_team = ["marketing", "technology", "finance", "operations"]
    print("[CEO STRATEGY] Assembling growth team...")

    for role in growth_team:
        result = _team_manager.hire_specialist(role)
        print(f"[+] Hired {result['member']['name']}")

    print("")

    # Check current state
    team = _team_manager.get_team()
    print(f"Team composition: {team['total_members']} senior leaders")
    print("Positions filled:")
    for member in team['members']:
        print(f"  • {member['name']} ({member['role']})")

    print("")

    # Scaling tasks
    print("[CEO DIRECTIVE] Critical tasks for scaling...")
    scaling_tasks = [
        ("finance", "Secure Series A funding and manage financial planning"),
        ("operations", "Build operational processes and infrastructure"),
        ("marketing", "Launch aggressive customer acquisition campaign"),
        ("technology", "Scale infrastructure for 10x growth"),
    ]

    for role, task in scaling_tasks:
        result = _team_manager.assign_task(role, task)
        print(f"  > {result['assigned_to']}")

    print("\n[STATUS] Team assembled for rapid scaling!")


def scenario_market_expansion():
    """SCENARIO 3: Market expansion - Full team deployment"""
    print_section("SCENARIO 3: Global Expansion - Full Department")

    # Reset
    _team_manager.team = {}
    _team_manager.team_counter = 0

    print("CEO: Time to dominate globally. Building complete department.")
    print("")

    # Hire full team
    print("[CEO VISION] Assembling world-class team for global dominance...")
    all_roles = list(AVAILABLE_SPECIALISTS.keys())

    for role in all_roles:
        result = _team_manager.hire_specialist(role)
        profile = AVAILABLE_SPECIALISTS[role]
        print(f"[+] {profile['name']:25} - {profile['description'][:45]}")

    print("")

    # View full team
    team = _team_manager.get_team()
    print(f"Total team size: {team['total_members']} C-level executives")
    print("")

    # Global expansion tasks
    print("[CEO STRATEGIC INITIATIVE] Global expansion tasks...")
    expansion_tasks = [
        ("marketing", "Launch campaigns in 5 new international markets"),
        ("technology", "Build global CDN and multi-region infrastructure"),
        ("finance", "Manage international expansion budget ($5M)"),
        ("product", "Localize product for 10 markets"),
        ("operations", "Establish regional offices in 3 continents"),
        ("analytics", "Build global analytics and reporting dashboard"),
    ]

    for role, task in expansion_tasks:
        result = _team_manager.assign_task(role, task)
        print(f"  > {result['assigned_to']}: Assigned task {result['task_id']}")

    print("")
    print("[STATUS] Global expansion plan launched!")
    print(f"          Total tasks assigned: {_team_manager.tasks_assigned}")


def scenario_performance_management():
    """SCENARIO 4: Performance management - Completing tasks and reporting"""
    print_section("SCENARIO 4: Performance Management")

    # Use existing team from previous scenario
    print(f"Current team size: {len(_team_manager.team)} members")
    print("")

    print("[CEO REVIEW] Checking team performance...")
    print("")

    # Mark some tasks as completed
    completed_roles = ["marketing", "technology", "finance"]
    print("Task completions:")
    for role in completed_roles:
        if role in _team_manager.team:
            result = _team_manager.complete_task(role)
            print(f"  [+] {result['member']}: {result['total_tasks']} tasks completed")

    print("")

    # Performance summary
    print("[CEO SUMMARY] Team Performance Report:")
    print("-" * 70)
    print(f"{'Name':<30} {'Role':<15} {'Status':<10} {'Tasks':<6}")
    print("-" * 70)

    for role, member in _team_manager.team.items():
        print(
            f"{member['name']:<30} "
            f"{member['role']:<15} "
            f"{member['status']:<10} "
            f"{member['tasks_completed']:<6}"
        )

    print("-" * 70)
    print(f"Total team members: {len(_team_manager.team)}")
    print(f"Total tasks completed: {sum(m['tasks_completed'] for m in _team_manager.team.values())}")
    print("")


def main():
    print("")
    print("=" * 70)
    print("CEO AGENT - REAL-WORLD SCENARIOS".center(70))
    print("=" * 70)
    print("")

    try:
        # Run scenarios
        scenario_startup()
        scenario_scaling()
        scenario_market_expansion()
        scenario_performance_management()

        # Summary
        print_section("SCENARIOS COMPLETED")
        print("You've seen how the CEO agent can:")
        print("")
        print("1. BUILD TEAMS")
        print("   - Hire specialists from available catalog")
        print("   - View team composition")
        print("   - Scale teams for growth")
        print("")
        print("2. DELEGATE WORK")
        print("   - Assign tasks to specialists")
        print("   - Track task completion")
        print("   - Monitor performance")
        print("")
        print("3. MAKE DECISIONS")
        print("   - Hire/fire based on strategy")
        print("   - Allocate resources")
        print("   - Plan expansion")
        print("")
        print("Next steps:")
        print("  1. Run: python quick_ceo_test.py")
        print("  2. Run: ollama serve (Terminal 1)")
        print("  3. Run: python ceo_service.py (Terminal 2)")
        print("  4. Give CEO commands and watch it manage!")
        print("")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
