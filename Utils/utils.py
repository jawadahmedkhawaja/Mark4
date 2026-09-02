# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: Utils / Shared Utilities
# Description: Helper functions for model invocation, structured output parsing,
#              and standard tools used across agent modules.
# ==============================================================================

"""
Shared Utility Functions for Mark4 Multi-Agent Framework.

This module provides common helper routines, including:
- Dynamic model initialization and invocation with optional Pydantic structured output.
- Custom LangChain tools for UI interaction and console printing.
"""

from typing import Any, Optional, Type
from os import getenv
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain.tools import tool


# ==============================================================================
#                             MODEL INVOCATION UTILS
# ==============================================================================

def callModel(structuredOutputModel: Optional[Type[BaseModel]] = None, prompt: str = "") -> Any:
    """
    Initialize and invoke the configured LLM model with an optional structured schema.

    Parameters
    ----------
    structuredOutputModel : Optional[Type[BaseModel]], default=None
        A Pydantic BaseModel class used to enforce structured output schema 
        from the LLM. If None, returns standard text response generation.
    prompt : str, default=""
        The input prompt message or instructions to send to the language model.

    Returns
    -------
    Any
        If `structuredOutputModel` is provided, returns an instance of that 
        Pydantic model containing parsed fields. Otherwise, returns a standard
        LangChain AI message response object.

    Raises
    ------
    ValueError
        If `MODEL_NAME` environment variable is not configured.
    """
    model_name = getenv("MODEL_NAME")
    if not model_name:
        raise ValueError(
            "MODEL_NAME environment variable is missing. "
            "Please configure your .env file with a valid model name (e.g., 'gpt-4o', 'gemini-1.5-pro')."
        )

    # --------------------------------------------------------------------------
    # Initialize model with or without structured output binding
    # --------------------------------------------------------------------------
    if structuredOutputModel is None:
        model = init_chat_model(model=model_name)
    else:
        model = init_chat_model(model=model_name).with_structured_output(
            structuredOutputModel
        )

    response = model.invoke(prompt)
    return response


# ==============================================================================
#                               LANGCHAIN TOOLS
# ==============================================================================

@tool
def printSomethingToTheScreen(stringToPrint: str) -> None:
    """
    Display a formatted status string or log message directly to the console output.

    Parameters
    ----------
    stringToPrint : str
        The textual content or notification message to display on screen.
    """
    if stringToPrint and len(stringToPrint.strip()) > 0:
        print(f"[MARK4 AGENT]: {stringToPrint}")
