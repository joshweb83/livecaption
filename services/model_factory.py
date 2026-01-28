"""
Model Factory
설정에 따라 적절한 STT/번역 서비스 구현체를 생성하는 팩토리
"""

from typing import Dict, Any, Optional
from services.base_stt import BaseSTTService
from services.base_translation import BaseTranslationService


class ModelFactory:
    """모델 팩토리 클래스"""
    
    # 등록된 STT 구현체
    _stt_implementations = {}
    
    # 등록된 번역 구현체
    _translation_implementations = {}
    
    @classmethod
    def register_stt(cls, name: str, implementation: type):
        """
        STT 구현체 등록
        
        Args:
            name: 구현체 이름
            implementation: BaseSTTService를 상속한 클래스
        """
        if not issubclass(implementation, BaseSTTService):
            raise TypeError(f"{implementation} must inherit from BaseSTTService")
        cls._stt_implementations[name] = implementation
    
    @classmethod
    def register_translation(cls, name: str, implementation: type):
        """
        번역 구현체 등록
        
        Args:
            name: 구현체 이름
            implementation: BaseTranslationService를 상속한 클래스
        """
        if not issubclass(implementation, BaseTranslationService):
            raise TypeError(f"{implementation} must inherit from BaseTranslationService")
        cls._translation_implementations[name] = implementation
    
    @classmethod
    def create_stt_service(
        cls, 
        profile: str,
        config: Dict[str, Any]
    ) -> Optional[BaseSTTService]:
        """
        STT 서비스 생성
        
        Args:
            profile: 성능 프로필 ('light', 'standard')
            config: STT 설정
            
        Returns:
            BaseSTTService: STT 서비스 인스턴스
        """
        # 프로필에 따라 구현체 선택
        if profile == 'light':
            implementation_name = 'whisper_light'
        elif profile == 'standard':
            implementation_name = 'whisper_standard'
        else:
            raise ValueError(f"Unknown profile: {profile}")
        
        # 구현체 가져오기
        implementation = cls._stt_implementations.get(implementation_name)
        if implementation is None:
            raise ValueError(f"STT implementation '{implementation_name}' not registered")
        
        # 인스턴스 생성
        return implementation(config)
    
    @classmethod
    def create_translation_service(
        cls,
        config: Dict[str, Any]
    ) -> Optional[BaseTranslationService]:
        """
        번역 서비스 생성
        
        Args:
            config: 번역 설정
            
        Returns:
            BaseTranslationService: 번역 서비스 인스턴스
        """
        # 모델 이름에서 구현체 선택
        model_name = config.get('model', 'Helsinki-NLP/opus-mt-ko-en')
        
        if 'opus-mt' in model_name.lower():
            implementation_name = 'opus_mt'
        else:
            implementation_name = 'opus_mt'  # 기본값
        
        # 구현체 가져오기
        implementation = cls._translation_implementations.get(implementation_name)
        if implementation is None:
            raise ValueError(f"Translation implementation '{implementation_name}' not registered")
        
        # 인스턴스 생성
        return implementation(config)
    
    @classmethod
    def list_stt_implementations(cls) -> list:
        """등록된 STT 구현체 목록"""
        return list(cls._stt_implementations.keys())
    
    @classmethod
    def list_translation_implementations(cls) -> list:
        """등록된 번역 구현체 목록"""
        return list(cls._translation_implementations.keys())
