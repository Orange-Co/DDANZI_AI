import re
import numpy as np
import pandas as pd
import pickle
import requests 
from sklearn.feature_extraction.text import CountVectorizer

# 불필요한 텍스트를 제거하는 함수
def clean_ocr_result(ocr_result):
    patterns = [
        r'.*지금 확인해 보세요!',
        r'.*메시지카드',
        r'.*감동카드',
        r'사용방법.*',
        r'수량.*'
    ]
    for pattern in patterns:
        ocr_result = re.sub(pattern, '', ocr_result, flags=re.DOTALL)
    return ocr_result

# 주요 텍스트 추출 함수
def extract_main_text(ocr_result):
    return clean_ocr_result(ocr_result)

# N-gram 기반 유사도 계산 함수
def ngram_similarity(ocr_text, origin_name, n=3):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(n, n))
    ocr_vec = vectorizer.fit_transform([ocr_text])
    origin_vec = vectorizer.transform([origin_name])
    similarity = np.dot(ocr_vec, origin_vec.T).toarray()[0][0]
    return similarity / max(ocr_vec.sum(), origin_vec.sum())

# OCR 결과와 가장 유사한 항목의 인덱스 찾기 함수
def find_most_similar(ocr_text, data_list):
    best_match_index = -1
    best_match_score = 0.0

    ocr_text = extract_main_text(ocr_text)

    for index, item in enumerate(data_list):
        origin_name = item["origin_name"]
        
        # N-gram 기반 유사도 계산
        score = ngram_similarity(ocr_text, origin_name)
        
        if score > best_match_score:
            best_match_score = score
            best_match_index = index

    return best_match_index, best_match_score

# 특정 OCR 텍스트를 입력받아 가장 유사한 데이터 인덱스를 출력하는 함수
def get_most_similar_index(ocr_text, data_list):
    # 가장 유사한 항목의 인덱스와 유사도 점수
    index, score = find_most_similar(ocr_text, data_list)
    return index

# 네이버 OCR API를 사용해 이미지를 텍스트로 변환하는 함수
def get_ocr_text_from_image(image_path):
    
    
    '''
    # 네이버 클라우드 플랫폼에서 발급받은 OCR API 키
    api_url = "https://api.ncloud.com/vision-ocr/v1/recognize"  # 실제 API URL로 변경
    headers = {
        "X-OCR-SECRET": "your_secret_key_here",  # 네이버 OCR API Secret Key
        "Content-Type": "application/json",
    }

    # 이미지 파일 읽기
    with open(image_path, "rb") as image_file:
        img = image_file.read()

    # API 요청 생성
    response = requests.post(api_url, headers=headers, files={"file": img})
    result = response.json()

    # OCR 결과 텍스트 추출
    ocr_text = result['images'][0]['fields'][0]['inferText']
    return ocr_text

    '''

# 메인 실행 함수
def main():
    # CSV 파일에서 데이터를 로드
    data = pd.read_csv('data/products_0827_12.csv')

    print("데이터가 성공적으로 로드되었습니다.")
    
    # 외부에서 이미지를 받아오는 부분
    image_path = input("이미지 파일의 경로를 입력하세요: ")
    
    # 네이버 OCR API를 호출해 텍스트 추출
    ocr_text = get_ocr_text_from_image(image_path)
    print(f"OCR로 추출한 텍스트: {ocr_text}")
    
    # 가장 유사한 인덱스 찾기
    most_similar_index = get_most_similar_index(ocr_text, data.to_dict(orient="records"))
    
    print(f"가장 유사한 데이터의 인덱스는: {most_similar_index} 입니다.")
    print(f"해당 데이터: {data.iloc[most_similar_index]}")

if __name__ == "__main__":
    main()
