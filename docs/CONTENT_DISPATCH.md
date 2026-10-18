# 콘텐츠 배포 디스패치 계약

콘텐츠 저장소는 웹 저장소 `PyLadiesKorea/pyladies-seoul-web`에
`repository_dispatch` 이벤트를 보내 배포할 콘텐츠 커밋을 지정한다.
두 송신 워크플로 모두 웹 저장소의 Contents: write 권한만 가진
`WEB_DISPATCH_TOKEN`을 사용한다.

## main 반영 후 prod 배포

`.github/workflows/notify-web.yml`은 `main` push만 처리한다.
기존 prod 배포 계약은 다음과 같다.

- `event_type`은 `content-updated`다.
- `client_payload.content_commit`은 해당 `push` 실행의 `GITHUB_SHA`와 정확히 같은
  40자리 Git 커밋 SHA다.
- `WEB_DISPATCH_TOKEN`이 없거나 SHA 형식이 올바르지 않으면 요청을 보내지 않고
  워크플로를 실패시킨다.

```json
{
  "event_type": "content-updated",
  "client_payload": {
    "content_commit": "0123456789abcdef0123456789abcdef01234567"
  }
}
```

## 콘텐츠 PR의 dev 배포

`.github/workflows/notify-web-pr.yml`은 `main` 또는 `dev`를 대상으로 하는
`pull_request_target`의 `opened`, `synchronize`, `reopened`, `edited`,
`ready_for_review` 이벤트를 처리한다. PR 생성, 커밋 추가, 다시 열기, 대상 브랜치
변경 후의 열린 PR을 dev에 미리 반영하기 위한 이벤트다.

- 같은 콘텐츠 저장소에서 만든 PR만 처리한다. fork PR은 job 조건에서 제외하므로
  토큰을 사용하는 단계에 진입하지 않는다.
- 이 워크플로는 PR 메타데이터만 읽는다. PR 코드 checkout이나 실행은 하지 않는다.
- 실행 단계에서도 이벤트, action, 저장소, 열린 상태, 대상 브랜치를 검사한다.
- `event_type`은 `content-pr-updated`다.
- `client_payload.content_pr`은 PR 번호인 양의 정수다.
- `client_payload.content_commit`은 이벤트의 `pull_request.head.sha`인 40자리 SHA다.
  PR 대상 브랜치의 커밋을 나타내는 `GITHUB_SHA`를 대신 사용하면 안 된다.
- 번호나 SHA가 올바르지 않거나 `WEB_DISPATCH_TOKEN`이 없으면 디스패치하지 않는다.
- PR 이벤트는 dev 전용이다. prod 배포는 기존 `main` push 경로를 사용한다.

```json
{
  "event_type": "content-pr-updated",
  "client_payload": {
    "content_pr": 17,
    "content_commit": "0123456789abcdef0123456789abcdef01234567"
  }
}
```

수신 워크플로는 PR의 현재 상태, 대상 저장소와 브랜치, head SHA를 GitHub API로
다시 확인해야 한다. 닫힌 PR이나 최신 head와 다른 오래된 이벤트는 배포하지 않는다.
검증된 `content_commit`으로 콘텐츠를 checkout하고, 웹 `dev` 코드로 dev에 배포한다.

dev에서도 글은 `published: true`일 때만 표시한다. `published: false`인 초안을
강제로 공개하는 빌드 옵션은 사용하지 않는다. PR마다 별도 사이트를 만드는 방식이
아니므로, 공용 dev에는 마지막으로 성공한 배포가 표시된다. PR이 닫혔을 때 이전
배포로 자동 복원하지 않으며 다음 배포가 dev를 갱신한다.

## 활성화 조건

이 변경을 담은 PR을 올리는 것만으로 새 자동 배포 경로가 활성화되지는 않는다.
다음 조건을 함께 충족해야 한다.

1. 콘텐츠 PR의 대상 브랜치인 `main` 또는 `dev`에 신뢰된 송신 워크플로가 있어야 한다.
   새 송신 워크플로를 추가하는 PR 자체의 코드를 실행하는 방식은 사용하지 않는다.
2. 웹 저장소의 default branch에 `.github/workflows/deploy.yml` 수신 워크플로와
   `content-pr-updated` 처리 코드가 있어야 한다. GitHub의 `repository_dispatch`는
   수신 워크플로 파일이 default branch에 있을 때만 실행된다.
3. 웹 저장소의 `dev`에 해당 콘텐츠 커밋을 빌드하고 dev로 배포하는 코드가 있어야 한다.
4. 콘텐츠 저장소의 `WEB_DISPATCH_TOKEN`과 웹 저장소의 dev 배포 환경 설정이
   준비되어 있어야 한다.

송신 요청 성공만으로 배포 성공을 판단하지 않는다. 활성화 후 실제 콘텐츠 PR로 웹
저장소의 dev 배포 실행과 게시된 페이지를 확인해야 한다. `main` 대상 송신 경로와
prod 변경의 활성화는 별도의 승격 절차를 따른다.
