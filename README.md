Mini FastAPI — Week 3 Day 1 ~ Week 4 Day 1
1. 학습 목적
Week 3 Day 1부터 Week 4 Day 1까지의 목표는 다음과 같다.

FastAPI 프로젝트의 기본 구조 확립
Router / Schema / Service 레이어 책임 분리
Service 단 테스트 → API 테스트의 테스트 레벨 분리
Python 표준 logging 기반의 레이어별 로그 기준 정립
FastAPI ValidationError 발생 위치 및 로그 부재 원인 관찰
기능 확장보다는 구조, 책임 경계, 운영 관점의 가시성에 초점을 둔다.

2. 디렉토리 구조
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
구조 설계 의도
main.py

FastAPI 애플리케이션 엔트리포인트
router 조립 전용
api/routers/

HTTP 레이어
요청 수신, Path/Body 매핑
Service 예외를 HTTPException으로 변환
schemas/

API 입력/출력 계약 정의 (Pydantic)
요청 모델과 응답 모델 분리
services/

비즈니스 로직 계층
FastAPI / HTTP 의존성 없음
core/

로깅, 설정 등 공통 인프라 코드
tests/

Service 테스트와 API 테스트 분리
3. 도메인 및 Schema 설계
Item: 시스템이 생성한 리소스 (응답 전용)
ItemCreate: 클라이언트 입력 데이터 (요청 전용)
요청과 응답 모델을 분리해 입력 계약과 출력 계약을 명확히 한다.

4. Service Layer 설계
in-memory 저장소를 Service 레이어가 소유
순수 동기 함수로 구성
HTTP, status code 개념 없음
실패 시 ValueError 발생
이 구조를 통해 이후 DB 도입 시 내부 구현만 교체 가능하도록 설계했다.

5. Router Layer 설계
Router의 책임은 다음으로 제한한다.

HTTP 요청 수신
Path / Body 매핑
Service 호출
Service 예외 → HTTPException 변환
response_model 기반 응답 계약 검증
비즈니스 로직은 포함하지 않는다.

6. 테스트 전략
Service 테스트
성공 / 실패 케이스 모두 검증
in-memory 상태 직접 확인
ValueError 발생 여부 고정
API 테스트
행복 경로 중심
HTTP status code와 응답 형태만 검증
Service 로직 재검증하지 않음
원칙

Service 테스트 수 > API 테스트 수
비즈니스 규칙은 Service에서만 검증
7. Logging 설계 (Week 4 Day 1)
공통 로깅 구조
Python 표준 logging 사용
FastAPI 비의존 코드
module 단위 logger name 사용
handler 중복 방지
Service Layer 로그 기준
info: 비즈니스 이벤트 성공 (Item 생성 등)
warning: 비즈니스 실패 (존재하지 않는 Item 조회)
debug: 내부 상태 (_items 길이 등)
Service 로그에는 HTTP, status code 개념이 등장하지 않는다.

Router Layer 로그 기준
info: 요청 수신, 정상 응답 반환
error: Service 예외를 HTTPException으로 변환하는 지점
Router 로그는 "어떤 요청이 실패했는가"에 집중한다.

8. Validation Error 관찰
잘못된 요청 payload 전송 시:

HTTP 422 Unprocessable Entity 반환
Service / Router 로그 모두 남지 않음
원인

Pydantic ValidationError는 Router 함수 실행 이전 단계에서 발생
현재 로깅 지점을 우회함
이를 통해 "로그가 남지 않는 에러"의 정체가 FastAPI 요청 처리 파이프라인 상단에 있음을 확인했다.

기존 Router try/except 방식의 문제점
초기 구현에서는 Router 레이어에서 Service 호출을 try/except로 감싸고, ValueError 등을 HTTPException으로 변환하는 방식을 사용했다.

이 방식에는 다음과 같은 구조적 문제가 있었다.

책임 혼재

Router가 비즈니스 실패의 의미를 해석하고 HTTP status를 결정함

Service의 실패 정책이 HTTP 레이어에 침투

중복 코드

각 Endpoint마다 유사한 try/except 패턴 반복

예외 유형이 늘어날수록 Router 코드 비대화

로그 일관성 붕괴

어떤 에러는 Router에서 로그가 남고

어떤 에러는 FastAPI 내부에서 처리되어 로그가 남지 않음

확장성 저하

새로운 도메인 예외 추가 시 모든 Router 수정 필요

결과적으로 Router가 “얇은 HTTP 어댑터” 역할을 수행하지 못하고 에러 정책의 중심이 되는 구조였다.

Global Exception Handler 구조 도입
위 문제를 해결하기 위해 Global Exception Handler 구조를 도입했다.

핵심 아이디어는 다음과 같다.

Service는 의미 있는 예외만 발생

Router는 예외를 처리하지 않음

예외 → HTTP 응답 변환은 단 하나의 레이어에서만 수행

이를 위해 app/core/exceptions.py에 예외 타입별 handler 함수를 정의하고, main.py에서 전역 등록했다.

구조 변화 요약

Router

try/except 제거

정상 흐름만 로깅

HTTP status 결정 권한 제거

Service

HTTP 개념 완전 제거

비즈니스 실패 시 ValueError 발생

Global Handler

예외 타입 → HTTP status 매핑

RFC 7807 기반 공통 ErrorResponse 생성

로그 레벨 일관성 유지

이 구조를 통해 모든 에러 응답은 동일한 JSON shape로 반환된다.

로그가 남지 않던 에러의 정체
잘못된 요청 payload를 보냈을 때:

HTTP 422 응답은 반환되지만

Router / Service 로그가 전혀 남지 않는 현상을 관찰했다.

원인은 FastAPI 요청 처리 파이프라인에 있었다.

RequestValidationError는

Router 함수 실행 이전 단계

Pydantic validation 단계에서 발생

즉, 기존 로깅 지점(Router / Service)을 우회하고 있었다.

Global Exception Handler에서 RequestValidationError를 명시적으로 처리함으로써:

ValidationError에도 로그가 남고

정상/비정상 요청 흐름을 로그로 완전히 추적 가능해졌다.

이 구조가 운영에 유리한 이유
Global Exception Handler 구조는 단순한 코드 정리가 아니라 운영 관점의 가시성을 개선한다.

모든 에러가 한 지점에서 로깅

로그 누락 케이스 제거

에러 유형별 로그 레벨 고정

HTTP status와 에러 의미 분리

status: 인프라 / 모니터링 관점

ErrorResponse: 애플리케이션 의미론

테스트 전략 명확화

Service 테스트: 비즈니스 규칙

API 테스트: HTTP 계약과 응답 형태

책임 경계가 테스트에도 그대로 반영됨

확장에 유리한 구조

도메인별 Custom Exception 추가 가능

에러 코드 체계화 용이

환경별(detail 노출 여부) 분리 가능

결과적으로 이 구조는 “에러를 처리하는 코드”가 아니라 “에러를 설계 가능한 대상”으로 만든다.