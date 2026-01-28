"""
System Tray
시스템 트레이
"""

from typing import Optional, Callable
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal


class SystemTray(QObject):
    """시스템 트레이"""
    
    # 시그널
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    show_window_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        
        # 트레이 아이콘
        self.tray_icon = QSystemTrayIcon(parent)
        
        # 아이콘 설정 (기본 아이콘)
        # TODO: 실제 아이콘 파일로 교체
        # self.tray_icon.setIcon(QIcon('icon.png'))
        
        # 메뉴 생성
        self._create_menu()
        
        # 더블클릭 이벤트
        self.tray_icon.activated.connect(self._on_activated)
        
        # 상태
        self.is_running = False
        
    def _create_menu(self):
        """메뉴 생성"""
        menu = QMenu()
        
        # 시작/중지
        self.start_action = QAction("시작", self)
        self.start_action.triggered.connect(self.start_requested.emit)
        menu.addAction(self.start_action)
        
        self.stop_action = QAction("중지", self)
        self.stop_action.triggered.connect(self.stop_requested.emit)
        self.stop_action.setEnabled(False)
        menu.addAction(self.stop_action)
        
        menu.addSeparator()
        
        # 창 표시
        show_action = QAction("창 표시", self)
        show_action.triggered.connect(self.show_window_requested.emit)
        menu.addAction(show_action)
        
        # 설정
        settings_action = QAction("설정", self)
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # 종료
        quit_action = QAction("종료", self)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def _on_activated(self, reason):
        """트레이 아이콘 활성화 이벤트"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window_requested.emit()
    
    def show(self):
        """트레이 아이콘 표시"""
        self.tray_icon.show()
    
    def hide(self):
        """트레이 아이콘 숨기기"""
        self.tray_icon.hide()
    
    def set_running_state(self, is_running: bool):
        """
        실행 상태 설정
        
        Args:
            is_running: 실행 중 여부
        """
        self.is_running = is_running
        self.start_action.setEnabled(not is_running)
        self.stop_action.setEnabled(is_running)
    
    def show_message(self, title: str, message: str, icon=QSystemTrayIcon.Information):
        """
        알림 메시지 표시
        
        Args:
            title: 제목
            message: 메시지
            icon: 아이콘 타입
        """
        self.tray_icon.showMessage(title, message, icon, 3000)
