"""
Audio Capture Module
마이크 입력 캡처 및 버퍼링
"""

import pyaudio
import numpy as np
from typing import Optional, Callable, Generator
import threading
import queue
import time


class AudioCapture:
    """오디오 캡처 클래스"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_duration: float = 3.0,
        buffer_size: int = 1024,
        channels: int = 1
    ):
        """
        Args:
            sample_rate: 샘플링 레이트 (Hz)
            chunk_duration: 청크 지속 시간 (초)
            buffer_size: 버퍼 크기
            channels: 채널 수 (1=모노, 2=스테레오)
        """
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.buffer_size = buffer_size
        self.channels = channels
        
        # 청크 크기 계산 (샘플 수)
        self.chunk_size = int(sample_rate * chunk_duration)
        
        # PyAudio 인스턴스
        self.audio = None
        self.stream = None
        
        # 버퍼 큐
        self.audio_queue = queue.Queue()
        
        # 상태
        self.is_recording = False
        self.record_thread = None
        
    def initialize(self) -> bool:
        """
        PyAudio 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        try:
            self.audio = pyaudio.PyAudio()
            return True
        except Exception as e:
            print(f"❌ PyAudio 초기화 실패: {e}")
            return False
    
    def list_devices(self) -> list:
        """
        사용 가능한 오디오 디바이스 목록
        
        Returns:
            list: 디바이스 정보 리스트
        """
        if self.audio is None:
            self.initialize()
        
        devices = []
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:  # 입력 디바이스만
                devices.append({
                    'index': i,
                    'name': info['name'],
                    'channels': info['maxInputChannels'],
                    'sample_rate': int(info['defaultSampleRate'])
                })
        return devices
    
    def start_recording(
        self,
        device_index: Optional[int] = None,
        callback: Optional[Callable[[np.ndarray], None]] = None
    ) -> bool:
        """
        녹음 시작
        
        Args:
            device_index: 디바이스 인덱스 (None=기본 디바이스)
            callback: 오디오 청크 콜백 함수
            
        Returns:
            bool: 시작 성공 여부
        """
        if self.is_recording:
            print("⚠️  이미 녹음 중입니다")
            return False
        
        try:
            # 스트림 열기
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.buffer_size
            )
            
            self.is_recording = True
            
            # 녹음 스레드 시작
            self.record_thread = threading.Thread(
                target=self._record_loop,
                args=(callback,),
                daemon=True
            )
            self.record_thread.start()
            
            print("✅ 녹음 시작")
            return True
            
        except Exception as e:
            print(f"❌ 녹음 시작 실패: {e}")
            return False
    
    def _record_loop(self, callback: Optional[Callable[[np.ndarray], None]]):
        """
        녹음 루프 (별도 스레드)
        
        Args:
            callback: 오디오 청크 콜백 함수
        """
        audio_buffer = []
        
        while self.is_recording:
            try:
                # 오디오 데이터 읽기
                data = self.stream.read(self.buffer_size, exception_on_overflow=False)
                
                # numpy 배열로 변환
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                
                # 버퍼에 추가
                audio_buffer.extend(audio_chunk)
                
                # 청크 크기에 도달하면 처리
                if len(audio_buffer) >= self.chunk_size:
                    # numpy 배열로 변환
                    audio_array = np.array(audio_buffer[:self.chunk_size], dtype=np.float32)
                    
                    # 정규화 (-1 to 1)
                    audio_array = audio_array / 32768.0
                    
                    # 큐에 추가
                    self.audio_queue.put(audio_array)
                    
                    # 콜백 호출
                    if callback:
                        callback(audio_array)
                    
                    # 버퍼 초기화 (오버랩 50%)
                    overlap = self.chunk_size // 2
                    audio_buffer = audio_buffer[self.chunk_size - overlap:]
                    
            except Exception as e:
                print(f"❌ 녹음 루프 에러: {e}")
                break
    
    def stop_recording(self):
        """녹음 중지"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        # 스레드 종료 대기
        if self.record_thread:
            self.record_thread.join(timeout=2.0)
        
        # 스트림 닫기
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        print("✅ 녹음 중지")
    
    def get_audio_stream(self) -> Generator[np.ndarray, None, None]:
        """
        오디오 스트림 생성기
        
        Yields:
            np.ndarray: 오디오 청크 (float32, -1 to 1)
        """
        while self.is_recording or not self.audio_queue.empty():
            try:
                # 타임아웃으로 큐에서 가져오기
                audio_chunk = self.audio_queue.get(timeout=0.5)
                yield audio_chunk
            except queue.Empty:
                continue
    
    def cleanup(self):
        """리소스 정리"""
        self.stop_recording()
        
        if self.audio:
            self.audio.terminate()
            self.audio = None
    
    def get_audio_level(self) -> float:
        """
        현재 오디오 레벨 (RMS)
        
        Returns:
            float: 오디오 레벨 (0-1)
        """
        if self.audio_queue.empty():
            return 0.0
        
        try:
            # 최근 청크 가져오기
            audio_chunk = self.audio_queue.queue[-1]
            
            # RMS 계산
            rms = np.sqrt(np.mean(audio_chunk ** 2))
            return float(rms)
        except:
            return 0.0
