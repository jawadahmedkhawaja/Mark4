# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# -------------------------------- ROOT -------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


# ========================== IMPORTS ===========================
from Collector.collector import Collector
from Designer.designer import Designer
from langchain.agents import create_agent
from os import getenv
from langchain.tools import tool
from Utils.utils import Utils

# from langchain.checkpoint.memory import InMemorySaver # type: ignore ERROR: Check it


# @tool
# def tavilySearch():
# TODO: Create Custom Tavily Search
# pass


class Orchestrator:

    SYSTEM_MESSAGE = """You are an experienced Product Manager with experience of 25 years. Your role is to process the user request and build the software requested by the user.
    You have to build the software by calling to tools and also by checking what they provide is correct, scalable, error free, without any security error. Also you have to print anything you do e.g. calling the tool or etc."""

    # Constructor
    def __init__(self):
        request = input("What you want?... ")
        if len(request) != 0:
            create_agent(
                getenv("MODEL_NAME"),
                system_prompt=self.SYSTEM_MESSAGE,
                tools=[
                    Collector().collect,  # Requirements Collector
                    Collector().findProjectDetials,  # Finds Project Details
                    Designer().prepareHLD,  # High Level Design Preparer
                    Designer().prepareLLD,  # Low Level Design Preparer
                    Designer().findEntities,  # Find Entities for the project.
                    Designer().prepareDatabaseSchema,  # DataBase Schema Preparer
                    Designer().prepareAPIStructure,  # API Structure Preparer
                    Designer().prepareCICDYamls,  # CI/CD Yaml File
                    Utils().printSomethingToTheScreen,  # print anything to the screen
                ],
            ).invoke({"messages": f"User Request: {request}"})

        else:
            print("Invalid Input...\nExiting...")
