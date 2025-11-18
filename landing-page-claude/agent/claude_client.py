"""
Claude API 클라이언트 모듈이다.
"""
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from anthropic import AsyncAnthropic
from anthropic.types import Message as AnthropicMessage

from config import config
from models.memory import ConversationMemory, MessageRole
from agent.recovery import retry_with_exponential_backoff, RecoveryManager

# 로깅 설정
logger = logging.getLogger(__name__)


class ClaudeClient:
    """
    Claude API와 통신하는 클라이언트 클래스이다.
    """
    
    def __init__(self):
        """
        ClaudeClient 인스턴스를 초기화한다.
        """
        self.client = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        self.memory = ConversationMemory(max_size=config.MAX_MEMORY_SIZE)
        self.recovery_manager = RecoveryManager()
        self.skill_content: Optional[str] = None
    
    async def load_skill(self, skill_dir: Path) -> None:
        """
        Skill 문서를 로드한다.
        
        Args:
            skill_dir: Skill 디렉토리 경로
        """
        try:
            skill_files = {
                "main": skill_dir / "SKILL.md",
                "elements": skill_dir / "references" / "11-essential-elements.md",
                "components": skill_dir / "references" / "component-examples.md"
            }
            
            skill_contents = []
            
            for name, file_path in skill_files.items():
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        skill_contents.append(f"## {name.upper()}\n\n{content}\n\n")
                    logger.info(f"{name} Skill 파일을 로드했다: {file_path}")
                else:
                    logger.warning(f"Skill 파일을 찾을 수 없다: {file_path}")
            
            if skill_contents:
                self.skill_content = "\n".join(skill_contents)
                logger.info("모든 Skill 문서를 성공적으로 로드했다")
            else:
                raise FileNotFoundError("Skill 파일을 찾을 수 없다")
                
        except Exception as e:
            self.recovery_manager.record_error(e, "Skill 로드 중 에러 발생")
            raise
    
    def _build_system_prompt(self) -> str:
        """
        시스템 프롬프트를 구성한다.
        
        Returns:
            str: 시스템 프롬프트
        """
        base_prompt = f"""당신은 Next.js 14+와 ShadCN UI를 사용하여 전문적인 랜딩 페이지를 생성하는 전문가이다.

다음 규칙을 반드시 따른다:

1. **11가지 필수 요소**: 모든 랜딩 페이지는 DESIGNNAS의 11가지 필수 요소를 포함해야 한다
2. **기술 스택**: Next.js 14+ App Router, TypeScript, Tailwind CSS, ShadCN UI를 사용한다
3. **문장 종결**: 모든 설명과 코멘트는 '{config.SENTENCE_ENDING}'로 끝난다
4. **코드 품질**: 프로덕션 레벨의 깔끔하고 최적화된 코드를 작성한다
5. **접근성**: WCAG 표준을 준수한다
6. **반응형**: 모바일 퍼스트 디자인을 적용한다

당신은 단계별로 컴포넌트를 생성하며, 각 단계가 완료되면 사용자의 확인을 기다린다."""
        
        if self.skill_content:
            return f"{base_prompt}\n\n# Landing Page Guide Skill\n\n{self.skill_content}"
        
        return base_prompt
    
    @retry_with_exponential_backoff(max_retries=3)
    async def generate_completion(
        self,
        user_message: str,
        temperature: float = 1.0,
        include_skill: bool = True
    ) -> str:
        """
        Claude API를 호출하여 응답을 생성한다.
        
        Args:
            user_message: 사용자 메시지
            temperature: 생성 온도
            include_skill: Skill 포함 여부
            
        Returns:
            str: Claude 응답
        """
        try:
            # 시스템 프롬프트 설정
            if include_skill and self.memory.system_prompt is None:
                system_prompt = self._build_system_prompt()
                self.memory.set_system_prompt(system_prompt)
            
            # 사용자 메시지 추가
            self.memory.add_user_message(user_message)
            
            # API 호출
            logger.info(f"Claude API를 호출한다 (메시지: {len(user_message)} 글자)")
            
            response = await self.client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                temperature=temperature,
                system=self.memory.system_prompt or self._build_system_prompt(),
                messages=self.memory.get_api_messages()
            )
            
            # 응답 추출
            assistant_message = response.content[0].text
            
            # 메모리에 저장
            self.memory.add_assistant_message(assistant_message)
            
            logger.info(f"Claude 응답을 받았다 (길이: {len(assistant_message)} 글자)")
            
            return assistant_message
            
        except Exception as e:
            self.recovery_manager.record_error(e, "Claude API 호출 중 에러 발생")
            raise
    
    async def generate_component(
        self,
        component_name: str,
        component_description: str,
        requirements: Optional[List[str]] = None
    ) -> str:
        """
        특정 컴포넌트를 생성한다.
        
        Args:
            component_name: 컴포넌트 이름
            component_description: 컴포넌트 설명
            requirements: 추가 요구사항
            
        Returns:
            str: 생성된 컴포넌트 코드
        """
        prompt_parts = [
            f"{component_name} 컴포넌트를 생성한다.",
            f"\n설명: {component_description}",
        ]
        
        if requirements:
            prompt_parts.append("\n\n요구사항:")
            for req in requirements:
                prompt_parts.append(f"- {req}")
        
        prompt_parts.append("\n\n완전한 TypeScript 코드를 생성한다. 코드만 반환하고 설명은 제외한다.")
        
        prompt = "".join(prompt_parts)
        
        response = await self.generate_completion(prompt, temperature=0.7)
        
        return self._extract_code(response)
    
    def _extract_code(self, response: str) -> str:
        """
        응답에서 코드 블록을 추출한다.
        
        Args:
            response: Claude 응답
            
        Returns:
            str: 추출된 코드
        """
        # 마크다운 코드 블록 추출
        if "```typescript" in response or "```tsx" in response or "```jsx" in response:
            # 첫 번째 코드 블록 찾기
            start_markers = ["```typescript", "```tsx", "```jsx"]
            start_idx = -1
            
            for marker in start_markers:
                idx = response.find(marker)
                if idx != -1 and (start_idx == -1 or idx < start_idx):
                    start_idx = idx
            
            if start_idx != -1:
                # 코드 블록 시작
                code_start = response.find("\n", start_idx) + 1
                code_end = response.find("```", code_start)
                
                if code_end != -1:
                    return response[code_start:code_end].strip()
        
        # 코드 블록이 없으면 전체 응답 반환
        return response.strip()
    
    async def validate_component(
        self,
        component_code: str,
        component_type: str
    ) -> tuple[bool, Optional[str]]:
        """
        생성된 컴포넌트를 검증한다.
        
        Args:
            component_code: 컴포넌트 코드
            component_type: 컴포넌트 타입
            
        Returns:
            tuple[bool, Optional[str]]: (유효성 여부, 에러 메시지)
        """
        # 기본 검증
        if not component_code or len(component_code.strip()) < 10:
            return False, "컴포넌트 코드가 너무 짧다"
        
        # TypeScript/React 기본 구문 확인
        required_patterns = {
            "import": "import 구문이 없다",
            "export": "export 구문이 없다",
        }
        
        for pattern, error_msg in required_patterns.items():
            if pattern not in component_code:
                return False, error_msg
        
        return True, None
    
    def get_memory_summary(self) -> str:
        """
        메모리 요약을 반환한다.
        
        Returns:
            str: 메모리 요약
        """
        return self.memory.get_conversation_summary()
    
    def get_error_summary(self) -> str:
        """
        에러 요약을 반환한다.
        
        Returns:
            str: 에러 요약
        """
        return self.recovery_manager.get_error_summary()
    
    def clear_memory(self) -> None:
        """
        대화 메모리를 초기화한다.
        """
        system_prompt = self.memory.system_prompt
        self.memory.clear()
        if system_prompt:
            self.memory.set_system_prompt(system_prompt)
        logger.info("대화 메모리를 초기화했다")
    
    async def chat(self, user_message: str) -> str:
        """
        일반 대화를 수행한다.
        
        Args:
            user_message: 사용자 메시지
            
        Returns:
            str: Assistant 응답
        """
        return await self.generate_completion(user_message, temperature=1.0)
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        대화 내역을 내보낸다.
        
        Returns:
            Dict[str, Any]: 대화 데이터
        """
        return {
            "memory": self.memory.export_to_dict(),
            "errors": self.recovery_manager.export_errors(),
            "recovery_stats": self.recovery_manager.get_recovery_stats()
        }
