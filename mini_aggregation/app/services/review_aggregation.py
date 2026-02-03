from collections import defaultdict
from app.types import Review, AggregatedStats

def aggregate_reviews(reviews: list[Review]) -> dict[str, AggregatedStats]:
    """
    defaultdict를 사용해 item_id별 초기 집계 구조를 자동 생성함으로써,
    조건 분기 없이 누적 로직에만 집중하도록 구현하였다.
    """
    temp: dict[str, dict[str, int]] = defaultdict(
        lambda: {"review_count": 0, "rating_sum": 0}
    )
    
    
    for review in reviews:
        item_id = review["item_id"]
        rating = review["rating"]
        
        temp[item_id]["review_count"] += 1
        temp[item_id]["rating_sum"] += rating
    
    result: dict[str, AggregatedStats] = {
        item_id: {
            "review_count": stats["review_count"],
            "average_rating": stats["rating_sum"] / stats["review_count"],
        }
        for item_id, stats in temp.items()
    }
        
    return result