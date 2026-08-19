# 콘텐츠 구조 검증 규칙

이 문서는 public 콘텐츠 저장소의 자동 구조 검사 범위를 정의한다. 현재 범위는
README의 이벤트 번들 작성 규칙 중 폴더 slug와 필수 한국어 파일, 그리고 공개
멤버의 전역 표시 순서 계약이다. 그 밖의 frontmatter 값, 본문과 번역 내용은
검사하지 않는다.

## 요구사항

### CONTENT-SCHEMA-001 이벤트 번들 기본 구조

- `events/`의 직계 하위 **폴더**는 모두 이벤트 번들이다.
- 폴더 이름은 정확히 다음 정규식과 일치해야 한다.

  ```text
  ^[0-9]{8}-[a-z0-9]+(?:-[a-z0-9]+)*$
  ```

- 각 이벤트 번들 폴더에는 일반 파일 `ko.md`가 반드시 있어야 한다.
- `events/`의 직계 파일과 번들 내부의 이미지·`en.md`·하위 항목은 이 검사의
  대상이 아니다.
- 검사는 외부 package 없이 Python 표준 라이브러리만 사용해야 한다.
- 위반 시 규칙 ID와 저장소 상대 경로를 출력하고 0이 아닌 상태로 종료한다.
- pull request와 `main`·`dev` push의 기존 content validation workflow에서
  테스트와 실제 저장소 검사를 실행한다.

### MEMBER-ORDER-001 공개 멤버 전역 표시 순서

- `members/<slug>/ko.md`에서 `listed`가 생략됐거나 `true`인 멤버만
  `All the PyLadies are . . .` 목록에 표시한다.
- 공개 멤버는 역할(`organizer`/`maker`/`member`)로 묶지 않고 `order`의
  오름차순으로 정렬한다. 같은 값이 생기면 이름을 안정적인 보조 정렬값으로
  사용하지만, 현재 공개 멤버의 `order`는 서로 다른 양의 정수여야 한다.
- `order`는 공통 metadata이므로 `ko.md`에서만 관리하고 ko/en 페이지가 같은
  순서를 사용한다.
- 현재 승인된 순서는 다음과 같다.

  1. 윤수진
  2. 차화영
  3. 백찬희
  4. 최혜림
  5. 최예리
- `members/pyladies-seoul`처럼 `listed: false`인 번들은 이 목록과 순서 검사의
  대상이 아니다.

## 검증표

| 요구사항 ID | 검증 | 상태 | 남은 일 |
|---|---|---|---|
| CONTENT-SCHEMA-001 | `tests/test_validate_content_schema.py`, `scripts/validate_content_schema.py`, `.github/workflows/validate-content.yml`; 현재 42개 번들 scan | Covered | frontmatter와 다른 카테고리는 의도적으로 검사하지 않는다. |
| MEMBER-ORDER-001 | `tests/test_member_display_order.py`; web `tests/test_models.py`, `tests/test_views.py`, `tests/test_bakery_views.py`, `tests/test_content_roundtrip.py`; paired ko/en 정적 빌드 | Covered | dev 병합 후 고유 배포 URL에서 최종 순서를 재확인한다. |

## 변경 절차

검사 범위를 다른 frontmatter, 본문 값 또는 카테고리로 넓힐 때는 이 문서와
검증표를 먼저 갱신하고 별도 요구사항 ID와 테스트를 추가한다.
