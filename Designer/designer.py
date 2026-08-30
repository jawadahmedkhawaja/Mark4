# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ------------------------------ DESIGNER -----------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


# ================================ IMPORTS  ==================================
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from os import getenv
from pydantic import BaseModel, Field
from Utils.utils import Utils

# Schema for Column
class Column(BaseModel):
    columnName: str = Field(description="contains the name of column in table.")
    columnDataType: str = Field(description="contains the data type of column.")
    columnLength: int | None = Field(
        None, description="specifies the length of data column can have."
    )
    isPrimaryKey: bool = Field(
        False, description="tell that if column is a primary key or not."
    )
    autoIncrement: bool = Field(
        False, description="tells if the column value will increment automatically."
    )
    canNull: bool = Field(
        False, description="tells if the column can have null value of not."
    )
    isForeignKey: bool | None = Field(
        None, description="tell if the column is a foreign key from another table."
    )
    referenceToForeignKey: str | None = Field(
        None,
        description="it is the name of another table column and will be set if the column is a foreign key",
    )
    isUnique: bool = Field(
        False,
        description="tells if the column will be unique, will true if column is primary key.",
    )

#Schema for Table
class Table(BaseModel):
    tableName: str = Field(description="Contains the name of table.")
    columns: list[Column] = Field(description="contains the columns table have.")

# Schema for DBSchema
class DBSchema(BaseModel):
    tables: list[Table] = Field(description="Contains the list of table db will have.")

# Schemaa for High Level Design 
class HLD(BaseModel):
    diagram: dict = Field(
        description="""It holds the Diagram of the LLD of the project request given by user in dict butt like JSON format for diagrams. JSON Example: {
                                "type": "SystemDesign",
                                "components": [
                                    {"name": "API Gateway", "function": "Handles external requests"},
                                    {"name": "Microservice A", "function": "Business logic"},
                                    {"name": "Database", "function": "Data storage"},
                                ],
                                "connections": [
                                    {"source": "API Gateway", "target": "Microservice A", "type": "HTTP/REST"}
                                ],
                            }"""
    )

# Schema for Low Level Design
class LLD(BaseModel):
    diagram: dict = Field(
        description="""It holds the Diagram of the LLD of the project request given by user in dict butt like JSON format for diagrams. JSON Example: {
                                "type": "SystemDesign",
                                "components": [
                                    {"name": "API Gateway", "function": "Handles external requests"},
                                    {"name": "Microservice A", "function": "Business logic"},
                                    {"name": "Database", "function": "Data storage"},
                                ],
                                "connections": [
                                    {"source": "API Gateway", "target": "Microservice A", "type": "HTTP/REST"}
                                ],
                            }"""
    )

# Schema for Entity
class Entity(BaseModel):
    entityName: str = Field(description="Name of the entitiy")

# Schema for Entities
class Entities(BaseModel):
    entities: list[Entity] = Field(description="List of entities project has")

# Main Class
class Designer:
    """Class for Designer, who prepares the system design for the project.
    It builds High Level Design (HLD) and Low Level Design (LLD) for the project.
    It will return High Level Design (HLD) and Low Level Design (LLD) of the project in JSON like Format.
    """

    @tool
    def prepareHLD(
        self, functionalRequirements: list[str], nonFunctionalRequierments: list[str]
    ) -> dict:
        """It prepares the High Level Design (HLD) diagram of the project. It will return dictionary type diagram like JSON."""
        print("Preparing High Level Design (HLD)...")
        highLevelDesign = Utils().callModel(
            HLD,
            f"""You are an expert desinger with experience of 25 years. You have to design the High Level Design of the project with each and everything involved in it. You are provided with functional and Non Functiona requirements for the project.
        Functional Requirement: {functionalRequirements}
        Non Functional Requirements: {nonFunctionalRequierments}""",
        )

        return highLevelDesign

    @tool
    def prepareLLD(
        self, functionalRequirements: list[str], nonFunctionalRequierments: list[str]
    ) -> dict:
        """It prepares the Low Level Design (LLD) diagram of the project. It will return dictionary type diagram like JSON."""
        print("Preparing Low Level Design (LLD)...")
        lowLevelDesign = Utils().callModel(
            LLD,
            f"""You are an expert desinger with experience of 25 years. You have to design the High Level Design of the project with each and everything involved in it. You are provided with functional and Non Functional requirements for the project.
                Functional Requirement: {functionalRequirements}
                Non Functional Requirements: {nonFunctionalRequierments}""",
        )

        return lowLevelDesign

    @tool
    def findEntities(self, functionalRequirements: list[str]) -> Entities:
        """It collects the entites from functional requirements given and return a list of entites."""
        print("Finding Entities...")
        entites = Utils().callModel(
            Entities,
            f"""You are an experienced designer with experience of 25 years. You have to find the entties for the project from functional requierments given below. Functional Requriements: {functionalRequirements}""",
        )

        return entites

    @tool
    def prepareDatabaseSchema(
        self, functionalRequirements: list[str], nonFunctionalRequierments: list[str]
    ) -> DBSchema:
        """It prepares the Database Schema for the project and returns it."""
        print("Preparing DB Schema...")
        schema = Utils().callModel(
            DBSchema,
            f"""You are an experienced database schema designer with experience of 25 years. You have to prepare the db schema for the project using functional and non functional requirements provided. Functional requirements: {functionalRequirements}, Non-Functional Requirements: {nonFunctionalRequierments}""",
        )
        print(f"DB Schema Prepared:\n{schema}\n")
        return schema

    @tool
    def prepareAPIStructure(
        self, functionalRequirements: list[str], nonFunctionalRequierments: list[str]
    ):
        """It prepares the API Structure for the project and returns it."""
        print("Preparing API Strucutre...")
        pass

    @tool
    def prepareCICDYamls(techStack: str) -> str:
        """It prepares the CI/CD File for Github Actions to check the code. It needs techstack to write a CI/CD Yaml File."""
        pass