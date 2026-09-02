# ==============================================================================
#                      MARK4 AI SOFTWARE ENGINEERING SUITE
# ==============================================================================
# Module: test.py / Development Sandbox & Schema Verification Tests
# Description: Test harness for validating Pydantic models, prompt generation,
#              and agent utility contracts.
# ==============================================================================

"""
Mark4 Development & Schema Verification Test Harness.

This script contains verification examples for:
- Pydantic database schema models (DBSchema, Table, Column).
- Questionnaire models and options mapping.
- Prototype prompt strings for Product Manager roles.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ==============================================================================
#                      EXPERIMENTAL PROMPT PROTOTYPES (INACTIVE)
# ==============================================================================
"""
# SYSTEM_MESSAGE_PROTOTYPE = \"\"\"
# You are an experienced Product Manager with 25 years of experience. 
# Your role is to process user requests and direct software generation.
# User Request: 
# \"\"\"
"""

# ==============================================================================
#                         DATABASE SCHEMA TEST MODELS
# ==============================================================================

class Column(BaseModel):
    """
    Test Schema representing a single database table column.
    """
    columnName: str = Field(description="Contains the name of the column in table.")
    columnDataType: str = Field(description="Contains the SQL data type of the column.")
    columnLength: Optional[int] = Field(
        default=None,
        description="Specifies the max length or precision of the data column."
    )
    isPrimaryKey: bool = Field(
        default=False,
        description="Indicates if the column serves as a primary key."
    )
    autoIncrement: bool = Field(
        default=False,
        description="Indicates if column auto-increments automatically."
    )
    canNull: bool = Field(
        default=False,
        description="Indicates if the column allows NULL values."
    )
    isForeignKey: Optional[bool] = Field(
        default=False,
        description="Indicates if column is a foreign key from another table."
    )
    referenceToForeignKey: Optional[str] = Field(
        default=None,
        description="Referenced parent table and column name."
    )
    isUnique: bool = Field(
        default=False,
        description="Indicates if values must be strictly unique."
    )


class Table(BaseModel):
    """
    Test Schema representing a single database table.
    """
    tableName: str = Field(description="Contains the name of table.")
    columns: List[Column] = Field(description="Contains the list of table columns.")


class DBSchema(BaseModel):
    """
    Test Schema representing full database structure.
    """
    tables: List[Table] = Field(description="Contains the list of tables in the database schema.")


# ==============================================================================
#                            VERIFICATION EXECUTION
# ==============================================================================

def run_tests() -> None:
    """
    Instantiate and print a sample database schema to verify Pydantic model validation.
    """
    print("\n[MARK4 TEST HARNESS] Verifying Pydantic DBSchema Instantiation...\n")
    
    schema_sample = DBSchema(
        tables=[
            Table(
                tableName="Users",
                columns=[
                    Column(
                        columnName="user_id",
                        columnDataType="INT",
                        columnLength=11,
                        isPrimaryKey=True,
                        autoIncrement=True,
                        canNull=False,
                        isUnique=True
                    ),
                    Column(
                        columnName="email",
                        columnDataType="VARCHAR",
                        columnLength=255,
                        isPrimaryKey=False,
                        autoIncrement=False,
                        canNull=False,
                        isUnique=True
                    )
                ]
            )
        ]
    )

    for table in schema_sample.tables:
        print(f"Table Name: {table.tableName}")
        print("Columns:")
        for col in table.columns:
            print(f" - {col.columnName} ({col.columnDataType}): PK={col.isPrimaryKey}, Unique={col.isUnique}")
    print("\n[MARK4 TEST HARNESS] Verification Completed Successfully!\n")


if __name__ == "__main__":
    run_tests()
