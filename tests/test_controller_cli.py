"""
Controller CLI Test
컨트롤러 통합 테스트 (CLI 버전)
"""

import sys
from pathlib import Path
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.controller import CaptionController


def caption_callback(caption_data):
    """자막 콜백 함수"""
    print("\n" + "=" * 60)
    print(f"⏰ 시간: {time.strftime('%H:%M:%S')}")
    print(f"🇰🇷 한국어: {caption_data['korean']}")
    print(f"🇺🇸 영어: {caption_data['english']}")
    print(f"📊 신뢰도: STT={caption_data['stt_confidence']:.2f}, 번역={caption_data['trans_confidence']:.2f}")
    print("=" * 60)


def main():
    """메인 함수"""
    print("=" * 60)
    print("Live Caption - Controller CLI Test")
    print("=" * 60)
    print()
    
    # 컨트롤러 생성
    controller = CaptionController()
    
    # 오디오 디바이스 목록
    print("=== 사용 가능한 오디오 디바이스 ===")
    devices = controller.list_audio_devices()
    for device in devices:
        print(f"  [{device['index']}] {device['name']}")
    print()
    
    # 초기화
    print("⏳ 컨트롤러 초기화 중...")
    if not controller.initialize():
        print("❌ 초기화 실패")
        return
    
    print()
    
    # 상태 확인
    status = controller.get_status()
    print("=== 컨트롤러 상태 ===")
    print(f"  프로필: {status['profile']}")
    print(f"  STT 초기화: {status['stt_initialized']}")
    print(f"  번역 초기화: {status['translation_initialized']}")
    print()
    
    # 자막 생성 시작
    print("🎤 자막 생성을 시작합니다...")
    print("   (Ctrl+C로 중지)")
    print()
    
    try:
        controller.start(caption_callback=caption_callback)
        
        # 실행 유지
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏳ 중지 중...")
    
    finally:
        # 정리
        controller.cleanup()
        print("\n✅ 테스트 완료")


if __name__ == '__main__':
    main()
