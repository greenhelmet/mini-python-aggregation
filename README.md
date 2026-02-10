# Mini FastAPI — Architecture & Dependency Design

## 1. 학습 목적

본 프로젝트는 기능 구현보다 **구조, 책임 경계, 실패의 위치**를 명확히 하는 FastAPI 학습을 목표로 한다.

Week 3 Day 1부터 Day 3까지의 핵심 질문은 다음과 같다.

- 각 레이어는 무엇을 알고, 무엇을 몰라야 하는가
- 비즈니스 로직은 어떤 전제를 가지고 실행되는가
- 인증 실패는 왜 비즈니스 로직이 아닌가
- Depends는 왜 Router에만 존재해야 하는가

본 README는 위 질문에 대한 **설계 수준의 답변을 고정**하기 위한 문서다.

---

## 2. 디렉토리 구조

mini_fastapi/
├── app/
│ ├── main.py
│ ├── api/
│ │ └── routers/
│ │     └── items.py
│ ├── schemas/
│ │ ├── item.py
│ │ └── user.py
│ ├── services/
│ │ └── item_service.py
│ └── dependencies/
│     └── auth.py
├── core/
│ ├── logging.py
│ └── exceptions.py
│ └── context.py
├── tests/
│ ├── test_item_service.py
│ └── test_item_api.py
└── README.md

---

## 3. 레이어별 책임 설계

### main.py

- 애플리케이션 엔트리포인트
- Router 및 Global Exception Handler 등록
- 비즈니스 로직 및 인증 로직 포함 금지

---

### api / routers

- HTTP 요청 수신
- Path / Query / Body 매핑
- Dependency 실행 (Depends)
- Service 호출
- 요청 단위 로깅

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

- 인증 관련 Dependency 정의
- 토큰 파싱, 검증, User 로딩 책임 분리
- 인증 실패 시 의미 있는 예외 발생 (`AuthenticationError`)
- Service에 인증 실패 개념 침투 금지

---

### core

- 로깅, 예외 처리 등 공통 인프라
- 애플리케이션 전반의 횡단 관심사 관리
- 비즈니스 규칙 포함 금지

---

## 4. Depends 실행 시점과 의미

FastAPI에서 `Depends`는 다음 시점에 실행된다.

1. HTTP 요청 수신
2. Dependency 그래프 구성
3. 모든 Dependency 실행
4. Router 함수 body 실행

즉, Router 함수 body가 실행될 때 **이미 주입값 생성 완료** 상태다.  
Dependency는 **비즈니스 로직의 일부가 아니라 진입 조건 계산기**다.

---

## 5. 요청 단위 캐싱 (Request Scope)

FastAPI Dependency는 요청 단위로 캐싱된다.

- 동일 요청 내 동일 Dependency 그래프에서 1회만 실행
- 중첩 Depends에서도 중복 호출 제거

---

## 6. Service / Router 경계 유지 전략

### Router Layer

- Depends 사용 가능
- HTTP 개념(status code, request, header) 허용
- 인증 실패 처리 가능

### Service Layer

- Depends 사용 금지
- FastAPI import 금지
- HTTP 개념 완전 배제
- user는 “그냥 인자”로만 전달받음

Service는 **인증 결과를 신뢰**하지만  
인증 과정을 책임지지 않는다.

---

## 7. 인증 실패가 Service에 들어가지 않는 이유

인증 실패는 다음 특성을 가진다.

- 비즈니스 규칙 위반이 아니다
- 도메인 실패가 아니다
- 비즈니스 로직이 실행되기 이전의 실패다
- HTTP 401 / 403은 인프라 언어다

따라서:

- 인증 실패는 Service에서 표현되지 않는다
- Service는 인증 실패 가능성을 고려하지 않는다
- 인증 실패 → HTTP 응답 변환은 Router / Global Handler의 책임이다

**정리 문장:**  
*“Authentication is a gate, not a rule”*  
→ 인증은 **Service 로직의 규칙이 아니라**, 요청 진입을 허용/차단하는 관문이다.

---

## 8. 테스트 전략과 Depends 위치

### Service 테스트

- user를 직접 생성해 인자로 전달
- Dependency 테스트하지 않음
- 비즈니스 성공 / 실패만 검증

### API 테스트

- Dependency override 사용
- 인증 로직 자체는 검증하지 않음
- HTTP status / response shape만 검증

이 분리를 통해:

- 인증 방식 변경이 Service 테스트에 영향을 주지 않고
- 비즈니스 규칙 변경이 API 테스트에 전파되지 않는다

---

## 9. Service Layer 비침투 원칙

Service Layer에는 다음 개념이 들어가지 않는다.

- Request / Header
- 인증 토큰
- HTTP status code
- Depends
- 인증 실패 가능성

Service는 **인증된 세계를 전제로 한 순수 비즈니스 규칙**만을 다룬다.

---

## 10. 설계 결론

이 프로젝트의 핵심은 기능 구현이 아니라 다음 질문에 대한 답이다.

- 이 로직은 어느 레이어의 책임인가
- 이 실패는 어느 레이어의 언어인가

Depends는 편의 기능이 아니라  
**책임 경계를 코드로 강제하는 장치**다.

그 결과, 이 구조는 에러를 처리하는 코드가 아니라  
**에러를 설계 가능한 대상으로 만든다.**
