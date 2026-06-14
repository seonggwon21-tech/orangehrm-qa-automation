# OrangeHRM UI Automation

> HR 관리 솔루션([OrangeHRM Demo](https://opensource-demo.orangehrmlive.com))의 핵심 화면을 **Playwright + pytest**로 자동화한 QA 포트폴리오
> — POM + Component 구조 · 크로스 브라우저 3종 · Ruff + GitHub Actions CI

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.x-2EAD33?logo=playwright&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B6B?logo=qameta&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
[![CI](https://github.com/seonggwon21-tech/orangehrm-qa-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/seonggwon21-tech/orangehrm-qa-automation/actions/workflows/ci.yml)

> ⚠️ **현재 기반 구축(foundation) 단계입니다.** 프레임워크·CI·POM 구조는 완성됐고, 테스트 케이스를 확장하는 중입니다. 자세한 범위는 [현재 범위 & 로드맵](#현재-범위--로드맵) 참고.

---

## 현재 범위 & 로드맵

| 영역 | 상태 | 내용 |
|:---|:---:|:---|
| **프레임워크 골격** | ✅ 완료 | BasePage 공통 액션 · POM 3종 · Component(Sidebar) · 공유 fixture |
| **UI 테스트** | 🟡 진행 | **11 TC** (smoke 5 · regression 6) — 로그인(정상/자격증명 오류/필수 입력) / 대시보드 / PIM 직원 목록 |
| **크로스 브라우저 CI** | ✅ 완료 | Chromium · Firefox · Edge matrix + Allure 아티팩트 업로드 |
| **품질 게이트** | ✅ 완료 | Ruff lint · format 검사를 test job의 선행 조건으로 |
| **API 테스트** | ⬜ 예정 | `tests/api/` 스캐폴딩만 존재 — requests 기반 인증/직원 API 검증 추가 예정 |
| **데이터 기반 · CRUD** | ⬜ 예정 | 직원 등록/검색/삭제 시나리오, parametrize 확장 예정 |

---

## 설계 포인트

기반 단계지만 "왜 이렇게 짰는지"가 드러나도록 구성했습니다.

- **POM + Component Object** — 페이지는 `pages/`, 화면 간 공유되는 사이드바는 `pages/components/sidebar.py`로 분리. UI가 바뀌어도 수정 범위를 컴포넌트 1개로 한정.
- **방어적 클릭** — `BasePage.click()`은 `wait_for(visible) → scroll_into_view → click` 순으로 동작해, 고정 `sleep` 없이 렌더링 타이밍 이슈를 흡수.
- **실패를 디버깅 가능하게** — `pytest_runtest_makereport` 훅으로 **실패 시 스크린샷을 Allure에 자동 첨부**. logging은 `utils/logger.py`로 일원화.
- **fixture로 인증 비용 제거** — `authenticated_page` fixture가 로그인 후 대시보드 진입까지 처리해, 각 테스트는 검증 로직에만 집중.
- **환경 분리** — `config/settings.py`가 `.env`(python-dotenv)에서 BASE_URL·계정·타임아웃을 읽어, 로컬/CI 환경을 코드 수정 없이 전환.

---

## 기술 스택

| 분류 | 사용 기술 |
|---|---|
| 언어 · 프레임워크 | Python 3.12 · pytest 8 (fixture, marker) |
| UI 자동화 | Playwright (Python) · **POM + Component Object Pattern** |
| 크로스 브라우저 | Chromium · Firefox · Edge (`--browser` 옵션) |
| API 자동화 *(예정)* | requests |
| 리포팅 | Allure (feature/title 계층 + 실패 스크린샷) |
| 품질 · CI/CD | Ruff(Lint 게이트) · GitHub Actions (Lint → Test matrix) |
| 환경 · 로깅 | python-dotenv · Python logging |

---

## 프로젝트 구조

```
.
├── config/
│   └── settings.py           # BASE_URL · 계정 · 타임아웃 (.env 로드)
├── pages/
│   ├── base_page.py          # 공통 액션 (click / fill / expect_visible …)
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── employee_list_page.py
│   └── components/
│       └── sidebar.py        # 재사용 사이드바 컴포넌트
├── tests/
│   ├── ui/                   # test_smoke · test_login · test_dashboard · test_employee_list
│   └── api/                  # (예정)
├── utils/logger.py
├── conftest.py               # login_page · authenticated_page fixture + 실패 스크린샷 훅
└── .github/workflows/ci.yml  # lint → test (Chromium / Firefox / Edge)
```

---

## 실행 방법

**요구사항:** Python 3.12+

```bash
# 1. 의존성 설치
pip install -r requirements.txt
python -m playwright install chromium firefox

# 2. 환경 변수 설정 (.env.example 복사 후 실제 값 입력)
cp .env.example .env
#   BASE_URL / ADMIN_USERNAME / ADMIN_PASSWORD

# 3. 테스트 실행
pytest                                          # headless Chromium
pytest --headed --slowmo 500                    # 화면 보며 디버깅
pytest --browser firefox                        # 브라우저 지정
pytest --browser chromium --browser-channel msedge
pytest -m smoke                                 # 마커 필터링

# 4. Allure 리포트
allure serve allure-results
```

> CI: `main`·`develop` push 또는 `main` PR 시 GitHub Actions가 **Lint → Test(Chromium/Firefox/Edge matrix)** 를 자동 실행하고, 결과 Allure 아티팩트를 업로드합니다.

---

## 테스트 범위

| 테스트 | 마커 | 설명 |
|--------|------|------|
| `test_login_page_loads` | smoke | 로그인 폼 3개 요소 렌더링 확인 |
| `test_login_with_valid_credentials` | smoke | 올바른 계정 로그인 → 대시보드 리다이렉트 |
| `test_login_with_invalid_credentials` | regression | 자격증명 오류 3종(비밀번호/아이디/둘 다) → "Invalid credentials" |
| `test_login_with_empty_fields` | regression | 필수 입력 누락 3종(아이디/비밀번호/둘 다) → "Required" |
| `test_dashboard_title_visible` | smoke | 로그인 후 Dashboard 헤딩 표시 |
| `test_sidebar_navigation_links_visible` | smoke | 사이드바 주요 메뉴(Admin/PIM/Leave/Time) 표시 |
| `test_employee_list_loads` | smoke | PIM 이동 후 직원 테이블 로드 + 행 존재 |

> 📋 전제조건 · 절차 · 기대결과를 포함한 상세 명세는 [테스트 케이스 문서](docs/test-cases.md)를 참고하세요.

---

## 프로젝트 배경

> QA 자동화 포트폴리오로, 공개 데모 환경인 OrangeHRM을 대상으로 **프레임워크 설계부터 CI 구성까지** 직접 구축하고 있습니다.

테스트 개수를 빠르게 늘리기보다, **구조를 먼저 옳게 세우는 것**을 우선했습니다 — POM에서 사이드바를 별도 컴포넌트로 뗀 것도, 인증을 fixture로 추상화한 것도, 실패 스크린샷을 자동화한 것도 같은 이유에서입니다. 골격이 검증된 만큼, 다음 단계는 API 테스트 착수와 직원 CRUD 시나리오 확장입니다.
