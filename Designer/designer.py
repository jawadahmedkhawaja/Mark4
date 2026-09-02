# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: Designer / System Architecture & Design Tools
# Description: Generates High-Level Design (HLD), Low-Level Design (LLD),
#              Domain Entities, 3NF Database Schemas, API Structures, and CI/CD YAML pipelines.
# ==============================================================================

"""
Designer Module for Mark4 AI SWE Framework.

Provides Pydantic schemas and LangChain tools for:
- High-Level Architecture (HLD) diagram JSON generation.
- Low-Level Architecture (LLD) component diagram JSON generation.
- Extraction of domain entities and relationships.
- Relational Database Schema generation (Tables, Columns, Primary/Foreign Keys).
- REST API endpoint structure definition.
- GitHub Actions CI/CD workflow YAML generation.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.tools import tool
from Utils.utils import callModel


# ==============================================================================
#                             DATABASE SCHEMAS
# ==============================================================================

class Column(BaseModel):
    """
    Schema representing a single database table column definition.
    """
    columnName: str = Field(
        ...,
        description="The exact name of the column in the database table (e.g., 'user_id', 'created_at')."
    )
    columnDataType: str = Field(
        ...,
        description="SQL data type (e.g., 'VARCHAR', 'INTEGER', 'TIMESTAMP', 'BOOLEAN', 'UUID')."
    )
    columnLength: Optional[int] = Field(
        default=None,
        description="Maximum storage length or precision for column data (if applicable)."
    )
    isPrimaryKey: bool = Field(
        default=False,
        description="Flag indicating whether this column serves as the Primary Key for the table."
    )
    autoIncrement: bool = Field(
        default=False,
        description="Flag indicating whether the column auto-increments upon new record creation."
    )
    canNull: bool = Field(
        default=False,
        description="Flag indicating whether NULL values are permitted in this column."
    )
    isForeignKey: Optional[bool] = Field(
        default=False,
        description="Flag indicating whether this column references a Foreign Key in another table."
    )
    referenceToForeignKey: Optional[str] = Field(
        default=None,
        description="Referenced parent table and column in 'TableName.ColumnName' format if foreign key."
    )
    isUnique: bool = Field(
        default=False,
        description="Flag indicating whether values in this column must be strictly unique."
    )


class Table(BaseModel):
    """
    Schema representing a database table containing a list of columns.
    """
    tableName: str = Field(
        ...,
        description="Name of the relational database table (e.g., 'users', 'orders', 'payments')."
    )
    columns: List[Column] = Field(
        default_factory=list,
        description="List of column definitions constituting the table schema."
    )


class DBSchema(BaseModel):
    """
    Schema representing the complete relational database schema for the application.
    """
    tables: List[Table] = Field(
        default_factory=list,
        description="Complete collection of relational database tables for the project."
    )


# ==============================================================================
#                            ARCHITECTURE SCHEMAS
# ==============================================================================

class HLD(BaseModel):
    """
    High-Level Architecture Design Schema (JSON structured system diagram).
    """
    diagram: Dict[str, Any] = Field(
        ...,
        description="""
JSON object containing system architecture components and communication links.
Example:
{
    "type": "SystemDesign",
    "components": [
        {"name": "API Gateway", "function": "Request routing and authentication"},
        {"name": "Auth Service", "function": "JWT issuing and user verification"},
        {"name": "Database", "function": "PostgreSQL persistent store"}
    ],
    "connections": [
        {"source": "API Gateway", "target": "Auth Service", "type": "gRPC/HTTP"}
    ]
}
"""
    )


class LLD(BaseModel):
    """
    Low-Level Architecture Design Schema (JSON structured module & class details).
    """
    diagram: Dict[str, Any] = Field(
        ...,
        description="""
JSON object containing detailed module structure, sequence interactions, and class relationships.
Example:
{
    "type": "LowLevelDesign",
    "modules": [
        {"name": "UserController", "methods": ["register()", "login()"]},
        {"name": "UserRepository", "methods": ["findById()", "save()"]}
    ],
    "data_flow": [
        {"from": "UserController", "to": "UserRepository", "action": "persist entity"}
    ]
}
"""
    )


class Entity(BaseModel):
    """
    Schema representing a single domain entity in the system domain model.
    """
    entityName: str = Field(
        ...,
        description="Name of the domain entity (e.g., 'User', 'Product', 'Order', 'Invoice')."
    )
    attributes: List[str] = Field(
        default_factory=list,
        description="Core properties and attributes associated with this entity."
    )


class Entities(BaseModel):
    """
    Schema containing the set of domain entities extracted from requirements.
    """
    entities: List[Entity] = Field(
        default_factory=list,
        description="Collection of domain entities identified for the application."
    )


class APIEndpoint(BaseModel):
    """
    Schema describing an individual REST API Endpoint.
    """
    method: str = Field(..., description="HTTP Method (GET, POST, PUT, DELETE, PATCH).")
    path: str = Field(..., description="Endpoint URI path (e.g., '/api/v1/users/{id}').")
    description: str = Field(..., description="Summary of what the API endpoint performs.")
    requestBody: Optional[str] = Field(default=None, description="Description or JSON sample of request body.")
    responsePayload: str = Field(..., description="Description or JSON sample of successful response payload.")


class APIStructure(BaseModel):
    """
    Schema representing the complete API contract for the application.
    """
    endpoints: List[APIEndpoint] = Field(
        default_factory=list,
        description="Collection of RESTful API endpoint specifications."
    )


# ==============================================================================
#                               LANGCHAIN TOOLS
# ==============================================================================

@tool
def prepareHLD(functionalRequirements: List[str], nonFunctionalRequierments: List[str]) -> Dict[str, Any]:
    """
    Generate High-Level System Architecture (HLD) diagram specifications in JSON format.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirements for the software project.
    nonFunctionalRequierments : List[str]
        List of non-functional requirements for the software project.

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of High-Level Design components, services, gateways, and communication links.
    """
    print("\n[MARK4 DESIGNER] Architecting High-Level System Design (HLD)...")

    prompt = f"""
You are a Principal Cloud Architect with 25+ years of software architecture experience.

Task:
Design a robust High-Level System Architecture (HLD) for a software application fulfilling the requirements below.

Functional Requirements:
{functionalRequirements}

Non-Functional Requirements:
{nonFunctionalRequierments}

Instructions:
Construct a JSON structure containing:
- "type": "SystemDesign"
- "components": List of key services, load balancers, caching layers, databases, and message queues with their core responsibility.
- "connections": List of communication flows showing source, target, and protocol (e.g., HTTP/REST, gRPC, WebSocket, AMQP).
"""

    hld_result: HLD = callModel(
        structuredOutputModel=HLD,
        prompt=prompt
    )

    result = hld_result.diagram if hld_result else {"type": "SystemDesign", "components": [], "connections": []}
    print("[MARK4 DESIGNER] HLD Generation Complete.")
    return result


@tool
def prepareLLD(functionalRequirements: List[str], nonFunctionalRequierments: List[str]) -> Dict[str, Any]:
    """
    Generate Low-Level Component Design (LLD) specifications in JSON format.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirements for the software project.
    nonFunctionalRequierments : List[str]
        List of non-functional requirements for the software project.

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of Low-Level Design modules, controllers, repositories, data flows, and class designs.
    """
    print("\n[MARK4 DESIGNER] Architecting Low-Level Component Design (LLD)...")

    prompt = f"""
You are a Senior Principal Software Engineer specializing in Object-Oriented and Modular Software Design.

Task:
Create a Low-Level Design (LLD) specification outlining class hierarchies, controller-service-repository patterns, and data flow.

Functional Requirements:
{functionalRequirements}

Non-Functional Requirements:
{nonFunctionalRequierments}

Instructions:
Construct a JSON structure containing:
- "type": "LowLevelDesign"
- "modules": List of internal application modules, classes, methods, and responsibilities.
- "data_flow": Internal sequence steps illustrating how requests move between components.
"""

    lld_result: LLD = callModel(
        structuredOutputModel=LLD,
        prompt=prompt
    )

    result = lld_result.diagram if lld_result else {"type": "LowLevelDesign", "modules": [], "data_flow": []}
    print("[MARK4 DESIGNER] LLD Generation Complete.")
    return result


@tool
def findEntities(functionalRequirements: List[str]) -> Dict[str, Any]:
    """
    Extract core domain entities and key attributes from functional requirements.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirements for the software application.

    Returns
    -------
    Dict[str, Any]
        Dictionary listing identified domain entities and their associated key attributes.
    """
    print("\n[MARK4 DESIGNER] Extracting Domain Entities...")

    prompt = f"""
You are a Domain-Driven Design (DDD) Expert.

Task:
Analyze the given functional requirements and identify all primary business domain entities, aggregate roots, and key attributes.

Functional Requirements:
{functionalRequirements}
"""

    entities_result: Entities = callModel(
        structuredOutputModel=Entities,
        prompt=prompt
    )

    result = entities_result.dict() if entities_result else {"entities": []}
    print(f"[MARK4 DESIGNER] Identified {len(result.get('entities', []))} Domain Entities.")
    return result


@tool
def prepareDatabaseSchema(functionalRequirements: List[str], nonFunctionalRequierments: List[str]) -> Dict[str, Any]:
    """
    Prepare a Third-Normal-Form (3NF) relational database schema including tables, columns, primary keys, and foreign keys.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirements for the software application.
    nonFunctionalRequierments : List[str]
        List of non-functional requirements for the software application.

    Returns
    -------
    Dict[str, Any]
        Structured relational database schema containing table definitions, data types, constraints, and relationships.
    """
    print("\n[MARK4 DESIGNER] Designing 3NF Relational Database Schema...")

    prompt = f"""
You are an expert Database Architect with 25+ years of experience designing high-throughput relational databases.

Task:
Create a normalized (3NF) relational database schema supporting the software requirements below.

Functional Requirements:
{functionalRequirements}

Non-Functional Requirements:
{nonFunctionalRequierments}

Instructions:
- Define all required tables.
- Specify precise column data types, nullability, auto-increment rules, primary keys, and unique constraints.
- Define foreign key references explicitly using 'ParentTable.ColumnName' notation.
"""

    schema_result: DBSchema = callModel(
        structuredOutputModel=DBSchema,
        prompt=prompt
    )

    result = schema_result.dict() if schema_result else {"tables": []}
    print(f"[MARK4 DESIGNER] Generated Database Schema with {len(result.get('tables', []))} tables.")
    return result


@tool
def prepareAPIStructure(functionalRequirements: List[str], nonFunctionalRequierments: List[str]) -> Dict[str, Any]:
    """
    Design a RESTful API specification detailing endpoint routes, HTTP methods, request bodies, and responses.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirements for the software application.
    nonFunctionalRequierments : List[str]
        List of non-functional requirements for the software application.

    Returns
    -------
    Dict[str, Any]
        JSON object listing endpoints, HTTP verbs, paths, descriptions, and request/response specifications.
    """
    print("\n[MARK4 DESIGNER] Specifying RESTful API Architecture...")

    prompt = f"""
You are a Principal API Architect.

Task:
Design a clean, RESTful API structure adhering to OpenAPI / Swagger best practices.

Functional Requirements:
{functionalRequirements}

Non-Functional Requirements:
{nonFunctionalRequierments}

Instructions:
Define endpoints for all necessary CRUD and business operations, including HTTP methods, paths, request payloads, and status codes.
"""

    api_result: APIStructure = callModel(
        structuredOutputModel=APIStructure,
        prompt=prompt
    )

    result = api_result.dict() if api_result else {"endpoints": []}
    print(f"[MARK4 DESIGNER] Prepared API Structure with {len(result.get('endpoints', []))} endpoints.")
    return result


@tool
def prepareCICDYamls(techStack: str) -> str:
    """
    Generate a complete GitHub Actions CI/CD workflow YAML pipeline file for automated testing, linting, and deployment.

    Parameters
    ----------
    techStack : str
        The primary technology stack of the application (e.g., 'Python / FastAPI / PostgreSQL', 'Node.js / Express').

    Returns
    -------
    str
        Production-ready YAML configuration string for GitHub Actions CI/CD.
    """
    print(f"\n[MARK4 DESIGNER] Generating GitHub Actions CI/CD YAML for tech stack: '{techStack}'...")

    prompt = f"""
You are a Principal DevOps & Site Reliability Engineer (SRE).

Task:
Write a complete, production-grade GitHub Actions CI/CD YAML configuration file (`.github/workflows/main.yml`) tailored for a project using the tech stack: "{techStack}".

Requirements:
- Include workflow triggers (on push and pull_request to main branch).
- Steps for checkout, environment setup, dependency caching, linting, unit testing, building, and deployment steps.
- Return raw valid YAML text.
"""

    yaml_response = callModel(
        structuredOutputModel=None,
        prompt=prompt
    )

    yaml_text = yaml_response.content if hasattr(yaml_response, 'content') else str(yaml_response)
    print("[MARK4 DESIGNER] CI/CD Pipeline YAML Generated.")
    return yaml_text
