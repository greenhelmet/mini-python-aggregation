from collections import defaultdict
from types import Review, AggregatedStats

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

reviews: list[Review] = [
    {
        "review_id": 1,
        "item_id": "A001",
        "review_text": "Good quality, works as expected.",
        "rating": 4,
    },
    {
        "review_id": 2,
        "item_id": "A001",
        "review_text": "Decent product for the price.",
        "rating": 3,
    },
    {
        "review_id": 3,
        "item_id": "A001",
        "review_text": "Exceeded my expectations.",
        "rating": 5,
    },
    {
        "review_id": 4,
        "item_id": "B002",
        "review_text": "Not very satisfied.",
        "rating": 2,
    },
    {
        "review_id": 5,
        "item_id": "B002",
        "review_text": "Poor packaging, but product is okay.",
        "rating": 3,
    },
    {
        "review_id": 6,
        "item_id": "C003",
        "review_text": "Excellent! Will buy again.",
        "rating": 5,
    },
]
            
aggregated = aggregate_reviews(reviews)

assert aggregated["A001"]["review_count"] == 3
assert aggregated["A001"]["average_rating"] == 4.0
assert aggregated["B002"]["average_rating"] == 2.5