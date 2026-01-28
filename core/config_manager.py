"""
Configuration Manager
설정 파일 로드 및 관리
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ConfigManager:
    """설정 관리자 클래스 (Singleton)"""
    
    _instance = None
    
    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_path: Optional[str] = None):
        if self._initialized:
            # 이미 초기화되었지만 config_path가 제공되면 로드
            if config_path and not self.config:
                self.load_config(config_path)
            return
        
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[Path] = None
        self._initialized = True
        
        # config_path가 제공되면 자동 로드
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: str = "config.yaml") -> Dict[str, Any]:
        """
        설정 파일 로드
        
        Args:
            config_path: 설정 파일 경로
            
        Returns:
            Dict: 설정 딕셔너리
        """
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 환경 변수로 오버라이드
        self._apply_env_overrides()
        
        return self.config
    
    def _apply_env_overrides(self):
        """환경 변수로 설정 오버라이드"""
        # 예: LIVE_CAPTION_PROFILE=standard
        profile = os.getenv('LIVE_CAPTION_PROFILE')
        if profile:
            self.config['performance']['profile'] = profile
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        설정 값 가져오기 (점 표기법 지원)
        
        Args:
            key: 설정 키 (예: 'performance.profile')
            default: 기본값
            
        Returns:
            설정 값
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        설정 값 변경 (점 표기법 지원)
        
        Args:
            key: 설정 키 (예: 'performance.profile')
            value: 설정 값
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self, config_path: Optional[str] = None):
        """
        설정 파일 저장
        
        Args:
            config_path: 저장할 파일 경로 (None이면 원본 경로)
        """
        path = Path(config_path) if config_path else self.config_path
        
        if path is None:
            raise ValueError("No config path specified")
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get_stt_config(self, profile: Optional[str] = None) -> Dict[str, Any]:
        """
        STT 설정 가져오기
        
        Args:
            profile: 성능 프로필 (None이면 현재 프로필)
            
        Returns:
            Dict: STT 설정
        """
        if profile is None:
            profile = self.get('performance.profile', 'light')
        
        stt_config = self.get(f'stt.whisper.{profile}', {})
        audio_config = self.get('stt.audio', {})
        
        return {
            **stt_config,
            'audio': audio_config
        }
    
    def get_translation_config(self) -> Dict[str, Any]:
        """
        번역 설정 가져오기
        
        Returns:
            Dict: 번역 설정
        """
        return self.get('translation', {})
    
    def get_gui_config(self) -> Dict[str, Any]:
        """
        GUI 설정 가져오기
        
        Returns:
            Dict: GUI 설정
        """
        return self.get('gui', {})
    
    def get_current_profile(self) -> str:
        """
        현재 성능 프로필 가져오기
        
        Returns:
            str: 프로필 이름 ('light' 또는 'standard')
        """
        return self.get('performance.profile', 'light')
    
    def set_profile(self, profile: str):
        """
        성능 프로필 변경
        
        Args:
            profile: 프로필 이름 ('light' 또는 'standard')
        """
        if profile not in ['light', 'standard']:
            raise ValueError(f"Invalid profile: {profile}")
        
        self.set('performance.profile', profile)
    
    def get_app_info(self) -> Dict[str, Any]:
        """
        애플리케이션 정보 가져오기
        
        Returns:
            Dict: 앱 정보
        """
        return self.get('app', {})
