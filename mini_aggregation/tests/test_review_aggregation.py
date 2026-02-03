from app.services.review_aggregation import aggregate_reviews
from app.types import Review


def test_aggregate_reviews_normal_case() -> None:
    reviews: list[Review] = [
        {
            "review_id": 1,
            "item_id": "A001",
            "review_text": "Good quality",
            "rating": 4,
        },
        {
            "review_id": 2,
            "item_id": "A001",
            "review_text": "Decent",
            "rating": 3,
        },
        {
            "review_id": 3,
            "item_id": "B002",
            "review_text": "Excellent",
            "rating": 5,
        },
    ]

    result = aggregate_reviews(reviews)

    assert result["A001"]["review_count"] == 2
    assert result["A001"]["average_rating"] == 3.5
    assert result["B002"]["review_count"] == 1
    assert result["B002"]["average_rating"] == 5.0
    
def test_aggregate_reviews_empty_list() -> None:
    reviews: list[Review] = []

    result = aggregate_reviews(reviews)

    assert result == {}
    
def test_aggregate_reviews_invalid_rating_value() -> None:
    reviews: list[Review] = [
        {
            "review_id": 1,
            "item_id": "A001",
            "review_text": "Invalid rating",
            "rating": -5,
        }
    ]

    result = aggregate_reviews(reviews)

    assert result["A001"]["average_rating"] == -5.0



