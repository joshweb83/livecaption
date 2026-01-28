"""
Speech-to-Text (STT) Service Interface
음성 인식 서비스 추상 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Generator, Dict, Any, Optional
import numpy as np


class BaseSTTService(ABC):
    """STT 서비스 추상 기본 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: STT 설정 딕셔너리
        """
        self.config = config
        self.is_initialized = False
        
    @abstractmethod
    def initialize(self) -> bool:
        """
        STT 모델 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        pass
    
    @abstractmethod
    def transcribe_stream(
        self, 
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Generator[Dict[str, Any], None, None]:
        """
        실시간 오디오 스트림을 텍스트로 변환
        
        Args:
            audio_data: 오디오 데이터 (numpy array)
            sample_rate: 샘플링 레이트 (기본 16000Hz)
            
        Yields:
            Dict: {
                'text': str,           # 인식된 텍스트
                'confidence': float,   # 신뢰도 (0-1)
                'is_final': bool,      # 최종 결과 여부
                'timestamp': float     # 타임스탬프
            }
        """
        pass
    
    @abstractmethod
    def transcribe_file(self, audio_path: str) -> str:
        """
        오디오 파일을 텍스트로 변환
        
        Args:
            audio_path: 오디오 파일 경로
            
        Returns:
            str: 인식된 텍스트
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """리소스 정리"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        모델 정보 반환
        
        Returns:
            Dict: 모델 정보 (이름, 크기, 언어 등)
        """
        return {
            'name': self.__class__.__name__,
            'config': self.config,
            'initialized': self.is_initialized
        }
