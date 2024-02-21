from app.bootstrap import ApplicationBootstrap
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CustomBaseModel(BaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExampleSchema(CustomBaseModel):
    uuid: str
    name: str
