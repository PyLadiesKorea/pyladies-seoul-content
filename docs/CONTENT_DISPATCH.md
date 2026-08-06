# 콘텐츠 배포 디스패치 계약

콘텐츠 저장소의 `main` 브랜치에 변경이 반영되면
`.github/workflows/notify-web.yml`이 웹 저장소에 `repository_dispatch` 이벤트를 보낸다.
디스패치가 어느 콘텐츠 스냅샷을 배포해야 하는지 모호하지 않도록, 송신자는 아래
계약을 지킨다.

- `event_type`은 `content-updated`다.
- `client_payload.content_commit`은 해당 `push` 실행의 `GITHUB_SHA`와 정확히 같은
  40자리 Git 커밋 SHA다.
- `WEB_DISPATCH_TOKEN`이 없거나 SHA 형식이 올바르지 않으면 요청을 보내지 않고
  워크플로를 실패시킨다.
- 이 워크플로는 `main` push만 처리한다. dev PR 이벤트는 보내지 않는다.

구현은 draft PR
[#5](https://github.com/PyLadiesKorea/pyladies-seoul-content/pull/5)에서 dev 대상으로
먼저 검토한다. workflow trigger가 `main`으로 제한되어 있으므로 이 코드를 dev에
병합하는 것만으로 외부 dispatch가 발생하지 않는다. 실제 활성화는 별도 승인을 받은
dev→main 승격 이후다.

예시 payload:

```json
{
  "event_type": "content-updated",
  "client_payload": {
    "content_commit": "0123456789abcdef0123456789abcdef01234567"
  }
}
```

웹 저장소의 수신 워크플로는 `client_payload.content_commit`을 콘텐츠 저장소의
checkout `ref`로 사용해야 한다. 이를 통해 실행 시점의 최신 브랜치가 아니라, 이벤트가
가리킨 정확한 콘텐츠 커밋으로 사이트를 빌드할 수 있다.

## 현재 수신 제한

GitHub의 `repository_dispatch`는 수신 워크플로 파일이 수신 저장소의 default branch에
있을 때만 실행된다. 따라서 웹 저장소의 default branch에
`.github/workflows/deploy.yml`이 존재하기 전에는 이 저장소의 송신 요청이 성공해도 웹
배포 실행이 시작되지 않는다. 이 제한이 해소되기 전까지 dev PR 디스패치를 추가해도
안전한 end-to-end 경로가 되지 않으므로 지원하지 않는다.
