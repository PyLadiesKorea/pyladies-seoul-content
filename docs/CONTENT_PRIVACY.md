# 공개 멤버 연락처 보호 규칙

이 저장소의 Markdown과 이미지 파일은 공개된다. 멤버 콘텐츠 작성자와 리뷰어는 아래 요구사항을 배포 계약으로 취급한다.

## 범위

- `members/`의 공개 멤버 콘텐츠
- pull request와 `main`·`dev` push에서 실행되는 자동 검사
- 현재 파일뿐 아니라 새로 추가하거나 수정하는 파일

실명과 의도적으로 공개한 입금정보는 이 자동 검사의 대상이 아니다.

## 요구사항

### CONTENT-PII-001 개인 이메일 금지

- 멤버 콘텐츠에 개인 이메일 주소를 넣지 않는다.
- 다음 조직 연락처만 허용한다.
  - `seoul@pyladies.com`
  - `coc@pyladies.com`
  - `conduct-wg@python.org`
- 새로운 조직 연락처가 필요하면 코드와 테스트의 allowlist를 함께 검토한다.

### CONTENT-PII-002 개인 전화번호 금지

- 휴대전화와 지역번호를 포함한 멤버 개인 전화번호를 공개 콘텐츠에 넣지 않는다.
- 하이픈이나 공백을 제거해 우회한 표기도 허용하지 않는다.

### CONTENT-CONSENT-001 Thanks to 공개 동의

- Thanks to의 이름과 사진은 당사자의 공개 동의를 받은 경우에만 게시한다.
- 익명을 원하면 동의한 표시명을 쓰고 사진을 생략한다.

### CONTENT-PII-003 안전한 검사 로그

- 자동 검사는 위반 파일, 줄 번호, 규칙 ID만 출력한다.
- 탐지한 이메일, 전화번호 또는 해당 원문은 CI 로그에 다시 출력하지 않는다.

### CONTENT-PII-004 병합 전 자동 차단

- pull request와 `main`·`dev` push에서 개인정보 검사를 실행한다.
- 위반이 하나라도 있으면 검사를 실패시켜 병합·배포 전에 수정하게 한다.

## 검증표

| 요구사항 ID | 검증 | 상태 |
|---|---|---|
| CONTENT-PII-001 | `tests/test_validate_content.py` 개인 이메일 거부, 조직 연락처 allowlist 허용 | Covered |
| CONTENT-PII-002 | `tests/test_validate_content.py` 휴대전화·지역번호 형식 거부 | Covered |
| CONTENT-CONSENT-001 | README 작성 규칙과 리뷰 체크 | Covered |
| CONTENT-PII-003 | `test_failure_output_does_not_echo_detected_values` | Covered |
| CONTENT-PII-004 | `.github/workflows/validate-content.yml` 테스트와 저장소 스캔 | Covered |

## 대응 절차

1. 멤버 콘텐츠에서 위반 내용을 제거한다.
2. 관련 PR과 CI 로그에는 실제 값을 복사하지 않는다.
3. 이미 공개된 git history 정리가 필요하면 저장소 관리자 승인 후 별도 작업으로 진행한다.
