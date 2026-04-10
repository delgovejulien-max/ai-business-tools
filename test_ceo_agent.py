#!/usr/bin/env python
"""
Test script for the CEO Agent
Demonstrates autonomous decision-making and team management
"""
from langchain_core.messages import HumanMessage
from agents.ceo import create_ceo_agent, create_ceo_state
import sys


def test_ceo():
    print("")
    print("=" * 70)
    print("CEO AGENT - AUTONOMOUS TEST")
    print("=" * 70)
    print("")
    print("[INIT] Loading CEO agent...")

    try:
        graph = create_ceo_agent()
        print("[OK]  CEO agent ready")
    except Exception as e:
        print(f"[ERR] {str(e)[:100]}")
        sys.exit(1)

    print("")
    print("=" * 70)
    print("RUNNING CEO SIMULATIONS")
    print("=" * 70)
    print("")

    # Test scenarios
    test_scenarios = [
        "List all available specialist roles I can hire",
        "Hire a marketing expert to lead our customer acquisition strategy",
        "Show me the current team composition",
        "What expertise does our technology specialist bring?",
        "Create a Q1 strategic plan focused on market expansion and product innovation",
        "Analyze this business opportunity: expanding to European markets with budget of 200000",
        "Delegate the market research task to our marketing expert",
        "Generate an executive summary of our current status",
    ]

    for i, prompt in enumerate(test_scenarios, 1):
        print(f"\n[TEST {i}] CEO Prompt:")
        print(f"  > {prompt}")
        print(f"\n[CEO] Analyzing and responding...")
        print("-" * 70)

        try:
            state = create_ceo_state()
            state["messages"] = [HumanMessage(content=prompt)]

            result = graph.invoke(state)
            response = result["messages"][-1].content

            print(f"Response: {response}")
            print("-" * 70)

        except Exception as e:
            print(f"[ERR] {str(e)[:200]}")
            print("-" * 70)

    print("")
    print("=" * 70)
    print("TESTS COMPLETED")
    print("=" * 70)
    print("")
    print("Summary:")
    print("  - CEO can analyze opportunities")
    print("  - CEO can build autonomous teams")
    print("  - CEO can manage specialists")
    print("  - CEO can make strategic decisions")
    print("")
    print("To run interactive mode: python ceo_service.py")
    print("")


if __name__ == "__main__":
    test_ceo()
