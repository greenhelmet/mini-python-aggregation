### 미니 스크립트 마무리 정리

**1. 스크립트 목적**

이 스크립트는 리뷰 로그 리스트를 입력으로 받아

`item_id` 기준으로 리뷰 개수와 평균 평점을 계산한다.

리뷰 데이터 집계라는 전형적인 백엔드/추천 시스템 전처리 작업을 단순화한 예제다.

---

**2. 입력 / 출력 형태**

입력

- `list[dict]`
- 각 리뷰는 다음 필드를 가진다.
    - `review_id: int`
    - `item_id: str`
    - `review_text: str`
    - `rating: int`

출력

- `dict[str, dict[str, float]]`
- key: `item_id`
- value:
    - `review_count: int`
    - `average_rating: float`

---

**3. 핵심 구현 포인트**

- **dict를 사용한 집계**
    - `item_id`를 key로 사용해 O(1) lookup으로 리뷰를 누적
    - 중간 집계용 dict(`temp`)에 count와 sum을 분리 저장
- **2단계 처리 구조**
    1. for-loop으로 review_count, rating_sum 계산
    2. dict comprehension으로 평균 계산 및 최종 결과 생성
- **type hint 적용**
    - 함수 시그니처와 내부 변수에 타입 명시
    - 입력/출력 구조가 코드만 봐도 명확해짐
- **assert 기반 검증**
    - 사람이 계산한 기대값과 결과를 직접 비교
    - 간단하지만 테스트의 역할을 수행

---

**4. 이 구현에서 일부러 선택한 트레이드오프**

- 평균 평점을 `float`로 반환
    
    → 반올림 규칙을 명시하지 않아도 되어 로직 단순화
    
- `review_text`는 사용하지 않음
    
    → 실제 로그 구조를 유지하면서도 집계 로직에 집중
    
- 예외 처리(빈 리스트, rating 누락 등)는 생략
    
    → Day 1 목표는 문법과 자료구조 숙련
    

---

**5. 개선 가능 포인트 (다음 단계용 메모)**

- `defaultdict`를 사용하면 초기화 로직을 줄일 수 있음
- `TypedDict`로 리뷰 스키마를 명시하면 타입 안정성 향상
- 빈 입력 리스트에 대한 early return 처리
- 이 함수를 FastAPI endpoint로 감싸면 실제 서비스 형태가 됨