# Mini FastAPI — Week 3 Day 1

## 1. Day 1 실습 목적

Week 3 Day 1에서는 기존 mini 스크립트 프로젝트를 기반으로,
**FastAPI 애플리케이션 구조를 이해하고 최소 단위의 API + 테스트 구조를 완성**하는 것을 목표로 했다.

핵심 목표는 다음과 같다.

- FastAPI 프로젝트 기본 구조 이해
- Router / Schema / Service 레이어 분리
- Create / Read 중심의 최소 CRUD API 구현
- Service 단 테스트 → API 테스트 순서로 테스트 레벨 분리
- in-memory 저장소 기반 로직 검증
- 이후 DB, 인증, 예외 확장을 고려한 구조 고정

기능의 다양성보다 **책임 경계, 테스트 전략, 구조적 일관성**에 초점을 둔다.

---

## 2. 디렉토리 구조

### 현재 구조

mini_fastapi/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routers/
│   │       └── items.py
│   ├── schemas/
│   │   └── item.py
│   └── services/
│       └── item_service.py
├── tests/
│   ├── test_item_service.py
│   └── test_item_api.py
└── README.md

### 구조 설계 의도

- `main.py`
  - FastAPI 애플리케이션 엔트리포인트
  - app 생성 및 router 조립만 담당

- `api/routers/`
  - HTTP 레이어
  - Path / Query / Body 매핑
  - Service 예외를 HTTP 예외로 변환

- `schemas/`
  - API 입력/출력 계약 정의 (Pydantic)
  - 요청 모델과 응답 모델을 명확히 분리

- `services/`
  - 비즈니스 로직 계층
  - FastAPI, HTTP, status code에 대한 의존성 없음

- `tests/`
  - Service 테스트와 API 테스트 분리
  - 테스트 레벨별 책임 명확화

이 구조는 이전 미니 스크립트에서 사용한
**실행 코드 / 서비스 로직 분리 원칙을 API + 테스트 구조로 확장**한 것이다.

---

## 3. 도메인 및 API 설계 개요

### 도메인 모델

- Item
  - 시스템이 생성한 리소스
- ItemCreate
  - 클라이언트가 전달하는 생성 요청 데이터

요청과 응답 모델을 분리해,
입력 계약과 출력 계약을 명확히 한다.

---

## 4. Schema 설계

```python
# app/schemas/item.py
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    name: str

class ItemCreate(BaseModel):
    name: str
ItemCreate

요청 전용 스키마

Item

응답 전용 스키마

TypedDict 기반 입력/출력 계약 분리 흐름을
Pydantic 기반 API 계약으로 확장했다.

5. Service 설계
# app/services/item_service.py
from typing import List
from uuid import uuid4

from app.schemas.item import Item, ItemCreate

_items: list[Item] = []

def get_items() -> List[Item]:
    return _items

def create_item(data: ItemCreate) -> Item:
    item_id = str(uuid4())
    item = Item(
        id=item_id,
        name=data.name,
    )
    _items.append(item)
    return item

def get_item_by_id(item_id: str) -> Item:
    for item in _items:
        if item.id == item_id:
            return item
    raise ValueError("Item not found")
설계 포인트
in-memory 저장소를 Service 레이어가 소유

Service는 순수 동기 함수

HTTP / FastAPI 의존성 없음

실패 시 ValueError 발생

이후 DB 도입 시 내부 구현만 교체 가능

6. Router 설계
# app/api/routers/items.py
from typing import List
from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate
from app.services.item_service import (
    get_items,
    create_item,
    get_item_by_id,
)

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items():
    return get_items()

@router.get("/items/{item_id}", response_model=Item)
async def get_item_by_id_endpoint(item_id: str):
    try:
        return get_item_by_id(item_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    return create_item(item)
Router의 책임
HTTP 요청 수신

Path / Body 매핑

Service 호출

Service 예외 → HTTP 예외 변환

response_model 기반 응답 계약 검증

비즈니스 로직은 포함하지 않는다.

7. 테스트 전략
Service 테스트
성공 / 실패 케이스 모두 검증

in-memory 상태 직접 확인

ValueError 발생 여부 고정

# tests/test_item_service.py
def test_get_item_by_id_success():
    ...

def test_get_item_by_id_not_found():
    ...
API 테스트 (얇게)
행복 경로 중심

HTTP status code와 응답 형태만 확인

Service 로직 재검증하지 않음

# tests/test_item_api.py
def test_create_item_api():
    ...

def test_get_item_by_id_api_404():
    ...
테스트 원칙
Service 테스트 수 > API 테스트 수

비즈니스 규칙은 Service에서 검증

API 테스트는 “보여지는 결과”만 확인

8. main.py 역할
# app/main.py
from fastapi import FastAPI
from app.api.routers import items

app = FastAPI()
app.include_router(items.router)
애플리케이션 조립 전용

도메인 로직 없음

이후 middleware, dependency 확장에 대비