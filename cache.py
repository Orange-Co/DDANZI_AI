import time
from sqlalchemy.orm import Session

from model import Product

# 전역 변수로 캐시된 데이터 및 마지막 로드 시간
cached_data = None
cache_timestamp = 0
CACHE_TIMEOUT = 7 * 24 * 60 * 60  # 1주일 (초 단위)

def load_product_data(db: Session):
    global cached_data, cache_timestamp
    current_time = time.time()

    # 캐시가 없거나, 1주일이 지났을 때 다시 로드
    if cached_data is None or (current_time - cache_timestamp) > CACHE_TIMEOUT:
        products = db.query(Product.product_id, Product.origin_name).all()
        cached_data = [{"product_id": prod.product_id, "origin_name": prod.origin_name} for prod in products]
        cache_timestamp = current_time
        print("데이터베이스에서 데이터를 다시 로드했습니다.")
    else:
        print("캐싱된 데이터를 사용합니다.")

    return cached_data

def invalidate_cache():
    global cached_data, cache_timestamp
    cached_data = None
    cache_timestamp = 0
    print("캐시가 무효화되었습니다.")