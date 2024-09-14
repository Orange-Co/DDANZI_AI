from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from cache import load_product_data, invalidate_cache
from google_storage import download_gcs
from ocr import get_text_from_image
from calculate_similarity import get_most_similar_index

app = FastAPI()

class Image(BaseModel): 
    image_url: str


@app.post("/test/image")
def gcs_test(image: Image):
    image = download_gcs(image.image_url)
    return {"result_image_url": image}


@app.post("/api/v1/image")
async def cal_most_similar_prod(image: Image, db: Session = Depends(get_db)):
    # 캐싱된 데이터 로드
    data = load_product_data(db)
    
    # 이미지 다운로드
    image = download_gcs(image.image_url)
    
    # 네이버 OCR API를 호출해 텍스트 추출
    ocr_text = get_text_from_image(image)
    print(f"OCR로 추출한 텍스트: {ocr_text}")
    
    # 가장 유사한 인덱스 찾기
    most_similar_index = get_most_similar_index(ocr_text, data)
    
    print(f"가장 유사한 데이터의 인덱스는: {most_similar_index} 입니다.")
    print(f"해당 데이터: {data[most_similar_index]}")

    product_id =  data[most_similar_index]['product_id']

    return {"productId": product_id}


# 캐시 무효화 
@app.post("/api/v1/cache/invalidate")
def cache_invalidate():
    invalidate_cache()
    return {"message": "캐시가 성공적으로 무효화되었습니다."}