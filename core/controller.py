"""
Caption Controller
실시간 자막 생성 메인 컨트롤러
"""

import threading
import time
from typing import Optional, Callable, Dict, Any
import numpy as np

from core.config_manager import ConfigManager
from core.audio_capture import AudioCapture
from services.model_factory import ModelFactory
from services.base_stt import BaseSTTService
from services.base_translation import BaseTranslationService


class CaptionController:
    """실시간 자막 생성 컨트롤러"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        self.config_mgr = ConfigManager()
        self.config_mgr.load_config(config_path)
        
        # 컴포넌트
        self.audio_capture: Optional[AudioCapture] = None
        self.stt_service: Optional[BaseSTTService] = None
        self.translation_service: Optional[BaseTranslationService] = None
        
        # 상태
        self.is_running = False
        self.process_thread: Optional[threading.Thread] = None
        
        # 콜백
        self.caption_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
    def initialize(self) -> bool:
        """
        컨트롤러 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        try:
            print("=== 컨트롤러 초기화 시작 ===")
            
            # 오디오 캡처 초기화
            audio_config = self.config_mgr.get('stt.audio', {})
            self.audio_capture = AudioCapture(
                sample_rate=audio_config.get('sample_rate', 16000),
                chunk_duration=audio_config.get('chunk_duration', 3.0),
                buffer_size=audio_config.get('buffer_size', 1024)
            )
            
            if not self.audio_capture.initialize():
                print("❌ 오디오 캡처 초기화 실패")
                return False
            
            print("✅ 오디오 캡처 초기화 완료")
            
            # STT 서비스 초기화
            profile = self.config_mgr.get_current_profile()
            stt_config = self.config_mgr.get_stt_config(profile)
            
            # 구현체 import (팩토리 등록)
            import implementations
            
            self.stt_service = ModelFactory.create_stt_service(profile, stt_config)
            
            print(f"⏳ STT 모델 로드 중... (프로필: {profile})")
            if not self.stt_service.initialize():
                print("❌ STT 서비스 초기화 실패")
                return False
            
            print("✅ STT 서비스 초기화 완료")
            
            # 번역 서비스 초기화
            trans_config = self.config_mgr.get_translation_config()
            self.translation_service = ModelFactory.create_translation_service(trans_config)
            
            print("⏳ 번역 모델 로드 중...")
            if not self.translation_service.initialize():
                print("❌ 번역 서비스 초기화 실패")
                return False
            
            print("✅ 번역 서비스 초기화 완료")
            print("=== 컨트롤러 초기화 완료 ===\n")
            
            return True
            
        except Exception as e:
            print(f"❌ 컨트롤러 초기화 실패: {e}")
            return False
    
    def start(
        self,
        caption_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        device_index: Optional[int] = None
    ) -> bool:
        """
        자막 생성 시작
        
        Args:
            caption_callback: 자막 콜백 함수
            device_index: 오디오 디바이스 인덱스
            
        Returns:
            bool: 시작 성공 여부
        """
        if self.is_running:
            print("⚠️  이미 실행 중입니다")
            return False
        
        if not self.audio_capture or not self.stt_service or not self.translation_service:
            print("❌ 초기화되지 않았습니다. initialize()를 먼저 호출하세요")
            return False
        
        self.caption_callback = caption_callback
        self.is_running = True
        
        # 오디오 캡처 시작
        if not self.audio_capture.start_recording(device_index):
            self.is_running = False
            return False
        
        # 처리 스레드 시작
        self.process_thread = threading.Thread(
            target=self._process_loop,
            daemon=True
        )
        self.process_thread.start()
        
        print("✅ 자막 생성 시작")
        return True
    
    def _process_loop(self):
        """처리 루프 (별도 스레드)"""
        print("🎤 오디오 스트림 처리 시작...")
        
        for audio_chunk in self.audio_capture.get_audio_stream():
            if not self.is_running:
                break
            
            try:
                # STT: 오디오 → 텍스트
                for stt_result in self.stt_service.transcribe_stream(audio_chunk):
                    korean_text = stt_result['text']
                    
                    if not korean_text or not korean_text.strip():
                        continue
                    
                    print(f"🇰🇷 한국어: {korean_text}")
                    
                    # 번역: 한국어 → 영어
                    trans_result = self.translation_service.translate(korean_text)
                    english_text = trans_result['translated_text']
                    
                    print(f"🇺🇸 영어: {english_text}")
                    
                    # 자막 데이터 생성
                    caption_data = {
                        'korean': korean_text,
                        'english': english_text,
                        'timestamp': time.time(),
                        'stt_confidence': stt_result['confidence'],
                        'trans_confidence': trans_result['confidence']
                    }
                    
                    # 콜백 호출
                    if self.caption_callback:
                        self.caption_callback(caption_data)
                    
            except Exception as e:
                print(f"❌ 처리 에러: {e}")
                continue
    
    def stop(self):
        """자막 생성 중지"""
        if not self.is_running:
            return
        
        print("⏳ 자막 생성 중지 중...")
        self.is_running = False
        
        # 오디오 캡처 중지
        if self.audio_capture:
            self.audio_capture.stop_recording()
        
        # 처리 스레드 종료 대기
        if self.process_thread:
            self.process_thread.join(timeout=3.0)
        
        print("✅ 자막 생성 중지 완료")
    
    def cleanup(self):
        """리소스 정리"""
        self.stop()
        
        if self.audio_capture:
            self.audio_capture.cleanup()
        
        if self.stt_service:
            self.stt_service.cleanup()
        
        if self.translation_service:
            self.translation_service.cleanup()
        
        print("✅ 리소스 정리 완료")
    
    def list_audio_devices(self) -> list:
        """
        사용 가능한 오디오 디바이스 목록
        
        Returns:
            list: 디바이스 정보 리스트
        """
        if not self.audio_capture:
            self.audio_capture = AudioCapture()
            self.audio_capture.initialize()
        
        return self.audio_capture.list_devices()
    
    def get_audio_level(self) -> float:
        """
        현재 오디오 레벨
        
        Returns:
            float: 오디오 레벨 (0-1)
        """
        if not self.audio_capture:
            return 0.0
        
        return self.audio_capture.get_audio_level()
    
    def set_profile(self, profile: str) -> bool:
        """
        성능 프로필 변경 (재초기화 필요)
        
        Args:
            profile: 프로필 이름 (light, standard)
            
        Returns:
            bool: 변경 성공 여부
        """
        if self.is_running:
            print("⚠️  실행 중에는 프로필을 변경할 수 없습니다")
            return False
        
        try:
            self.config_mgr.set_profile(profile)
            print(f"✅ 프로필 변경: {profile}")
            return True
        except Exception as e:
            print(f"❌ 프로필 변경 실패: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        컨트롤러 상태 정보
        
        Returns:
            Dict: 상태 정보
        """
        return {
            'is_running': self.is_running,
            'profile': self.config_mgr.get_current_profile(),
            'stt_initialized': self.stt_service is not None and self.stt_service.is_initialized,
            'translation_initialized': self.translation_service is not None and self.translation_service.is_initialized,
            'audio_level': self.get_audio_level()
        }
