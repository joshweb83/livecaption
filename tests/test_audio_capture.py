"""
Audio Capture Test
오디오 캡처 단위 테스트
"""

import sys
from pathlib import Path
import time
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.audio_capture import AudioCapture


def test_audio_capture_init():
    """오디오 캡처 초기화 테스트"""
    print("\n=== 오디오 캡처 초기화 테스트 ===")
    
    capture = AudioCapture(
        sample_rate=16000,
        chunk_duration=3.0,
        buffer_size=1024
    )
    
    assert capture.initialize() is True
    print("✅ 초기화 성공")
    
    capture.cleanup()
    print("✅ 정리 완료")


def test_list_devices():
    """디바이스 목록 테스트"""
    print("\n=== 오디오 디바이스 목록 테스트 ===")
    
    capture = AudioCapture()
    capture.initialize()
    
    devices = capture.list_devices()
    print(f"✅ 발견된 디바이스: {len(devices)}개")
    
    for device in devices:
        print(f"  [{device['index']}] {device['name']}")
        print(f"      채널: {device['channels']}, 샘플레이트: {device['sample_rate']}Hz")
    
    capture.cleanup()


def test_audio_capture_recording():
    """녹음 테스트 (5초)"""
    print("\n=== 녹음 테스트 (5초) ===")
    
    capture = AudioCapture(
        sample_rate=16000,
        chunk_duration=1.0,  # 1초 청크
        buffer_size=1024
    )
    
    capture.initialize()
    
    # 청크 카운터
    chunk_count = [0]
    
    def audio_callback(audio_chunk: np.ndarray):
        chunk_count[0] += 1
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        print(f"  청크 #{chunk_count[0]}: 크기={len(audio_chunk)}, RMS={rms:.4f}")
    
    # 녹음 시작
    capture.start_recording(callback=audio_callback)
    
    # 5초 대기
    time.sleep(5)
    
    # 녹음 중지
    capture.stop_recording()
    
    print(f"✅ 총 {chunk_count[0]}개 청크 수신")
    
    capture.cleanup()


def test_audio_stream_generator():
    """오디오 스트림 생성기 테스트"""
    print("\n=== 오디오 스트림 생성기 테스트 ===")
    
    capture = AudioCapture(
        sample_rate=16000,
        chunk_duration=1.0,
        buffer_size=1024
    )
    
    capture.initialize()
    capture.start_recording()
    
    print("⏳ 3초간 스트림 수신...")
    
    chunk_count = 0
    start_time = time.time()
    
    for audio_chunk in capture.get_audio_stream():
        chunk_count += 1
        print(f"  청크 #{chunk_count}: 크기={len(audio_chunk)}")
        
        # 3초 후 중지
        if time.time() - start_time > 3:
            break
    
    capture.stop_recording()
    
    print(f"✅ 총 {chunk_count}개 청크 수신")
    
    capture.cleanup()


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - Audio Capture Tests")
    print("=" * 60)
    
    try:
        test_audio_capture_init()
        test_list_devices()
        
        # 실제 녹음 테스트는 마이크가 있을 때만 실행
        print("\n⚠️  실제 녹음 테스트는 마이크가 필요합니다")
        print("   샌드박스 환경에서는 스킵합니다")
        
        # test_audio_capture_recording()
        # test_audio_stream_generator()
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료")
    print("=" * 60)
