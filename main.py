# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Entry Point: main.py
# Description: Application entry point for initializing environment variables and 
#              launching the interactive Orchestrator agent session.
# ==============================================================================

"""
Main Application Launcher for Mark4 AI SWE Platform.

This script loads environment settings from .env and boots the primary 
`Orchestrator` Product Manager agent.
"""

from dotenv import load_dotenv
from Orchestrator.orchestrator import Orchestrator


def main() -> None:
    """
    Bootstrap the Mark4 application, load environment variables, and launch Orchestrator.
    """
    # --------------------------------------------------------------------------
    # Load Environment Configuration (.env)
    # --------------------------------------------------------------------------
    load_dotenv()

    # --------------------------------------------------------------------------
    # Initialize and Launch Main Orchestrator Agent Session
    # --------------------------------------------------------------------------
    print("=" * 70)
    print("          MARK4 AI SOFTWARE ENGINEERING AGENT PLATFORM          ")
    print("=" * 70)
    
    Orchestrator()


if __name__ == "__main__":
    main()
