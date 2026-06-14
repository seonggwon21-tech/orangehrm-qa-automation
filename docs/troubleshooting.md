# Troubleshooting

> 작성일: 2026-06-14
> 브랜치: `develop`

기능은 통과하지만 구조·견고성 측면에서 손볼 부분을 코드 리뷰 라운드에서 정리한 기록이다.
(AI 보조 리뷰를 함께 활용했고, 지적 사항은 직접 검토 후 반영했다.)
각 항목은 적용 후 `ruff check`/`ruff format`/전체 테스트(11 TC) 통과를 확인했다.

---

## 1. POM 이점 무력화 — 테스트가 사이드바 셀렉터를 직접 재구현

**현상**
`Sidebar` 컴포넌트에 `expect_link_visible()`을 만들어 뒀는데, 정작 대시보드 테스트는 이를 쓰지 않고 raw 로케이터를 다시 작성하고 있었다.

```python
# tests/ui/test_dashboard.py — 컴포넌트를 두고도 셀렉터를 복제
locator = authenticated_page.locator(".oxd-main-menu-item").filter(has_text=name)
expect(locator).to_be_visible()
```

**원인**
테스트가 컴포넌트 내부 셀렉터(`.oxd-main-menu-item`)를 그대로 들고 있어, 사이드바 마크업이 바뀌면 컴포넌트와 테스트 두 곳을 모두 고쳐야 했다. "수정 범위를 컴포넌트 1개로 한정"한다는 POM 도입 목적이 깨진 상태.

**해결**
테스트는 컴포넌트 메서드만 호출하도록 바꾸고, `expect_link_visible`이 실제로 쓰이게 했다.

```python
dashboard = DashboardPage(authenticated_page)
for name in ("Admin", "PIM", "Leave", "Time"):
    dashboard.sidebar.expect_link_visible(name)
```

**교훈**
컴포넌트에 동작을 정의했으면 테스트는 그 동작만 호출해야 한다. 테스트에 셀렉터 문자열이 보이면 추상화가 새는 신호다.

---

## 2. `get_row_count()` — 빈 목록에서 0 대신 타임아웃 예외

**현상**
직원 목록 행 수를 세는 메서드가, 행이 0개인 화면에서 `0`을 반환하지 못하고 10초 대기 후 `TimeoutError`를 던졌다.

```python
def get_row_count(self) -> int:
    self.rows.first.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)  # 0행이면 예외
    return self.rows.count()
```

**원인**
첫 번째 행이 보일 때까지 기다리는 전제라, "결과 없음" 상태 자체를 정상값으로 표현할 수 없었다. 현재 테스트는 `> 0`만 검증해 우연히 통과했지만, 향후 검색 결과 0건 시나리오에서 바로 깨진다.

**해결**
행이 아니라 테이블 컨테이너가 보이는지 기다린 뒤 개수를 반환하도록 변경. 빈 목록은 자연스럽게 `0`이 된다.

```python
def get_row_count(self) -> int:
    self.table.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
    return self.rows.count()
```

**교훈**
"개수를 센다"는 메서드는 0을 정상 결과로 다뤄야 한다. 0을 예외로 처리하면 negative 시나리오를 못 쓴다.

---

## 3. 빈 필드 검증이 첫 메시지만 확인

**현상**
빈 입력 시 노출되는 `Required` 메시지를 검증하는데, 두 필드가 모두 비는 케이스에서도 첫 번째 메시지만 텍스트를 확인했다.

```python
expect(self.field_errors).to_have_count(count, timeout=DEFAULT_TIMEOUT)
expect(self.field_errors.first).to_have_text("Required", timeout=DEFAULT_TIMEOUT)
```

**원인**
`.first`만 보면 두 번째 메시지가 다른 문구여도 통과한다. 개수 검증과 내용 검증이 분리돼 있어 의도("모든 빈 필드에 Required")를 온전히 담지 못했다.

**해결**
리스트를 넘기면 개수와 각 요소 텍스트를 한 번에 검증하는 `to_have_text`로 통합.

```python
def expect_field_required(self, count: int) -> None:
    expect(self.field_errors).to_have_text(["Required"] * count, timeout=DEFAULT_TIMEOUT)
```

---

## 4. BasePage 헬퍼 우회 + 죽은 코드

**현상**
`BasePage.wait_for_url()`을 만들어 놓고 페이지 객체들은 `self.page.wait_for_url(...)`을 직접 호출했다. 동시에 `get_text`, `is_visible` 등 한 번도 호출되지 않는 헬퍼와 미사용 로케이터(`search_button`)가 남아 있었다.

**원인**
헬퍼를 추가한 뒤 호출부를 통일하지 않았고, 향후 쓸 것을 미리 만들어 둔 메서드들이 그대로 방치됐다. 포트폴리오에서 "쓰지 않는 코드"는 오히려 골격의 신뢰도를 떨어뜨린다.

**해결**
- 페이지의 URL 대기를 모두 `self.wait_for_url()` 경유로 통일
- 미사용 헬퍼(`get_text`, `is_visible`)와 `search_button` 제거 (검색 시나리오 도입 시 그때 추가)
- 후속 정리에서 같은 패턴을 `expect_visible()`에서도 발견 — `dashboard_page`·`employee_list_page`가 `expect(x).to_be_visible(...)`를 인라인 복제하고 있어 헬퍼 호출로 통일 (래퍼가 sidebar·dashboard·employee 세 곳 모두에서 쓰이도록)

```python
# pages/dashboard_page.py
def expect_loaded(self) -> None:
    self.wait_for_url("**/dashboard/**")
    expect(self.heading).to_be_visible(timeout=DEFAULT_TIMEOUT)
```

**교훈**
헬퍼는 만든 즉시 호출부를 통일하고, 쓰지 않으면 지운다. "나중에 쓸지도" 코드는 필요할 때 추가하는 편이 깔끔하다.

---

## 5. 마커 오타가 조용히 통과됨

**현상**
`pytest.ini`에 마커를 등록해 뒀지만, 오타 난 마커(`@pytest.mark.smoek` 등)를 달아도 경고 없이 그대로 수집됐다.

**원인**
`--strict-markers`가 없으면 등록되지 않은 마커도 허용된다. 마커 기반 필터링(`-m smoke`)에 의존하는 구조에서 오타는 곧 "조용히 누락된 테스트"로 이어진다.

**해결**
`addopts`에 strict 옵션을 추가해 미등록 마커·잘못된 설정을 즉시 실패로 만들었다.

```ini
addopts =
    --alluredir=allure-results
    --strict-markers
    --strict-config
    -v
```

**교훈**
마커로 테스트를 분류·필터링한다면 strict 모드는 필수다. 거버넌스를 코드가 강제하게 둔다.

---

## 6. 의존성·셀렉터·로깅 견고성 정리

리뷰 중 함께 정리한 소소하지만 운영에 영향 있는 항목들.

**playwright 본체 버전 미고정** — `requirements.txt`에 `pytest-playwright`만 핀돼 있어 브라우저 드라이버를 제공하는 `playwright` 본체는 매 설치마다 버전이 달라질 수 있었다. CI 재현성을 위해 명시적으로 고정.

```
playwright==1.60.0
pytest-playwright==0.6.2
```

**사이드바 부분일치 셀렉터** — `filter(has_text=menu_name)`는 substring 매칭이라 메뉴명이 다른 항목의 일부와 겹치면 오작동 위험이 있었다. 정확 일치로 변경하고 매칭 로직을 헬퍼로 모음.

```python
def _item(self, menu_name: str) -> Locator:
    return self._menu.filter(has=self.page.get_by_text(menu_name, exact=True))
```

**로거 중복 출력** — 루트 로거가 설정된 환경에서 로그가 두 번 찍힐 수 있어 `logger.propagate = False`로 차단.

**setup 단계 실패 시 스크린샷 훅 방어** — `pytest_runtest_makereport`에서 `item.funcargs`가 없을 가능성에 대비해 `getattr(item, "funcargs", {})`로 안전하게 접근.

**중복 설정 제거** — `--alluredir`가 `pytest.ini`와 CI 커맨드 양쪽에 있어 `pytest.ini`로 일원화.

**교훈**
재현성(버전 고정), 셀렉터 정확성, 로그 위생은 기능 테스트로는 드러나지 않는다. 리뷰 단계에서 의식적으로 점검할 영역.

---

## 7. 동적 렌더링 페이지에서 즉시 반환되는 가시성 체크

**현상**
OrangeHRM은 Vue.js 기반이라 로그인·대시보드 화면이 동적으로 렌더링되는데, `is_visible()`로 요소 노출을 확인하면 렌더링이 끝나기 전에 `False`가 반환돼 간헐적으로 실패했다.

```python
# 렌더링 완료 전 호출되면 "없음"으로 오판
assert page.locator(".oxd-form").is_visible()
```

**원인**
`is_visible()`은 호출 시점의 상태를 *즉시* 반환할 뿐 대기하지 않는다. 동적 렌더링 구간에서는 "아직 안 그려짐"을 "없음"으로 잘못 판단한다.

**해결**
auto-waiting이 내장된 `expect(locator).to_be_visible()`로 통일하고, `BasePage`에 래퍼를 두어 개별 테스트가 직접 `is_visible`을 쓰지 않게 했다.

```python
# pages/base_page.py
def expect_visible(self, locator: Locator) -> None:
    expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
```

**교훈**
동적 렌더링 SPA에서 "보이는가"는 단발성 조회가 아니라 *조건 충족까지의 대기*다. 즉시 반환 API(`is_visible`)와 대기 API(`expect`)를 구분해 써야 한다.
</content>
