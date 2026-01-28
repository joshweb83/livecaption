"""
Opus-MT Translation Implementation
Helsinki-NLP Opus-MT 기반 번역 구현
"""

from typing import Dict, Any, List, Optional
from pathlib import Path


from services.base_translation import BaseTranslationService


class OpusMTTranslationService(BaseTranslationService):
    """Helsinki-NLP Opus-MT 기반 번역 서비스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 번역 설정 딕셔너리
                - model: 모델 이름 (Helsinki-NLP/opus-mt-ko-en)
                - source_lang: 원본 언어 (ko)
                - target_lang: 대상 언어 (en)
                - max_length: 최대 토큰 길이
        """
        super().__init__(config)
        self.model_name = config.get('model', 'Helsinki-NLP/opus-mt-ko-en')
        self.max_length = config.get('max_length', 512)
        self.tokenizer = None
        self.model = None
        
    def initialize(self) -> bool:
        """
        Opus-MT 모델 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        try:
            from transformers import MarianMTModel, MarianTokenizer
            
            # 토크나이저 로드
            self.tokenizer = MarianTokenizer.from_pretrained(
                self.model_name,
                cache_dir="models/translation"
            )
            
            # 모델 로드
            self.model = MarianMTModel.from_pretrained(
                self.model_name,
                cache_dir="models/translation"
            )
            
            # CPU로 이동 (경량 버전)
            self.model.eval()
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Opus-MT 초기화 실패: {e}")
            self.is_initialized = False
            return False
    
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
        if not self.is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        if not text or not text.strip():
            return {
                'translated_text': '',
                'source_lang': self.source_lang,
                'target_lang': self.target_lang,
                'confidence': 0.0
            }
        
        try:
            # 토큰화
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.max_length
            )
            
            # 번역
            outputs = self.model.generate(**inputs)
            
            # 디코딩
            translated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            return {
                'translated_text': translated_text.strip(),
                'source_lang': self.source_lang,
                'target_lang': self.target_lang,
                'confidence': 0.9  # Opus-MT는 신뢰도 제공 안 함 (고정값)
            }
            
        except Exception as e:
            print(f"❌ 번역 실패: {e}")
            return {
                'translated_text': '',
                'source_lang': self.source_lang,
                'target_lang': self.target_lang,
                'confidence': 0.0
            }
    
    def translate_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        여러 텍스트 일괄 번역
        
        Args:
            texts: 번역할 텍스트 리스트
            
        Returns:
            List[Dict]: 번역 결과 리스트
        """
        if not self.is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        if not texts:
            return []
        
        try:
            # 빈 텍스트 필터링
            valid_texts = [t for t in texts if t and t.strip()]
            if not valid_texts:
                return [self.translate('') for _ in texts]
            
            # 토큰화
            inputs = self.tokenizer(
                valid_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.max_length
            )
            
            # 번역
            outputs = self.model.generate(**inputs)
            
            # 디코딩
            translated_texts = [
                self.tokenizer.decode(output, skip_special_tokens=True)
                for output in outputs
            ]
            
            # 결과 포맷팅
            results = []
            valid_idx = 0
            for text in texts:
                if text and text.strip():
                    results.append({
                        'translated_text': translated_texts[valid_idx].strip(),
                        'source_lang': self.source_lang,
                        'target_lang': self.target_lang,
                        'confidence': 0.9
                    })
                    valid_idx += 1
                else:
                    results.append(self.translate(''))
            
            return results
            
        except Exception as e:
            print(f"❌ 일괄 번역 실패: {e}")
            return [self.translate('') for _ in texts]
    
    def cleanup(self):
        """리소스 정리"""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        self.is_initialized = False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        모델 정보 반환
        
        Returns:
            Dict: 모델 정보
        """
        return {
            'name': 'Helsinki-NLP Opus-MT',
            'model': self.model_name,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'max_length': self.max_length,
            'initialized': self.is_initialized
        }
    
    def get_supported_languages(self) -> List[str]:
        """
        지원하는 언어 목록 반환
        
        Returns:
            List[str]: 언어 코드 리스트
        """
        # Opus-MT ko-en 모델은 한국어 → 영어만 지원
        return ['ko', 'en']
