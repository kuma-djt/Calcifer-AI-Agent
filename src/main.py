# Calcifer entry point
"""
Calcifer – Entry Point
Orchestrates:
- Memory loading
- Skill routing
- Approval flow
- Response synthesis
"""

from core.agent import Calcifer

def main():
    agent = Calcifer()
    agent.load_context()
    agent.run()

if __name__ == "__main__":
    main()
