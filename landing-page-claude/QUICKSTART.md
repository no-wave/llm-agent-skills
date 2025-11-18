# 빠른 시작 가이드

Landing Page Agent를 빠르게 시작하는 방법이다.

## 1단계: 환경 설정

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY를 입력한다
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
- `.env` 파일에 올바른 ANTHROPIC_API_KEY를 설정했는지 확인한다

### Skills 오류
- Skills 디렉토리가 올바른 위치에 있는지 확인한다
- `--skills-dir` 옵션으로 경로를 명시한다

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
