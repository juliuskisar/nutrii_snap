from collections import Counter
import sys
from app.database.schema import ClientSchema, PictureSchema, ReportInterface, UploadFileInterface
from app.service.service import Service
from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from uuid import uuid4
from app.database.repository import Repository
from app.utils.compress_image import compress_image

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
                    raise HTTPException(
                        status_code=400, detail="Senha incorreta")
        except Exception:
            raise HTTPException(
                status_code=400, detail="Usuário não encontrado")

    @router.post("/upload")
    def upload_file(self, picture: UploadFileInterface):
        # print("**************** COMPRESSING ******************")
        # print(
        #     f"Original size: {sys.getsizeof(picture.base64_encoded_data) / 1024}")

        image_compressed = compress_image(
            base64_image=picture.base64_encoded_data,
            max_size=400,
            quality=70
        )

        # print(f"Compressed size: {sys.getsizeof(image_compressed) / 1024}")

        picture_extrated_info = self.service.extract_info_from_image(
            image_compressed
        )

        # Parse extracted info with defaults
        is_healthy = picture_extrated_info.get('is_healthy', False)
        is_healthy = is_healthy if isinstance(is_healthy, bool) else False

        ingredients = picture_extrated_info.get('ingredientes', ['ar'])
        ingredients = ingredients if isinstance(ingredients, list) else ['ar']

        total_calories = picture_extrated_info.get('calorias', 123)
        total_calories = total_calories if isinstance(
            total_calories, int) else 123

        comment = picture_extrated_info.get('comentario', 'Wow, que original')
        comment = comment if isinstance(comment, str) else 'Wow, que original'

        picture_schema = PictureSchema(
            picture_uuid=f'picture_{str(uuid4())}',
            client_uuid=picture.client_uuid,
            name=picture.name,
            file_name=picture.name,
            is_healthy=is_healthy,
            ingredients=ingredients,
            total_calories=total_calories,
            nutrients=[],
            picture_base_64=image_compressed,
            comment=comment
        )

        # print("**************** FINAL OUTPUT ******************")
        # print(f"Name: {picture_schema.name}")
        # print(f"Is healthy: {picture_schema.is_healthy}")
        # print(f"Ingredients: {picture_schema.ingredients}")
        # print(f"Total calories: {picture_schema.total_calories}")
        # print(f"Comment: {picture_schema.comment}")

        self.repository.insert_picture(**picture_schema.dict())

    @router.get("/get_weekly_report")
    def get_weekly_report(self):
        meals = self.repository.get_all_pictures()
        healthy_counter = Counter([meal.is_healthy for meal in meals])
        total_calories = sum([int(meal.total_calories) for meal in meals])
        average_calories = total_calories / len(meals)
        return ReportInterface(
            healthy_meals=healthy_counter[True],
            total_meals=len(meals),
            unhealthy_meals=healthy_counter[False],
            total_calories=total_calories,
            average_calories=average_calories
        )

    @router.get("/get_info/{client_uuid}")
    def get_picture_info(self, client_uuid: str, picture_uuid: str):
        pass

    @router.get("/get_meals_list")
    def get_meals_list(self, client_uuid: str):
        return self.repository.get_all_pictures(client_uuid=client_uuid)

    @router.get("/get_pic_sizes")
    def get_pic_sizes(self, client_uuid: str):
        pics = self.repository.get_all_pictures(client_uuid=client_uuid)
        string = [
            f"{p.name}=>{sys.getsizeof(p.picture_base_64) / 1024}" for p in pics]
        for each in string:
            print(each)
        return string
