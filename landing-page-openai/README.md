# Landing Page Agent (OpenAI)

OpenAI GPT-4를 활용한 고품질 랜딩 페이지 자동 생성 Agent이다.

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
│   ├── openai_client.py              # OpenAI API 클라이언트
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

1. **OpenAI GPT-4 통합**
   - GPT-4 또는 GPT-4-turbo를 사용한 고품질 코드 생성
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
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4-turbo
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
3. OpenAI API를 호출하여 컴포넌트를 순차적으로 생성한다
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

- **LLM**: OpenAI GPT-4 / GPT-4-turbo
- **프레임워크**: asyncio (비동기 처리)
- **검증**: Pydantic v2
- **API 클라이언트**: openai SDK
- **환경 관리**: python-dotenv

## Anthropic Claude와의 차이점

### API 구조
- **Claude**: 시스템 프롬프트와 메시지를 분리하여 전달
- **OpenAI**: 모든 메시지(시스템 포함)를 하나의 배열로 전달

### 응답 형식
- **Claude**: `response.content[0].text`
- **OpenAI**: `response.choices[0].message.content`

### 모델 선택
- **Claude**: `claude-sonnet-4-20250514`
- **OpenAI**: `gpt-4-turbo`, `gpt-4`, `gpt-4-turbo-preview`

### 토큰 제한
- **Claude**: 최대 8000 토큰
- **OpenAI**: 모델에 따라 다름 (기본 4000 토큰)

## 비대화형 모드

설정 파일을 사용하여 자동으로 실행한다:

```bash
# 설정 파일 복사
cp config.example.json my-config.json

# 설정 파일 편집
# my-config.json 파일을 열어 프로젝트 정보를 입력한다

# 비대화형 모드로 실행
python main.py --config-file my-config.json --non-interactive
```

## 생성된 프로젝트 실행

```bash
# 1. 출력 디렉토리로 이동
cd output

# 2. 의존성 설치
npm install

# 3. 개발 서버 실행
npm run dev

# 4. 브라우저에서 http://localhost:3000 열기
```

## API 키 발급 방법

### OpenAI API 키
1. https://platform.openai.com 방문
2. 계정 생성 또는 로그인
3. API Keys 섹션으로 이동
4. "Create new secret key" 클릭
5. 생성된 키를 복사하여 `.env` 파일에 입력

## 문제 해결

### API 키 오류
```
ValueError: OPENAI_API_KEY 환경변수가 설정되지 않았다
```
**해결 방법**: `.env` 파일에 올바른 API 키를 설정한다.

### Skills 디렉토리 오류
```
FileNotFoundError: Skills 디렉토리를 찾을 수 없다
```
**해결 방법**: 
- Skills 디렉토리가 올바른 위치에 있는지 확인한다
- `--skills-dir` 옵션으로 경로를 지정한다

### Rate Limit 에러
```
RateLimitError: Rate limit exceeded
```
**해결 방법**: 
- API 사용량 제한을 확인한다
- 재시도 횟수를 늘린다: `--max-retries 5`
- OpenAI 대시보드에서 사용량을 확인한다

## 생성 리포트

`generation_report.json` 파일은 다음 정보를 포함한다:

- 요청 정보
- 생성된 컴포넌트 목록
- 검증 결과
- 대화 기록
- 에러 통계

## 성능 최적화 팁

1. **모델 선택**: 
   - 빠른 생성: `gpt-4-turbo`
   - 높은 품질: `gpt-4`

2. **Temperature 조정**:
   - 일관된 결과: 0.3-0.5
   - 창의적 결과: 0.7-1.0

3. **토큰 제한**:
   - 짧은 컴포넌트: 2000 토큰
   - 긴 컴포넌트: 4000 토큰

## 라이선스

이 프로젝트의 라이선스 정보는 LICENSE 파일을 참조한다.

## 지원

문제가 발생하면:
1. 로그 파일을 확인한다
2. `generation_report.json`을 검토한다
3. GitHub Issues에 보고한다

## 기여

Pull Request는 언제나 환영한다!
