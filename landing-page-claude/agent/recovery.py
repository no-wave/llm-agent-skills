"""
에러 복구 및 재시도 로직 모듈이다.
"""
import asyncio
import functools
from typing import TypeVar, Callable, Any, Optional
from datetime import datetime
import logging

from config import config

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_with_exponential_backoff(
    max_retries: Optional[int] = None,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_delay: float = 60.0
):
    """
    지수 백오프 재시도 데코레이터이다.
    
    Args:
        max_retries: 최대 재시도 횟수
        initial_delay: 초기 대기 시간 (초)
        exponential_base: 지수 증가 기준
        max_delay: 최대 대기 시간 (초)
    """
    if max_retries is None:
        max_retries = config.MAX_RETRIES
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"최대 재시도 횟수 {max_retries}회를 초과했다: {str(e)}")
                        break
                    
                    # 대기 시간 계산
                    delay = min(initial_delay * (exponential_base ** attempt), max_delay)
                    
                    logger.warning(
                        f"시도 {attempt + 1}/{max_retries + 1} 실패했다. "
                        f"{delay:.2f}초 후 재시도한다. 에러: {str(e)}"
                    )
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator


class RecoveryManager:
    """
    에러 발생 시 복구 전략을 관리하는 클래스이다.
    """
    
    def __init__(self):
        """
        RecoveryManager 인스턴스를 초기화한다.
        """
        self.error_history: list[dict] = []
        self.recovery_count: int = 0
    
    def record_error(
        self,
        error: Exception,
        context: str,
        component_type: Optional[str] = None
    ) -> None:
        """
        에러를 기록한다.
        
        Args:
            error: 발생한 예외
            context: 에러 발생 컨텍스트
            component_type: 컴포넌트 타입
        """
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "component_type": component_type
        }
        
        self.error_history.append(error_record)
        logger.error(f"에러가 기록되었다 - {context}: {str(error)}")
    
    def get_error_summary(self) -> str:
        """
        에러 요약 정보를 반환한다.
        
        Returns:
            str: 에러 요약
        """
        if not self.error_history:
            return "기록된 에러가 없다"
        
        summary_lines = [f"총 {len(self.error_history)}개의 에러가 발생했다:\n"]
        
        for i, error in enumerate(self.error_history[-5:], 1):  # 최근 5개만
            summary_lines.append(
                f"{i}. [{error['timestamp']}] {error['error_type']}: "
                f"{error['error_message'][:100]}"
            )
        
        return "\n".join(summary_lines)
    
    async def attempt_recovery(
        self,
        operation: Callable,
        *args,
        fallback_value: Any = None,
        **kwargs
    ) -> tuple[bool, Any]:
        """
        작업 실행을 시도하고 실패 시 복구를 시도한다.
        
        Args:
            operation: 실행할 작업
            *args: 작업 인자
            fallback_value: 복구 실패 시 반환할 기본값
            **kwargs: 작업 키워드 인자
            
        Returns:
            tuple[bool, Any]: (성공 여부, 결과값)
        """
        try:
            result = await operation(*args, **kwargs)
            return True, result
        except Exception as e:
            self.record_error(e, "작업 실행 중 에러 발생")
            logger.warning(f"작업이 실패했다. fallback 값을 반환한다: {str(e)}")
            return False, fallback_value
    
    async def safe_execute(
        self,
        operation: Callable,
        *args,
        retry_count: int = 3,
        **kwargs
    ) -> Optional[Any]:
        """
        안전하게 작업을 실행한다.
        
        Args:
            operation: 실행할 작업
            *args: 작업 인자
            retry_count: 재시도 횟수
            **kwargs: 작업 키워드 인자
            
        Returns:
            Optional[Any]: 실행 결과 또는 None
        """
        for attempt in range(retry_count):
            try:
                result = await operation(*args, **kwargs)
                if attempt > 0:
                    self.recovery_count += 1
                    logger.info(f"복구 성공했다 (시도 {attempt + 1}/{retry_count})")
                return result
            except Exception as e:
                self.record_error(e, f"실행 시도 {attempt + 1}/{retry_count}")
                
                if attempt == retry_count - 1:
                    logger.error(f"모든 재시도가 실패했다: {str(e)}")
                    return None
                
                await asyncio.sleep(config.RETRY_DELAY * (attempt + 1))
        
        return None
    
    def get_recovery_stats(self) -> dict:
        """
        복구 통계를 반환한다.
        
        Returns:
            dict: 복구 통계 정보
        """
        return {
            "total_errors": len(self.error_history),
            "recovery_count": self.recovery_count,
            "error_types": self._count_error_types(),
            "recent_errors": self.error_history[-5:]
        }
    
    def _count_error_types(self) -> dict[str, int]:
        """
        에러 타입별 발생 횟수를 계산한다.
        
        Returns:
            dict[str, int]: 에러 타입별 카운트
        """
        error_counts: dict[str, int] = {}
        for error in self.error_history:
            error_type = error["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts
    
    def clear_history(self) -> None:
        """
        에러 기록을 초기화한다.
        """
        self.error_history.clear()
        self.recovery_count = 0
        logger.info("에러 기록이 초기화되었다")
    
    def export_errors(self) -> list[dict]:
        """
        에러 기록을 내보낸다.
        
        Returns:
            list[dict]: 에러 기록 목록
        """
        return self.error_history.copy()


class CircuitBreaker:
    """
    Circuit Breaker 패턴을 구현하는 클래스이다.
    연속된 실패가 임계값을 초과하면 일시적으로 요청을 차단한다.
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        """
        CircuitBreaker 인스턴스를 초기화한다.
        
        Args:
            failure_threshold: 실패 임계값
            timeout: 차단 시간 (초)
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.is_open = False
    
    async def call(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Circuit Breaker를 통해 작업을 실행한다.
        
        Args:
            operation: 실행할 작업
            *args: 작업 인자
            **kwargs: 작업 키워드 인자
            
        Returns:
            Any: 실행 결과
            
        Raises:
            Exception: Circuit이 열려있거나 작업 실행 실패 시
        """
        if self.is_open:
            if self._should_attempt_reset():
                logger.info("Circuit Breaker 재시도를 시도한다")
                self.is_open = False
            else:
                raise Exception("Circuit Breaker가 열려있다. 잠시 후 다시 시도한다")
        
        try:
            result = await operation(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self) -> None:
        """
        작업 성공 시 호출된다.
        """
        self.failure_count = 0
        self.is_open = False
    
    def _on_failure(self) -> None:
        """
        작업 실패 시 호출된다.
        """
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(
                f"Circuit Breaker가 열렸다 (실패 횟수: {self.failure_count})"
            )
    
    def _should_attempt_reset(self) -> bool:
        """
        Circuit Breaker를 재시도해야 하는지 판단한다.
        
        Returns:
            bool: 재시도 여부
        """
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout
    
    def reset(self) -> None:
        """
        Circuit Breaker를 리셋한다.
        """
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False
        logger.info("Circuit Breaker가 리셋되었다")
