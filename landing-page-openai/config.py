"""
설정 및 환경변수 관리 모듈이다.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """
    애플리케이션 전역 설정을 관리하는 클래스이다.
    """
    
    # API 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4-turbo")
    
    # 경로 설정
    BASE_DIR: Path = Path(__file__).parent
    SKILLS_DIR: Path = BASE_DIR / "skills" / "landing-page-guide"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    # API 호출 설정
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "2.0"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "300"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # 메모리 설정
    MAX_MEMORY_SIZE: int = int(os.getenv("MAX_MEMORY_SIZE", "50"))
    
    # 한글 문장 종결
    SENTENCE_ENDING: str = "다"
    
    @classmethod
    def validate(cls) -> None:
        """
        필수 설정값들이 올바르게 설정되었는지 검증한다.
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았다")
        
        if not cls.SKILLS_DIR.exists():
            raise FileNotFoundError(f"Skills 디렉토리를 찾을 수 없다: {cls.SKILLS_DIR}")
    
    @classmethod
    def set_skills_dir(cls, path: str) -> None:
        """
        Skills 디렉토리 경로를 설정한다.
        
        Args:
            path: Skills 디렉토리 경로
        """
        cls.SKILLS_DIR = Path(path)
    
    @classmethod
    def set_output_dir(cls, path: str) -> None:
        """
        출력 디렉토리 경로를 설정한다.
        
        Args:
            path: 출력 디렉토리 경로
        """
        cls.OUTPUT_DIR = Path(path)
    
    @classmethod
    def set_max_retries(cls, retries: int) -> None:
        """
        최대 재시도 횟수를 설정한다.
        
        Args:
            retries: 재시도 횟수
        """
        cls.MAX_RETRIES = retries


# 설정 인스턴스
config = Config()
