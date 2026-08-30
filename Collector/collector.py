# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ------------------------ REQUIREMENTS COLLECTOR ---------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# ================================ IMPORTS  ==================================
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain.tools import tool
from os import getenv
from Utils.utils import Utils


class Question(BaseModel):
    question: str = Field(
        description="Question you should ask to the user to clarify the Requiremetns for the software."
    )
    answer_options_for_question: list[str] = Field(
        description="answer options for the question to ask the user. It can be none, as We can ask the user a question and user can provide the answer by themselves."
    )
    default_answer: str = Field(
        description="Default answer for the question. Used in case when user haven't answered to the question."
    )


class Questions(BaseModel):
    questions: list[Question] = Field(
        description="List of questions to ask from the user to clarify the requirements."
    )


class Requirements(BaseModel):
    functionalRequirements: list[str] = Field(
        description="Functional requirements list."
    )
    nonFunctionalRequirements: list[str] = Field(
        description="Non-Functional requirements list."
    )


class ProjectDetails(BaseModel):
    name: str = Field(description="name of the project")
    techStack: str = Field(
        description="tells the teck stack that will use for developing the project."
    )


# ===================================
# -----------------------------------
# ----------- MAIN CLASS ------------
# -----------------------------------
# ===================================


class Collector:

    # Constructor
    def __init__(self):
        self.details = ""

    @tool
    def findProjectDetials(cls, functionalRequirements: list[str]) -> dict:
        """It finds the project name using functional requirements. It will return the project detail in dictionary."""
        print("Finding Project Detials...")
        projectDetails = Utils().callModel(
            structuredOutputModel=ProjectDetails,
            prompt=f"""You are an experienced software engineer, you have to find the best suitable project details using functional requirements provided below. Functional Requirements: {functionalRequirements} """,
        )

        return projectDetails

    # Function to start collecting
    @tool
    def collect(self, requestByUser: str) -> dict[str:list]:
        """
        It collects requirements for the given project requested by the user.
        It will prepare Functional and Non-Functional Requirements.
        It will return dict of Functional and Non-Functional Requirements.
        """
        print("Collecting Requirements...")
        self.details = requestByUser

        # Generating Questions
        questionWithAnswers = self.generateQuestions()

        # Creating model with Structured Questions Model
        newModel = self.model.with_structured_output(Requirements)

        # Running model
        requirements = Utils().callModel(
            structuredOutputModel=Requirements,
            prompt=f"""
        You are an expert Product Manager or Business Analyst with a experience of 50 years. You are provided with the user request for a particular software and some questions asked to the user (for requirements clarfication) along with the answers to them.
        User Request: {self.details}
        Questions and Answers: {questionWithAnswers}.
        You have to do thorough research and prepare Functional and Non-Functional Requirements for the product request by the user.""",
        )

        # ========================= Spliting Requirements ====================================
        functionalRequirements = requirements["functionalRequirements"]
        print(f"Functional Requirements Generated:\n{functionalRequirements}\n")
        nonFunctionalRequirements = requirements["nonFunctionalRequirements"]
        print(f"Non-Functional Requirements Generated:\n{nonFunctionalRequirements}\n")

        return {
            "functionalRequirements": functionalRequirements,
            "nonFunctionalRequirements": nonFunctionalRequirements,
        }

    # Question Generator
    def generateQuestions(self) -> dict:
        """Function to generate questions to ask from the user to clarify the requirements for the software user wants. It will return a dict of questions along with user answers to the questions."""
        print("Generating Questions...")
        # Getting Questions
        q = Utils().callModel(
            structuredOutputModel=Questions,
            prompt=f"""
You are an expert Product Manager or Business Analyst with a experience of 15 years.
You have to generate questions from the details provided by the user to clarify the requirements for the software user wants.
Do thorough research and prepare questions well.
Detail Provided by the user: {self.details}.""",
        )

        questionsWithUserAnswersBinding = {}
        for question in q:
            print(f"Question: {question.question}")
            print(f"==================Answers=============")
            for i in range(len(question.answers_to_the_question)):
                print(f"{i}. {question.answers_to_the_question[i]}")
            answer = input("Enter options or press enter for default...\n")
            if len(answer) == 0:
                questionsWithUserAnswersBinding[question.question] = (
                    question.default_answer
                )
            elif answer.isdecimal():
                questionsWithUserAnswersBinding[question.question] = (
                    question.answers_to_the_question[int(answer)]
                )
            else:
                questionsWithUserAnswersBinding[question.question] = (
                    question.default_answer
                )

            return questionsWithUserAnswersBinding
