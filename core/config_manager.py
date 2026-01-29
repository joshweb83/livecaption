"""
Configuration Manager
설정 파일 로드 및 관리

PyInstaller 환경에서의 파일 경로 처리:
- PyInstaller는 --onefile 모드에서 실행 시 임시 디렉토리(_MEIPASS)에 번들된 파일을 압축 해제합니다.
- sys._MEIPASS를 사용하여 번들된 데이터 파일(config.yaml, themes/)에 접근해야 합니다.
- sys.executable.parent는 EXE 파일이 있는 디렉토리이며, 번들된 파일이 아닌 외부 파일을 찾을 때 사용합니다.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os
import sys


def get_resource_path(relative_path: str) -> Path:
    """
    PyInstaller 환경에서 리소스 파일의 절대 경로를 반환합니다.
    
    PyInstaller --onefile 모드에서:
    - 번들된 파일은 sys._MEIPASS 임시 디렉토리에 압축 해제됩니다.
    - 이 함수는 해당 디렉토리에서 파일을 찾습니다.
    
    일반 Python 실행 시:
    - 스크립트가 있는 디렉토리를 기준으로 파일을 찾습니다.
    
    Args:
        relative_path: 상대 경로 (예: 'config.yaml', 'themes/panel.yaml')
        
    Returns:
        Path: 리소스 파일의 절대 경로
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller로 패키징된 경우: _MEIPASS 임시 디렉토리 사용
        base_path = Path(sys._MEIPASS)
    else:
        # 일반 Python 스크립트: 이 파일이 있는 디렉토리의 부모 (프로젝트 루트)
        base_path = Path(__file__).parent.parent
    
    return base_path / relative_path


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
        
        PyInstaller 환경에서는 _MEIPASS 디렉토리에서 번들된 config.yaml을 찾습니다.
        
        Args:
            config_path: 설정 파일 경로 (상대 경로 권장)
            
        Returns:
            Dict: 설정 딕셔너리
            
        Raises:
            FileNotFoundError: 설정 파일을 찾을 수 없는 경우
        """
        # 절대 경로가 아닌 경우, 리소스 경로 함수 사용
        if not os.path.isabs(config_path):
            self.config_path = get_resource_path(config_path)
        else:
            self.config_path = Path(config_path)
        
        # 파일 존재 확인
        if not self.config_path.exists():
            # 디버깅을 위한 상세 오류 메시지
            error_msg = f"Config file not found: {self.config_path}\n"
            error_msg += f"  - sys.frozen: {getattr(sys, 'frozen', False)}\n"
            error_msg += f"  - sys._MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}\n"
            error_msg += f"  - sys.executable: {sys.executable}\n"
            error_msg += f"  - __file__: {__file__}\n"
            raise FileNotFoundError(error_msg)
        
        # YAML 파일 로드
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
        
        주의: PyInstaller 환경에서는 _MEIPASS 디렉토리에 쓰기가 불가능합니다.
        사용자 설정을 저장하려면 별도의 사용자 디렉토리를 사용해야 합니다.
        
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
            profile = self.get('performance.profile', 'lightweight')
        
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
            str: 프로필 이름 ('lightweight' 또는 'standard')
        """
        return self.get('performance.profile', 'lightweight')
    
    def set_profile(self, profile: str):
        """
        성능 프로필 변경
        
        Args:
            profile: 프로필 이름 ('lightweight' 또는 'standard')
        """
        if profile not in ['lightweight', 'standard']:
            raise ValueError(f"Invalid profile: {profile}")
        
        self.set('performance.profile', profile)
    
    def get_app_info(self) -> Dict[str, Any]:
        """
        애플리케이션 정보 가져오기
        
        Returns:
            Dict: 앱 정보
        """
        return self.get('app', {})


# 테마 파일 로드를 위한 헬퍼 함수
def get_theme_path(theme_name: str) -> Path:
    """
    테마 파일의 절대 경로를 반환합니다.
    
    Args:
        theme_name: 테마 이름 (예: 'panel', 'transparent', 'ticker')
        
    Returns:
        Path: 테마 파일의 절대 경로
    """
    return get_resource_path(f'themes/{theme_name}.yaml')
