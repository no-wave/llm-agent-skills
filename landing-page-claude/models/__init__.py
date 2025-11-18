"""
데이터 모델 패키지이다.
"""
from .validation import (
    ComponentType,
    ComponentMetadata,
    LandingPageComponent,
    LandingPageValidation,
    ValidationResult
)
from .memory import ConversationMemory, Message, MessageRole

__all__ = [
    "ComponentType",
    "ComponentMetadata",
    "LandingPageComponent",
    "LandingPageValidation",
    "ValidationResult",
    "ConversationMemory",
    "Message",
    "MessageRole"
]
