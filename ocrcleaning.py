import openai
import os
from dotenv import load_dotenv

class OcrCleaning:
    def __init__(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        openai.api_key = OPENAI_API_KEY

    def process_text(self, text):
        message = {
            "role": "user",
            "content": f"Como um analisador de dados experiente, limpe esse texto retirado de um ocr de um stories do instagram e retorne somente o texto limpo no formato utf8 e que fique de forma coerente com a lingua portuguesa: {text}"
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[message]
        )

        return response['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')
