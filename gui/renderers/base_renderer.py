"""
Base Renderer
자막 렌더러 추상 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QColor


class BaseRenderer(ABC):
    """자막 렌더러 베이스 클래스"""
    
    def __init__(self, theme_config: Dict[str, Any]):
        """
        Args:
            theme_config: 테마 설정
        """
        self.theme_config = theme_config
        self.widget: QWidget = None
        self.captions: List[Dict[str, Any]] = []
        
    @abstractmethod
    def create_widget(self) -> QWidget:
        """
        렌더러 위젯 생성
        
        Returns:
            QWidget: 자막 위젯
        """
        pass
    
    @abstractmethod
    def add_caption(self, caption_data: Dict[str, Any]):
        """
        자막 추가
        
        Args:
            caption_data: 자막 데이터
                - korean: 한국어 텍스트
                - english: 영어 텍스트
                - timestamp: 타임스탬프
        """
        pass
    
    @abstractmethod
    def clear_captions(self):
        """모든 자막 삭제"""
        pass
    
    @abstractmethod
    def update_display(self):
        """화면 업데이트"""
        pass
    
    def get_window_config(self) -> Dict[str, Any]:
        """
        창 설정 가져오기
        
        Returns:
            Dict: 창 설정
        """
        return self.theme_config.get('window', {})
    
    def get_caption_config(self) -> Dict[str, Any]:
        """
        자막 설정 가져오기
        
        Returns:
            Dict: 자막 설정
        """
        return self.theme_config.get('caption', {})
    
    def get_layout_config(self) -> Dict[str, Any]:
        """
        레이아웃 설정 가져오기
        
        Returns:
            Dict: 레이아웃 설정
        """
        return self.theme_config.get('layout', {})
    
    def get_background_config(self) -> Dict[str, Any]:
        """
        배경 설정 가져오기
        
        Returns:
            Dict: 배경 설정
        """
        return self.theme_config.get('background', {})
    
    def apply_fade_animation(self, widget: QWidget, fade_in: bool = True):
        """
        페이드 애니메이션 적용
        
        Args:
            widget: 대상 위젯
            fade_in: True=페이드 인, False=페이드 아웃
        """
        caption_config = self.get_caption_config()
        duration = int(caption_config.get('fade_duration', 0.5) * 1000)
        
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        if fade_in:
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
        else:
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
        
        animation.start()
    
    def hex_to_qcolor(self, hex_color: str) -> QColor:
        """
        HEX 색상을 QColor로 변환
        
        Args:
            hex_color: HEX 색상 (#RRGGBB)
            
        Returns:
            QColor: Qt 색상 객체
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return QColor(r, g, b)
    
    def build_stylesheet(self) -> str:
        """
        테마 설정을 기반으로 스타일시트 생성
        
        Returns:
            str: Qt 스타일시트
        """
        bg_config = self.get_background_config()
        caption_config = self.get_caption_config()
        
        # 배경 색상
        bg_color = bg_config.get('color', '#000000')
        bg_opacity = int(bg_config.get('opacity', 0.7) * 255)
        bg_rgba = f"rgba({self.hex_to_qcolor(bg_color).red()}, " \
                  f"{self.hex_to_qcolor(bg_color).green()}, " \
                  f"{self.hex_to_qcolor(bg_color).blue()}, " \
                  f"{bg_opacity})"
        
        # 테두리 반경
        border_radius = bg_config.get('border_radius', 0)
        
        # 한국어 자막 스타일
        korean_config = caption_config.get('korean', {})
        korean_color = korean_config.get('color', '#FFFFFF')
        korean_font_size = korean_config.get('font_size', 24)
        korean_font_family = korean_config.get('font_family', 'Arial')
        korean_font_weight = 'bold' if korean_config.get('font_weight') == 'bold' else 'normal'
        
        # 영어 자막 스타일
        english_config = caption_config.get('english', {})
        english_color = english_config.get('color', '#FFFF00')
        english_font_size = english_config.get('font_size', 20)
        english_font_family = english_config.get('font_family', 'Arial')
        english_font_weight = 'bold' if english_config.get('font_weight') == 'bold' else 'normal'
        
        stylesheet = f"""
            QWidget#CaptionWidget {{
                background-color: {bg_rgba};
                border-radius: {border_radius}px;
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
            
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            
            QScrollBar:vertical {{
                background: transparent;
                width: 10px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-height: 20px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
        
        return stylesheet
