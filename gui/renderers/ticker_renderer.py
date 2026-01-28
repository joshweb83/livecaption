"""
Ticker Renderer
뉴스 자막형 렌더러 (하단 배너)
"""

from typing import Dict, Any
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont

from gui.renderers.base_renderer import BaseRenderer


class TickerRenderer(BaseRenderer):
    """뉴스 자막형 렌더러"""
    
    def __init__(self, theme_config: Dict[str, Any]):
        super().__init__(theme_config)
        self.korean_label = None
        self.english_label = None
        self.current_caption = None
        
    def create_widget(self) -> QWidget:
        """뉴스 자막형 위젯 생성"""
        # 메인 위젯
        self.widget = QWidget()
        self.widget.setObjectName("CaptionWidget")
        
        # 레이아웃
        layout = QHBoxLayout(self.widget)
        layout_config = self.get_layout_config()
        padding = layout_config.get('padding', 15)
        layout.setContentsMargins(padding, padding, padding, padding)
        layout.setSpacing(layout_config.get('spacing', 20))
        
        # 한국어 라벨
        self.korean_label = QLabel("")
        self.korean_label.setObjectName("KoreanCaption")
        self.korean_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.korean_label.setWordWrap(False)
        
        layout.addWidget(self.korean_label, 1)
        
        # 구분선
        separator = QLabel("|")
        separator.setStyleSheet("color: #888888; font-size: 24px;")
        layout.addWidget(separator, 0)
        
        # 영어 라벨
        self.english_label = QLabel("")
        self.english_label.setObjectName("EnglishCaption")
        self.english_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.english_label.setWordWrap(False)
        
        layout.addWidget(self.english_label, 1)
        
        # 스타일시트 적용
        self.widget.setStyleSheet(self.build_stylesheet())
        
        return self.widget
    
    def add_caption(self, caption_data: Dict[str, Any]):
        """자막 추가 (최신 자막만 표시)"""
        if not self.korean_label or not self.english_label:
            return
        
        # 자막 데이터 저장
        self.captions.append(caption_data)
        
        # 최대 1개만 유지
        if len(self.captions) > 1:
            self.captions.pop(0)
        
        self.current_caption = caption_data
        
        # 자막 업데이트
        self.korean_label.setText(caption_data['korean'])
        self.english_label.setText(caption_data['english'])
        
        # 슬라이드 애니메이션 (선택사항)
        # self._apply_slide_animation()
    
    def _apply_slide_animation(self):
        """슬라이드 애니메이션"""
        if not self.widget:
            return
        
        caption_config = self.get_caption_config()
        duration = int(caption_config.get('fade_duration', 0.3) * 1000)
        
        # 아래에서 위로 슬라이드
        animation = QPropertyAnimation(self.widget, b"geometry")
        animation.setDuration(duration)
        
        current_geo = self.widget.geometry()
        start_geo = QRect(
            current_geo.x(),
            current_geo.y() + 50,
            current_geo.width(),
            current_geo.height()
        )
        
        animation.setStartValue(start_geo)
        animation.setEndValue(current_geo)
        animation.start()
    
    def clear_captions(self):
        """모든 자막 삭제"""
        self.captions.clear()
        self.current_caption = None
        
        if self.korean_label:
            self.korean_label.setText("")
        if self.english_label:
            self.english_label.setText("")
    
    def update_display(self):
        """화면 업데이트"""
        if self.widget:
            self.widget.update()
