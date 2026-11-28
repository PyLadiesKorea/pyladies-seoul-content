---
title: "PyLadies Seoul과 함께 한 나의 첫 글로벌 PyCon"
author: 차화영
date: 2026-11-25
image: IMG_6517.webp
published: true
---

지난 10월 17일, 18일 양일 동안 PyCon Taiwan 2026에 참석하였습니다. 포스터 세션에서 서울의 Python 커뮤니티를 소개하고, 발표를 듣고, 아시아 여러 지역의 PyLadies와 Python 커뮤니티 사람들을 만났습니다.

![PyCon TW 26 포토월](/content-media/stories/20261125-pycon-tw-2026-recap-chy/pycon-tw-2026-photo-wall.webp)

*REFACTOR. FIND YOUR NEXT SHAPE. PyCon Taiwan 2026 포토월.*

## 포스터 앞에서 PyLadies Seoul을 소개하며

포스터 세션에서 *Growing Together with PyLadies Seoul* PyLadies Seoul을 소개했습니다. 모임과 스터디를 통해 서로를 알게 되고, 배운 내용을 나누거나 행사를 함께 준비하면서 맡을 수 있는 일이 늘어나는 과정을 설명했습니다. 포스터를 보러 온 분들에게는 11월 서울에서 열리는 PyLadies Asia Conference도 함께 소개했습니다. [PyCon Taiwan 공식 포스터 프로그램](https://tw.pycon.org/2026/en-us/events/poster-sessions) · [PyLadies Asia Conference 2026](https://www.meetup.com/ko-kr/seoul-pyladies-meetup/events/317021466/)

![포스터 앞에서 참가자들에게 PyLadies Seoul을 설명하는 모습](/content-media/stories/20261125-pycon-tw-2026-recap-chy/pyladies-seoul-poster-1.webp)

*포스터 앞에서 PyLadies Seoul을 설명하는 중.*

![PyLadies Seoul 포스터 앞에서 함께 찍은 단체 사진](/content-media/stories/20261125-pycon-tw-2026-recap-chy/IMG_6517.webp)

*포스터 세션을 함께한 사람들과.*

## PyLadies Kaohsiung 오거나이저와의 만남

PyLadies Kaohsiung 부스에 찾아가 오거나이저를 만났습니다. 서로의 커뮤니티가 어떻게 모임을 운영하는지 이야기를 나누었습니다.

![PyLadies Kaohsiung 오거나이저와 팻말을 들고 찍은 사진](/content-media/stories/20261125-pycon-tw-2026-recap-chy/pyladies-kaohsiung-booth.webp)

*PyLadies Kaohsiung 오거나이저와 함께.*

이어서 PyLadies Asia 멤버들과 포토월 앞에 모여 단체 사진도 찍었습니다. 서로 다른 도시에서 활동하지만 같은 이름으로 모인 사람들을 한자리에서 만나니, 11월 서울에서 다시 만날 날이 더 기다려졌습니다.

![PyCon TW 26 포토월 앞에 모인 PyLadies Asia 멤버들](/content-media/stories/20261125-pycon-tw-2026-recap-chy/pyladies-asia-group-pic.webp)

*PyLadies Asia 멤버들과 단체 사진.*

## 들은 발표

**Claudia Ng | Learning from 8,000+ Prompts to My AI App Without Reading the Messages: Privacy-First Topic Modeling in Python**

AI 앱에 쌓인 대화 기록에는 제품을 개선할 단서가 많지만, 가족 이야기나 건강 정보처럼 민감한 내용도 함께 들어 있습니다. 대화를 직접 읽어 보는 방식은 규모가 커지면 감당하기 어렵고 개인정보 위험도 큽니다. Claudia는 자신이 만든 광둥어 회화 튜터 CantoAI의 대화 8,000여 턴을, 메시지를 하나하나 읽지 않고 분석한 과정을 소개했습니다.

파이프라인은 다섯 단계입니다. 다국어 임베딩(SentenceTransformer)으로 문장을 벡터로 바꾸고, UMAP으로 차원을 줄인 뒤, BERTopic으로 HDBSCAN 클러스터링을 합니다. 그다음 LLM으로 주제 이름과 카테고리를 붙이고, pandas로 집계해 Plotly treemap으로 시각화합니다. 저장 단계에서 정규식으로 개인정보를 지우고, `min_cluster_size`를 개인정보 보호 기준으로 활용하며, 공개 결과에는 원문 대신 집계와 키워드만 남긴다는 점이 인상 깊었습니다. [공식 세션 소개](https://tw.pycon.org/2026/en-us/conference/talk/387)

![Claudia Ng 발표의 5단계 비지도 학습 파이프라인 슬라이드](/content-media/stories/20261125-pycon-tw-2026-recap-chy/Claudia-Ng-talk.webp)

*Claudia Ng 발표의 5-Step Unsupervised Pipeline 슬라이드.*

**조성수 | Should we translate open source in the age of AI?**

파이콘 한국 준비위원회 멤버이자 OpenStack i18n SIG 메인테이너인 성수님의 라이트닝 토크도 들었습니다. AI 시대에도 오픈소스를 번역해야 하는지에 대한 질문을 던진 발표였습니다. 타이베이에서 한국 커뮤니티 분의 발표를 들으니 반가웠습니다.

![조성수 님의 라이트닝 토크 제목 슬라이드](/content-media/stories/20261125-pycon-tw-2026-recap-chy/Seongsoo-lightning-talk.webp)

*성수님의 라이트닝 토크.*

## Airflow User Group Korea 부스

한국에서 온 Airflow User Group Korea 부스에도 들렀습니다. 바람개비와 Apache Airflow 깃발을 들고 함께 사진을 찍었습니다.

![Apache Airflow 깃발과 바람개비를 든 Airflow User Group Korea 부스 사람들](/content-media/stories/20261125-pycon-tw-2026-recap-chy/airflow-usergroup-korea-booth.webp)

*Airflow User Group Korea 부스에서.*

첫 해외 PyCon을 PyLadies Seoul과 함께할 수 있어 더욱 뜻깊었습니다. 글로벌 Pythonista로 거듭나는 기분이었달까요?!