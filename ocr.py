
import os
import requests
import uuid
import time
import json

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('CLOVA_SECRET_KEY')
API_URL = os.getenv('CLOVA_API_INVOKE_URL')


# 네이버 OCR API를 사용해 이미지를 텍스트로 변환하는 함수
def get_text_from_image(image_url):

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(image_url,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': SECRET_KEY
    }

    response = requests.request("POST", API_URL, headers=headers, data = payload, files = files)
    
    text = ""
    for i in response.json()['images'][0]['fields']:
        text = text + " " + i['inferText']
    print(text)
    
    return text

if __name__ == "__main__":
    get_text_from_image("ddanzi-storage/test1-1.png")