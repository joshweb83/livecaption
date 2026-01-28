"""
Transparent Overlay Renderer
투명 오버레이 자막 렌더러 (배경 투명)
"""

from typing import Dict, Any
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen

from gui.renderers.base_renderer import BaseRenderer


class TransparentRenderer(BaseRenderer):
    """투명 오버레이 자막 렌더러"""
    
    def __init__(self, theme_config: Dict[str, Any]):
        super().__init__(theme_config)
        self.korean_label = None
        self.english_label = None
        
    def create_widget(self) -> QWidget:
        """투명 오버레이 위젯 생성"""
        # 메인 위젯
        self.widget = TransparentCaptionWidget()
        self.widget.setObjectName("CaptionWidget")
        
        # 투명 배경 설정
        self.widget.setAttribute(Qt.WA_TranslucentBackground)
        self.widget.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # 레이아웃
        layout = QVBoxLayout(self.widget)
        layout_config = self.get_layout_config()
        padding = layout_config.get('padding', 10)
        layout.setContentsMargins(padding, padding, padding, padding)
        layout.setSpacing(layout_config.get('spacing', 5))
        
        # 한국어 라벨
        self.korean_label = OutlinedLabel("")
        self.korean_label.setObjectName("KoreanCaption")
        self.korean_label.setAlignment(Qt.AlignCenter)
        self.korean_label.setWordWrap(True)
        
        caption_config = self.get_caption_config()
        korean_config = caption_config.get('korean', {})
        self.korean_label.set_outline_color(QColor(0, 0, 0))
        self.korean_label.set_outline_width(3)
        
        layout.addWidget(self.korean_label)
        
        # 영어 라벨
        self.english_label = OutlinedLabel("")
        self.english_label.setObjectName("EnglishCaption")
        self.english_label.setAlignment(Qt.AlignCenter)
        self.english_label.setWordWrap(True)
        
        english_config = caption_config.get('english', {})
        self.english_label.set_outline_color(QColor(0, 0, 0))
        self.english_label.set_outline_width(2)
        
        layout.addWidget(self.english_label)
        
        # 스타일시트 적용 (배경 투명)
        self.widget.setStyleSheet(self._build_transparent_stylesheet())
        
        return self.widget
    
    def _build_transparent_stylesheet(self) -> str:
        """투명 오버레이용 스타일시트"""
        caption_config = self.get_caption_config()
        
        # 한국어 자막 스타일
        korean_config = caption_config.get('korean', {})
        korean_color = korean_config.get('color', '#FFFFFF')
        korean_font_size = korean_config.get('font_size', 32)
        korean_font_family = korean_config.get('font_family', 'Arial')
        korean_font_weight = 'bold' if korean_config.get('font_weight') == 'bold' else 'normal'
        
        # 영어 자막 스타일
        english_config = caption_config.get('english', {})
        english_color = english_config.get('color', '#FFFF00')
        english_font_size = english_config.get('font_size', 28)
        english_font_family = english_config.get('font_family', 'Arial')
        english_font_weight = 'bold' if english_config.get('font_weight') == 'bold' else 'normal'
        
        stylesheet = f"""
            QWidget#CaptionWidget {{
                background: transparent;
            }}
            
            QLabel#KoreanCaption {{
                color: {korean_color};
                font-size: {korean_font_size}px;
                font-family: "{korean_font_family}";
                font-weight: {korean_font_weight};
                background: transparent;
            }}
            
            QLabel#EnglishCaption {{
                color: {english_color};
                font-size: {english_font_size}px;
                font-family: "{english_font_family}";
                font-weight: {english_font_weight};
                background: transparent;
            }}
        """
        
        return stylesheet
    
    def add_caption(self, caption_data: Dict[str, Any]):
        """자막 추가 (최신 자막만 표시)"""
        if not self.korean_label or not self.english_label:
            return
        
        # 자막 데이터 저장
        self.captions.append(caption_data)
        
        # 최대 1개만 유지
        if len(self.captions) > 1:
            self.captions.pop(0)
        
        # 자막 업데이트
        self.korean_label.setText(caption_data['korean'])
        self.english_label.setText(caption_data['english'])
        
        # 페이드 인 애니메이션
        # self.apply_fade_animation(self.widget, fade_in=True)
    
    def clear_captions(self):
        """모든 자막 삭제"""
        self.captions.clear()
        
        if self.korean_label:
            self.korean_label.setText("")
        if self.english_label:
            self.english_label.setText("")
    
    def update_display(self):
        """화면 업데이트"""
        if self.widget:
            self.widget.update()


class TransparentCaptionWidget(QWidget):
    """투명 배경 자막 위젯"""
    
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)


class OutlinedLabel(QLabel):
    """외곽선이 있는 라벨"""
    
    def __init__(self, text=""):
        super().__init__(text)
        self.outline_color = QColor(0, 0, 0)
        self.outline_width = 2
    
    def set_outline_color(self, color: QColor):
        """외곽선 색상 설정"""
        self.outline_color = color
    
    def set_outline_width(self, width: int):
        """외곽선 두께 설정"""
        self.outline_width = width
    
    def paintEvent(self, event):
        """페인트 이벤트 (외곽선 그리기)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 외곽선 그리기
        pen = QPen(self.outline_color, self.outline_width)
        painter.setPen(pen)
        painter.setFont(self.font())
        
        # 텍스트 위치 계산
        rect = self.rect()
        alignment = self.alignment()
        
        # 외곽선 (8방향)
        for dx in [-self.outline_width, 0, self.outline_width]:
            for dy in [-self.outline_width, 0, self.outline_width]:
                if dx == 0 and dy == 0:
                    continue
                offset_rect = rect.adjusted(dx, dy, dx, dy)
                painter.drawText(offset_rect, alignment, self.text())
        
        # 원본 텍스트 (부모 클래스 호출)
        super().paintEvent(event)
