"""
Service Layer Unit Tests
서비스 레이어 단위 테스트
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.base_stt import BaseSTTService
from services.base_translation import BaseTranslationService
from services.model_factory import ModelFactory
from core.config_manager import ConfigManager
from core.theme_manager import ThemeManager


class MockSTTService(BaseSTTService):
    """Mock STT 서비스 (테스트용)"""
    
    def initialize(self) -> bool:
        self.is_initialized = True
        return True
    
    def transcribe_stream(self, audio_data, sample_rate=16000):
        yield {
            'text': 'Test transcription',
            'confidence': 0.95,
            'is_final': True,
            'timestamp': 0.0
        }
    
    def transcribe_file(self, audio_path: str) -> str:
        return "Test transcription from file"
    
    def cleanup(self):
        self.is_initialized = False


class MockTranslationService(BaseTranslationService):
    """Mock 번역 서비스 (테스트용)"""
    
    def initialize(self) -> bool:
        self.is_initialized = True
        return True
    
    def translate(self, text: str):
        return {
            'translated_text': f'Translated: {text}',
            'source_lang': 'ko',
            'target_lang': 'en',
            'confidence': 0.9
        }
    
    def translate_batch(self, texts):
        return [self.translate(text) for text in texts]
    
    def cleanup(self):
        self.is_initialized = False


class TestBaseSTTService:
    """BaseSTTService 테스트"""
    
    def test_initialization(self):
        """초기화 테스트"""
        config = {'model_size': 'small'}
        service = MockSTTService(config)
        assert service.initialize() is True
        assert service.is_initialized is True
    
    def test_transcribe_stream(self):
        """스트림 변환 테스트"""
        config = {'model_size': 'small'}
        service = MockSTTService(config)
        service.initialize()
        
        import numpy as np
        audio_data = np.zeros(16000)  # 1초 오디오
        
        results = list(service.transcribe_stream(audio_data))
        assert len(results) > 0
        assert 'text' in results[0]
        assert 'confidence' in results[0]
    
    def test_get_model_info(self):
        """모델 정보 가져오기 테스트"""
        config = {'model_size': 'small'}
        service = MockSTTService(config)
        
        info = service.get_model_info()
        assert 'name' in info
        assert 'config' in info
        assert info['config']['model_size'] == 'small'


class TestBaseTranslationService:
    """BaseTranslationService 테스트"""
    
    def test_initialization(self):
        """초기화 테스트"""
        config = {'source_lang': 'ko', 'target_lang': 'en'}
        service = MockTranslationService(config)
        assert service.initialize() is True
        assert service.is_initialized is True
    
    def test_translate(self):
        """번역 테스트"""
        config = {'source_lang': 'ko', 'target_lang': 'en'}
        service = MockTranslationService(config)
        service.initialize()
        
        result = service.translate('안녕하세요')
        assert 'translated_text' in result
        assert 'source_lang' in result
        assert result['source_lang'] == 'ko'
    
    def test_translate_batch(self):
        """일괄 번역 테스트"""
        config = {'source_lang': 'ko', 'target_lang': 'en'}
        service = MockTranslationService(config)
        service.initialize()
        
        texts = ['안녕하세요', '감사합니다']
        results = service.translate_batch(texts)
        assert len(results) == 2
    
    def test_set_languages(self):
        """언어 설정 테스트"""
        config = {'source_lang': 'ko', 'target_lang': 'en'}
        service = MockTranslationService(config)
        
        service.set_languages('en', 'ko')
        assert service.source_lang == 'en'
        assert service.target_lang == 'ko'


class TestModelFactory:
    """ModelFactory 테스트"""
    
    def test_register_stt(self):
        """STT 구현체 등록 테스트"""
        ModelFactory.register_stt('mock_stt', MockSTTService)
        assert 'mock_stt' in ModelFactory.list_stt_implementations()
    
    def test_register_translation(self):
        """번역 구현체 등록 테스트"""
        ModelFactory.register_translation('mock_translation', MockTranslationService)
        assert 'mock_translation' in ModelFactory.list_translation_implementations()


class TestConfigManager:
    """ConfigManager 테스트"""
    
    def test_singleton(self):
        """싱글톤 패턴 테스트"""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        assert manager1 is manager2
    
    def test_get_set(self):
        """설정 가져오기/설정하기 테스트"""
        manager = ConfigManager()
        manager.config = {'test': {'key': 'value'}}
        
        assert manager.get('test.key') == 'value'
        
        manager.set('test.key', 'new_value')
        assert manager.get('test.key') == 'new_value'
    
    def test_get_with_default(self):
        """기본값과 함께 가져오기 테스트"""
        manager = ConfigManager()
        manager.config = {}
        
        assert manager.get('nonexistent.key', 'default') == 'default'


class TestThemeManager:
    """ThemeManager 테스트"""
    
    def test_singleton(self):
        """싱글톤 패턴 테스트"""
        manager1 = ThemeManager()
        manager2 = ThemeManager()
        assert manager1 is manager2
    
    def test_create_default_themes(self):
        """기본 테마 생성 테스트"""
        manager = ThemeManager()
        manager.create_default_themes()
        
        assert 'panel' in manager.themes
        assert 'transparent' in manager.themes
        assert 'ticker' in manager.themes
    
    def test_get_theme(self):
        """테마 가져오기 테스트"""
        manager = ThemeManager()
        manager.create_default_themes()
        
        panel_theme = manager.get_theme('panel')
        assert panel_theme is not None
        assert 'theme' in panel_theme
        assert 'window' in panel_theme
    
    def test_set_current_theme(self):
        """현재 테마 설정 테스트"""
        manager = ThemeManager()
        manager.create_default_themes()
        
        assert manager.set_current_theme('panel') is True
        assert manager.current_theme == 'panel'
        
        assert manager.set_current_theme('nonexistent') is False
    
    def test_list_themes(self):
        """테마 목록 테스트"""
        manager = ThemeManager()
        manager.create_default_themes()
        
        themes = manager.list_themes()
        assert len(themes) >= 3
        assert 'panel' in themes


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
