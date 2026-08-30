from langchain.chat_models import init_chat_model
from langchain.tools import tool
from os import getenv
from pydantic import BaseModel


class Utils:

    def callModel(self, structuredOutputModel: BaseModel | None, prompt: str):
        if structuredOutputModel == None:
            model = init_chat_model(model=getenv("MODEL_NAME"))
        else:
            model = init_chat_model(model=getenv("MODEL_NAME")).with_structured_output(
                structuredOutputModel
            )

        response = model.invoke(prompt)
        return response

    # Tool to print something to print to the screen
    @tool
    def printSomethingToTheScreen(self, stringToPrint: str) -> None:
        """It will print something on the screen, It takes string to be printed on the screen."""
        if len(stringToPrint) > 0:
            print(stringToPrint)



