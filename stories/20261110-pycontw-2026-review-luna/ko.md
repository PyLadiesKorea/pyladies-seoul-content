---
title: "타이베이에서 소개한 PyLadies Seoul의 참여와 기여"
author: 윤수진
date: 2026-11-10
image: cover.webp
published: true
---

10월 17일과 18일, PyLadies Seoul 동료들과 타이베이 의학대학교에서 열린 PyCon Taiwan 2026에 다녀왔습니다. 포스터 세션에서 서울의 Python 커뮤니티를 소개하고, 처음 모임에 온 사람이 이후에 어떤 방식으로 활동에 참여하고 기여할 수 있는지 이야기했습니다.

## 포스터 앞에서 나눈 이야기

발표 제목은 *From Connection to Contribution: Growing Together with PyLadies Seoul*이었습니다. 모임과 스터디를 통해 서로를 알게 되고, 배운 내용을 나누거나 행사를 함께 준비하면서 맡을 수 있는 일이 늘어나는 과정을 포스터에 담았습니다. 처음 오는 분에게 어떤 모임을 소개할지, 관심이 생긴 분에게 다음 활동을 어떻게 안내할지는 서울에서 모임을 열 때도 계속 고민하는 질문입니다. [PyCon Taiwan 공식 포스터 프로그램](https://tw.pycon.org/2026/en-us/events/poster-sessions)

![참가자들과 함께 PyLadies Seoul 포스터 앞에서 찍은 사진](/content-media/stories/20261110-pycontw-2026-review-luna/pyladies-seoul-poster.webp)

*PyLadies Seoul 포스터 세션.*

현장에서는 PyLadies Kaohsiung 부스를 찾아가 서로의 커뮤니티 활동을 이야기했습니다.

![PyLadies Kaohsiung 팻말을 든 부스 참가자들](/content-media/stories/20261110-pycontw-2026-review-luna/pyladies-kaohsiung-booth.webp)

*PyLadies Kaohsiung 부스에서.*

PythonAsia 관계자들과도 교류하고, 포스터를 보러 온 분들에게 11월 서울에서 열리는 PyLadies Asia Conference를 소개했습니다. 다음 행사에서는 처음 온 분이 다음 모임이나 참여 방법을 쉽게 찾을 수 있도록 안내를 더 잘 정리해 보고 싶습니다. [PyLadies Asia Conference 2026](https://www.meetup.com/ko-kr/seoul-pyladies-meetup/events/317021466/)

![PyCon Taiwan 포토월 앞에 모인 PyLadies Asia 사람들](/content-media/stories/20261110-pycontw-2026-review-luna/pyladies-asia-group.webp)

*PyCon Taiwan에서 만난 PyLadies Asia 사람들과 함께.*

## 첫날에 들은 세 세션

**프렐리아(Freilla Mae Espinola) | From PyCon APAC to PythonAsia**

PyCon APAC이 PythonAsia로 이어지는 과정과 아시아의 여러 Python 커뮤니티가 함께 행사를 운영하는 방식을 들었습니다. 대만은 2014년과 2022년에 PyCon APAC을 열었습니다. 지금은 개최지의 커뮤니티가 행사를 이끌고, Python Asia Organization(PAO)이 공용 인프라, 후원, 운영 절차를 지원합니다. 덕분에 개최지와 운영팀이 바뀌어도 앞선 팀이 쌓은 경험을 이어받을 수 있습니다. PyLadies Seoul에서도 행사 준비 과정과 결정 이유를 남겨 두면 다음 운영팀이 그 위에서 시작할 수 있겠다고 생각했습니다. [공식 세션 소개](https://tw.pycon.org/2026/en-us/conference/talk/373)

![프렐리아가 PyCon APAC에서 PythonAsia로 이어진 과정을 소개하는 장면](/content-media/stories/20261110-pycontw-2026-review-luna/freilla-pythonasia-talk.webp)

*프렐리아의 PythonAsia 발표.*

**유이치(Yuichi, @whitphx) | The hidden current context**

하나의 스레드에서 여러 `asyncio` 태스크가 번갈아 실행되면, `threading.local()`로 저장한 값은 같은 스레드의 태스크들이 공유합니다. 두 요청의 로그가 번갈아 찍힐 때 `ContextVar`에 요청 ID를 담아두면 호출이 여러 함수를 거쳐도 해당 태스크의 값을 읽을 수 있습니다. 유이치는 WebAssembly 기반의 Pyodide를 써서 브라우저에서 Streamlit 앱을 실행하는 Stlite를 예로 들었습니다. 작업 디렉터리는 같은 런타임에서 여전히 공유되기 때문에, Stlite는 태스크별 정보를 기억해 두고 코루틴이 다시 실행될 때 해당 작업 디렉터리를 적용합니다. [공식 세션 소개](https://tw.pycon.org/2026/en-us/conference/talk/376)

![유이치가 contextvars 발표의 제목 슬라이드를 가리키는 장면](/content-media/stories/20261110-pycontw-2026-review-luna/yuichi-contextvars-talk.webp)

*유이치의 contextvars 발표.*

**Cheuk Ting Ho | Audit and evaluate AI generated Python code**

AI가 작성한 Python 코드를 어떻게 검증할지 다룬 워크숍이었습니다. `pytest`로 기대한 동작을 확인하고, Hypothesis로 여러 입력에서도 지켜야 하는 조건을 검사합니다. 이어 정적 분석 도구로 보안과 의존성을 살피고, 공격자가 줄 법한 입력을 넣어 프로그램을 시험합니다. Ruff로 코드 규칙을, `ty`로 타입을 검사하고, 프롬프트의 성능을 지표로 측정해 기록하는 방법도 다뤘습니다. 팀 리뷰에서도 확인한 동작과 실패 조건을 남겨 두면 다음 사람이 검증을 이어갈 수 있겠습니다. [공식 워크숍 소개](https://tw.pycon.org/2026/en-us/conference/tutorial/28)

![Cheuk이 Hypothesis 실습 슬라이드를 띄워 설명하는 장면](/content-media/stories/20261110-pycontw-2026-review-luna/cheuk-hypothesis-workshop.webp)

*Cheuk의 워크숍에서 다룬 Hypothesis 실습.*

## 본행사 다음 날의 Taipei.py After-Sprint

10월 19일에는 타이베이의 Python 커뮤니티 Taipei.py가 비공식 After-Sprint를 열었습니다. 장소는 타이베이 다안구 둔화남로 2단 206번지 12층에 있는 Taiwan Mobile의 TWM Social Hub였습니다. 대만의 오픈소스 프로젝트와 기여자 양성을 지원하는 Taione Open Source Foundation(財團法人開源基金會)이 행사 장소를 지원했습니다. 이 재단은 오픈소스 AI 인프라 프로젝트의 유지관리자에게 코드 리뷰를 받고 실제 이슈에 기여할 수 있는 펠로십도 운영합니다. [Taipei.py 행사 안내](https://www.meetup.com/taipei_py/events/316510887/) · [Taione 재단 행사 일정](https://taione.org/calendar) · [Taione 펠로십](https://taione.org/fellowship/about)

![After-Sprint 장소 벽에 불이 들어온 OPEN POSSIBLE 문구](/content-media/stories/20261110-pycontw-2026-review-luna/after-sprint-entrance.webp)

*After-Sprint 장소에서 본 OPEN POSSIBLE 문구.*

저는 늦게 도착해서 이번에는 프로젝트에 직접 기여하지 못했습니다. 행사 안내에는 프로젝트를 소개하고, 기능 개발이나 문서 개선, 테스트 등을 함께 한 뒤 결과를 공유하는 순서가 나와 있었습니다. [After-Sprint 프로그램](https://www.meetup.com/taipei_py/events/316510887/)

![After-Sprint 참가자들이 테이블에서 노트북을 열고 작업하는 모습](/content-media/stories/20261110-pycontw-2026-review-luna/after-sprint-workspace.webp)

*Taipei.py After-Sprint 작업 시간.*

포스터에서 이야기한 첫 참여를 실제 기여로 이어가려면, 이렇게 그날 시작할 수 있는 작업과 옆에서 물어볼 사람이 있는 자리를 만드는 게 좋겠다고 생각했습니다.

![Taiwan Mobile과 TWM Social Hub 표지 앞에 모인 After-Sprint 참가자들](/content-media/stories/20261110-pycontw-2026-review-luna/after-sprint-group.webp)

*TWM Social Hub에서 찍은 After-Sprint 단체 사진.*

함께 포스터를 준비하고 타이베이에서 자리를 지켜 준 차화영, 채서영, 최연우, 박지호 님께 감사드립니다.

대표 사진 최연우.
