import base64
from app.database.schema import ClientSchema, PictureSchema, UploadFileInterface
from app.service.service import Service
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi_utils.cbv import cbv
from uuid import uuid4
from app.database.repository import Repository

router = APIRouter()

@cbv(router)
class Controller:
    def __init__(self):
        self.repository = Repository()
        self.service = Service()

    @router.post("/create_login", status_code=201)
    def create_login(self, email: str, password: str):
        client_uuid = f'client_{str(uuid4())}'
        client_schema = ClientSchema(
            client_uuid=client_uuid,
            email=email,
            password=password
        )
        self.repository.insert_client(**client_schema.dict())
        return {
            "client_uuid": client_uuid,
            "email": email,
        }

    @router.post("/login", status_code=201)
    def do_login(self, email: str, password: str):
        try:
            login_info = self.repository.get_login(email=email)
            if login_info:
                if login_info.password == password:
                    return {
                        "email": login_info.email,
                        "client_uuid": login_info.client_uuid
                    }
                else:
                    raise HTTPException(status_code=400, detail="Senha incorreta")
        except Exception:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")
        
    @router.post("/upload")
    def upload_file(self, picture: UploadFileInterface): #file: UploadFile = None):
        # file_content = file.file.read()
        # base64_encoded_data = base64.b64encode(file_content).decode('utf-8')
        picture_extrated_info = self.service.extract_info_from_image(picture.base64_encoded_data)
        picture_schema = PictureSchema(
            picture_uuid=f'picture_{str(uuid4())}',
            client_uuid=picture.client_uuid,
            name=picture.name,
            file_name=picture.name,
            is_healty=picture_extrated_info['saudável'],
            ingredients=picture_extrated_info['ingredientes'] if isinstance(picture_extrated_info['ingredientes'], list) else [picture_extrated_info['ingredientes']],
            total_calories=picture_extrated_info['calorias'],
            nutrients=picture_extrated_info['nutrientes'] if isinstance(picture_extrated_info['nutrientes'], list) else [picture_extrated_info['nutrientes']],
            picture_base_64=picture.base64_encoded_data
        )
        self.repository.insert_picture(**picture_schema.dict())
    
    @router.get("/get_weekly_report")
    def get_weekly_report(self):
        pass

    @router.get("/get_info/{client_uuid}")
    def get_picture_info(self, client_uuid: str, picture_uuid: str):
        pass

    @router.get("/get_meals_list")
    def get_meals_list(self, client_uuid: str):
        return self.repository.get_all_pictures(client_uuid=client_uuid)


