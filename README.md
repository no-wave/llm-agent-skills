# Agent Skills 활용으로  똑똑한 AI 에이전트 만들기


<img src="https://beat-by-wire.gitbook.io/beat-by-wire/~gitbook/image?url=https%3A%2F%2F3055094660-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FYzxz4QeW9UTrhrpWwKiQ%252Fuploads%252FGS6krP9wPXxdK8ZJ5mfb%252FLLM-Router.png%3Falt%3Dmedia%26token%3D80f4d16a-047d-463c-ac8b-63a447fdfa87&width=300&dpr=4&quality=100&sign=9ba1c420&sv=2" width="500" height="707"/>



## 책 소개

인공지능 에이전트 기술은 이제 단순한 질의응답을 넘어 복잡한 작업을 자율적으로 수행하는 단계로 진화하고 있다. 특히 대규모 언어 모델(LLM)의 발전과 함께 에이전트가 특정 도메인 지식과 작업 수행 능력을 갖추도록 하는 것이 중요해졌다. 이러한 맥락에서 'Agent Skills'는 에이전트에게 전문성을 부여하고, 복잡한 작업을 체계적으로 처리할 수 있도록 하는 핵심 메커니즘이다.

본서는 Claude API와 OpenAI API라는 두 가지 주요 LLM 플랫폼을 활용하여 Agent Skills를 구현하고 활용하는 실전 가이드를 제공한다. 단순히 이론적 설명에 그치지 않고, 실제 코드 구현부터 실무에 바로 적용할 수 있는 파이프라인 자동화까지 전 과정을 다룬다. Skills를 통해 에이전트는 마치 숙련된 전문가처럼 특정 작업을 일관되고 정확하게 수행할 수 있게 된다.

AI 에이전트 개발 영역에서 가장 중요한 도전 과제 중 하나는 에이전트의 행동을 예측 가능하고 제어 가능하게 만드는 것이다. Skills 기반 접근법은 이러한 문제에 대한 효과적인 해결책을 제시한다. 각 Skill은 명확하게 정의된 목적과 실행 방법을 가지며, 이를 통해 에이전트의 작업 흐름을 체계적으로 관리할 수 있다. 또한 Skills는 모듈화되어 있어 재사용성과 유지보수성이 뛰어나다.

본서를 집필하게 된 계기는 AI 에이전트 개발 현장에서 겪은 실제 경험에서 비롯되었다. 많은 개발자들이 강력한 LLM을 활용하면서도, 에이전트의 행동을 일관되게 제어하고 복잡한 워크플로우를 구성하는 데 어려움을 겪고 있다. Skills 패턴은 이러한 문제를 해결하는 검증된 방법론이지만, 실제 구현 사례와 체계적인 학습 자료가 부족한 실정이다. 본서는 이러한 간극을 메우고자 한다.

책의 전반부에서는 Skills의 기본 개념부터 시작하여 점진적으로 복잡도를 높여간다. 처음에는 간단한 텍스트 기반 Skill을 직접 구현하고, 이어서 Markdown과 YAML 파일을 활용한 구조화된 Skills 관리 방법을 배운다. 이 과정에서 독자는 Skills의 설계 원칙과 베스트 프랙티스를 자연스럽게 체득하게 된다.
중반부에서는 Claude와 OpenAI라는 두 가지 주요 LLM 제공자를 모두 지원하는 통합 아키텍처를 구축한다. 각 플랫폼의 특성과 장단점을 이해하고, 동일한 Skill을 두 플랫폼에서 모두 활용할 수 있는 방법을 학습한다. 실전 예제로는 랜딩 페이지 생성 시스템을 구축하는데, 이를 통해 Skills가 실제 비즈니스 문제를 해결하는 방식을 경험하게 된다.

후반부에서는 Skills를 활용한 고급 패턴들을 다룬다. ReAct와 Plan-Execute 같은 에이전트 워크플로우 패턴을 Skills와 결합하여 구현하고, 여러 Skills를 연결하는 파이프라인 자동화 시스템을 구축한다. 이러한 고급 패턴들은 복잡한 실무 문제를 해결하는 데 필수적인 도구가 된다.
본서의 모든 코드는 실제로 동작하는 완전한 예제이며, Python 생태계의 표준 도구들을 활용한다. Pydantic을 통한 데이터 검증, 타입 힌팅을 통한 코드 안정성 확보, 객체지향 설계 원칙 적용 등 현대적인 Python 개발 방법론을 따른다. 독자는 단순히 AI 에이전트 개발뿐만 아니라, 전문적인 Python 코드 작성 방법도 함께 배우게 된다.
AI 기술은 빠르게 변화하고 있지만, 본서에서 다루는 Skills 기반 접근법의 핵심 원칙은 시간이 지나도 유효하다. 작업을 명확하게 정의하고, 모듈화하며, 재사용 가능하게 만드는 것은 소프트웨어 공학의 보편적 원칙이다. 본서를 통해 독자는 이러한 원칙을 AI 에이전트 개발에 적용하는 방법을 익히게 될 것이다.


## 목 차

저자 소개
Table of Contents (목차)
서문: 들어가며

1장: Agent Skills 개요

1.1. Agent Skills 개요
1.2. 개요 및 환경 설정
1.3. 직접 읽기 방식 (Direct Reading Method)
1.4. Class 기반 구현 (Object-Oriented Approach)
1.5. 나만의 Skill 만들기 실습

2장: Markdown과 YAML 파일로 Skills 구현

2.1. Markdown 파일로 Skill 정의하기
2.2. YAML 파일로 Skill 메타데이터 관리하기
2.3. 또 다른 Skill 예제 생성
2.4. 파일 기반 SkillLoader 클래스 구현
2.5. 파일 기반 SkillAgent 구현
2.6. 파일 기반 Skills 실행 테스트
2.7. Skill 내보내기 및 공유

3장: Claud와 OpenAI API와 Skills 구현 비교

3.1. Claude API vs OpenAI API 개요
3.2. API 제공자 열거형 정의
3.3. 추상 베이스 클래스로 AI Client 인터페이스 정의
3.4. Client 구현
3.5. Unified Skill Agent 구현
3.6. Skills 디렉토리 생성 및 통합 테스트
3.7. 제공자별 비교 테스트

4장: Landing Page 에이전트 - Claude Skills

4.1. Landing Page Guide Skill 개요
4.2. Landing Page Guide Skill 정의
4.3. SkillAgent 클래스 준비
4.4. 에이전트 초기화 및 테스트 준비
4.5. 실습 AI 글쓰기 도구 랜딩 페이지
4.6. 생성된 파일 확인 및 분석
4.7. 커스터마이징 가이드 생성

5장: Landing Page 에이전트 - OpenAI API Skills

5.2. Landing Page Guide Skill 정의하기
5.3. Pydantic 모델로 랜딩 페이지 요구사항 정의
5.4. OpenAI 기반 LandingPageAgent 구현
5.5. 에이전트 초기화 및 Skill 로드
5.6. 랜딩 페이지 생성 및 저장
5.7. 생성된 랜딩 페이지 분석
5.8. 커스터마이징 가이드 생성

6장: Skills로 에이전트 워크플로우 자동화 - Claude

6.1. 에이전트 워크플로우 개요
6.2. 에이전트 상태 관리
6.3. ReAct 에이전트 구현
6.4. 예제1: 리서치 에이전트
6.5. Plan-Execute 에이전트 구현
6.6. 예제 2: 코딩 어시스턴트 에이전트
6.7. 워크플로우 결과 저장 및 분석

7장: Skills로 에이전트 워크플로우 자동화 - OpenAI

7.1. 에이전트 워크플로우 개요
7.2. Pydantic 모델로 에이전트 상태 관리
7.3. OpenAI 기반 ReAct 에이전트 구현
7.4. ReAct 에이전트용 Skills 생성
7.5. 예제 1: 리서치 에이전트
7.6. OpenAI 기반 Plan-Execute 에이전트 구현
7.7. 예제 2: OpenAI 코딩 어시스턴트 에이전트
7.8. 워크플로우 결과 저장 및 분석

8장: Skills 파이프라인 자동화 - Claude

8.1. Skills 파이프라인 개요
8.2. 파이프라인 단계 정의
8.3. 파이프라인 실행 엔진
8.4. 실습용 Skills 생성
8.5. 예제 1: 순차 파이프라인 구축
8.6. 예제 2: 조건부 파이프라인
8.7. 파이프라인 템플릿 저장 및 재사용

9장. Skills 파이프라인 자동화 - OpenAI API

9.1. Skills 파이프라인 개요
9.2. Pydantic 모델 정의
9.3. 파이프라인 구성 요소 모델
9.4. OpenAI 기반 파이프라인 엔진
9.5. Skills 정의 및 등록
9.6. 파이프라인 구성 및 실행
9.7. 결과 확인 및 저장
9.8. Pydantic 검증 예제

10장: Skills 실전 프로젝트

10.1. 프로젝트 landing-page-claude 개요
10.2. 프로젝트 landing-page-opanai 개요
10.3. 설치 및 환경 설정

11장: 결론 - 마무리 하며

References. 참고 문헌

## E-Book 구매

- Yes24: https://www.yes24.com/product/goods/167462940
- 교보문고: https://ebook-product.kyobobook.co.kr/dig/epd/sam/E000012247160
- 알라딘: http://aladin.kr/p/AEFAs

## Github 코드: 

https://github.com/no-wave/llm-agent-router
