"""
-> a model to create a model (for particular task) args: model_name | ---> MODEL_OBJECT
-> a util to create file args: path, filename | ---> filePath
-> a util to create folder args: foldername | ---> folderPath
-> a util to write in file args: filename, content to write in file | ---> filePath
-> a util to create tools args: docstring for tool, arguments for tool along with their type | ---> TOOL_OBJECT
-> a util to run cmd commands and get the output args: command | ---> ouput of the command
"""

# =====================================================
# ==================== IMPORTS ========================
# =====================================================

from pydantic import BaseModel, Field

# =====================================================
# ==================== MODELS =========================
# =====================================================


# Node Structure
class TaskModel(BaseModel):
    """It is model for creating AI MODEL for specific tasks, like for coding we can create a model called CODER"""

    modelName: str = Field(description="Contains the name of model")
    role: str = Field(
        description="Tells the role of model",
        examples=[
            "CODER",
            "PLANNER",
            "CODE OPTIMIZER",
            "SYSTEM DESIGNER",
            "DEBUGGER",
            "CYBER CHECKER",
            "GIT PUSHER",
            "GIT ACTIONS CHECKER",
            "DEPLOYER",
            "TESTER",
        ],
    )
    modelWork: str = Field(description="Tells what model will do")
    

class Root:
    pass
