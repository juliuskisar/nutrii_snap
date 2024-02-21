import requests
from app.database.schema import ExampleSchema
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi_utils.cbv import cbv
from uuid import uuid4
from app.bootstrap import ApplicationBootstrap
from app.database.repository import ExampleRepository
import settings
from datetime import datetime

router = APIRouter()

@cbv(router)
class ExampleController:
    def __init__(self):
        self.repository = ExampleRepository()

    @router.post("/test", status_code=201)
    def test(self, test: str):
        try:
            schema_object = ExampleSchema(uuid=str(uuid4()), name=test)
            bd_insert = schema_object.dict()
            self.repository.insert_example(**bd_insert)
            example = self.repository.get_example(**bd_insert)
            examples = self.repository.get_all_active_examples(name=test)
            return {
                "inserido": example.dict(),
                "todos": {
                    "total": len(examples),
                    "items": [example.dict() for example in examples]
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

