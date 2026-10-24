from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, FiniteFloat, StringConstraints

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RegisterInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class ProjectInput(Input):
    name: Name
    description: str = Field(default="", max_length=2000)


class ProjectOut(ProjectInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ExperimentInput(Input):
    name: Name
    model: Name
    dataset_version: Name
    metric_name: Annotated[str, StringConstraints(min_length=1, max_length=60)]
    metric_value: FiniteFloat
    notes: str = Field(default="", max_length=4000)


class ExperimentOut(ExperimentInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    created_at: datetime
