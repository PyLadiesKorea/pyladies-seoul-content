# content/ — 사이트 글 저장소

이 폴더가 **PyLadies Seoul 웹사이트의 내용**이에요. 여기 파일을 고쳐서 PR을 올리고,
`main`에 머지되면 사이트에 자동으로 반영돼요. (더 이상 구글 시트 안 씁니다.)

**핵심 규칙: 글 하나 = 폴더 하나.** 그 안에 언어별 파일 `ko.md`(+ 선택 `en.md`)와 이미지를 둬요.

```
content/
├── events/     이벤트  (하나당 폴더)
├── stories/    활동 후기·이야기
├── members/    멤버    (하나당 폴더)
├── about/      행동강령 등
└── thanks/     후원·자원봉사·기여 감사 인사
```

> 왜 언어별 파일이냐(gettext `.po` 아니고)는 `docs/I18N_CONTENT_TRANSLATION.md` 참고.

---

## 새 이벤트 올리기

1. `events/` 안에 폴더를 만들어요. **이름은 `날짜-영문제목`** (이게 웹주소가 돼요):

   ```
   events/20260726-git-tutorial-workshop/
   ```
   - 날짜 `YYYYMMDD`(행사 시작일)를 앞에 → 자동 시간순 정렬.
   - **한글 제목은 파일명이 아니라 `ko.md` 안 `title:` 에** 적어요.

2. 그 안에 **`ko.md`** (한국어):

   ```markdown
   ---
   title: 깃 튜토리얼 워크샵 (2회차)
   type: workshop
   start: 2026-07-26 13:00
   end: 2026-07-26 17:00
   location: 신림 관악청년청
   image: poster.png
   published: true
   links:
   - meetup: https://www.meetup.com/seoul-pyladies-meetup/events/315705865/
   ---

   여기부터 한국어 본문. 마크다운으로 자유롭게.
   ```

3. 영어가 있으면 같은 폴더에 **`en.md`** (선택 — 없으면 한국어로 폴백):

   ```markdown
   ---
   title: Git Tutorial Workshop (2nd Edition)
   location: Seminar Room (4th Floor), Gwanak Youth Center, Sillim
   ---

   English body here.
   ```
   - `title:`과 `location:`은 각각 생략 가능하며, 생략한 값은 한국어로 표시돼요. **본문만 넣어도 돼요.**
   - 날짜·링크 같은 **공통 정보는 `ko.md`에만** 두면 돼요.

4. **사진**은 폴더에 같이 넣고(예: `poster.png`) `image:` 에 파일명을 적어요. 이미지는 언어 공통 — 한 번만.

### 이벤트 필드 (`ko.md` frontmatter)

| 필드 | 뜻 | 필수 |
|------|-----|------|
| `title` | 한글 제목 | ✅ |
| `type` | 아래 종류 중 하나 | ✅ |
| `start` | 시작 `YYYY-MM-DD HH:MM` (한국시간) | ✅ |
| `end` | 종료 시각 | |
| `location` | 장소 | |
| `price` | 참가비(원). 무료면 비워둠 | |
| `image` | 폴더 안 사진 파일명, 또는 전체 URL | |
| `published` | `true` 공개 / `false` 숨김 | ✅ |
| `links` | 신청/외부 링크 목록 | |

- **type**: `workshop` `seminar` `tutorial` `study` `bookclub` `networking` `conference` `other`
- **links 플랫폼**: `meetup` `eventus` `instagram` `twitter` `linkedin`

---

## 새 스토리(활동 후기) 올리기

`stories/` 안에 폴더 + `ko.md`. **행사 후기·활동 기록·이야기**를 여기 남겨요 (이벤트는 "홍보", 스토리는 "후기").

```markdown
---
title: 깃 워크샵 2회차 후기
date: 2026-07-27
image: photo.jpg
published: true
related_events:
- 20260726-git-tutorial-workshop-2
---

후기 본문을 마크다운으로. 영어는 `en.md`에.
```

- `date`: 작성일 `YYYY-MM-DD` (목록 정렬용)
- `related_events`: **관련 이벤트 폴더 이름** 목록. 여기 한 번만 적으면 → 이벤트 페이지엔 "Related Stories", 스토리 페이지엔 "Related Events"가 **자동으로 양방향 표시**돼요.
- 파일명(폴더명)은 이벤트처럼 `날짜-영문제목` 권장.

---

## 새 멤버 추가

`members/<이름>/ko.md`:

```markdown
---
name: 최예리
type: maker
intro: 한 줄 소개 (카드에 인용으로 표시)
image: cover.webp
links:
- github: https://github.com/...
- linkedin: https://linkedin.com/in/...
---

여기 본문은 **인터뷰**. 없으면 비워둬도 돼요 (그럼 인터뷰 섹션이 안 뜸).

**Q. 파이썬 어떻게 시작하셨어요?**
A. ...
```

- **type**: `organizer` (운영진) / `maker` / `member`
- **intro**: 짧은 인용(frontmatter) — 카드·목록에 표시. **인터뷰**: 본문(길게) — 상세페이지에만.
- **image**: 사진 파일을 폴더에 넣고(예: `cover.webp`) 파일명을 적어요. 이미지는 언어 공통.
- **links 플랫폼**: `github` `linkedin` `twitter` `discord`
- 영어는 `en.md` — frontmatter `name`·`intro`(영문) + 본문(영문 인터뷰).
- ⚠️ **이메일·전화번호는 절대 넣지 마세요.** 이 저장소는 공개예요.
- 멤버가 나가면 그 폴더를 지우면 돼요.

조직 연락처 allowlist 등 공개 멤버 연락처 보호 규칙은
[`docs/CONTENT_PRIVACY.md`](docs/CONTENT_PRIVACY.md)를 따릅니다.

---

## Thanks to에 감사 인사 추가

`thanks/<영문-슬러그>/ko.md`:

```markdown
---
name: 공개 동의를 받은 표시 이름
type: volunteer
contribution: 2026 Git 워크숍 현장 운영과 사진 촬영
image: cover.webp
order: 10
published: true
---

행사가 매끄럽게 진행되도록 도와주셔서 감사합니다.
```

- **type**: `donor` / `volunteer` / `contributor` / `sponsor` / `partner` / `other`
- **contribution**: 어떤 도움을 주었는지 짧게 적어요.
- 본문: 카드에 표시할 감사 문구를 Markdown으로 적어요.
- **image**: 선택. 폴더 안 사진을 지정하며, 없으면 PyLadies Seoul 로고가 표시돼요.
- **order**: 작은 숫자가 먼저 표시돼요.
- **published**: `false`면 사이트에 표시되지 않아요.
- 영어는 선택 `en.md`에 `name`·`contribution` frontmatter와 영문 감사 문구를 적어요. 비워두면 한국어로 폴백해요.

> ⚠️ 이름과 사진은 배포 즉시 공개됩니다. 당사자에게 공개 동의를 받은 자료만 추가하고, 이메일·전화번호 등 개인 연락처는 절대 넣지 마세요. 익명을 원하면 동의한 표시명을 사용하고 사진을 생략하세요.

---

## 행동강령(About) 고치기

`about/code-of-conduct/ko.md` (한국어), `en.md` (영어) 를 고치면 돼요.

---

## 글 올리는 흐름

1. 브랜치 만들고 파일 추가/수정
2. PR 올리기 → 리뷰 → `main` 머지
3. 몇 분 뒤 사이트에 반영 ✨

`main` 머지 후 웹 저장소에 전달되는 커밋 SHA와 현재 수신 제한은
[`docs/CONTENT_DISPATCH.md`](docs/CONTENT_DISPATCH.md)에 정리되어 있어요.
