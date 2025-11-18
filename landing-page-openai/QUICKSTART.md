# 빠른 시작 가이드

Landing Page Agent (OpenAI)를 빠르게 시작하는 방법이다.

## 1단계: 환경 설정

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력한다
```

## 2단계: Skills 디렉토리 준비

Skills 디렉토리 구조를 확인한다:

```
landing_page_agent/
└── skills/
    └── landing-page-guide/
        ├── SKILL.md
        └── references/
            ├── 11-essential-elements.md
            └── component-examples.md
```

업로드한 파일을 `skills/landing-page-guide/` 디렉토리에 배치한다.

## 3단계: 실행

### 대화형 모드 (추천)

```bash
python main.py
```

프롬프트를 따라 프로젝트 정보를 입력한다.

### 설정 파일 사용

```bash
# 1. 설정 파일 복사
cp config.example.json my-config.json

# 2. my-config.json 파일을 편집한다

# 3. 실행
python main.py --config-file my-config.json --non-interactive
```

## 4단계: 생성된 프로젝트 실행

```bash
# 1. 출력 디렉토리로 이동
cd output

# 2. 의존성 설치
npm install

# 3. 개발 서버 실행
npm run dev

# 4. 브라우저에서 http://localhost:3000 열기
```

## 주요 옵션

```bash
# Skills 디렉토리 지정
python main.py --skills-dir /path/to/skills

# 출력 디렉토리 지정
python main.py --output-dir /path/to/output

# 재시도 횟수 조정
python main.py --max-retries 5

# 모든 옵션 사용
python main.py \
  --skills-dir ./skills/landing-page-guide \
  --output-dir ./my-landing-page \
  --config-file config.json \
  --non-interactive
```

## 문제 해결

### API 키 오류
- `.env` 파일에 올바른 OPENAI_API_KEY를 설정했는지 확인한다
- API 키는 https://platform.openai.com/api-keys 에서 발급받는다

### Skills 오류
- Skills 디렉토리가 올바른 위치에 있는지 확인한다
- `--skills-dir` 옵션으로 경로를 명시한다

### Rate Limit 에러
- OpenAI API 사용량 제한을 확인한다
- 잠시 대기 후 재시도한다
- `--max-retries` 옵션으로 재시도 횟수를 늘린다

### 자세한 정보
- `USAGE.md` 파일을 참조한다
- `README.md` 파일을 참조한다

## 생성되는 파일

- `app/layout.tsx` - 루트 레이아웃
- `app/page.tsx` - 메인 페이지
- `components/*.tsx` - 각종 컴포넌트 (11가지 요소)
- `package.json` - npm 설정
- `README.md` - 프로젝트 문서
- `generation_report.json` - 생성 리포트

모든 파일은 프로덕션 레벨의 TypeScript/React 코드이며, Next.js 14+ App Router와 ShadCN UI를 사용한다.

## OpenAI 모델 선택

환경 변수에서 모델을 선택할 수 있다:

```bash
# .env 파일에서
MODEL_NAME=gpt-4-turbo        # 빠르고 효율적 (추천)
MODEL_NAME=gpt-4              # 높은 품질
MODEL_NAME=gpt-4-turbo-preview # 최신 기능
```

## 예상 비용

OpenAI API 사용 비용 (2024년 기준):

### GPT-4-turbo
- 입력: $10 / 1M 토큰
- 출력: $30 / 1M 토큰
- 랜딩 페이지 1개 생성: 약 $0.50-1.00

### GPT-4
- 입력: $30 / 1M 토큰
- 출력: $60 / 1M 토큰
- 랜딩 페이지 1개 생성: 약 $1.50-3.00

**참고**: 실제 비용은 생성되는 컴포넌트의 복잡도에 따라 달라진다.

## 다음 단계

1. 생성된 랜딩 페이지를 커스터마이징한다
2. 이미지와 콘텐츠를 실제 데이터로 교체한다
3. ShadCN UI 컴포넌트를 추가로 설치한다
4. SEO 메타데이터를 최적화한다
5. 프로덕션 배포를 준비한다

## 지원

문제가 발생하면:
1. 로그 파일을 확인한다
2. `generation_report.json`을 검토한다
3. GitHub Issues에 보고한다
