"""
Live Caption Application
메인 애플리케이션 클래스
"""

import sys
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from core.controller import CaptionController
from core.config_manager import ConfigManager
from gui.caption_window import CaptionWindow
from gui.settings_window import SettingsWindow
from gui.system_tray import SystemTray


class LiveCaptionApp:
    """Live Caption 메인 애플리케이션"""
    
    def __init__(self, config_path: str = "config.yaml", theme_name: str = 'panel'):
        """
        Args:
            config_path: 설정 파일 경로
            theme_name: 초기 테마 이름
        """
        # Qt 애플리케이션
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("Live Caption")
        self.qt_app.setOrganizationName("Manus")
        self.qt_app.setQuitOnLastWindowClosed(False)  # 트레이 아이콘 지원
        
        # 설정 관리자
        self.config_mgr = ConfigManager(config_path)
        
        # 컨트롤러
        self.controller = CaptionController(config_path)
        
        # 자막 창
        self.caption_window: Optional[CaptionWindow] = None
        self.theme_name = theme_name
        
        # 설정 창
        self.settings_window: Optional[SettingsWindow] = None
        
        # 시스템 트레이
        self.system_tray: Optional[SystemTray] = None
        
        # 상태
        self.is_initialized = False
        self.is_running = False
        
    def initialize(self) -> bool:
        """
        애플리케이션 초기화
        
        Returns:
            bool: 초기화 성공 여부
        """
        print("=== Live Caption 초기화 시작 ===")
        
        # 컨트롤러 초기화
        if not self.controller.initialize():
            print("❌ 컨트롤러 초기화 실패")
            return False
        
        # 자막 창 생성
        try:
            self.caption_window = CaptionWindow(self.theme_name)
            self.caption_window.show()
            print(f"✅ 자막 창 생성 완료 (테마: {self.theme_name})")
        except Exception as e:
            print(f"❌ 자막 창 생성 실패: {e}")
            return False
        
        # 시스템 트레이 생성
        try:
            self.system_tray = SystemTray()
            self._connect_tray_signals()
            self.system_tray.show()
            print("✅ 시스템 트레이 생성 완료")
        except Exception as e:
            print(f"⚠️  시스템 트레이 생성 실패: {e}")
            # 트레이 없이도 계속 진행
        
        self.is_initialized = True
        print("=== Live Caption 초기화 완료 ===\n")
        return True
    
    def _connect_tray_signals(self):
        """트레이 시그널 연결"""
        if not self.system_tray:
            return
        
        self.system_tray.start_requested.connect(self._on_start_requested)
        self.system_tray.stop_requested.connect(self._on_stop_requested)
        self.system_tray.settings_requested.connect(self._on_settings_requested)
        self.system_tray.show_window_requested.connect(self._on_show_window_requested)
        self.system_tray.quit_requested.connect(self._on_quit_requested)
    
    def _on_start_requested(self):
        """시작 요청"""
        if not self.is_running:
            self.start()
    
    def _on_stop_requested(self):
        """중지 요청"""
        if self.is_running:
            self.stop()
    
    def _on_settings_requested(self):
        """설정 요청"""
        self.show_settings()
    
    def _on_show_window_requested(self):
        """창 표시 요청"""
        if self.caption_window:
            self.caption_window.show()
            self.caption_window.activateWindow()
    
    def _on_quit_requested(self):
        """종료 요청"""
        self.cleanup()
        self.qt_app.quit()
    
    def start(self, device_index: Optional[int] = None) -> bool:
        """
        자막 생성 시작
        
        Args:
            device_index: 오디오 디바이스 인덱스
            
        Returns:
            bool: 시작 성공 여부
        """
        if not self.is_initialized:
            print("❌ 초기화되지 않았습니다. initialize()를 먼저 호출하세요")
            return False
        
        if self.is_running:
            print("⚠️  이미 실행 중입니다")
            return False
        
        # 컨트롤러 시작 (자막 콜백 연결)
        if not self.controller.start(
            caption_callback=self._on_caption_received,
            device_index=device_index
        ):
            print("❌ 컨트롤러 시작 실패")
            return False
        
        self.is_running = True
        
        # 트레이 상태 업데이트
        if self.system_tray:
            self.system_tray.set_running_state(True)
            self.system_tray.show_message("Live Caption", "자막 생성이 시작되었습니다")
        
        print("✅ 자막 생성 시작")
        return True
    
    def stop(self):
        """자막 생성 중지"""
        if not self.is_running:
            return
        
        print("⏳ 자막 생성 중지 중...")
        self.controller.stop()
        self.is_running = False
        
        # 트레이 상태 업데이트
        if self.system_tray:
            self.system_tray.set_running_state(False)
            self.system_tray.show_message("Live Caption", "자막 생성이 중지되었습니다")
        
        print("✅ 자막 생성 중지 완료")
    
    def _on_caption_received(self, caption_data: Dict[str, Any]):
        """
        자막 수신 콜백
        
        Args:
            caption_data: 자막 데이터
        """
        if self.caption_window:
            # Qt 메인 스레드에서 실행
            QTimer.singleShot(0, lambda: self.caption_window.add_caption(caption_data))
    
    def change_theme(self, theme_name: str):
        """
        테마 변경
        
        Args:
            theme_name: 새 테마 이름
        """
        if self.caption_window:
            self.caption_window.change_theme(theme_name)
            self.theme_name = theme_name
            
            if self.system_tray:
                self.system_tray.show_message("Live Caption", f"테마가 '{theme_name}'으로 변경되었습니다")
    
    def clear_captions(self):
        """모든 자막 삭제"""
        if self.caption_window:
            self.caption_window.clear_captions()
    
    def show_settings(self):
        """설정 창 표시"""
        if not self.settings_window:
            self.settings_window = SettingsWindow(self.config_mgr, self.caption_window)
            self.settings_window.on_settings_changed = self._on_settings_changed
        
        self.settings_window.show()
        self.settings_window.activateWindow()
    
    def _on_settings_changed(self, settings: Dict[str, Any]):
        """
        설정 변경 콜백
        
        Args:
            settings: 변경된 설정
        """
        print(f"⏳ 설정 적용 중: {settings}")
        
        # 테마 변경
        if 'theme' in settings:
            self.change_theme(settings['theme'])
        
        # 창 설정 변경
        if 'window' in settings and self.caption_window:
            window_config = settings['window']
            self.caption_window.setWindowOpacity(window_config.get('opacity', 0.9))
            
            # Always on top
            if window_config.get('always_on_top', True):
                self.caption_window.setWindowFlags(
                    self.caption_window.windowFlags() | Qt.WindowStaysOnTopHint
                )
            else:
                self.caption_window.setWindowFlags(
                    self.caption_window.windowFlags() & ~Qt.WindowStaysOnTopHint
                )
            
            self.caption_window.show()
        
        # 성능 프로필 변경
        if 'performance' in settings:
            # TODO: 컨트롤러 재시작 필요
            print("⚠️  성능 프로필 변경은 재시작이 필요합니다")
        
        print("✅ 설정 적용 완료")
    
    def list_audio_devices(self) -> list:
        """
        사용 가능한 오디오 디바이스 목록
        
        Returns:
            list: 디바이스 정보 리스트
        """
        return self.controller.list_audio_devices()
    
    def get_status(self) -> Dict[str, Any]:
        """
        애플리케이션 상태 정보
        
        Returns:
            Dict: 상태 정보
        """
        controller_status = self.controller.get_status()
        
        return {
            'initialized': self.is_initialized,
            'running': self.is_running,
            'theme': self.theme_name,
            'controller': controller_status
        }
    
    def run(self) -> int:
        """
        애플리케이션 실행 (블로킹)
        
        Returns:
            int: 종료 코드
        """
        if not self.is_initialized:
            print("❌ 초기화되지 않았습니다")
            return 1
        
        print("🚀 Live Caption 실행 중...")
        print("   (창을 닫으면 트레이로 최소화됩니다)")
        print("   (트레이 아이콘 우클릭 → 종료)")
        
        # Qt 이벤트 루프 실행
        exit_code = self.qt_app.exec_()
        
        # 정리
        self.cleanup()
        
        return exit_code
    
    def cleanup(self):
        """리소스 정리"""
        print("\n⏳ 리소스 정리 중...")
        
        self.stop()
        
        if self.controller:
            self.controller.cleanup()
        
        if self.system_tray:
            self.system_tray.hide()
        
        if self.settings_window:
            self.settings_window.close()
        
        if self.caption_window:
            self.caption_window.close()
        
        print("✅ 리소스 정리 완료")
