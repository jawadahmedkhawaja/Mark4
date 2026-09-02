# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: Collector / Requirements Gathering Agent & Tools
# Description: Interactively clarifies user software requests, generates Q&A options,
#              extracts functional and non-functional requirements, and determines tech stacks.
# ==============================================================================

"""
Collector Module for Mark4 AI SWE Framework.

Provides Pydantic schemas and LangChain tools for:
- Asking interactive clarification questions to users.
- Generating Functional & Non-Functional Software Requirements.
- Analyzing technical requirements to infer project details and tech stacks.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from langchain.tools import tool
from Utils.utils import callModel


# ==============================================================================
#                             PYDANTIC SCHEMAS
# ==============================================================================

class Question(BaseModel):
    """
    Schema for a single clarifying question presented to the user.
    """
    question: str = Field(
        ...,
        description="The clarification question to ask the user regarding system scope, features, or constraints."
    )
    answer_options_for_question: List[str] = Field(
        default_factory=list,
        description="List of suggested multiple-choice answer options for the user to choose from. Can be empty."
    )
    default_answer: str = Field(
        ...,
        description="Recommended fallback answer to use if the user skips or provides empty input."
    )


class Questions(BaseModel):
    """
    Schema containing a structured list of clarifying questions.
    """
    questions: List[Question] = Field(
        default_factory=list,
        description="A targeted list of clarification questions generated to resolve ambiguities in software requirements."
    )


class Requirements(BaseModel):
    """
    Schema containing structured Functional and Non-Functional software requirements.
    """
    functionalRequirements: List[str] = Field(
        default_factory=list,
        description="Detailed list of specific system capabilities, user features, and operational behaviors."
    )
    nonFunctionalRequirements: List[str] = Field(
        default_factory=list,
        description="Detailed list of system performance, security, availability, scalability, and compliance specifications."
    )


class ProjectDetails(BaseModel):
    """
    Schema containing inferred project metadata and technical architecture choices.
    """
    name: str = Field(
        ...,
        description="Appropriate, professional software project name inferred from functional requirements."
    )
    techStack: str = Field(
        ...,
        description="Recommended technology stack (e.g., Python/FastAPI/PostgreSQL, Node.js/React/MongoDB, etc.)."
    )


# ==============================================================================
#                               HELPER ROUTINES
# ==============================================================================

def generateQuestions(user_request: str) -> Dict[str, str]:
    """
    Generate targeted requirement clarification questions, prompt the user for responses,
    and map user choices back to key requirements.

    Parameters
    ----------
    user_request : str
        The initial software request string submitted by the user.

    Returns
    -------
    Dict[str, str]
        A dictionary mapping each generated question to the corresponding answer selected or provided by the user.
    """
    print("\n[MARK4 COLLECTOR] Analyzing project scope and generating clarification questions...")

    prompt = f"""
You are an Principal Business Analyst & Software Architect with 25+ years of software consulting experience.

Task:
Analyze the following user software request and generate 3 to 5 critical clarification questions to resolve ambiguities regarding core features, data constraints, user roles, and scale.

User Request: "{user_request}"

Instructions:
- Formulate clear, concise questions.
- Provide 3 realistic multiple-choice options per question when applicable.
- Specify a sensible default answer for each question if the user skips it.
"""

    structured_questions: Questions = callModel(
        structuredOutputModel=Questions,
        prompt=prompt
    )

    questions_with_answers: Dict[str, str] = {}

    if not structured_questions or not structured_questions.questions:
        print("[MARK4 COLLECTOR] No explicit clarification questions required. Proceeding...")
        return questions_with_answers

    print("\n" + "=" * 60)
    print("           REQUIREMENT CLARIFICATION QUESTIONNAIRE")
    print("=" * 60)

    for idx, q in enumerate(structured_questions.questions, 1):
        print(f"\nQuestion {idx}: {q.question}")
        options = q.answer_options_for_question

        if options:
            print("Options:")
            for opt_idx, opt in enumerate(options):
                print(f"  [{opt_idx}] {opt}")
            print(f"  (Default: '{q.default_answer}')")

        user_input = input("\nEnter option number, custom text, or press Enter for default: ").strip()

        if not user_input:
            questions_with_answers[q.question] = q.default_answer
            print(f"-> Selected Default: {q.default_answer}")
        elif user_input.isdigit() and options and 0 <= int(user_input) < len(options):
            selected_option = options[int(user_input)]
            questions_with_answers[q.question] = selected_option
            print(f"-> Selected: {selected_option}")
        else:
            questions_with_answers[q.question] = user_input
            print(f"-> Custom Response Saved: {user_input}")

    print("=" * 60 + "\n")
    return questions_with_answers


# ==============================================================================
#                               LANGCHAIN TOOLS
# ==============================================================================

@tool
def findProjectDetials(functionalRequirements: List[str]) -> Dict[str, Any]:
    """
    Analyze functional requirements to suggest an optimal project name and technology stack.

    Parameters
    ----------
    functionalRequirements : List[str]
        List of functional requirement specifications for the software product.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing 'name' (Project Name) and 'techStack' (Recommended Tech Stack).
    """
    print("\n[MARK4 COLLECTOR] Evaluating optimal project architecture and technology stack...")

    prompt = f"""
You are a Lead Software Architect.
Analyze the functional requirements provided below and recommend:
1. A concise, professional project name.
2. An industry-standard, production-grade tech stack best suited for these requirements.

Functional Requirements:
{functionalRequirements}
"""

    project_details: ProjectDetails = callModel(
        structuredOutputModel=ProjectDetails,
        prompt=prompt
    )

    result = {
        "name": project_details.name if project_details else "SoftwareProject",
        "techStack": project_details.techStack if project_details else "Python / FastAPI / PostgreSQL"
    }
    print(f"[MARK4 COLLECTOR] Identified Project: {result['name']} | Tech Stack: {result['techStack']}")
    return result


@tool
def collect(requestByUser: str) -> Dict[str, List[str]]:
    """
    Collect, clarify, and formulate detailed Functional and Non-Functional Requirements for a user project request.

    Parameters
    ----------
    requestByUser : str
        The raw request or description of the software application requested by the user.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary containing two keys:
        - 'functionalRequirements': List of functional system behaviors and user features.
        - 'nonFunctionalRequirements': List of quality attributes (performance, security, scalability, maintenance).
    """
    print(f"\n[MARK4 COLLECTOR] Starting Requirements Gathering Process for: '{requestByUser}'...")

    # Step 1: Conduct interactive clarification Q&A session
    clarifications = generateQuestions(requestByUser)

    # Step 2: Generate comprehensive SRS (Software Requirements Specification) via LLM
    prompt = f"""
You are an expert Chief Product Officer & Senior Business Analyst with 25+ years of experience.

Task:
Transform the raw user request and clarified Q&A responses into a structured Software Requirements Specification (SRS).

Input Details:
- Initial User Request: "{requestByUser}"
- Clarification Q&A Context: {clarifications}

Guidelines:
1. Functional Requirements:
   - Define exhaustive, granular features covering user roles, authentication, data processing, APIs, and workflows.
   - Each item must be actionable, clear, and testable.
2. Non-Functional Requirements:
   - Specify strict standards for performance (response times, latency), security (encryption, auth protocols), scalability, availability, and error handling.
"""

    requirements_output: Requirements = callModel(
        structuredOutputModel=Requirements,
        prompt=prompt
    )

    func_reqs = requirements_output.functionalRequirements if requirements_output else []
    non_func_reqs = requirements_output.nonFunctionalRequirements if requirements_output else []

    print(f"\n[MARK4 COLLECTOR] Requirements Gathering Completed!")
    print(f" -> Functional Requirements ({len(func_reqs)} items)")
    print(f" -> Non-Functional Requirements ({len(non_func_reqs)} items)\n")

    return {
        "functionalRequirements": func_reqs,
        "nonFunctionalRequirements": non_func_reqs
    }
