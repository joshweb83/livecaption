"""
Panel Renderer
패널형 자막 렌더러 (우측 패널)
"""

from typing import Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from gui.renderers.base_renderer import BaseRenderer


class PanelRenderer(BaseRenderer):
    """패널형 자막 렌더러"""
    
    def __init__(self, theme_config: Dict[str, Any]):
        super().__init__(theme_config)
        self.scroll_area = None
        self.content_widget = None
        self.content_layout = None
        
    def create_widget(self) -> QWidget:
        """패널 위젯 생성"""
        # 메인 위젯
        self.widget = QWidget()
        self.widget.setObjectName("CaptionWidget")
        
        # 레이아웃
        main_layout = QVBoxLayout(self.widget)
        layout_config = self.get_layout_config()
        padding = layout_config.get('padding', 20)
        main_layout.setContentsMargins(padding, padding, padding, padding)
        main_layout.setSpacing(layout_config.get('spacing', 10))
        
        # 스크롤 영역
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 컨텐츠 위젯
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(layout_config.get('spacing', 10))
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addStretch()
        
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        
        # 스타일시트 적용
        self.widget.setStyleSheet(self.build_stylesheet())
        
        return self.widget
    
    def add_caption(self, caption_data: Dict[str, Any]):
        """자막 추가"""
        if not self.content_layout:
            return
        
        # 자막 데이터 저장
        self.captions.append(caption_data)
        
        # 최대 라인 수 제한
        caption_config = self.get_caption_config()
        max_lines = caption_config.get('max_lines', 10)
        
        if len(self.captions) > max_lines:
            self.captions.pop(0)
            # 첫 번째 자막 위젯 제거
            item = self.content_layout.itemAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        # 자막 프레임 생성
        caption_frame = self._create_caption_frame(caption_data)
        
        # 스트레치 제거 후 자막 추가
        stretch_item = self.content_layout.takeAt(self.content_layout.count() - 1)
        self.content_layout.addWidget(caption_frame)
        self.content_layout.addStretch()
        
        # 스크롤을 맨 아래로
        QTimer.singleShot(100, self._scroll_to_bottom)
    
    def _create_caption_frame(self, caption_data: Dict[str, Any]) -> QFrame:
        """자막 프레임 생성"""
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        caption_config = self.get_caption_config()
        
        # 한국어 자막
        korean_label = QLabel(caption_data['korean'])
        korean_label.setObjectName("KoreanCaption")
        korean_label.setWordWrap(True)
        korean_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        korean_config = caption_config.get('korean', {})
        alignment = korean_config.get('alignment', 'left')
        if alignment == 'center':
            korean_label.setAlignment(Qt.AlignCenter)
        elif alignment == 'right':
            korean_label.setAlignment(Qt.AlignRight)
        else:
            korean_label.setAlignment(Qt.AlignLeft)
        
        layout.addWidget(korean_label)
        
        # 영어 자막
        english_label = QLabel(caption_data['english'])
        english_label.setObjectName("EnglishCaption")
        english_label.setWordWrap(True)
        english_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        english_config = caption_config.get('english', {})
        alignment = english_config.get('alignment', 'left')
        if alignment == 'center':
            english_label.setAlignment(Qt.AlignCenter)
        elif alignment == 'right':
            english_label.setAlignment(Qt.AlignRight)
        else:
            english_label.setAlignment(Qt.AlignLeft)
        
        layout.addWidget(english_label)
        
        return frame
    
    def _scroll_to_bottom(self):
        """스크롤을 맨 아래로"""
        if self.scroll_area:
            scrollbar = self.scroll_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def clear_captions(self):
        """모든 자막 삭제"""
        self.captions.clear()
        
        if not self.content_layout:
            return
        
        # 모든 위젯 제거
        while self.content_layout.count() > 1:  # 스트레치 제외
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def update_display(self):
        """화면 업데이트"""
        if self.widget:
            self.widget.update()
