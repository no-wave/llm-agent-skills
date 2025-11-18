"""
데이터 모델 패키지이다.
"""
from .validation import (
    ComponentType,
    ComponentMetadata,
    LandingPageComponent,
    LandingPageValidation,
    ValidationResult,
    AgentRequest,
    AgentResponse
)
from .memory import ConversationMemory, Message, MessageRole

__all__ = [
    "ComponentType",
    "ComponentMetadata",
    "LandingPageComponent",
    "LandingPageValidation",
    "ValidationResult",
    "AgentRequest",
    "AgentResponse",
    "ConversationMemory",
    "Message",
    "MessageRole"
]
