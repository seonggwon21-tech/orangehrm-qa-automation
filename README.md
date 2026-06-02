# OrangeHRM UI Automation

Playwright + pytest 기반 E2E UI 자동화 포트폴리오 프로젝트.

대상 사이트: [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com) (공개 테스트 환경)

## Tech Stack

| 역할 | 도구 |
|------|------|
| 브라우저 자동화 | Playwright (Python) |
| 테스트 러너 | pytest + pytest-playwright |
| 리포팅 | Allure Report |
| 린터/포매터 | Ruff |
| CI/CD | GitHub Actions |

## 프로젝트 구조

```
.
├── config/
│   └── settings.py          # BASE_URL, 인증 정보, 타임아웃 상수
├── pages/
│   ├── base_page.py          # 공통 액션 (click, fill, expect)
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── employee_list_page.py
│   └── components/
│       └── sidebar.py        # 재사용 사이드바 컴포넌트
├── tests/
│   └── ui/
│       ├── test_smoke.py
│       ├── test_login.py
│       ├── test_dashboard.py
│       └── test_employee_list.py
├── conftest.py               # 공유 픽스처 (login_page, authenticated_page)
└── .github/workflows/ci.yml  # lint → test (Chromium / Firefox / Edge)
```

## 로컬 셋업

**요구사항:** Python 3.12+

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. Playwright 브라우저 설치
python -m playwright install chromium firefox

# 3. (선택) 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 BASE_URL / ADMIN_USERNAME / ADMIN_PASSWORD 수정
```

## 테스트 실행

```bash
# 기본 실행 (headless Chromium)
pytest

# 브라우저 화면 보면서 실행
pytest --headed

# 브라우저 지정
pytest --browser firefox
pytest --browser chromium --browser-channel msedge

# 마커로 필터링
pytest -m smoke
pytest -m regression

# 속도 조절 (ms 단위, 디버깅 시 유용)
pytest --headed --slowmo 500
```

## Allure 리포트

```bash
# 리포트 생성 및 열기
allure serve allure-results
```

## 테스트 범위

| 테스트 | 마커 | 설명 |
|--------|------|------|
| `test_login_page_loads` | smoke | 로그인 폼 3개 요소 렌더링 확인 |
| `test_login_with_valid_credentials` | smoke | 올바른 계정 로그인 → 대시보드 리다이렉트 |
| `test_login_with_invalid_password` | regression | 잘못된 비밀번호 → 에러 메시지 노출 |
| `test_dashboard_title_visible` | smoke | 로그인 후 Dashboard 헤딩 표시 |
| `test_sidebar_navigation_links_visible` | smoke | 사이드바 주요 메뉴 표시 |
| `test_employee_list_loads` | smoke | PIM 이동 후 직원 테이블 로드 |

## CI

`main` / `develop` 브랜치 push 또는 PR 시 자동 실행됩니다.

- **lint job**: `ruff check` + `ruff format --check`
- **test job**: Chromium / Firefox / Edge 병렬 실행 (matrix)
- 실패 시 Allure 결과물을 GitHub Actions Artifacts에 업로드
