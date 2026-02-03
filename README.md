# Mini FastAPI — Week 3 Day 1

## 1. Day 1 실습 목적

Week 3 Day 1에서는 기존 mini 스크립트 프로젝트를 기반으로,
**FastAPI 애플리케이션 구조를 이해하고 최소 단위의 API를 설계·구현**하는 것을 목표로 했다.

핵심 목표는 다음과 같다.

- FastAPI 프로젝트의 기본 구조 이해
- Router / Schema / Service 레이어 분리
- Create / Read 중심의 최소 CRUD API 구현
- 실행 코드와 도메인 로직 분리 원칙 유지
- 이후 테스트·DB·인증 확장을 고려한 구조 고정

기능의 완성도보다 **책임 경계와 구조적 일관성**에 초점을 둔다.

---

## 2. 디렉토리 구조

### 현재 구조

mini_fastapi/
├── app/
│ ├── main.py
│ ├── api/
│ │ └── routers/
│ │ └── items.py
│ ├── schemas/
│ │ └── item.py
│ └── services/
│ └── item_service.py
└── README.md


### 구조 설계 의도

- `main.py`
  - FastAPI 애플리케이션 엔트리포인트
  - app 생성 및 router 조립만 담당
- `api/routers/`
  - HTTP 레이어
  - 요청/응답 스키마 연결 및 Service 호출
- `schemas/`
  - API 입력/출력 계약 정의 (Pydantic)
  - 요청 모델과 응답 모델을 명확히 분리
- `services/`
  - 비즈니스 로직 계층
  - FastAPI, HTTP, Request/Response를 모르는 순수 Python 코드

이 구조는 이전 Day 3에서 적용한
**실행 코드 / 서비스 로직 분리 원칙을 API 레벨로 확장**한 것이다.

---

## 3. API 설계 개요 (Create / Read)

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

class ItemCreate(BaseModel):
    name: str

ItemCreate는 요청 전용

Item은 응답 전용

TypedDict로 입력/출력 계약을 분리하던 흐름을
Pydantic 기반 API 계약으로 확장

# app/services/item_service.py
from typing import Dict, List
from uuid import uuid4

from app.schemas.item import Item, ItemCreate

_items: Dict[str, Item] = {}

def get_items() -> List[Item]:
    return list(_items.values())

def create_item(data: ItemCreate) -> Item:
    item_id = str(uuid4())
    item = Item(id=item_id)
    _items[item_id] = item
    return item

5. Service 설계
# app/services/item_service.py
from typing import Dict, List
from uuid import uuid4

from app.schemas.item import Item, ItemCreate

_items: Dict[str, Item] = {}

def get_items() -> List[Item]:
    return list(_items.values())

def create_item(data: ItemCreate) -> Item:
    item_id = str(uuid4())
    item = Item(id=item_id)
    _items[item_id] = item
    return item


설계 포인트:

in-memory 저장소를 Service 레이어가 소유

Service는 동기 함수

FastAPI, HTTP, status code에 대한 의존성 없음

이후 DB 도입 시 Service 내부 구현만 교체 가능

6. Router 설계
# app/api/routers/items.py
from typing import List
from fastapi import APIRouter

from app.schemas.item import Item, ItemCreate
from app.services.item_service import get_items, create_item

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items():
    return get_items()

@router.post("/items/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    return create_item(item)


Router의 책임:

HTTP 요청 수신

Pydantic Schema를 통한 입력 검증

Service 호출

응답 모델 검증(response_model)

비즈니스 로직은 포함하지 않는다.

7. main.py 역할
# app/main.py
from fastapi import FastAPI
from app.api.routers import items

app = FastAPI()

app.include_router(items.router)


애플리케이션 조립 전용

도메인 로직 없음

이후 router, middleware, dependency 확장에 대비