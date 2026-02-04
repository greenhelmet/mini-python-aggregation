# Mini FastAPI — Week 3 Day 1 ~ Week 4 Day 1

## 1. 학습 목적

Week 3 Day 1부터 Week 4 Day 1까지의 목표는 다음과 같다.

* FastAPI 프로젝트의 기본 구조 확립
* Router / Schema / Service 레이어 책임 분리
* Service 단 테스트 → API 테스트의 테스트 레벨 분리
* Python 표준 logging 기반의 레이어별 로그 기준 정립
* FastAPI ValidationError 발생 위치 및 로그 부재 원인 관찰

기능 확장보다는 **구조, 책임 경계, 운영 관점의 가시성**에 초점을 둔다.

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
│       └── logging.py
├── tests/
│   ├── test_item_service.py
│   └── test_item_api.py
└── README.md
```

### 구조 설계 의도

* **main.py**

  * FastAPI 애플리케이션 엔트리포인트
  * router 조립 전용

* **api/routers/**

  * HTTP 레이어
  * 요청 수신, Path/Body 매핑
  * Service 예외를 HTTPException으로 변환

* **schemas/**

  * API 입력/출력 계약 정의 (Pydantic)
  * 요청 모델과 응답 모델 분리

* **services/**

  * 비즈니스 로직 계층
  * FastAPI / HTTP 의존성 없음

* **core/**

  * 로깅, 설정 등 공통 인프라 코드

* **tests/**

  * Service 테스트와 API 테스트 분리

---

## 3. 도메인 및 Schema 설계

* **Item**: 시스템이 생성한 리소스 (응답 전용)
* **ItemCreate**: 클라이언트 입력 데이터 (요청 전용)

요청과 응답 모델을 분리해 입력 계약과 출력 계약을 명확히 한다.

---

## 4. Service Layer 설계

* in-memory 저장소를 Service 레이어가 소유
* 순수 동기 함수로 구성
* HTTP, status code 개념 없음
* 실패 시 ValueError 발생

이 구조를 통해 이후 DB 도입 시 내부 구현만 교체 가능하도록 설계했다.

---

## 5. Router Layer 설계

Router의 책임은 다음으로 제한한다.

* HTTP 요청 수신
* Path / Body 매핑
* Service 호출
* Service 예외 → HTTPException 변환
* response_model 기반 응답 계약 검증

비즈니스 로직은 포함하지 않는다.

---

## 6. 테스트 전략

### Service 테스트

* 성공 / 실패 케이스 모두 검증
* in-memory 상태 직접 확인
* ValueError 발생 여부 고정

### API 테스트

* 행복 경로 중심
* HTTP status code와 응답 형태만 검증
* Service 로직 재검증하지 않음

**원칙**

* Service 테스트 수 > API 테스트 수
* 비즈니스 규칙은 Service에서만 검증

---

## 7. Logging 설계 (Week 4 Day 1)

### 공통 로깅 구조

* Python 표준 logging 사용
* FastAPI 비의존 코드
* module 단위 logger name 사용
* handler 중복 방지

### Service Layer 로그 기준

* **info**: 비즈니스 이벤트 성공 (Item 생성 등)
* **warning**: 비즈니스 실패 (존재하지 않는 Item 조회)
* **debug**: 내부 상태 (_items 길이 등)

Service 로그에는 HTTP, status code 개념이 등장하지 않는다.

### Router Layer 로그 기준

* **info**: 요청 수신, 정상 응답 반환
* **error**: Service 예외를 HTTPException으로 변환하는 지점

Router 로그는 "어떤 요청이 실패했는가"에 집중한다.

---

## 8. Validation Error 관찰

잘못된 요청 payload 전송 시:

* HTTP 422 Unprocessable Entity 반환
* Service / Router 로그 모두 남지 않음

**원인**

* Pydantic ValidationError는 Router 함수 실행 이전 단계에서 발생
* 현재 로깅 지점을 우회함

이를 통해 "로그가 남지 않는 에러"의 정체가 FastAPI 요청 처리 파이프라인 상단에 있음을 확인했다.
