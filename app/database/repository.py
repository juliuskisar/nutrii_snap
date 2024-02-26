from app.bootstrap import ApplicationBootstrap
from app.database.schema import ClientSchema, ExampleSchema
import settings
from datetime import datetime

class Repository:
    def __init__(self):
        self.client = ApplicationBootstrap().get_mongo_client().clients
        self.picture = ApplicationBootstrap().get_mongo_client().pictures

    def get_login(self, **kwargs):
        try:
            login = self.client.find_one(kwargs)
            return ClientSchema(**login)
        except Exception:
            return None
    
    def insert_client(self, **kwargs):
        self.client.insert_one(kwargs)
        return True

    def insert_picture(self, **kwargs):
        self.picture.insert_one(kwargs)
        return True

    def get_example(self, **kwargs) -> ExampleSchema:
        example = self.example.find_one(kwargs)
        teste = ExampleSchema(**example)
        return teste

    def get_all_active_examples(self, **kwargs) -> list:
        filter = {
            k: v for k, v in kwargs.items()
            if v is not None
            and k in ExampleSchema.__fields__.keys()
        }
        examples = self.example.find({**filter, "deleted_at": None})
        return [ExampleSchema(**example) for example in examples]

    def insert_example(self, **kwargs):
        self.example.insert_one(kwargs)
        return True
    
    def update_example(self, example_uuid: str, **kwargs):
        filter = {"uuid": example_uuid}
        self.clients.update_one(filter, {"$set": kwargs})
        return True

    def delete_exemple(self, **kwargs):
        self.example.update_one(kwargs, {"$set": {"deleted_at": datetime.now()}})
        return True
