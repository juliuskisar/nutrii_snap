from time import sleep
import requests
import settings

import json


class Service:
    def __init__(self):
        self.openai_api_key = settings.OPEN_AI['OPENAI_API_KEY']
        self.openai_completions_url = settings.OPEN_AI['OPENAI_API_COMPLETIONS_URL']
        self.openai_chat_completions_url = settings.OPEN_AI['OPENAI_API_CHAT_COMPLETIONS_URL']

    def extract_info_from_image(self, base64_encoded_data: str, attempt: int = 0):
        if attempt > 1:
            return {'error': 'Could not extract information from image. Please try again later.'}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{PROMPT}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_encoded_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4096
        }
        # print("**************** OPENAI REQUEST ******************")

        response = requests.post(
            self.openai_chat_completions_url, headers=headers, json=payload
        )

        # print("**************** OPENAI RESPONSE ******************")
        # print(response.json())

        # parse response
        try:
            parsed_str = response.json()['choices'][0]['message']['content']
            parsed_str = parsed_str.replace("\n", "")
            parsed_str = parsed_str.replace("\t", "")
            parsed_str = parsed_str.replace("`", "")
            parsed_str = parsed_str.replace("json", "")

            # print("**************** PARSED ******************")
            # print(parsed_str)

            info = json.loads(parsed_str)
        except Exception as err:
            print("ERROR: ", err)
            print("Attempting again...")
            sleep(0.5)
            return self.extract_info_from_image(base64_encoded_data, attempt + 1)
        return info


# PROMPT = '''
#     retorne no formato json descrito a seguir as informações contidas na foto em relação aos itens do prato 
#     retorne um campo json chamado 'saudável' como true ou false em relação a se tratar de um prato saudável ou não 
#     retorne um campo json chamado 'ingredientes' com os ingredientes contidos no prato , em uma lista de ingredientes, ex: ['arroz', 'feijão', 'carne', 'legumes']
#     retorne um campo json chamado 'nutrientes' com os nutrientes contidos no prato em uma lista de strings, ex: ['vitamina A', 'vitamina C', 'ferro', 'cálcio']
#     retorne uma estimativa de valor calórico total no campo 'calorias', retorne somente o valor em calorias, ex: 500
#     se for a imagem de uma bebida devolva o mesmo formato de json, com o campo 'ingredientes' vazio e o campo 'nutrientes' vazio
#     retorne somente o json no formato descrito a seguir:
#     {
#         calorias: number;
#         ingredientes: string[];
#         nutrientes: string[];
#         saudável: boolean;
#         }
# '''

PROMPT = '''
You are a nutritionist AI bot and you need to identify the following nutritional information and comment from a picture:
	- If the dish is healthy or not
	- The ingredients of the dish
	- The total caloric value of the dish
    - A sarcastic comment about the dish

You need to return a JSON in portuguese with the following fields:
{
	"calorias": int,
	"ingredientes": list[str],
	"is_healthy": boolean,
    "comentario": str
}

For example, if the dish is a salad, return the following JSON:
{
	"calorias": 300,
	"ingredientes": ["alface", "tomate", "cenora"],
	"is_healthy": true,
    "comentario": "Wow, uma salada, que original!"
}

Another example, if the dish is a hamburger, return the following JSON:
{
	"calorias": 800,
	"ingredientes": ["carne", "pao", "queijo"],
	"is_healthy": false,
    "comentario": "Que saudável, só que não"
}
Another example, if the dish is a plate with rice, black beans and pork meat, return the following JSON:
{
	"calorias": 800,
	"ingredientes": ["carne", "arroz", "feijão"],
	"is_healthy": false,
    "comentario": "Pra onde você acha que vai tanta gordura?"
}


Only respond with a JSON, absolutely do not include any other information.
'''
