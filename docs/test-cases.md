# 테스트 케이스 / 테스트 시나리오

OrangeHRM 오픈소스 데모(`https://opensource-demo.orangehrmlive.com`)를 대상으로 한 UI 자동화 테스트 케이스 명세입니다.
본 문서는 `tests/ui/` 하위의 실제 테스트 코드를 기준으로 작성되었습니다.

## 환경 / 전제 조건

| 항목 | 값 |
| --- | --- |
| 대상 URL | `BASE_URL` (기본값: `https://opensource-demo.orangehrmlive.com`) |
| 관리자 계정 | `ADMIN_USERNAME` / `ADMIN_PASSWORD` (기본값: `Admin` / `admin123`) |
| 기본 타임아웃 | 10,000ms |
| 실행 도구 | Python · Playwright · pytest |
| 브라우저 | Chromium / Firefox / Edge (cross-browser) |

- 공통 픽스처
  - `login_page`: `BASE_URL` 진입 후 로그인 페이지 객체 반환
  - `authenticated_page`: 관리자 계정으로 로그인하여 대시보드 진입까지 완료된 페이지 반환
- 실패 시 스크린샷이 Allure 리포트에 자동 첨부됩니다.

## 마커 / 분류

| 마커 | 의미 |
| --- | --- |
| `@pytest.mark.ui` | UI 자동화 테스트 |
| `@pytest.mark.smoke` | 핵심 정상 동작 확인(스모크) |
| `@pytest.mark.regression` | 회귀 / 예외 케이스 확인 |

---

## 1. 인증 (Authentication)

로그인은 입력값 성격에 따라 검증 동작이 다르므로 **정상 / 자격증명 오류 / 필수 입력 누락** 세 그룹으로 나눠 검증한다.

### 1-1. 정상 (Happy Path)

#### TC-AUTH-001 · 유효한 자격증명 로그인 → 대시보드 이동
- **테스트**: `tests/ui/test_login.py::TestLogin::test_login_with_valid_credentials`
- **분류**: ui, smoke
- **전제조건**: 로그인 페이지 진입 (`login_page`)
- **절차**
  1. Username에 `Admin` 입력
  2. Password에 `admin123` 입력
  3. Login 버튼 클릭
- **기대결과**
  - URL이 `**/dashboard/**`로 이동한다
  - "Dashboard" 헤딩이 표시된다

### 1-2. 자격증명 오류 (Invalid Credentials)

값은 입력됐으나 일치하지 않는 경우 → 상단 알럿 **"Invalid credentials"** 노출, 대시보드 이동 없음.

- **테스트**: `tests/ui/test_login.py::TestLogin::test_login_with_invalid_credentials` (parametrize 3건)
- **분류**: ui, regression
- **전제조건**: 로그인 페이지 진입 (`login_page`)

| TC ID | case_id | Username | Password | 기대결과 |
| --- | --- | --- | --- | --- |
| TC-AUTH-002 | `wrong_password` | `Admin` | `wrong_password` | "Invalid credentials" 표시 |
| TC-AUTH-003 | `wrong_username` | `wrong_user` | `admin123` | "Invalid credentials" 표시 |
| TC-AUTH-004 | `both_wrong` | `wrong_user` | `wrong_password` | "Invalid credentials" 표시 |

### 1-3. 필수 입력 누락 (Required Validation)

값이 비어 있는 경우 → 서버 인증 전 클라이언트 검증이 동작하여 빈 필드 하단에 **"Required"** 메시지 노출.

- **테스트**: `tests/ui/test_login.py::TestLogin::test_login_with_empty_fields` (parametrize 3건)
- **분류**: ui, regression
- **전제조건**: 로그인 페이지 진입 (`login_page`)

| TC ID | case_id | Username | Password | 기대결과 |
| --- | --- | --- | --- | --- |
| TC-AUTH-005 | `empty_username` | (빈값) | `admin123` | "Required" 메시지 1개 |
| TC-AUTH-006 | `empty_password` | `Admin` | (빈값) | "Required" 메시지 1개 |
| TC-AUTH-007 | `both_empty` | (빈값) | (빈값) | "Required" 메시지 2개 |

---

## 2. 대시보드 (Dashboard)

### TC-DASH-001 · 로그인 후 대시보드 헤딩 표시
- **테스트**: `tests/ui/test_dashboard.py::TestDashboard::test_dashboard_title_visible`
- **분류**: ui, smoke
- **전제조건**: 관리자 로그인 완료 (`authenticated_page`)
- **절차**
  1. 대시보드 페이지 로드 확인
- **기대결과**
  - URL이 `**/dashboard/**`이다
  - "Dashboard" 헤딩이 표시된다

### TC-DASH-002 · 사이드바 내비게이션 링크 표시
- **테스트**: `tests/ui/test_dashboard.py::TestDashboard::test_sidebar_navigation_links_visible`
- **분류**: ui, smoke
- **전제조건**: 관리자 로그인 완료 (`authenticated_page`)
- **절차**
  1. 사이드바의 주요 메뉴 항목 확인
- **기대결과**
  - `Admin`, `PIM`, `Leave`, `Time` 메뉴 항목이 모두 표시된다

---

## 3. 직원 관리 (Employee Management)

### TC-EMP-001 · PIM 이동 후 직원 목록 테이블 로드
- **테스트**: `tests/ui/test_employee_list.py::TestEmployeeList::test_employee_list_loads`
- **분류**: ui, smoke
- **전제조건**: 관리자 로그인 완료 (`authenticated_page`)
- **절차**
  1. 사이드바에서 `PIM` 메뉴 클릭
  2. 직원 목록 페이지 로드 확인
- **기대결과**
  - URL이 `**/pim/viewEmployeeList**`로 이동한다
  - 직원 목록 테이블이 표시된다
  - 테이블 행(직원 데이터) 개수가 1개 이상이다

---

## 4. 스모크 (Smoke)

### TC-SMOKE-001 · 로그인 페이지 기본 요소 로드
- **테스트**: `tests/ui/test_smoke.py::test_login_page_loads`
- **분류**: ui, smoke
- **전제조건**: 없음 (`BASE_URL` 직접 진입)
- **절차**
  1. `BASE_URL` 접속
- **기대결과**
  - Username 입력 필드가 표시된다
  - Password 입력 필드가 표시된다
  - Submit(Login) 버튼이 표시된다

---

## 추적 매트릭스 (Traceability)

| TC ID | 기능 | 테스트 함수 | 마커 |
| --- | --- | --- | --- |
| TC-AUTH-001 | 인증 | `test_login_with_valid_credentials` | ui, smoke |
| TC-AUTH-002~004 | 인증 | `test_login_with_invalid_credentials` (parametrize) | ui, regression |
| TC-AUTH-005~007 | 인증 | `test_login_with_empty_fields` (parametrize) | ui, regression |
| TC-DASH-001 | 대시보드 | `test_dashboard_title_visible` | ui, smoke |
| TC-DASH-002 | 대시보드 | `test_sidebar_navigation_links_visible` | ui, smoke |
| TC-EMP-001 | 직원 관리 | `test_employee_list_loads` | ui, smoke |
| TC-SMOKE-001 | 스모크 | `test_login_page_loads` | ui, smoke |
