from typing import TypedDict

class Review(TypedDict):
    review_id: int
    item_id: str
    review_text: str
    rating: int
    
class AggregatedStats(TypedDict):
    review_count: int
    average_rating: float