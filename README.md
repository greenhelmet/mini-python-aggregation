### 미니 스크립트 Day 2 마무리 정리

**1. Day 2 실습 목적**

Day 2에서는 코드 작성 자체보다,

- Linux 환경에서의 기본적인 파일·디렉토리 조작
- Git 저장소 상태 확인 및 히스토리 추적
- Windows + WSL 혼합 환경에서의 파일 시스템 개념

을 실습을 통해 익히는 것을 목표로 했다.

이후 백엔드 개발, Docker, 서버 환경에서 필수적으로 요구되는  
**개발 환경 이해 능력**을 기르는 단계다.

---

**2. 실습 입력 / 출력 형태**

입력

- 사용자 명령어
    - Linux shell 명령어 (`ls`, `cd`, `mkdir`, `rm` 등)
    - Git 명령어 (`git status`, `git log` 등)
- 작업 대상
    - Windows 파일 시스템 내 프로젝트 디렉토리
    - 경로 예시:
        - Windows: `C:\Users\chach\Downloads\mini`
        - WSL: `/mnt/c/Users/chach/Downloads/mini`

출력

- 터미널 출력
    - 파일 목록
    - 현재 경로
    - Git 저장소 상태 및 커밋 로그
- 파일 시스템 변화
    - 디렉토리 / 파일 생성·삭제
    - Git이 추적하는 변경 사항

---

**3. 핵심 실습 포인트**

- **Linux 기본 명령어 사용**
    - 파일 시스템을 직접 조작하며 명령어의 역할을 체감
- **Git 상태 기반 워크플로우**
    - “지금 어떤 파일이 추적되고 있는가”를 기준으로 사고
- **Windows ↔ WSL 경로 매핑 이해**
    - `/mnt/c`는 Windows C 드라이브의 마운트 지점
    - 동일한 파일을 서로 다른 OS 관점에서 접근 가능

---

**4. 이 실습에서 일부러 선택한 트레이드오프**

- Windows 디렉토리를 그대로 사용  
  → WSL 전용 홈 디렉토리보다 권한 이슈를 직접 경험

- 고급 Git 명령어는 사용하지 않음  
  → Day 2 목표는 개념 정착과 환경 이해

- 자동화 스크립트 작성은 생략  
  → 명령어 단위 동작을 손으로 확인하는 데 집중

---

**5. 문제 상황 및 해결 기록**

- **Git dubious ownership 에러 발생**

  원인:
  - Windows 사용자와 WSL 사용자의 파일 소유권 불일치

  해결:
  ```bash
  git config --global --add safe.directory /mnt/c/Users/chach/Downloads/mini
