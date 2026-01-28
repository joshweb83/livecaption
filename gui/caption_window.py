"""
Caption Window
자막 표시 메인 창
"""

from typing import Dict, Any, Optional
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QScreen

from core.theme_manager import ThemeManager
from gui.renderers import RendererFactory, BaseRenderer


class CaptionWindow(QMainWindow):
    """자막 표시 메인 창"""
    
    def __init__(self, theme_name: str = 'panel'):
        """
        Args:
            theme_name: 테마 이름
        """
        super().__init__()
        
        # 테마 로드
        self.theme_mgr = ThemeManager()
        self.theme_mgr.load_themes('themes')
        self.theme_name = theme_name
        self.theme_config = self.theme_mgr.get_theme(theme_name)
        
        if self.theme_config is None:
            raise ValueError(f"테마를 찾을 수 없습니다: {theme_name}")
        
        # 렌더러 생성
        self.renderer: BaseRenderer = RendererFactory.create_renderer(self.theme_config)
        
        # 창 설정
        self._setup_window()
        
        # 렌더러 위젯 설정
        renderer_widget = self.renderer.create_widget()
        self.setCentralWidget(renderer_widget)
        
        # 드래그 이동 지원
        self.dragging = False
        self.drag_position = QPoint()
        
    def _setup_window(self):
        """창 설정"""
        window_config = self.renderer.get_window_config()
        
        # 창 제목
        theme_meta = self.theme_config.get('theme', {})
        self.setWindowTitle(f"Live Caption - {theme_meta.get('name', self.theme_name)}")
        
        # 창 크기
        width = window_config.get('width', 400)
        height = window_config.get('height', 600)
        self.resize(width, height)
        
        # 창 플래그
        flags = Qt.Window
        
        # Always on top
        if window_config.get('always_on_top', True):
            flags |= Qt.WindowStaysOnTopHint
        
        # 프레임리스 (투명 오버레이용)
        if self.theme_name == 'transparent':
            flags |= Qt.FramelessWindowHint
            flags |= Qt.Tool
            self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setWindowFlags(flags)
        
        # Click-through (클릭 투과)
        if window_config.get('click_through', False):
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # 창 투명도
        opacity = window_config.get('opacity', 1.0)
        self.setWindowOpacity(opacity)
        
        # 창 위치
        self._set_window_position(window_config.get('position', 'right'))
    
    def _set_window_position(self, position: str):
        """
        창 위치 설정
        
        Args:
            position: 위치 (left, right, top, bottom, center, custom)
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        window_width = self.width()
        window_height = self.height()
        
        if position == 'right':
            x = screen_geometry.width() - window_width
            y = (screen_geometry.height() - window_height) // 2
        elif position == 'left':
            x = 0
            y = (screen_geometry.height() - window_height) // 2
        elif position == 'top':
            x = (screen_geometry.width() - window_width) // 2
            y = 0
        elif position == 'bottom':
            x = (screen_geometry.width() - window_width) // 2
            y = screen_geometry.height() - window_height
        elif position == 'center':
            x = (screen_geometry.width() - window_width) // 2
            y = (screen_geometry.height() - window_height) // 2
        else:
            # custom: 현재 위치 유지
            return
        
        self.move(x, y)
    
    def add_caption(self, caption_data: Dict[str, Any]):
        """
        자막 추가
        
        Args:
            caption_data: 자막 데이터
                - korean: 한국어 텍스트
                - english: 영어 텍스트
                - timestamp: 타임스탬프
        """
        self.renderer.add_caption(caption_data)
    
    def clear_captions(self):
        """모든 자막 삭제"""
        self.renderer.clear_captions()
    
    def change_theme(self, theme_name: str):
        """
        테마 변경
        
        Args:
            theme_name: 새 테마 이름
        """
        # 새 테마 로드
        new_theme_config = self.theme_mgr.get_theme(theme_name)
        if new_theme_config is None:
            print(f"⚠️  테마를 찾을 수 없습니다: {theme_name}")
            return
        
        # 기존 자막 저장
        old_captions = self.renderer.captions.copy()
        
        # 새 렌더러 생성
        self.theme_name = theme_name
        self.theme_config = new_theme_config
        self.renderer = RendererFactory.create_renderer(new_theme_config)
        
        # 렌더러 위젯 교체
        renderer_widget = self.renderer.create_widget()
        self.setCentralWidget(renderer_widget)
        
        # 창 설정 재적용
        self._setup_window()
        
        # 자막 복원
        for caption in old_captions:
            self.renderer.add_caption(caption)
        
        print(f"✅ 테마 변경: {theme_name}")
    
    def mousePressEvent(self, event):
        """마우스 누름 이벤트 (드래그 시작)"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """마우스 이동 이벤트 (드래그)"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """마우스 놓음 이벤트 (드래그 종료)"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def closeEvent(self, event):
        """창 닫기 이벤트"""
        # 렌더러 정리
        if self.renderer:
            self.renderer.clear_captions()
        
        event.accept()
