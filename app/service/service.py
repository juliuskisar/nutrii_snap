import requests
import settings

import json


class Service:
    def __init__(self):
        self.openai_api_key = settings.OPEN_AI['OPENAI_API_KEY']
        self.openai_completions_url = settings.OPEN_AI['OPENAI_API_COMPLETIONS_URL']
        self.openai_chat_completions_url = settings.OPEN_AI['OPENAI_API_CHAT_COMPLETIONS_URL']

    def extract_info_from_image(self, base64_encoded_data: str):
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
        response = requests.post(
            settings.OPEN_AI["OPENAI_API_CHAT_COMPLETIONS_URL"], headers=headers, json=payload)

        with open("./response.txt", 'w') as f:
            f.write(str(response.json()))

        print(response.json())
        # ajusting response
        try:
            content = response.json()['choices'][0]['message']['content']
            cleaned_string = content.strip('`')
            cleaned_string = '\n'.join(cleaned_string.split('\n')[1:])
            cleaned_string = cleaned_string.rsplit('\n', 1)[0]
            info = json.loads(cleaned_string)
        except Exception as err:
            raise err
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
You are a nutritionist AI bot and you need to identify the following nutritional information from a picture:
	- If the dish is healthy or not
	- The ingredients of the dish
	- The total caloric value of the dish

You need to return a JSON with the following fields:
{
	"calories": int,
	"ingredients": list[str],
	"is_healthy": boolean,
}

For example, if the dish is a salad, return the following JSON:
{
	"calories": 300,
	"ingredients": ["lettuce", "tomato", "carrot"],
	"is_healthy": true,
}

Another example, if the dish is a hamburger, return the following JSON:
{
	"calories": 800,
	"ingredients": ["meat", "bread", "cheese"],
	"is_healthy": false,
}

Only respond with a JSON, absolutely do not include any other information.
'''
