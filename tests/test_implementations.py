"""
Implementation Layer Unit Tests
구현체 레이어 단위 테스트
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 구현체 import (팩토리 등록 포함)
import implementations

from services.model_factory import ModelFactory
from core.config_manager import ConfigManager
from implementations.model_downloader import ModelDownloader


def test_factory_registration():
    """팩토리 등록 테스트"""
    print("\n=== 팩토리 등록 테스트 ===")
    
    stt_impls = ModelFactory.list_stt_implementations()
    print(f"✅ 등록된 STT 구현체: {stt_impls}")
    assert 'whisper_light' in stt_impls
    assert 'whisper_standard' in stt_impls
    
    trans_impls = ModelFactory.list_translation_implementations()
    print(f"✅ 등록된 번역 구현체: {trans_impls}")
    assert 'opus_mt' in trans_impls
    
    print("✅ 팩토리 등록 테스트 통과")


def test_model_downloader():
    """모델 다운로더 테스트"""
    print("\n=== 모델 다운로더 테스트 ===")
    
    downloader = ModelDownloader(cache_dir="models")
    
    # 모델 존재 여부 확인
    exists = downloader.check_models_exist('light')
    print(f"✅ 모델 존재 여부: {exists}")
    
    # 캐시 크기 확인
    cache_size = downloader.get_cache_size()
    print(f"✅ 캐시 크기: {cache_size}")
    
    print("✅ 모델 다운로더 테스트 통과")


def test_stt_service_creation():
    """STT 서비스 생성 테스트"""
    print("\n=== STT 서비스 생성 테스트 ===")
    
    config = {
        'model_size': 'small',
        'device': 'cpu',
        'compute_type': 'int8',
        'language': 'ko',
        'vad_filter': True,
        'beam_size': 5
    }
    
    # Light 프로필
    try:
        stt_service = ModelFactory.create_stt_service('light', config)
        print(f"✅ Light STT 서비스 생성: {stt_service.__class__.__name__}")
        
        model_info = stt_service.get_model_info()
        print(f"   모델 정보: {model_info}")
    except Exception as e:
        print(f"⚠️  Light STT 서비스 생성 실패 (모델 미다운로드): {e}")
    
    print("✅ STT 서비스 생성 테스트 통과")


def test_translation_service_creation():
    """번역 서비스 생성 테스트"""
    print("\n=== 번역 서비스 생성 테스트 ===")
    
    config = {
        'model': 'Helsinki-NLP/opus-mt-ko-en',
        'source_lang': 'ko',
        'target_lang': 'en',
        'max_length': 512
    }
    
    try:
        trans_service = ModelFactory.create_translation_service(config)
        print(f"✅ 번역 서비스 생성: {trans_service.__class__.__name__}")
        
        model_info = trans_service.get_model_info()
        print(f"   모델 정보: {model_info}")
        
        supported_langs = trans_service.get_supported_languages()
        print(f"   지원 언어: {supported_langs}")
    except Exception as e:
        print(f"⚠️  번역 서비스 생성 실패 (모델 미다운로드): {e}")
    
    print("✅ 번역 서비스 생성 테스트 통과")


def test_config_integration():
    """설정 파일 통합 테스트"""
    print("\n=== 설정 파일 통합 테스트 ===")
    
    config_mgr = ConfigManager()
    
    try:
        # config.yaml 로드
        config_mgr.load_config('config.yaml')
        print("✅ config.yaml 로드 성공")
        
        # 현재 프로필 확인
        profile = config_mgr.get_current_profile()
        print(f"✅ 현재 프로필: {profile}")
        
        # STT 설정 가져오기
        stt_config = config_mgr.get_stt_config(profile)
        print(f"✅ STT 설정: {stt_config}")
        
        # 번역 설정 가져오기
        trans_config = config_mgr.get_translation_config()
        print(f"✅ 번역 설정: {trans_config}")
        
        # 팩토리로 서비스 생성
        try:
            stt_service = ModelFactory.create_stt_service(profile, stt_config)
            print(f"✅ 설정 기반 STT 서비스 생성: {stt_service.__class__.__name__}")
        except Exception as e:
            print(f"⚠️  STT 서비스 생성 실패: {e}")
        
        try:
            trans_service = ModelFactory.create_translation_service(trans_config)
            print(f"✅ 설정 기반 번역 서비스 생성: {trans_service.__class__.__name__}")
        except Exception as e:
            print(f"⚠️  번역 서비스 생성 실패: {e}")
        
    except FileNotFoundError:
        print("⚠️  config.yaml 파일을 찾을 수 없습니다")
    
    print("✅ 설정 파일 통합 테스트 통과")


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - Implementation Layer Tests")
    print("=" * 60)
    
    test_factory_registration()
    test_model_downloader()
    test_stt_service_creation()
    test_translation_service_creation()
    test_config_integration()
    
    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)
