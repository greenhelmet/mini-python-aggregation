# Mini FastAPI — Architecture, Dependency & Middleware Design

## 1. 학습 목적

본 프로젝트는 기능 구현보다 **구조, 책임 경계, 실패의 위치**를 명확히 하는 FastAPI 학습을 목표로 한다.

Week 3 Day 1부터 Week 5 Day 4까지의 핵심 질문은 다음과 같다.

- 각 레이어는 무엇을 알고, 무엇을 몰라야 하는가
- 비즈니스 로직은 어떤 전제를 가지고 실행되는가
- 인증 실패는 왜 비즈니스 로직이 아닌가
- Depends는 왜 Router에만 존재해야 하는가
- Middleware는 무엇을 처리하고, 무엇을 처리하면 안 되는가

본 README는 위 질문들에 대한 **설계 수준의 답변을 고정**하기 위한 문서다.

---

## 2. 디렉토리 구조

mini_fastapi/
├── app/
│ ├── main.py
│ ├── api/
│ │ └── routers/
│ │ └── items.py
│ ├── schemas/
│ │ ├── item.py
│ │ └── user.py
│ ├── services/
│ │ └── item_service.py
│ └── dependencies/
│ └── auth.py
├── core/
│ ├── middleware.py
│ ├── logging.py
│ ├── context.py
│ └── exceptions.py
├── tests/
│ ├── test_item_service.py
│ ├── test_item_api.py
│ └── test_middleware.py
└── README.md


---

## 3. 레이어별 책임 설계

### main.py

- 애플리케이션 엔트리포인트
- Router, Middleware, Global Exception Handler 조립
- 비즈니스 로직 및 인증 로직 포함 금지
- 구현이 아닌 **wiring만 담당**

---

### api / routers

- HTTP 요청 수신
- Path / Query / Body 매핑
- Dependency 실행 (`Depends`)
- Service 호출
- 요청 단위 흐름 제어

Router는 **요청을 해석하고 흐름을 연결하는 계층**이다.  
판단, 정책, 비즈니스 규칙을 소유하지 않는다.

---

### schemas

- API 입력 / 출력 계약 정의
- 요청 모델과 응답 모델 분리
- Pydantic을 계약 검증 도구로 사용

Schema는 로직이 아니라 **명세**다.

---

### services

- 비즈니스 로직 계층
- FastAPI 및 HTTP 비의존
- in-memory 저장소 소유
- 실패는 도메인 의미의 예외로만 표현

Service는 **이미 인증된 세계를 전제로 동작**하지만,  
인증이라는 개념 자체는 알지 않는다.

---

### dependencies / auth.py

- 인증 / 인가 관련 Dependency 정의
- 토큰 파싱, 검증, User 로딩 책임 분리
- 인증/인가 실패 시 의미 있는 예외 발생
- Service에 인증 실패 개념 침투 금지

---

### core

- 로깅, Middleware, 예외 처리 등 공통 인프라
- 애플리케이션 전반의 횡단 관심사 관리
- 비즈니스 규칙 포함 금지

---

## 4. Depends 실행 시점과 의미

FastAPI에서 `Depends`는 다음 순서로 실행된다.

1. HTTP 요청 수신
2. Dependency 그래프 구성
3. 모든 Dependency 실행
4. Router 함수 body 실행

즉, Router 함수 body가 실행될 때  
**이미 모든 진입 조건은 계산 완료 상태**다.

Dependency는 **비즈니스 로직의 일부가 아니라 진입 조건 계산기**다.

---

## 5. 요청 단위 캐싱 (Request Scope)

FastAPI Dependency는 요청 단위로 캐싱된다.

- 동일 요청 내 동일 Dependency는 1회만 실행
- 중첩 Depends에서도 중복 호출 제거

---

## 6. Service / Router 경계 유지 전략

### Router Layer

- Depends 사용 가능
- HTTP 개념(status code, request, header) 허용
- 인증/인가 실패 처리 가능

### Service Layer

- Depends 사용 금지
- FastAPI import 금지
- HTTP 개념 완전 배제
- user는 “그냥 인자”로만 전달받
