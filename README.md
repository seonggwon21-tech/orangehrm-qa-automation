# OrangeHRM UI Automation

> HR 관리 솔루션([OrangeHRM Demo](https://opensource-demo.orangehrmlive.com))의 핵심 화면을 **Playwright + pytest**로 자동화한 QA 포트폴리오
> — POM + Component 구조 · 크로스 브라우저 3종 · Ruff + GitHub Actions CI

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.x-2EAD33?logo=playwright&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B6B?logo=qameta&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
[![CI](https://github.com/seonggwon21-tech/orangehrm-qa-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/seonggwon21-tech/orangehrm-qa-automation/actions/workflows/ci.yml)

> ⚠️ **기반 구축(foundation) 단계** — 프레임워크·CI·POM 구조는 완성됐고 테스트 케이스를 확장하는 중입니다.

---

## 현황

| 테스트 | 마커 | CI | 브라우저 |
|:---:|:---:|:---:|:---:|
| **11 TC** (UI) | smoke 5 · regression 6 | GitHub Actions | 3종 (Chromium·Firefox·Edge) |

**핵심 기능**

- **POM + Component Object** — 페이지는 `pages/`, 화면 간 공유되는 사이드바는 `pages/components/sidebar.py`로 분리해 UI 변경 시 수정 범위를 컴포넌트 1개로 한정
- **방어적 클릭** — `BasePage.click()`이 `wait_for(visible) → scroll_into_view → click` 순으로 동작해 고정 `sleep` 없이 렌더링 타이밍 이슈를 흡수
- **fixture로 인증 비용 제거** — `authenticated_page` fixture가 로그인 후 대시보드 진입까지 처리해 각 테스트는 검증 로직에만 집중
- **data-driven 검증** — 로그인 예외를 `parametrize`로 자격증명 오류·필수 입력 누락까지 분기 검증
- **실패를 디버깅 가능하게** — `pytest_runtest_makereport` 훅으로 실패 시 스크린샷을 Allure에 자동 첨부하고, Playwright Trace(`retain-on-failure`)를 남겨 CI 아티팩트로 업로드 (타임라인·DOM 스냅샷·네트워크까지 재현)
- **코드 리뷰로 구조 점검** — POM 추상화 누수·죽은 코드·셀렉터 견고성 등을 리뷰로 잡고 수정 ([코드 리뷰 →](docs/code-review.md))

---

## 기술 스택

| 분류 | 사용 기술 |
|---|---|
| 언어 · 프레임워크 | Python 3.14 · pytest 8 (fixture, marker, parametrize) |
| UI 자동화 | Playwright (Python) · **POM + Component Object Pattern** |
| 크로스 브라우저 | Chromium · Firefox · Edge (`--browser` 옵션) |
| API 자동화 *(예정)* | requests |
| 리포팅 | Allure (feature/title 계층 + 실패 스크린샷, GitHub Pages 게시) · Playwright Trace |
| 품질 · CI/CD | Ruff(Lint 게이트) · pre-commit · GitHub Actions (Lint → Test matrix → Pages, 캐싱·`-n auto` 병렬) |
| 환경 · 로깅 | python-dotenv · Python logging |

---

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt          # 테스트 실행용 (런타임)
pip install -r requirements-dev.txt      # 린트·pre-commit 포함 (개발용)
python -m playwright install chromium firefox

# 2. 환경 변수 설정 (.env.example 복사 후 실제 값 입력)
cp .env.example .env
#   BASE_URL / ADMIN_USERNAME / ADMIN_PASSWORD

# 3. (선택) pre-commit 훅 설치 — 커밋 시 ruff lint/format 자동 실행
pre-commit install

# 4. 테스트 실행
pytest                                          # headless Chromium
pytest --browser firefox                        # 브라우저 지정
pytest --browser chromium --browser-channel msedge
pytest -m smoke                                 # 마커 필터링
pytest -n auto                                  # 병렬 실행 (pytest-xdist)

# 5. Allure 리포트
allure serve allure-results
```

> CI: `main`·`develop` push 또는 `main` PR 시 GitHub Actions가 **Lint → Test(Chromium/Firefox/Edge matrix) → Allure 리포트 게시** 를 자동 실행합니다. pip·Playwright 브라우저를 캐싱하고 테스트를 `-n auto`로 병렬 실행하며, `develop`/`main` push 시 Allure HTML 리포트를 [GitHub Pages](https://seonggwon21-tech.github.io/orangehrm-qa-automation/)에 history와 함께 배포합니다.

---

## 상세 문서

| 문서 | 내용 |
|---|---|
| [테스트 케이스](docs/test-cases.md) | 전제조건·절차·기대결과 + 추적 매트릭스 |
| [코드 리뷰](docs/code-review.md) | 리뷰 관점·범위·결과 요약 + 설계 결정 기록 |
| [트러블슈팅](docs/troubleshooting.md) | 리뷰에서 잡은 구조·견고성 이슈와 해결 상세 |

---

## 프로젝트 배경

> QA 자동화 포트폴리오로, 공개 데모 환경인 OrangeHRM을 대상으로 **프레임워크 설계부터 CI 구성까지** 직접 구축하고 있습니다.

테스트 개수를 빠르게 늘리기보다 **구조를 먼저 옳게 세우는 것**을 우선했습니다 — 사이드바를 별도 컴포넌트로 뗀 것도, 인증을 fixture로 추상화한 것도, 실패 스크린샷을 자동화한 것도 같은 이유에서입니다. 골격이 검증된 만큼 다음 단계는 API 테스트 착수와 직원 CRUD 시나리오 확장입니다.
</content>
