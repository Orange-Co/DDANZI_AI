import pandas as pd
import logging
from urllib.parse import unquote
from pydantic import BaseModel
from fastapi import FastAPI

from google_storage import download_gcs
from ocr import get_text_from_image
from calculate_similarity import get_most_similar_index


app = FastAPI()

class Image(BaseModel): 
    image_url: str


@app.get("/")
async def test():
    return {"message": "Hello World"}

@app.post("/test/image")
def gcs_test(image: Image):
    image = download_gcs(image.image_url)
    return {"result_image_url": image}


@app.post("/api/v1/image")
async def cal_most_similar_prod(image: Image):
    # CSV 파일에서 데이터를 로드
    data = pd.read_csv('data/src/products_0827_12.csv', dtype={'product_id': str})
    print("데이터가 성공적으로 로드되었습니다.")
    
    # 이미지 다운로드
    image = download_gcs(image.image_url)
    
    # 네이버 OCR API를 호출해 텍스트 추출
    ocr_text = get_text_from_image(image)
    print(f"OCR로 추출한 텍스트: {ocr_text}")
    
    # 가장 유사한 인덱스 찾기
    most_similar_index = get_most_similar_index(ocr_text, data.to_dict(orient="records"))
    
    print(f"가장 유사한 데이터의 인덱스는: {most_similar_index} 입니다.")
    print(f"해당 데이터: {data.iloc[most_similar_index]}")

    product_id =  data.iloc[most_similar_index]['product_id']

    return {"productId": product_id}
