#!/usr/bin/env python
"""
CEO Agent Interactive Service
Interact with your autonomous CEO and watch them build their team
"""
from langchain_core.messages import HumanMessage
from agents.ceo import create_ceo_agent, create_ceo_state
import sys


def main():
    print("")
    print("=" * 70)
    print("AUTONOMOUS CEO AGENT - LANGGRAPH")
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
    print("CEO OPERATIONAL - READY FOR COMMANDS")
    print("=" * 70)
    print("")
    print("Commands:")
    print("  - Ask CEO to analyze opportunities")
    print("  - Ask CEO to build their team")
    print("  - Ask CEO to delegate tasks")
    print("  - Ask CEO to generate reports")
    print("  - Type 'quit' or 'exit' to exit")
    print("  - Ctrl+C to stop")
    print("")
    print("Example prompts:")
    print("  - 'Hire a marketing expert'")
    print("  - 'Show me the current team'")
    print("  - 'Create a Q1 plan with these objectives: launch product, expand market'")
    print("  - 'Generate an executive report'")
    print("")

    while True:
        try:
            user_input = input("CEO: ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print("")
            print("Shutting down...")
            break

        if user_input.lower() in ["quit", "exit", "q"]:
            print("CEO: Thank you for the strategic guidance. Goodbye!")
            break

        if not user_input:
            continue

        print("[CEO] Processing...")
        try:
            state = create_ceo_state()
            state["messages"] = [HumanMessage(content=user_input)]

            result = graph.invoke(state)
            response = result["messages"][-1].content

            print(f"CEO Response: {response}")
            print("")
        except Exception as e:
            print(f"[ERR] {str(e)[:100]}")
            print("")


if __name__ == "__main__":
    main()
