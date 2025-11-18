"""
랜딩 페이지 생성 로직 모듈이다.
"""
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import json

from agent.openai_client import OpenAIClient
from models.validation import (
    ComponentType,
    ComponentMetadata,
    LandingPageComponent,
    LandingPageValidation,
    AgentRequest
)
from config import config

# 로깅 설정
logger = logging.getLogger(__name__)


class LandingPageGenerator:
    """
    랜딩 페이지를 생성하는 클래스이다.
    """
    
    # 컴포넌트 생성 순서 정의
    COMPONENT_ORDER = [
        {
            "type": ComponentType.LAYOUT,
            "name": "layout.tsx",
            "path": "app/layout.tsx",
            "description": "Next.js App Router의 루트 레이아웃을 정의한다",
            "element": 1
        },
        {
            "type": ComponentType.HEADER,
            "name": "Header.tsx",
            "path": "components/Header.tsx",
            "description": "회사 로고와 네비게이션을 포함하는 헤더 컴포넌트를 생성한다",
            "element": 2
        },
        {
            "type": ComponentType.HERO,
            "name": "Hero.tsx",
            "path": "components/Hero.tsx",
            "description": "SEO 최적화된 제목, 부제목, 주요 CTA, 소셜 프루프를 포함하는 히어로 섹션을 생성한다",
            "element": [3, 4, 5]
        },
        {
            "type": ComponentType.MEDIA_SECTION,
            "name": "MediaSection.tsx",
            "path": "components/MediaSection.tsx",
            "description": "제품/서비스를 시각적으로 보여주는 이미지 또는 비디오 섹션을 생성한다",
            "element": 6
        },
        {
            "type": ComponentType.BENEFITS,
            "name": "Benefits.tsx",
            "path": "components/Benefits.tsx",
            "description": "3-6개의 핵심 혜택과 기능을 카드 형태로 표시하는 섹션을 생성한다",
            "element": 7
        },
        {
            "type": ComponentType.TESTIMONIALS,
            "name": "Testimonials.tsx",
            "path": "components/Testimonials.tsx",
            "description": "4-6개의 고객 후기를 표시하는 섹션을 생성한다",
            "element": 8
        },
        {
            "type": ComponentType.FAQ,
            "name": "FAQ.tsx",
            "path": "components/FAQ.tsx",
            "description": "5-10개의 자주 묻는 질문을 아코디언 형태로 표시하는 섹션을 생성한다",
            "element": 9
        },
        {
            "type": ComponentType.FINAL_CTA,
            "name": "FinalCTA.tsx",
            "path": "components/FinalCTA.tsx",
            "description": "페이지 하단의 최종 행동 유도 섹션을 생성한다",
            "element": 10
        },
        {
            "type": ComponentType.FOOTER,
            "name": "Footer.tsx",
            "path": "components/Footer.tsx",
            "description": "연락처 정보와 법적 페이지 링크를 포함하는 푸터를 생성한다",
            "element": 11
        },
        {
            "type": ComponentType.PAGE,
            "name": "page.tsx",
            "path": "app/page.tsx",
            "description": "모든 컴포넌트를 조합하는 메인 페이지를 생성한다",
            "element": None
        },
        {
            "type": ComponentType.GLOBALS_CSS,
            "name": "globals.css",
            "path": "app/globals.css",
            "description": "Tailwind CSS 설정과 글로벌 스타일을 정의한다",
            "element": None
        },
        {
            "type": ComponentType.PACKAGE_JSON,
            "name": "package.json",
            "path": "package.json",
            "description": "프로젝트 의존성과 스크립트를 정의한다",
            "element": None
        }
    ]
    
    def __init__(self, client: OpenAIClient, output_dir: Path):
        """
        LandingPageGenerator 인스턴스를 초기화한다.
        
        Args:
            client: OpenAI 클라이언트
            output_dir: 출력 디렉토리
        """
        self.client = client
        self.output_dir = output_dir
        self.validation = LandingPageValidation()
        self.request: Optional[AgentRequest] = None
    
    def set_request(self, request: AgentRequest) -> None:
        """
        생성 요청 정보를 설정한다.
        
        Args:
            request: Agent 요청
        """
        self.request = request
    
    async def generate_all_components(
        self,
        interactive: bool = True
    ) -> LandingPageValidation:
        """
        모든 컴포넌트를 순차적으로 생성한다.
        
        Args:
            interactive: 대화형 모드 여부
            
        Returns:
            LandingPageValidation: 검증 결과를 포함한 랜딩 페이지
        """
        if not self.request:
            raise ValueError("생성 요청 정보가 설정되지 않았다")
        
        logger.info("랜딩 페이지 생성을 시작한다")
        
        # 컨텍스트 메시지 생성
        context_message = self._build_context_message()
        await self.client.chat(context_message)
        
        # 각 컴포넌트 생성
        for i, component_config in enumerate(self.COMPONENT_ORDER, 1):
            logger.info(
                f"[{i}/{len(self.COMPONENT_ORDER)}] "
                f"{component_config['name']} 생성을 시작한다"
            )
            
            component = await self._generate_single_component(component_config)
            
            if component:
                self.validation.add_component(component)
                await self._save_component(component)
                
                if interactive:
                    user_input = input(
                        f"\n✓ {component_config['name']} 생성 완료했다. "
                        f"다음 컴포넌트를 생성할까? (y/n): "
                    )
                    
                    if user_input.lower() != 'y':
                        logger.info("사용자가 생성을 중단했다")
                        break
            else:
                logger.error(f"{component_config['name']} 생성에 실패했다")
                if interactive:
                    retry = input("재시도할까? (y/n): ")
                    if retry.lower() == 'y':
                        component = await self._generate_single_component(component_config)
                        if component:
                            self.validation.add_component(component)
                            await self._save_component(component)
        
        # 최종 검증
        validation_result = self.validation.validate_all_elements()
        self._print_validation_result(validation_result)
        
        return self.validation
    
    def _build_context_message(self) -> str:
        """
        컨텍스트 메시지를 구성한다.
        
        Returns:
            str: 컨텍스트 메시지
        """
        if not self.request:
            raise ValueError("요청 정보가 없다")
        
        message_parts = [
            f"다음 정보로 랜딩 페이지를 생성한다:",
            f"\n프로젝트명: {self.request.project_name}",
            f"제품/서비스명: {self.request.product_name}",
            f"설명: {self.request.description}",
            f"타겟 고객: {self.request.target_audience}",
            f"브랜드 색상: {self.request.brand_color}"
        ]
        
        if self.request.key_features:
            message_parts.append("\n주요 기능:")
            for feature in self.request.key_features:
                message_parts.append(f"- {feature}")
        
        message_parts.append(
            "\n\n이제 순차적으로 각 컴포넌트를 생성한다. "
            "각 컴포넌트는 11가지 필수 요소를 포함해야 한다."
        )
        
        return "\n".join(message_parts)
    
    async def _generate_single_component(
        self,
        component_config: Dict[str, Any]
    ) -> Optional[LandingPageComponent]:
        """
        단일 컴포넌트를 생성한다.
        
        Args:
            component_config: 컴포넌트 설정
            
        Returns:
            Optional[LandingPageComponent]: 생성된 컴포넌트 또는 None
        """
        try:
            # 프롬프트 생성
            prompt = self._build_component_prompt(component_config)
            
            # OpenAI API 호출
            response = await self.client.generate_completion(prompt, temperature=0.7)
            
            # 코드 추출
            code = self.client._extract_code(response)
            
            # 검증
            is_valid, error_msg = await self.client.validate_component(
                code,
                component_config['type'].value
            )
            
            if not is_valid:
                logger.error(f"컴포넌트 검증 실패: {error_msg}")
                return None
            
            # 컴포넌트 메타데이터 생성
            element_number = None
            if isinstance(component_config['element'], list):
                element_number = component_config['element'][0]
            elif component_config['element'] is not None:
                element_number = component_config['element']
            
            metadata = ComponentMetadata(
                name=component_config['name'],
                type=component_config['type'],
                file_path=component_config['path'],
                description=component_config['description'],
                element_number=element_number
            )
            
            # 컴포넌트 객체 생성
            component = LandingPageComponent(
                metadata=metadata,
                content=code,
                dependencies=self._extract_dependencies(code)
            )
            
            logger.info(f"{component_config['name']} 생성에 성공했다")
            return component
            
        except Exception as e:
            logger.error(f"컴포넌트 생성 중 에러 발생: {str(e)}")
            self.client.recovery_manager.record_error(
                e,
                f"{component_config['name']} 생성 중",
                component_config['type'].value
            )
            return None
    
    def _build_component_prompt(self, component_config: Dict[str, Any]) -> str:
        """
        컴포넌트 생성 프롬프트를 구성한다.
        
        Args:
            component_config: 컴포넌트 설정
            
        Returns:
            str: 프롬프트
        """
        prompt_parts = [
            f"{component_config['name']} 파일을 생성한다.",
            f"\n{component_config['description']}",
        ]
        
        # 특정 컴포넌트별 추가 지침
        if component_config['type'] == ComponentType.HERO:
            prompt_parts.append(
                "\n\n다음을 반드시 포함한다:"
                "\n- SEO 최적화된 H1 제목"
                "\n- 명확한 부제목"
                "\n- 주요 CTA 버튼 (ShadCN Button 사용)"
                "\n- 소셜 프루프 (별점, 사용자 수 등)"
            )
        elif component_config['type'] == ComponentType.BENEFITS:
            prompt_parts.append(
                "\n\n3-6개의 혜택/기능을 ShadCN Card 컴포넌트로 표시한다."
            )
        elif component_config['type'] == ComponentType.FAQ:
            prompt_parts.append(
                "\n\n5-10개의 FAQ를 ShadCN Accordion 컴포넌트로 표시한다."
            )
        
        prompt_parts.append(
            "\n\n완전한 TypeScript/TSX 코드를 생성한다. "
            "코드 블록만 반환하고 추가 설명은 제외한다. "
            "모든 주석은 '다'로 끝나야 한다."
        )
        
        return "".join(prompt_parts)
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """
        코드에서 의존성을 추출한다.
        
        Args:
            code: 컴포넌트 코드
            
        Returns:
            List[str]: 의존성 목록
        """
        dependencies = []
        
        # import 구문에서 패키지 추출
        for line in code.split('\n'):
            if line.strip().startswith('import'):
                if 'from' in line:
                    parts = line.split('from')
                    if len(parts) > 1:
                        pkg = parts[1].strip().strip("'\"")
                        if not pkg.startswith('.') and not pkg.startswith('@/'):
                            dependencies.append(pkg)
        
        return list(set(dependencies))
    
    async def _save_component(self, component: LandingPageComponent) -> None:
        """
        컴포넌트를 파일로 저장한다.
        
        Args:
            component: 저장할 컴포넌트
        """
        file_path = self.output_dir / component.metadata.file_path
        
        # 디렉토리 생성
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(component.content)
        
        logger.info(f"파일을 저장했다: {file_path}")
    
    def _print_validation_result(self, result) -> None:
        """
        검증 결과를 출력한다.
        
        Args:
            result: 검증 결과
        """
        print("\n" + "="*60)
        print("랜딩 페이지 생성 완료")
        print("="*60)
        
        if result.is_valid:
            print("✓ 모든 11가지 필수 요소가 포함되었다")
        else:
            print("✗ 일부 요소가 누락되었다")
            if result.missing_elements:
                print(f"누락된 요소: {result.missing_elements}")
        
        if result.errors:
            print("\n에러:")
            for error in result.errors:
                print(f"  - {error}")
        
        if result.warnings:
            print("\n경고:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        print(f"\n출력 디렉토리: {self.output_dir}")
        print("="*60 + "\n")
    
    async def generate_readme(self) -> None:
        """
        프로젝트 README 파일을 생성한다.
        """
        if not self.request:
            return
        
        readme_content = f"""# {self.request.project_name}

{self.request.description}

## 프로젝트 정보

- **제품/서비스명**: {self.request.product_name}
- **타겟 고객**: {self.request.target_audience}
- **브랜드 색상**: {self.request.brand_color}

## 주요 기능

"""
        
        for feature in self.request.key_features:
            readme_content += f"- {feature}\n"
        
        readme_content += """
## 기술 스택

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- ShadCN UI

## 설치 방법

```bash
npm install
```

## 실행 방법

```bash
npm run dev
```

브라우저에서 http://localhost:3000 을 열어 확인한다.

## 빌드

```bash
npm run build
```

## 11가지 필수 요소

이 랜딩 페이지는 DESIGNNAS의 11가지 필수 요소를 모두 포함한다:

1. ✓ URL with Keywords
2. ✓ Company Logo
3. ✓ SEO-Optimized Title and Subtitle
4. ✓ Primary CTA
5. ✓ Social Proof
6. ✓ Images or Videos
7. ✓ Core Benefits/Features
8. ✓ Customer Testimonials
9. ✓ FAQ Section
10. ✓ Final CTA
11. ✓ Contact Information/Legal Pages
"""
        
        readme_path = self.output_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info(f"README를 생성했다: {readme_path}")
    
    def export_report(self) -> Dict[str, Any]:
        """
        생성 리포트를 내보낸다.
        
        Returns:
            Dict[str, Any]: 리포트 데이터
        """
        validation_result = self.validation.validate_all_elements()
        
        return {
            "request": self.request.model_dump() if self.request else None,
            "components": [
                {
                    "name": comp.metadata.name,
                    "type": comp.metadata.type,
                    "path": comp.metadata.file_path,
                    "element": comp.metadata.element_number
                }
                for comp in self.validation.components
            ],
            "validation": {
                "is_valid": validation_result.is_valid,
                "missing_elements": validation_result.missing_elements,
                "errors": validation_result.errors,
                "warnings": validation_result.warnings
            },
            "conversation": self.client.export_conversation()
        }
