from Orchestrator.orchestrator import Orchestrator
from dotenv import load_dotenv
def main():
    # Loading Environment Variables
    load_dotenv()

    # Starting the Orchestrator
    Orchestrator()

if __name__ == "__main__":
    main()
