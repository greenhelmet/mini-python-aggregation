from app.services.review_aggregation import aggregate_reviews
from app.types import Review

def main() -> None:
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

    print(aggregated)

if __name__ == "__main__":
    main()