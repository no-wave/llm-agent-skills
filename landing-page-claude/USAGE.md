# Landing Page Agent 사용 가이드

이 문서는 Landing Page Agent의 상세한 사용 방법을 설명한다.

## 목차

1. [설치](#설치)
2. [기본 사용법](#기본-사용법)
3. [고급 사용법](#고급-사용법)
4. [설정 파일](#설정-파일)
5. [출력 구조](#출력-구조)
6. [문제 해결](#문제-해결)

## 설치

### 1. 저장소 클론

```bash
git clone <repository-url>
cd landing_page_agent
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정한다:

```bash
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY를 입력한다
```

### 4. Skills 디렉토리 설정

Skills 디렉토리가 올바른 위치에 있는지 확인한다:

```
landing_page_agent/
└── skills/
    └── landing-page-guide/
        ├── SKILL.md
        └── references/
            ├── 11-essential-elements.md
            └── component-examples.md
```

## 기본 사용법

### 대화형 모드 (권장)

가장 쉬운 사용 방법이다. 프로그램이 단계별로 안내한다:

```bash
python main.py
```

프로그램 실행 후:
1. 프로젝트 정보를 입력한다
2. 각 컴포넌트 생성 후 확인한다
3. 생성이 완료되면 출력 디렉토리를 확인한다

### 비대화형 모드

설정 파일을 사용하여 자동으로 실행한다:

```bash
python main.py --config-file config.example.json --non-interactive
```

## 고급 사용법

### 커스텀 Skills 디렉토리 지정

```bash
python main.py --skills-dir /path/to/custom/skills
```

### 커스텀 출력 디렉토리 지정

```bash
python main.py --output-dir /path/to/output
```

### 재시도 횟수 조정

API 호출 실패 시 재시도 횟수를 조정한다:

```bash
python main.py --max-retries 5
```

### 모든 옵션 사용

```bash
python main.py \
  --skills-dir ./skills/landing-page-guide \
  --output-dir ./my-project \
  --max-retries 3 \
  --config-file my-config.json \
  --non-interactive
```

## 설정 파일

### JSON 설정 파일 형식

`config.json` 파일을 생성하여 프로젝트 정보를 정의한다:

```json
{
  "project_name": "프로젝트명",
  "product_name": "제품/서비스명",
  "description": "제품 설명이다",
  "target_audience": "타겟 고객",
  "key_features": [
    "기능 1",
    "기능 2",
    "기능 3"
  ],
  "brand_color": "blue"
}
```

### 필드 설명

- **project_name**: 프로젝트 디렉토리명 (영문 권장)
- **product_name**: 랜딩 페이지에 표시될 제품/서비스명
- **description**: 제품 설명 (반드시 '다'로 끝나야 함)
- **target_audience**: 타겟 고객층
- **key_features**: 주요 기능 목록 (3-6개 권장)
- **brand_color**: 브랜드 색상 (blue, green, purple 등)

## 출력 구조

생성된 랜딩 페이지의 디렉토리 구조이다:

```
output/
├── README.md                    # 프로젝트 설명
├── package.json                 # npm 패키지 설정
├── generation_report.json       # 생성 리포트
├── app/
│   ├── layout.tsx              # 루트 레이아웃
│   ├── page.tsx                # 메인 페이지
│   └── globals.css             # 글로벌 스타일
├── components/
│   ├── Header.tsx              # 헤더 (요소 2)
│   ├── Hero.tsx                # 히어로 (요소 3, 4, 5)
│   ├── MediaSection.tsx        # 미디어 (요소 6)
│   ├── Benefits.tsx            # 혜택 (요소 7)
│   ├── Testimonials.tsx        # 후기 (요소 8)
│   ├── FAQ.tsx                 # FAQ (요소 9)
│   ├── FinalCTA.tsx            # 최종 CTA (요소 10)
│   └── Footer.tsx              # 푸터 (요소 11)
└── public/
    └── images/                 # 이미지 디렉토리
```

## 생성 후 실행 방법

### 1. 출력 디렉토리로 이동

```bash
cd output
```

### 2. 의존성 설치

```bash
npm install
```

### 3. 개발 서버 실행

```bash
npm run dev
```

### 4. 브라우저에서 확인

```
http://localhost:3000
```

### 5. 프로덕션 빌드

```bash
npm run build
npm start
```

## 문제 해결

### API 키 오류

```
ValueError: ANTHROPIC_API_KEY 환경변수가 설정되지 않았다
```

**해결 방법**: `.env` 파일에 올바른 API 키를 설정한다.

### Skills 디렉토리 오류

```
FileNotFoundError: Skills 디렉토리를 찾을 수 없다
```

**해결 방법**: 
- Skills 디렉토리가 올바른 위치에 있는지 확인한다
- `--skills-dir` 옵션으로 경로를 지정한다

### 생성 중단

생성 중 프로그램이 중단되면:
1. 에러 로그를 확인한다
2. 네트워크 연결을 확인한다
3. API 키 유효성을 확인한다
4. `--max-retries` 옵션을 늘려 재시도한다

### 컴포넌트 검증 실패

특정 컴포넌트가 검증에 실패하면:
1. `generation_report.json`에서 에러 내용을 확인한다
2. 해당 컴포넌트를 수동으로 수정한다
3. 또는 프로그램을 재실행한다

## 생성 리포트

`generation_report.json` 파일은 다음 정보를 포함한다:

- 요청 정보
- 생성된 컴포넌트 목록
- 검증 결과
- 대화 기록
- 에러 통계

이 파일을 통해 생성 과정을 분석하고 문제를 진단할 수 있다.

## 팁

### 1. 단계별 확인

대화형 모드에서는 각 컴포넌트 생성 후 확인할 수 있다. 문제가 있으면 즉시 재생성을 요청한다.

### 2. 설정 파일 재사용

자주 사용하는 프로젝트 설정은 JSON 파일로 저장해두고 재사용한다.

### 3. 커스터마이징

생성된 코드는 완전히 커스터마이징 가능하다. 원하는 대로 수정한다.

### 4. ShadCN UI 컴포넌트

생성된 프로젝트는 ShadCN UI를 사용한다. 추가 컴포넌트가 필요하면:

```bash
npx shadcn-ui@latest add [component-name]
```

## 지원

문제가 발생하면:
1. 로그 파일을 확인한다
2. `generation_report.json`을 검토한다
3. GitHub Issues에 보고한다

## 라이선스

이 프로젝트의 라이선스 정보는 LICENSE 파일을 참조한다.
