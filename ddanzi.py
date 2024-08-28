import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from typing import Union
from fastapi import FastAPI

from google_storage import download_gcs, test_download_gcs
from ocr import get_text_from_image
from calculate_similarity import get_most_similar_index


app = FastAPI()

@app.get("/")
async def test():
    return {"message": "Hello World"}

@app.get("/test/image/{img_url}")
def gcs_test(img_url: str):
    image = test_download_gcs(img_url)
    return {"success"}


@app.get("/api/v1/image/{img_url}")
async def cal_most_similar_prod(img_url: str):
    # CSV 파일에서 데이터를 로드
    data = pd.read_csv('data/src/products_0827_12.csv')
    print("데이터가 성공적으로 로드되었습니다.")
    
    # 외부에서 이미지를 받아오는 부분
    image = download_gcs(img_url)
    
    # 네이버 OCR API를 호출해 텍스트 추출
    ocr_text = get_text_from_image(image)
    print(f"OCR로 추출한 텍스트: {ocr_text}")
    
    # 가장 유사한 인덱스 찾기
    most_similar_index = get_most_similar_index(ocr_text, data.to_dict(orient="records"))
    
    print(f"가장 유사한 데이터의 인덱스는: {most_similar_index} 입니다.")
    print(f"해당 데이터: {data.iloc[most_similar_index]}")

    return {"productId": most_similar_index}
