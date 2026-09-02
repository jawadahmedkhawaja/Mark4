# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: PLAN-2 / Meta-Agent Dynamic Architecture (Root)
# Description: Defines meta-models and configuration structures for dynamically 
#              instantiating specialized AI agents (Coders, Designers, Debuggers, Testers).
# ==============================================================================

"""
PLAN-2 Meta-Agent Root Specifications.

Provides Pydantic models for dynamic sub-agent creation, including:
- Specification of agent roles, responsibilities, and system prompts.
- Utility contracts for workspace file generation, directory creation, tool synthesis, and shell command execution.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ==============================================================================
#                             META-AGENT MODELS
# ==============================================================================

class TaskModel(BaseModel):
    """
    Pydantic schema representing a dynamic AI sub-agent definition.
    
    Used by the Meta-Orchestrator to instantiate domain-specific agents with custom system prompts
    and operational boundaries.
    """

    modelName: str = Field(
        ...,
        description="Unique identifier or name for the sub-agent (e.g., 'BackendCoder', 'DBArchitect')."
    )
    role: str = Field(
        ...,
        description="Specific engineering role assigned to the AI model.",
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
    modelWork: str = Field(
        ...,
        description="Detailed description of primary duties, task domain, and expected deliverables."
    )
    systemPrompt: Optional[str] = Field(
        default=None,
        description="Custom system prompt guiding agent behavior and operational rules."
    )


class Root:
    """
    Root controller class for managing multi-agent PLAN-2 lifecycle events.
    """
    pass
