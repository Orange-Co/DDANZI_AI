import os

from google.cloud import storage
from google.oauth2 import service_account

import uuid
from urllib.parse import urlparse

# # 서비스 계정 인증 정보가 담긴 JSON 파일 경로
DOWNLOAD_DIR = 'ddanzi-storage'
KEY_PATH = "data/key/indigo-splice-428205-j0-e2fd7880856c.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= KEY_PATH

bucket_name = 'ddanzi_bucket'    

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
    print("이미지 가져오기 성공")
 
    return blob


# Download image to Google Cloud Storage
def test_download_gcs(image): 
    parsed = urlparse(image)
    image_path = '/'.join(parsed.path.split('/')[2:])
    print("전처리된 이미지 경로: " + image_path)
    
    storage_client = storage.Client()
    print("storage_client: " + str(storage_client))
    bucket = storage_client.bucket(bucket_name)
    print("버킷 정보 가져오기 성공")
    
    blob = bucket.blob(image_path)
    print("이미지 가져오기 성공")
    
    # 파일명을 추출하고 다운로드 디렉토리와 결합하여 저장 경로를 생성
    image_name = image_path.split('/')[-1]
    local_file_path = os.path.join(DOWNLOAD_DIR, image_name)

    # 파일을 저장할 디렉토리가 없으면 생성
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    blob.download_to_filename(local_file_path)
    print("이미지 다운로드 성공")
    
    return local_file_path


if __name__ == "__main__":
    download_gcs('ddanzi-storage', "https://storage.googleapis.com/ddanzi_bucket/test/test1-1.png")