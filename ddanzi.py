from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engineconn, get_db
from google_storage import download_gcs
from ocr import get_text_from_image
from calculate_similarity import get_most_similar_index
from model import Product


app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

class Image(BaseModel): 
    image_url: str

@app.get("/db")
async def dbTest():
    example = session.query(Product).all()
    return example


@app.post("/test/image")
def gcs_test(image: Image):
    image = download_gcs(image.image_url)
    return {"result_image_url": image}


@app.post("/api/v1/image")
async def cal_most_similar_prod(image: Image, db: Session = Depends(get_db)):
    #042370524
    products = db.query(Product.product_id, Product.origin_name).all()
    data = [{"product_id": prod.product_id, "origin_name": prod.origin_name} for prod in products]
    
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
