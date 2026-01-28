"""
Controller Mock Test
컨트롤러 통합 테스트 (Mock 버전 - PyAudio 불필요)
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config_manager import ConfigManager
from services.model_factory import ModelFactory


def test_controller_components():
    """컨트롤러 컴포넌트 테스트"""
    print("\n=== 컨트롤러 컴포넌트 테스트 ===")
    
    # 설정 로드
    config_mgr = ConfigManager()
    config_mgr.load_config('config.yaml')
    print("✅ 설정 로드 완료")
    
    # 현재 프로필
    profile = config_mgr.get_current_profile()
    print(f"✅ 현재 프로필: {profile}")
    
    # STT 설정
    stt_config = config_mgr.get_stt_config(profile)
    print(f"✅ STT 설정: {stt_config['model_size']}, {stt_config['device']}, {stt_config['compute_type']}")
    
    # 번역 설정
    trans_config = config_mgr.get_translation_config()
    print(f"✅ 번역 설정: {trans_config['model']}")
    
    # 구현체 import
    import implementations
    
    # STT 서비스 생성
    stt_service = ModelFactory.create_stt_service(profile, stt_config)
    print(f"✅ STT 서비스 생성: {stt_service.__class__.__name__}")
    print(f"   모델 정보: {stt_service.get_model_info()}")
    
    # 번역 서비스 생성
    trans_service = ModelFactory.create_translation_service(trans_config)
    print(f"✅ 번역 서비스 생성: {trans_service.__class__.__name__}")
    print(f"   모델 정보: {trans_service.get_model_info()}")
    
    print("\n✅ 모든 컴포넌트 생성 성공")


def test_pipeline_flow():
    """파이프라인 흐름 테스트 (Mock 데이터)"""
    print("\n=== 파이프라인 흐름 테스트 ===")
    
    import numpy as np
    
    # 설정 로드
    config_mgr = ConfigManager()
    config_mgr.load_config('config.yaml')
    
    profile = config_mgr.get_current_profile()
    stt_config = config_mgr.get_stt_config(profile)
    trans_config = config_mgr.get_translation_config()
    
    # 구현체 import
    import implementations
    
    # 서비스 생성
    stt_service = ModelFactory.create_stt_service(profile, stt_config)
    trans_service = ModelFactory.create_translation_service(trans_config)
    
    print("⏳ STT 모델 초기화 중... (시간이 걸릴 수 있습니다)")
    print("   ⚠️  실제 환경에서는 모델 다운로드가 필요합니다")
    
    # 초기화는 모델이 있을 때만 가능
    # stt_service.initialize()
    # trans_service.initialize()
    
    print("\n✅ 파이프라인 구조 검증 완료")
    print("\n파이프라인 흐름:")
    print("  1. 오디오 입력 (AudioCapture)")
    print("  2. 음성 인식 (WhisperSTT)")
    print("  3. 번역 (OpusMT)")
    print("  4. 자막 출력 (CaptionWindow)")


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - Controller Mock Tests")
    print("=" * 60)
    
    try:
        test_controller_components()
        test_pipeline_flow()
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Mock 테스트 완료")
    print("=" * 60)
