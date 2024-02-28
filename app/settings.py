from dotenv import load_dotenv

load_dotenv()

import os

BASIC_AUTH = {
    "BASIC_AUTH_USER": os.getenv("BASIC_AUTH_USER"),
    "BASIC_AUTH_PASSWORD": os.getenv("BASIC_AUTH_PASSWORD"),
}

JWT = {
    "JWT_SECRET": os.getenv("JWT_SECRET"),
    "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM"),
    "JWT_CREDENTIALS_USER": os.getenv("JWT_CREDENTIALS_USER"),
    "JWT_CREDENTIALS_CODE": os.getenv("JWT_CREDENTIALS_CODE"),
}

MONGO = {
    "MONGO_HOST": os.getenv("MONGO_HOST"),
    "MONGO_DATABASE": os.getenv("MONGO_DATABASE"),
}

OPEN_AI = {
    "OPENAI_API_COMPLETIONS_URL": os.getenv("OPENAI_API_COMPLETIONS_URL"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "OPENAI_API_CHAT_COMPLETIONS_URL": os.getenv("OPENAI_API_CHAT_COMPLETIONS_URL"),
}
