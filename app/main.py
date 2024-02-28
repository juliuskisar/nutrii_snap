from loguru import logger

from fastapi import Depends, FastAPI
import app.controllers.controller as Controller

from starlette.responses import RedirectResponse



# from security.jwt_security import jwt_auth
# from security.basic_security import basic_auth
# from security.keys_security import api_key

# from middleware.sample_middleware import SampleMiddleware


# logger.add("./logs/file_app.log", rotation="1 MB")

# tags_metadata = [
#     {
#         "name": "Example",
#         "description": "Example Route"
#     },
#     {
#         "name": "Example 2",
#         "description": "Exampljhkjhkjhe Route"
#     },
# ]


app = FastAPI(
    title="FastAPI",
    description="",
    version="0.75.2",
    # openapi_tags=tags_metadata
)

@app.get("/", tags=["Home"])
async def redirect():
    response = RedirectResponse(url='/docs')
    return response

app.include_router(
    Controller.router,
    prefix="/nutrii",
    tags=["Nutrii Route"],
    # dependencies=[Depends(api_key)],
)
