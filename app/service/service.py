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
        # response = requests.post(settings.OPEN_AI["OPENAI_API_CHAT_COMPLETIONS_URL"], headers=headers, json=payload)
        # ajusting response
        try:
            # content = response.json()['choices'][0]['message']['content']
            # cleaned_string = content.strip('`')
            # cleaned_string = '\n'.join(cleaned_string.split('\n')[1:])
            # cleaned_string = cleaned_string.rsplit('\n', 1)[0]
            # info = json.loads(cleaned_string)
            info = RESPONSE_MOCK
        except json.JSONDecodeError as err:
            pass
        except Exception as err:
            pass
        return info
        

PROMPT = '''
    retorne as informações contidas na foto em relação aos itens do prato 
    retorne um campo json chamado 'saudável' como true ou false em relação a se tratar de um prato saudável ou não 
    retorne um campo json chamado 'composição' com os ingredientes contidos no prato 
    retorne um campo json chamado 'nutrientes' com os nutrientes contidos no prato
    retorne uma estimativa de valor calórico total no campo 'calorias' 
    só retorne o json
'''


RESPONSE_MOCK = {'saudável': True, 'composição': {'arroz': 'Arroz branco', 'carne': 'Bife de carne bovina', 'feijão': 'Feijão cozido', 'legumes': ['Tomate', 'Alface']}, 'nutrientes': {'carboidratos': 'Arroz', 'proteínas': ['Carne bovina', 'Feijão'], 'fibras': ['Feijão', 'Alface', 'Tomate'], 'vitaminas': ['Tomate', 'Alface'], 'minerais': ['Feijão', 'Carne bovina', 'Alface', 'Tomate']}, 'calorias': 'Aproximadamente 500-700 calorias'}