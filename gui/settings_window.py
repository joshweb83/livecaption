"""
Settings Window
설정 창
"""

from typing import Dict, Any, Optional, Callable
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QComboBox, QPushButton, QGroupBox, QSpinBox,
    QSlider, QCheckBox, QColorDialog, QFontDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

from core.config_manager import ConfigManager
from core.theme_manager import ThemeManager


class SettingsWindow(QDialog):
    """설정 창"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        """
        Args:
            config_manager: 설정 관리자
            parent: 부모 위젯
        """
        super().__init__(parent)
        
        self.config_mgr = config_manager
        self.theme_mgr = ThemeManager()
        self.theme_mgr.load_themes('themes')
        
        # 콜백
        self.on_settings_changed: Optional[Callable[[Dict[str, Any]], None]] = None
        
        # 임시 설정 (적용 전)
        self.temp_settings = {}
        
        self._setup_ui()
        self._load_current_settings()
        
    def _setup_ui(self):
        """UI 설정"""
        self.setWindowTitle("Live Caption - 설정")
        self.setMinimumSize(600, 500)
        
        # 메인 레이아웃
        layout = QVBoxLayout(self)
        
        # 탭 위젯
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # 탭 추가
        self.tabs.addTab(self._create_general_tab(), "일반")
        self.tabs.addTab(self._create_theme_tab(), "테마")
        self.tabs.addTab(self._create_performance_tab(), "성능")
        self.tabs.addTab(self._create_audio_tab(), "오디오")
        
        # 버튼
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("적용")
        self.apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        self.ok_btn = QPushButton("확인")
        self.ok_btn.clicked.connect(self._ok_clicked)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("취소")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self) -> QWidget:
        """일반 탭"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 창 설정
        window_group = QGroupBox("창 설정")
        window_layout = QVBoxLayout()
        
        # Always on top
        self.always_on_top_check = QCheckBox("항상 위에 표시")
        window_layout.addWidget(self.always_on_top_check)
        
        # Click through
        self.click_through_check = QCheckBox("클릭 투과 (마우스 이벤트 무시)")
        window_layout.addWidget(self.click_through_check)
        
        # 창 투명도
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("창 투명도:"))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(90)
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        opacity_layout.addWidget(self.opacity_slider)
        self.opacity_label = QLabel("90%")
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f"{v}%")
        )
        opacity_layout.addWidget(self.opacity_label)
        window_layout.addLayout(opacity_layout)
        
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)
        
        # 자동 시작
        startup_group = QGroupBox("시작 설정")
        startup_layout = QVBoxLayout()
        
        self.auto_start_check = QCheckBox("프로그램 시작 시 자동으로 자막 생성 시작")
        startup_layout.addWidget(self.auto_start_check)
        
        self.minimize_to_tray_check = QCheckBox("최소화 시 시스템 트레이로")
        startup_layout.addWidget(self.minimize_to_tray_check)
        
        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)
        
        layout.addStretch()
        return widget
    
    def _create_theme_tab(self) -> QWidget:
        """테마 탭"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 테마 선택
        theme_group = QGroupBox("테마 선택")
        theme_layout = QVBoxLayout()
        
        theme_select_layout = QHBoxLayout()
        theme_select_layout.addWidget(QLabel("테마:"))
        self.theme_combo = QComboBox()
        
        # 테마 목록 로드
        themes = self.theme_mgr.list_themes()
        for theme in themes:
            theme_info = self.theme_mgr.get_theme_info(theme)
            if theme_info:
                self.theme_combo.addItem(theme_info['name'], theme)
        
        theme_select_layout.addWidget(self.theme_combo)
        theme_layout.addLayout(theme_select_layout)
        
        # 테마 설명
        self.theme_description = QLabel("")
        self.theme_description.setWordWrap(True)
        self.theme_combo.currentIndexChanged.connect(self._update_theme_description)
        theme_layout.addWidget(self.theme_description)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # 폰트 설정
        font_group = QGroupBox("폰트 설정")
        font_layout = QVBoxLayout()
        
        # 한국어 폰트
        korean_font_layout = QHBoxLayout()
        korean_font_layout.addWidget(QLabel("한국어 폰트:"))
        self.korean_font_btn = QPushButton("선택...")
        self.korean_font_btn.clicked.connect(lambda: self._select_font('korean'))
        korean_font_layout.addWidget(self.korean_font_btn)
        self.korean_font_label = QLabel("맑은 고딕, 24pt")
        korean_font_layout.addWidget(self.korean_font_label)
        font_layout.addLayout(korean_font_layout)
        
        # 영어 폰트
        english_font_layout = QHBoxLayout()
        english_font_layout.addWidget(QLabel("영어 폰트:"))
        self.english_font_btn = QPushButton("선택...")
        self.english_font_btn.clicked.connect(lambda: self._select_font('english'))
        english_font_layout.addWidget(self.english_font_btn)
        self.english_font_label = QLabel("Arial, 20pt")
        english_font_layout.addWidget(self.english_font_label)
        font_layout.addLayout(english_font_layout)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # 색상 설정
        color_group = QGroupBox("색상 설정")
        color_layout = QVBoxLayout()
        
        # 한국어 색상
        korean_color_layout = QHBoxLayout()
        korean_color_layout.addWidget(QLabel("한국어 색상:"))
        self.korean_color_btn = QPushButton("선택...")
        self.korean_color_btn.clicked.connect(lambda: self._select_color('korean'))
        korean_color_layout.addWidget(self.korean_color_btn)
        self.korean_color_label = QLabel("■")
        self.korean_color_label.setStyleSheet("color: #FFFFFF; font-size: 24px;")
        korean_color_layout.addWidget(self.korean_color_label)
        color_layout.addLayout(korean_color_layout)
        
        # 영어 색상
        english_color_layout = QHBoxLayout()
        english_color_layout.addWidget(QLabel("영어 색상:"))
        self.english_color_btn = QPushButton("선택...")
        self.english_color_btn.clicked.connect(lambda: self._select_color('english'))
        english_color_layout.addWidget(self.english_color_btn)
        self.english_color_label = QLabel("■")
        self.english_color_label.setStyleSheet("color: #FFFF00; font-size: 24px;")
        english_color_layout.addWidget(self.english_color_label)
        color_layout.addLayout(english_color_layout)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        layout.addStretch()
        return widget
    
    def _create_performance_tab(self) -> QWidget:
        """성능 탭"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 성능 프로필
        profile_group = QGroupBox("성능 프로필")
        profile_layout = QVBoxLayout()
        
        profile_select_layout = QHBoxLayout()
        profile_select_layout.addWidget(QLabel("프로필:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItem("경량 (CPU, 빠른 시작)", "light")
        self.profile_combo.addItem("표준 (GPU, 고품질)", "standard")
        profile_select_layout.addWidget(self.profile_combo)
        profile_layout.addLayout(profile_select_layout)
        
        # 프로필 설명
        self.profile_description = QLabel(
            "경량: CPU 전용, Whisper Small, 1-1.6초 지연\n"
            "표준: GPU 필요, Whisper Large, 0.3-0.7초 지연"
        )
        self.profile_description.setWordWrap(True)
        profile_layout.addWidget(self.profile_description)
        
        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)
        
        # 고급 설정
        advanced_group = QGroupBox("고급 설정")
        advanced_layout = QVBoxLayout()
        
        # 청크 크기
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("오디오 청크 크기 (초):"))
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(1, 10)
        self.chunk_size_spin.setValue(3)
        chunk_layout.addWidget(self.chunk_size_spin)
        advanced_layout.addLayout(chunk_layout)
        
        # VAD 필터
        self.vad_filter_check = QCheckBox("VAD 필터 사용 (무음 제거)")
        self.vad_filter_check.setChecked(True)
        advanced_layout.addWidget(self.vad_filter_check)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        return widget
    
    def _create_audio_tab(self) -> QWidget:
        """오디오 탭"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 오디오 디바이스
        device_group = QGroupBox("오디오 디바이스")
        device_layout = QVBoxLayout()
        
        device_select_layout = QHBoxLayout()
        device_select_layout.addWidget(QLabel("입력 디바이스:"))
        self.device_combo = QComboBox()
        self.device_combo.addItem("기본 디바이스", None)
        device_select_layout.addWidget(self.device_combo)
        
        refresh_btn = QPushButton("새로고침")
        refresh_btn.clicked.connect(self._refresh_audio_devices)
        device_select_layout.addWidget(refresh_btn)
        
        device_layout.addLayout(device_select_layout)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # 샘플레이트
        sample_rate_group = QGroupBox("샘플레이트")
        sample_rate_layout = QHBoxLayout()
        sample_rate_layout.addWidget(QLabel("샘플레이트:"))
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItem("16000 Hz (권장)", 16000)
        self.sample_rate_combo.addItem("44100 Hz", 44100)
        self.sample_rate_combo.addItem("48000 Hz", 48000)
        sample_rate_layout.addWidget(self.sample_rate_combo)
        sample_rate_group.setLayout(sample_rate_layout)
        layout.addWidget(sample_rate_group)
        
        layout.addStretch()
        return widget
    
    def _update_theme_description(self):
        """테마 설명 업데이트"""
        theme_id = self.theme_combo.currentData()
        if theme_id:
            theme_info = self.theme_mgr.get_theme_info(theme_id)
            if theme_info:
                self.theme_description.setText(theme_info['description'])
    
    def _select_font(self, lang: str):
        """폰트 선택"""
        font, ok = QFontDialog.getFont()
        if ok:
            font_str = f"{font.family()}, {font.pointSize()}pt"
            if lang == 'korean':
                self.korean_font_label.setText(font_str)
                self.temp_settings['korean_font'] = font
            else:
                self.english_font_label.setText(font_str)
                self.temp_settings['english_font'] = font
    
    def _select_color(self, lang: str):
        """색상 선택"""
        color = QColorDialog.getColor()
        if color.isValid():
            if lang == 'korean':
                self.korean_color_label.setStyleSheet(
                    f"color: {color.name()}; font-size: 24px;"
                )
                self.temp_settings['korean_color'] = color.name()
            else:
                self.english_color_label.setStyleSheet(
                    f"color: {color.name()}; font-size: 24px;"
                )
                self.temp_settings['english_color'] = color.name()
    
    def _refresh_audio_devices(self):
        """오디오 디바이스 새로고침"""
        # TODO: AudioCapture에서 디바이스 목록 가져오기
        pass
    
    def _load_current_settings(self):
        """현재 설정 로드"""
        # 일반 설정
        window_config = self.config_mgr.get('gui.window', {})
        self.always_on_top_check.setChecked(window_config.get('always_on_top', True))
        self.click_through_check.setChecked(window_config.get('click_through', False))
        opacity = int(window_config.get('opacity', 0.9) * 100)
        self.opacity_slider.setValue(opacity)
        
        # 테마
        current_theme = self.config_mgr.get('gui.theme', 'panel')
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        # 성능
        profile = self.config_mgr.get('performance.profile', 'light')
        index = self.profile_combo.findData(profile)
        if index >= 0:
            self.profile_combo.setCurrentIndex(index)
    
    def _apply_settings(self):
        """설정 적용"""
        settings = self._collect_settings()
        
        if self.on_settings_changed:
            self.on_settings_changed(settings)
        
        QMessageBox.information(self, "설정", "설정이 적용되었습니다.")
    
    def _ok_clicked(self):
        """확인 버튼 클릭"""
        self._apply_settings()
        self.accept()
    
    def _collect_settings(self) -> Dict[str, Any]:
        """설정 수집"""
        return {
            'window': {
                'always_on_top': self.always_on_top_check.isChecked(),
                'click_through': self.click_through_check.isChecked(),
                'opacity': self.opacity_slider.value() / 100.0
            },
            'theme': self.theme_combo.currentData(),
            'performance': {
                'profile': self.profile_combo.currentData(),
                'chunk_size': self.chunk_size_spin.value(),
                'vad_filter': self.vad_filter_check.isChecked()
            },
            'audio': {
                'device_index': self.device_combo.currentData(),
                'sample_rate': self.sample_rate_combo.currentData()
            }
        }
