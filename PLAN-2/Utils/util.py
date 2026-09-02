# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: PLAN-2 / Utilities & Execution Helpers
# Description: Helper routines for running shell commands, file manipulation, and directory management.
# ==============================================================================

"""
PLAN-2 Execution Utilities.

Provides system utilities for managing workspace files, executing terminal commands,
and capturing command stdout/stderr output.
"""

import os
import subprocess
from typing import Tuple


class Util:
    """
    Utility class for system execution and workspace management routines.
    """

    @staticmethod
    def executeCommand(command: str, cwd: str = ".") -> Tuple[int, str, str]:
        """
        Execute a shell command asynchronously or synchronously and capture output.

        Parameters
        ----------
        command : str
            The CLI command line string to execute.
        cwd : str, default="."
            Current working directory context for execution.

        Returns
        -------
        Tuple[int, str, str]
            Tuple containing (return_code, stdout_output, stderr_output).
        """
        print(f"\n[PLAN-2 UTIL] Running Command: '{command}' in '{cwd}'...")
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    @staticmethod
    def createFile(filePath: str, content: str = "") -> bool:
        """
        Create a file at the specified path and write initial text content into it.

        Parameters
        ----------
        filePath : str
            Target file system path.
        content : str, default=""
            Text content to write into the file.

        Returns
        -------
        bool
            True if file creation succeeded, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[PLAN-2 UTIL] Created File: {filePath}")
            return True
        except Exception as e:
            print(f"[PLAN-2 UTIL ERROR] Failed to create file '{filePath}': {e}")
            return False