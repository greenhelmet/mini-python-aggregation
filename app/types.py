from typing import TypedDict

class Review(TypedDict):
    """
    단일 리뷰 로그의 스키마 정의
    """
    review_id: int
    item_id: str
    review_text: str
    rating: int
    
class AggregatedStats(TypedDict):
    """
    item_id 기준 리뷰 집계 결과 스키마
    """
    review_count: int
    average_rating: float