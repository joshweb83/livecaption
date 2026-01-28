"""
Whisper STT Implementation
Faster Whisper 기반 음성 인식 구현
"""

import numpy as np
from typing import Dict, Any, Generator, Optional
from pathlib import Path
import time

from services.base_stt import BaseSTTService


class WhisperSTTService(BaseSTTService):
    """Faster Whisper 기반 STT 서비스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: STT 설정 딕셔너리
                - model_size: 모델 크기 (small, large-v3-turbo)
                - device: 디바이스 (cpu, cuda)
                - compute_type: 연산 타입 (int8, float16)
                - language: 언어 코드 (ko)
                - vad_filter: VAD 필터 사용 여부
                - beam_size: 빔 서치 크기
        """
        super().__init__(config)
        self.model = None
        self.model_size = config.get('model_size', 'small')
        self.device = config.get('device', 'cpu')
        self.compute_type = config.get('compute_type', 'int8')
        self.language = config.get('language', 'ko')
        self.vad_filter = config.get('vad_filter', True)
        self.beam_size = config.get('beam_size', 5)
        
    def initialize(self) -> bool:
        """
        Whisper 모델 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        try:
            from faster_whisper import WhisperModel
            
            # 모델 로드
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root="models/whisper"
            )
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Whisper 초기화 실패: {e}")
            self.is_initialized = False
            return False
    
    def transcribe_stream(
        self, 
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Generator[Dict[str, Any], None, None]:
        """
        실시간 오디오 스트림을 텍스트로 변환
        
        Args:
            audio_data: 오디오 데이터 (numpy array, float32)
            sample_rate: 샘플링 레이트 (기본 16000Hz)
            
        Yields:
            Dict: {
                'text': str,           # 인식된 텍스트
                'confidence': float,   # 신뢰도 (0-1)
                'is_final': bool,      # 최종 결과 여부
                'timestamp': float     # 타임스탬프
            }
        """
        if not self.is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        try:
            # 오디오 데이터 정규화 (float32, -1 to 1)
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Whisper 모델로 변환
            segments, info = self.model.transcribe(
                audio_data,
                language=self.language,
                beam_size=self.beam_size,
                vad_filter=self.vad_filter,
                word_timestamps=False
            )
            
            # 세그먼트별로 결과 반환
            for segment in segments:
                yield {
                    'text': segment.text.strip(),
                    'confidence': segment.avg_logprob,  # 로그 확률
                    'is_final': True,
                    'timestamp': segment.start
                }
                
        except Exception as e:
            print(f"❌ 변환 실패: {e}")
            yield {
                'text': '',
                'confidence': 0.0,
                'is_final': True,
                'timestamp': 0.0
            }
    
    def transcribe_file(self, audio_path: str) -> str:
        """
        오디오 파일을 텍스트로 변환
        
        Args:
            audio_path: 오디오 파일 경로
            
        Returns:
            str: 인식된 텍스트
        """
        if not self.is_initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        try:
            segments, info = self.model.transcribe(
                audio_path,
                language=self.language,
                beam_size=self.beam_size,
                vad_filter=self.vad_filter
            )
            
            # 모든 세그먼트 합치기
            full_text = " ".join([segment.text.strip() for segment in segments])
            return full_text
            
        except Exception as e:
            print(f"❌ 파일 변환 실패: {e}")
            return ""
    
    def cleanup(self):
        """리소스 정리"""
        if self.model is not None:
            del self.model
            self.model = None
        self.is_initialized = False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        모델 정보 반환
        
        Returns:
            Dict: 모델 정보
        """
        return {
            'name': 'Faster Whisper',
            'model_size': self.model_size,
            'device': self.device,
            'compute_type': self.compute_type,
            'language': self.language,
            'initialized': self.is_initialized
        }


# 경량 버전 (Light Profile)
class WhisperLightSTT(WhisperSTTService):
    """경량 Whisper STT (CPU, Small, int8)"""
    
    def __init__(self, config: Dict[str, Any]):
        # 경량 설정 강제
        config['model_size'] = 'small'
        config['device'] = 'cpu'
        config['compute_type'] = 'int8'
        super().__init__(config)


# 고성능 버전 (Standard Profile)
class WhisperStandardSTT(WhisperSTTService):
    """고성능 Whisper STT (GPU, Large-v3-turbo, float16)"""
    
    def __init__(self, config: Dict[str, Any]):
        # 고성능 설정 강제
        config['model_size'] = 'large-v3-turbo'
        config['device'] = 'cuda'
        config['compute_type'] = 'float16'
        super().__init__(config)
