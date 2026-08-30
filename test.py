# # class Question:
# #     def __init__(self, question, answers, default_answer= None):
# #         self.question = question
# #         self.answers_to_the_question = answers
# #         self.default_answer = default_answer


# # class Questions:
# #     questions: list[Question] = []

# #     def addQuestion(self, question: str, answers: list[str]):
# #         self.questions.append(Question(question, answers))

# #     def getQuestions(self) -> list[Question]:
# #         return self.questions


# # que = Questions()
# # que.addQuestion("How are you?", ["Fine", "Not Fine", "Nothing"])
# # que.addQuestion("Why are you?", ["Means", "Yeah", "Nothing"])
# # que.addQuestion("When are you?", ["2003", "3004", "Nothing"])
# # q = que.getQuestions()

# # questionsWithUserAnswersBinding = {}
# # for question in q:
# #     print(f"Question: {question.question}")
# #     print(f"==================Answers=============")
# #     for i in range(len(question.answers_to_the_question)):
# #         print(f"{i}. {question.answers_to_the_question[i]}")
# #     answer = input("Enter options or press enter for default...\n")
# #     if len(answer) == 0:
# #         questionsWithUserAnswersBinding[question.question] = question.default_answer
# #     elif answer.isdecimal():
# #         questionsWithUserAnswersBinding[question.question] = question.answers_to_the_question[int(answer)]
# #     else:
# #         questionsWithUserAnswersBinding[question.question] = question.default_answer

# #     print(questionsWithUserAnswersBinding)
# # # Questions("Jawad" , ["Fine", "Not Fine", "Nothing"])


# SYSTEM_MESSAGE = """You are an experienced Product Manager with experience of 25 years. Your role is to process the user request and build the software requested by the user.
# User Request: """

# print(SYSTEM_MESSAGE + "I want an app!")


# from pydantic import BaseModel, Field
# from typing import List, Optional, Union


# # Define the structure for a single column
# class Column(BaseModel):
#     columnName: str = Field(description="Contains the name of column in table.")
#     columnDataType: str = Field(description="Contains the data type of column.")
#     columnLength: Optional[int] = Field(
#         description="Specifies the length of data the column can have."
#     )
#     isPrimaryKey: bool = Field(description="Tells if the column is a primary key.")
#     autoIncrement: bool = Field(
#         description="Tells if the column value will increment automatically."
#     )
#     canNull: bool = Field(
#         description="Tells if the column can have a null value (False if it cannot be null)."
#     )
#     isForeignKey: Optional[bool] = Field(
#         description="Tells if the column is a foreign key from another table."
#     )
#     referenceToForeignKey: Optional[str] = Field(
#         description="The name of the other table column this is a foreign key referencing."
#     )
#     isUnique: bool = Field(
#         description="Tells if the column will be unique (True if it is the primary key)."
#     )


# # Define the structure for a single table
# class Table(BaseModel):
#     tableName: str = Field(description="Contains the name of the table.")
#     columns: List[Column] = Field(
#         description="Contains the list of columns the table has."
#     )


# # Define the structure for the entire database schema
# class DBSchema(BaseModel):
#     tables: List[Table] = Field(
#         description="Contains the list of tables in the database schema."
#     )

from pydantic import BaseModel, Field


class Column(BaseModel):
    columnName: str = Field(description="contains the name of column in table.")
    columnDataType: str = Field(description="contains the data type of column.")
    columnLength: int | None = Field(
        description="specifies the length of data column can have."
    )
    isPrimaryKey: bool | False = Field(
        description="tell that if column is a primary key or not."
    )
    autoIncrement: bool | False = Field(
        description="tells if the column value will increment automatically."
    )
    canNull: bool | False = Field(
        description="tells if the column can have null value of not."
    )
    isForeignKey: bool | None = Field(
        description="tell if the column is a foreign key from another table."
    )
    referenceToForeignKey: str | None = Field(
        description="it is the name of another table column and will be set if the column is a foreign key"
    )
    isUnique: bool | False = Field(
        description="tells if the column will be unique, will true if column is primary key."
    )


class Table(BaseModel):
    tableName: str = Field(description="Contains the name of table.")
    columns: list[Column] = Field(description="contains the columns table have.")


class DBSchema(BaseModel):
    tables: list[Table] = Field(description="Contains the list of table db will have.")


# Example Usage:
schema_data = DBSchema(
    tables=[
        Table(
            tableName="Users",
            columns=[
                Column(
                    columnName="user_id",
                    columnDataType="INT",
                    # columnLength=20,
                    # isPrimaryKey=False,
                    # autoIncrement=False,
                    # canNull=False,
                    # isForeignKey=False,
                    # referenceToForeignKey="False",
                    # isUnique=False,
                )
            ],
        )
    ]
)
print(schema_data.tables)
