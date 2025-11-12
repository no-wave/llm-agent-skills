"""
대화 기록 관리 모듈이다.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """
    메시지 역할을 정의한다.
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """
    대화 메시지를 정의한다.
    """
    role: MessageRole = Field(..., description="메시지 역할")
    content: str = Field(..., description="메시지 내용")
    timestamp: datetime = Field(default_factory=datetime.now, description="생성 시간")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="추가 메타데이터")
    
    def to_api_format(self) -> Dict[str, str]:
        """
        Claude API 포맷으로 변환한다.
        
        Returns:
            Dict[str, str]: API 포맷 메시지
        """
        # role이 이미 문자열인 경우와 Enum인 경우 모두 처리한다
        role_value = self.role if isinstance(self.role, str) else self.role.value
        return {
            "role": role_value,
            "content": self.content
        }
    
    class Config:
        use_enum_values = True


class ConversationMemory:
    """
    대화 기록을 메모리에 저장하고 관리하는 클래스이다.
    """
    
    def __init__(self, max_size: int = 50):
        """
        ConversationMemory 인스턴스를 초기화한다.
        
        Args:
            max_size: 최대 메모리 크기
        """
        self.messages: List[Message] = []
        self.max_size = max_size
        self.system_prompt: Optional[str] = None
    
    def add_message(self, role: MessageRole, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        메시지를 메모리에 추가한다.
        
        Args:
            role: 메시지 역할
            content: 메시지 내용
            metadata: 추가 메타데이터
        """
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        
        # 메모리 크기 제한 체크
        if len(self.messages) > self.max_size:
            # 시스템 메시지는 유지하고 오래된 대화만 제거
            system_role = MessageRole.SYSTEM if isinstance(MessageRole.SYSTEM, str) else MessageRole.SYSTEM.value
            non_system_messages = [m for m in self.messages if m.role != system_role and m.role != "system"]
            system_messages = [m for m in self.messages if m.role == system_role or m.role == "system"]
            
            if len(non_system_messages) > self.max_size:
                non_system_messages = non_system_messages[-(self.max_size - len(system_messages)):]
            
            self.messages = system_messages + non_system_messages
    
    def add_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        사용자 메시지를 추가한다.
        
        Args:
            content: 메시지 내용
            metadata: 추가 메타데이터
        """
        self.add_message(MessageRole.USER, content, metadata)
    
    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        어시스턴트 메시지를 추가한다.
        
        Args:
            content: 메시지 내용
            metadata: 추가 메타데이터
        """
        self.add_message(MessageRole.ASSISTANT, content, metadata)
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        시스템 프롬프트를 설정한다.
        
        Args:
            prompt: 시스템 프롬프트 내용
        """
        self.system_prompt = prompt
        # 기존 시스템 메시지 제거
        self.messages = [m for m in self.messages if m.role != "system" and m.role != MessageRole.SYSTEM]
        # 새로운 시스템 메시지 추가
        self.add_message(MessageRole.SYSTEM, prompt)
    
    def get_messages(self, include_system: bool = True) -> List[Message]:
        """
        저장된 메시지 목록을 반환한다.
        
        Args:
            include_system: 시스템 메시지 포함 여부
            
        Returns:
            List[Message]: 메시지 목록
        """
        if include_system:
            return self.messages.copy()
        return [m for m in self.messages if m.role != "system" and m.role != MessageRole.SYSTEM]
    
    def get_api_messages(self) -> List[Dict[str, str]]:
        """
        Claude API 포맷의 메시지 목록을 반환한다.
        
        Returns:
            List[Dict[str, str]]: API 포맷 메시지 목록
        """
        # 시스템 메시지는 별도로 처리되므로 제외
        messages = [m for m in self.messages if m.role != "system" and m.role != MessageRole.SYSTEM]
        return [m.to_api_format() for m in messages]
    
    def get_last_message(self) -> Optional[Message]:
        """
        마지막 메시지를 반환한다.
        
        Returns:
            Optional[Message]: 마지막 메시지 또는 None
        """
        if not self.messages:
            return None
        return self.messages[-1]
    
    def get_conversation_summary(self) -> str:
        """
        대화 요약을 생성한다.
        
        Returns:
            str: 대화 요약
        """
        if not self.messages:
            return "대화 기록이 없다"
        
        summary_lines = []
        for msg in self.messages[-10:]:  # 최근 10개 메시지만
            # role이 문자열일 수도 있고 Enum일 수도 있으므로 처리
            role_str = msg.role if isinstance(msg.role, str) else msg.role.value
            role_name = {
                "user": "사용자",
                "assistant": "어시스턴트",
                "system": "시스템"
            }.get(role_str, "알 수 없음")
            
            content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
            summary_lines.append(f"[{role_name}] {content_preview}")
        
        return "\n".join(summary_lines)
    
    def clear(self) -> None:
        """
        메모리를 초기화한다.
        """
        system_messages = [m for m in self.messages if m.role == "system" or m.role == MessageRole.SYSTEM]
        self.messages = system_messages
    
    def get_message_count(self) -> int:
        """
        저장된 메시지 개수를 반환한다.
        
        Returns:
            int: 메시지 개수
        """
        return len(self.messages)
    
    def get_context_window_size(self) -> int:
        """
        현재 컨텍스트 윈도우 크기를 대략적으로 계산한다.
        
        Returns:
            int: 대략적인 토큰 수
        """
        # 간단한 추정: 한글 1글자 ≈ 2토큰, 영문 4글자 ≈ 1토큰
        total_chars = sum(len(m.content) for m in self.messages)
        estimated_tokens = total_chars * 2  # 보수적 추정
        return estimated_tokens
    
    def export_to_dict(self) -> Dict[str, Any]:
        """
        메모리를 딕셔너리로 내보낸다.
        
        Returns:
            Dict[str, Any]: 메모리 데이터
        """
        return {
            "system_prompt": self.system_prompt,
            "messages": [
                {
                    "role": m.role if isinstance(m.role, str) else m.role.value,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat(),
                    "metadata": m.metadata
                }
                for m in self.messages
            ],
            "message_count": len(self.messages),
            "max_size": self.max_size
        }
    
    def __len__(self) -> int:
        """
        메시지 개수를 반환한다.
        
        Returns:
            int: 메시지 개수
        """
        return len(self.messages)
    
    def __repr__(self) -> str:
        """
        객체의 문자열 표현을 반환한다.
        
        Returns:
            str: 객체 표현
        """
        return f"ConversationMemory(messages={len(self.messages)}, max_size={self.max_size})"