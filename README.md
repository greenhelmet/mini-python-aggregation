# Mini FastAPI — Architecture & Authentication Design

## 1. 학습 목적

본 프로젝트는 기능 구현보다 **구조, 책임 경계, 운영 가시성**을 우선하는 FastAPI 학습을 목표로 한다.
<<<<<<< HEAD
Week 3 Day 1부터 Week 4 Day 1까지는 다음 질문에 대한 명확한 답을 설계 수준에서 확립하는 데 집중했다.
=======
Week 3 Day 1부터 Week 5 Day 1까지는 다음 질문에 대한 명확한 답을 설계 수준에서 확립하는 데 집중했다.
>>>>>>> 1962998 (Apply dependency injection design and document auth boundaries)

* 각 레이어는 무엇을 알고, 무엇을 몰라야 하는가
* 비즈니스 로직은 어떤 전제를 가지고 실행되는가
* 에러와 실패는 어디에서 정의되고, 어디에서 변환되는가

---

## 2. 디렉토리 구조

```
mini_fastapi/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routers/
│   │       └── items.py
│   ├── schemas/
│   │   └── item.py
│   ├── services/
│   │   └── item_service.py
│   └── core/
│       ├── logging.py
│       └── exceptions.py
├── tests/
│   ├── test_item_service.py
│   └── test_item_api.py
└── README.md
```

---

## 3. 레이어별 책임 설계

### main.py

* 애플리케이션 엔트리포인트
* Router 및 Global Exception Handler 등록 전용
* 비즈니스 로직 포함 금지

### api / routers

* HTTP 요청 수신
* Path / Body 매핑
* Service 호출
* 정상 흐름 로깅

HTTP 레이어는 **요청을 해석하고 전달하는 역할**에 한정되며, 비즈니스 규칙이나 예외 정책을 소유하지 않는다.

### schemas

* API 입력 / 출력 계약 정의
* 요청 모델과 응답 모델 분리
* Pydantic을 계약 검증 도구로 사용

Schema는 검증 로직이 아니라 **계약 명세**다.

### services

* 비즈니스 로직 계층
* FastAPI 및 HTTP 비의존
* 저장소(in-memory) 소유
* 실패는 도메인 의미의 예외로만 표현

Service는 **인증된 세계를 전제로 동작**하지만, 인증이라는 개념을 알지 않는다.

### core

* 로깅, 예외 처리 등 공통 인프라
* FastAPI 의존 최소화
* 애플리케이션 전반의 횡단 관심사 관리

---

## 4. Service / Router 설계 원칙 요약

### Service Layer

* 순수 동기 함수
* HTTP / status code 개념 제거
* 비즈니스 실패는 도메인 의미의 예외로 표현
* Web 환경이 없어도 실행 가능해야 함

### Router Layer

* HTTP 요청 수신 및 매핑
* Service 호출
* response_model 기반 응답 계약 검증

Router는 **흐름만 연결**하며, 판단하지 않는다.

---

## 5. 테스트 전략

### Service 테스트

* 성공 / 실패 케이스 모두 검증
* in-memory 상태 직접 확인
* 도메인 예외 발생 여부 고정

### API 테스트

* 행복 경로 중심
* HTTP status code 및 응답 형태만 검증
* Service 로직 재검증 금지

원칙적으로:

* Service 테스트 수 > API 테스트 수
* 비즈니스 규칙은 Service에서만 검증

---

## 6. Logging 및 예외 처리 설계

### Logging 원칙

* Python 표준 logging 사용
* module 단위 logger name
* handler 중복 방지

### 로그 책임 분리

* Service: 비즈니스 이벤트와 상태
* Router: 요청 단위 성공 / 실패 맥락

### Global Exception Handler

* 모든 예외를 단일 지점에서 처리
* 예외 의미 → HTTP 응답 변환 담당
* ValidationError 포함 모든 에러 로깅

이 구조를 통해 **로그 누락 없는 에러 가시성**을 확보한다.

---

## 7. Authentication / Authorization 설계 원칙

### 개념 정의

* Authentication: 이 사용자가 누구인가를 확인하는 과정
* Authorization: 이 사용자가 무엇을 할 수 있는지를 결정하는 과정

두 개념은 목적, 실패 성격, 책임 레이어가 다르며 반드시 분리되어야 한다.

---

## 8. 인증 정보의 레이어 위치

인증과 관련된 정보는 다음 원칙을 따른다.

* Request Context (header, token 등)는 애플리케이션 경계까지만 유효하다
* 인증 정보 해석은 비즈니스 진입 이전에 완료되어야 한다
* Service Layer에는 인증 결과만 전달된다

Service는 다음을 전제로 한다.

* 요청 주체는 이미 인증되었다
* 전달된 주체 정보는 유효하다

---

## 9. 인증 실패의 예외 처리 철학

* 인증 실패는 도메인 규칙 위반이 아니다
* 인증 실패는 비즈니스 로직이 평가되기 이전의 실패다
* HTTP 401 / 403은 도메인 언어가 아니라 인프라 언어다

따라서:

* 인증 실패는 Service에서 표현되지 않는다
* 도메인 예외는 HTTP 개념을 포함하지 않는다
* 모든 변환은 Global Exception Handler에서 수행된다

---

## 10. Service Layer 비침투 원칙

Service Layer에는 다음 개념이 들어가지 않는다.

* 인증 토큰
* Request / Header
* HTTP status code
* 인증 실패 가능성

Service는 **인증된 세계를 전제로 한 순수 비즈니스 규칙**만을 다룬다.

이 원칙을 통해:

* Service 테스트 단순화
* Batch / Script / Offline 환경 재사용 가능
* 인증 방식 변경에 대한 내성 확보

---

## 11. 설계 결론

이 프로젝트의 핵심은 기능 구현이 아니라 다음 질문에 대한 명확한 답이다.

* 이 로직은 어느 레이어의 책임인가
* 이 실패는 어느 레이어의 언어인가

그 결과, 본 구조는 에러를 처리하는 코드가 아니라 **에러를 설계 가능한 대상으로 만든다.**
