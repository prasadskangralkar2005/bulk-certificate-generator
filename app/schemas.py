from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr, Field


class RecipientCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr


class JobCreate(BaseModel):
    event_name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    event_date: date

    recipients: List[RecipientCreate] = Field(
        ...,
        min_length=1
    )