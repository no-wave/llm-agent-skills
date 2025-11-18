# Landing Page Agent

Claude Sonnet 4.5를 활용한 고품질 랜딩 페이지 자동 생성 Agent이다.

## 프로젝트 구조

```
landing_page_agent/
├── README.md                          # 프로젝트 설명 문서
├── requirements.txt                   # Python 의존성 패키지
├── config.py                         # 설정 및 환경변수 관리
├── main.py                           # Agent 실행 메인 파일
├── models/
│   ├── __init__.py
│   ├── validation.py                 # Pydantic 검증 모델
│   └── memory.py                     # 대화 기록 관리
├── agent/
│   ├── __init__.py
│   ├── claude_client.py              # Claude API 클라이언트
│   ├── landing_page_generator.py     # 랜딩 페이지 생성 로직
│   └── recovery.py                   # 에러 복구 및 재시도
├── skills/
│   └── landing-page-guide/           # Skill 문서 디렉토리
│       ├── SKILL.md
│       └── references/
│           ├── 11-essential-elements.md
│           └── component-examples.md
└── output/                           # 생성된 파일 출력 디렉토리
```

## 주요 기능

1. **Claude Sonnet 4.5 Skills 통합**
   - Landing Page Guide Skill을 읽어 컨텍스트 제공한다
   - 11가지 필수 요소를 모두 포함하는 랜딩 페이지를 생성한다

2. **Memory 시스템**
   - 대화 기록을 메모리에 저장하고 관리한다
   - 컨텍스트 연속성을 유지한다

3. **Pydantic 검증**
   - 생성된 컴포넌트의 데이터 구조를 검증한다
   - 타입 안정성을 보장한다

4. **비동기 처리**
   - asyncio를 사용한 효율적인 API 호출을 수행한다
   - 여러 컴포넌트를 동시에 생성할 수 있다

5. **자동 복구**
   - API 실패 시 자동으로 재시도한다
   - 에러 발생 시 복구 전략을 실행한다

## 설치 방법

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가한다:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## 사용 방법

```bash
# 기본 실행 (현재 디렉토리의 skills 폴더 사용)
python main.py

# Skill 디렉토리 지정
python main.py --skills-dir /path/to/skills/landing-page-guide

# 출력 디렉토리 지정
python main.py --output-dir /path/to/output

# 전체 옵션 사용
python main.py \
  --skills-dir ./skills/landing-page-guide \
  --output-dir ./output \
  --max-retries 3
```

## 실행 흐름

1. Skill 문서를 읽어 컨텍스트를 구성한다
2. 사용자에게 랜딩 페이지 요구사항을 입력받는다
3. Claude API를 호출하여 컴포넌트를 순차적으로 생성한다
4. 각 컴포넌트 생성 후 사용자 확인을 받는다
5. 생성된 파일을 output 디렉토리에 저장한다
6. 모든 11가지 요소가 포함되었는지 검증한다

## 출력 예시

```
output/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── Header.tsx
│   ├── Hero.tsx
│   ├── MediaSection.tsx
│   ├── Benefits.tsx
│   ├── Testimonials.tsx
│   ├── FAQ.tsx
│   ├── FinalCTA.tsx
│   └── Footer.tsx
├── public/
│   └── images/
└── package.json
```

## 기술 스택

- **LLM**: Claude Sonnet 4.5
- **프레임워크**: asyncio (비동기 처리)
- **검증**: Pydantic v2
- **API 클라이언트**: anthropic SDK
- **환경 관리**: python-dotenv
