"""
Translation Service Interface
번역 서비스 추상 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseTranslationService(ABC):
    """번역 서비스 추상 기본 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 번역 설정 딕셔너리
        """
        self.config = config
        self.source_lang = config.get('source_lang', 'ko')
        self.target_lang = config.get('target_lang', 'en')
        self.is_initialized = False
        
    @abstractmethod
    def initialize(self) -> bool:
        """
        번역 모델 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        pass
    
    @abstractmethod
    def translate(self, text: str) -> Dict[str, Any]:
        """
        텍스트 번역
        
        Args:
            text: 번역할 텍스트
            
        Returns:
            Dict: {
                'translated_text': str,  # 번역된 텍스트
                'source_lang': str,      # 원본 언어
                'target_lang': str,      # 대상 언어
                'confidence': float      # 신뢰도 (0-1)
            }
        """
        pass
    
    @abstractmethod
    def translate_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        여러 텍스트 일괄 번역
        
        Args:
            texts: 번역할 텍스트 리스트
            
        Returns:
            List[Dict]: 번역 결과 리스트
        """
        pass
    
    def set_languages(self, source_lang: str, target_lang: str):
        """
        번역 언어 설정
        
        Args:
            source_lang: 원본 언어 코드 (예: 'ko')
            target_lang: 대상 언어 코드 (예: 'en')
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
    
    @abstractmethod
    def cleanup(self):
        """리소스 정리"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        모델 정보 반환
        
        Returns:
            Dict: 모델 정보
        """
        return {
            'name': self.__class__.__name__,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'config': self.config,
            'initialized': self.is_initialized
        }
    
    def get_supported_languages(self) -> List[str]:
        """
        지원하는 언어 목록 반환
        
        Returns:
            List[str]: 언어 코드 리스트
        """
        # 기본 구현 (하위 클래스에서 오버라이드)
        return ['ko', 'en']
