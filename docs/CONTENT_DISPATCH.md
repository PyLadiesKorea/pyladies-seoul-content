# 콘텐츠 배포 디스패치 계약

콘텐츠 저장소의 `main` 또는 `dev` 브랜치에 변경이 반영되면
`.github/workflows/notify-web.yml`이 웹 저장소에 `repository_dispatch` 이벤트를 보낸다.
송신 브랜치와 배포 환경이 섞이지 않고, 디스패치가 어느 콘텐츠 스냅샷을 배포해야
하는지 모호하지 않도록 아래 계약을 지킨다.

## 범위와 용어

- **prod 콘텐츠**: 콘텐츠 저장소 `main` 브랜치의 커밋
- **dev 콘텐츠**: 콘텐츠 저장소 `dev` 브랜치의 커밋
- **정확한 콘텐츠 리비전**: 해당 `push` 실행의 `GITHUB_SHA`와 정확히 같은 40자리
  Git 커밋 SHA
- 이 계약은 콘텐츠 저장소의 송신 동작만 정의한다. 웹 저장소 수신 워크플로의
  배포·복구 동작은 웹 저장소의 `.github/workflows/deploy.yml`이 정의한다.

## 요구사항

### CD-001 prod 콘텐츠 디스패치

- `main` push는 `event_type: content-updated`를 보낸다.
- `client_payload.content_commit`은 정확한 콘텐츠 리비전이다.
- `main` push에서 `content-dev-updated`를 보내면 안 된다.

### CD-002 dev 콘텐츠 디스패치

- `dev` push는 `event_type: content-dev-updated`를 보낸다.
- `client_payload.content_commit`은 정확한 콘텐츠 리비전이다.
- `dev` push에서 `content-updated`를 보내면 안 된다.

### CD-003 실패 시 요청 차단

- `WEB_DISPATCH_TOKEN`이 없으면 GitHub API를 호출하지 않고 워크플로를 실패시킨다.
- `GITHUB_SHA`가 40자리 16진수 Git 커밋 SHA가 아니면 GitHub API를 호출하지 않고
  워크플로를 실패시킨다.
- 실행 브랜치가 `main` 또는 `dev`가 아니거나 비어 있으면 GitHub API를 호출하지
  않고 워크플로를 실패시킨다.

### CD-004 토큰 비공개

- `WEB_DISPATCH_TOKEN` 값은 payload, 명령 인자, 표준 출력 또는 표준 오류에
  포함하면 안 된다.

## Payload 예시

`main` push:

```json
{
  "event_type": "content-updated",
  "client_payload": {
    "content_commit": "0123456789abcdef0123456789abcdef01234567"
  }
}
```

`dev` push:

```json
{
  "event_type": "content-dev-updated",
  "client_payload": {
    "content_commit": "89abcdef0123456789abcdef0123456789abcdef"
  }
}
```

웹 저장소의 수신 워크플로는 `client_payload.content_commit`을 콘텐츠 저장소의
checkout `ref`로 사용하고, 이벤트와 허용 브랜치의 계보도 검증해야 한다. 이를 통해
실행 시점의 최신 브랜치가 아니라 이벤트가 가리킨 정확한 콘텐츠 커밋으로 사이트를
빌드한다.

## 활성화 조건과 제한

- 이 변경을 PR 브랜치에 push하는 것만으로는 dispatch가 발생하지 않는다. 워크플로는
  대상 브랜치에 존재한 뒤 그 브랜치에 발생한 다음 push부터 실행된다.
- 이 PR을 콘텐츠 `dev`에 병합하면 그 merge push 자체가 `content-dev-updated`를
  보낼 수 있다. 따라서 수신 워크플로와 dev 설정 준비 전에는 병합하지 않는다.
- GitHub의 `repository_dispatch`는 수신 워크플로 파일이 수신 저장소의 default branch에
  있을 때만 실행된다. 웹 저장소 default branch의 수신 계약이
  `content-dev-updated`와 `content-updated`를 모두 지원해야 한다.
- 수동 dispatch와 이 PR의 병합은 별도의 외부 변경이므로 명시적 승인 없이 실행하지
  않는다.

## 검증 매트릭스

| 요구사항 ID | 검증 내용 | 테스트 | 상태 |
|---|---|---|---|
| CD-001 | main은 prod 이벤트와 정확한 SHA만 전송 | `test_main_dispatches_prod_event_with_exact_content_commit` | Covered |
| CD-002 | dev는 dev 이벤트와 정확한 SHA만 전송 | `test_dev_dispatches_dev_event_with_exact_content_commit` | Covered |
| CD-003 | 토큰·SHA·브랜치 오류는 API 호출 전에 실패 | `test_missing_token_fails_before_calling_github`, `test_non_full_commit_sha_fails_before_calling_github`, `test_unknown_or_missing_branch_fails_before_calling_github` | Covered |
| CD-004 | 토큰이 payload·인자·출력에 노출되지 않음 | `test_token_is_not_exposed_in_payload_arguments_or_output`, `test_token_is_not_exposed_when_validation_fails` | Covered |
