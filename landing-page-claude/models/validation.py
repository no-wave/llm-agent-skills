"""
Pydantic을 사용한 데이터 검증 모델이다.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ComponentType(str, Enum):
    """
    랜딩 페이지 컴포넌트 타입을 정의한다.
    """
    LAYOUT = "layout"
    PAGE = "page"
    HEADER = "Header"
    HERO = "Hero"
    MEDIA_SECTION = "MediaSection"
    BENEFITS = "Benefits"
    TESTIMONIALS = "Testimonials"
    FAQ = "FAQ"
    FINAL_CTA = "FinalCTA"
    FOOTER = "Footer"
    GLOBALS_CSS = "globals.css"
    PACKAGE_JSON = "package.json"


class ComponentMetadata(BaseModel):
    """
    컴포넌트 메타데이터를 정의한다.
    """
    name: str = Field(..., description="컴포넌트 이름")
    type: ComponentType = Field(..., description="컴포넌트 타입")
    file_path: str = Field(..., description="파일 경로")
    description: str = Field(..., description="컴포넌트 설명")
    element_number: Optional[int] = Field(None, description="11가지 요소 번호")
    
    @validator("description")
    def validate_description_ending(cls, v: str) -> str:
        """
        설명이 '다'로 끝나는지 검증한다.
        """
        if not v.endswith("다"):
            return v + "다"
        return v


class LandingPageComponent(BaseModel):
    """
    생성된 랜딩 페이지 컴포넌트를 정의한다.
    """
    metadata: ComponentMetadata = Field(..., description="컴포넌트 메타데이터")
    content: str = Field(..., description="컴포넌트 코드 내용")
    dependencies: List[str] = Field(default_factory=list, description="의존성 목록")
    
    @validator("content")
    def validate_content_not_empty(cls, v: str) -> str:
        """
        컴포넌트 내용이 비어있지 않은지 검증한다.
        """
        if not v or not v.strip():
            raise ValueError("컴포넌트 내용이 비어있다")
        return v
    
    class Config:
        use_enum_values = True


class ValidationResult(BaseModel):
    """
    검증 결과를 정의한다.
    """
    is_valid: bool = Field(..., description="검증 통과 여부")
    missing_elements: List[int] = Field(default_factory=list, description="누락된 요소 번호")
    errors: List[str] = Field(default_factory=list, description="에러 메시지 목록")
    warnings: List[str] = Field(default_factory=list, description="경고 메시지 목록")
    
    @property
    def has_errors(self) -> bool:
        """
        에러가 존재하는지 확인한다.
        """
        return len(self.errors) > 0
    
    @property
    def has_warnings(self) -> bool:
        """
        경고가 존재하는지 확인한다.
        """
        return len(self.warnings) > 0


class LandingPageValidation(BaseModel):
    """
    랜딩 페이지 전체 검증을 수행한다.
    """
    components: List[LandingPageComponent] = Field(default_factory=list, description="컴포넌트 목록")
    
    def validate_all_elements(self) -> ValidationResult:
        """
        11가지 필수 요소가 모두 포함되었는지 검증한다.
        
        Returns:
            ValidationResult: 검증 결과
        """
        required_elements = set(range(1, 12))
        present_elements = set()
        errors = []
        warnings = []
        
        # 각 컴포넌트의 요소 번호 수집
        for component in self.components:
            if component.metadata.element_number:
                present_elements.add(component.metadata.element_number)
        
        # 누락된 요소 확인
        missing_elements = sorted(list(required_elements - present_elements))
        
        if missing_elements:
            errors.append(f"다음 요소들이 누락되었다: {missing_elements}")
        
        # 필수 컴포넌트 타입 확인
        component_types = {comp.metadata.type for comp in self.components}
        required_types = {
            ComponentType.LAYOUT,
            ComponentType.PAGE,
            ComponentType.HEADER,
            ComponentType.HERO,
            ComponentType.BENEFITS,
            ComponentType.TESTIMONIALS,
            ComponentType.FAQ,
            ComponentType.FINAL_CTA,
            ComponentType.FOOTER
        }
        
        missing_types = required_types - component_types
        if missing_types:
            warnings.append(f"다음 컴포넌트 타입이 누락되었다: {[t.value for t in missing_types]}")
        
        return ValidationResult(
            is_valid=len(missing_elements) == 0 and len(errors) == 0,
            missing_elements=missing_elements,
            errors=errors,
            warnings=warnings
        )
    
    def get_component_by_type(self, component_type: ComponentType) -> Optional[LandingPageComponent]:
        """
        특정 타입의 컴포넌트를 조회한다.
        
        Args:
            component_type: 조회할 컴포넌트 타입
            
        Returns:
            Optional[LandingPageComponent]: 해당 타입의 컴포넌트 또는 None
        """
        for component in self.components:
            if component.metadata.type == component_type:
                return component
        return None
    
    def add_component(self, component: LandingPageComponent) -> None:
        """
        컴포넌트를 추가한다.
        
        Args:
            component: 추가할 컴포넌트
        """
        self.components.append(component)


class AgentRequest(BaseModel):
    """
    Agent 요청 데이터를 정의한다.
    """
    project_name: str = Field(..., description="프로젝트 이름")
    product_name: str = Field(..., description="제품/서비스 이름")
    description: str = Field(..., description="제품/서비스 설명")
    target_audience: str = Field(default="일반 사용자", description="타겟 고객")
    key_features: List[str] = Field(default_factory=list, description="주요 기능 목록")
    brand_color: str = Field(default="blue", description="브랜드 색상")
    
    @validator("description")
    def validate_description_ending(cls, v: str) -> str:
        """
        설명이 '다'로 끝나는지 검증한다.
        """
        if not v.endswith("다"):
            return v + "다"
        return v


class AgentResponse(BaseModel):
    """
    Agent 응답 데이터를 정의한다.
    """
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="응답 메시지")
    component: Optional[LandingPageComponent] = Field(None, description="생성된 컴포넌트")
    validation_result: Optional[ValidationResult] = Field(None, description="검증 결과")
    
    @validator("message")
    def validate_message_ending(cls, v: str) -> str:
        """
        메시지가 '다'로 끝나는지 검증한다.
        """
        if not v.endswith("다"):
            return v + "다"
        return v
