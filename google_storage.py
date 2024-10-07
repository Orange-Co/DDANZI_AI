import os

from google.cloud import storage

import uuid
from urllib.parse import urlparse

# # 서비스 계정 인증 정보가 담긴 JSON 파일 경로
DOWNLOAD_DIR = 'ddanzi-storage'
KEY_PATH = "data/key/inspiring-folio-437200-j6-86fdd3a21261.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= KEY_PATH

bucket_name = os.getenv('BUCKET')

# Upload image to Google Cloud Storage
def upload_gcs(enhance_image):
    #Image upload to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(enhance_image)

    blob.upload_from_filename(enhance_image +".jpg")
    return "https://storage.googleapis.com/" + bucket_name + "/" + enhance_image


# Download image to Google Cloud Storage
def download_gcs(image): 
    parsed = urlparse(image)
    image_path = '/'.join(parsed.path.split('/')[2:])
    print("전처리된 이미지 경로: " + image_path)
    
    storage_client = storage.Client()
    print("storage_client: " + str(storage_client))
    bucket = storage_client.bucket(bucket_name)
    print("버킷 정보 가져오기 성공")
    
    blob = bucket.blob(image_path)
    
    image_name = image_path.split('/')[-1]
    local_file_path = os.path.join(DOWNLOAD_DIR, image_name)

    blob.download_to_filename(local_file_path)
    print("이미지 다운로드 성공")
    
    return local_file_path