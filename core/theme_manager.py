"""
Theme Manager
테마 로드 및 관리
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class ThemeManager:
    """테마 관리자 클래스 (Singleton)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.themes: Dict[str, Dict[str, Any]] = {}
        self.current_theme: Optional[str] = None
        self.themes_dir: Path = Path("themes")
        self._initialized = True
    
    def load_themes(self, themes_dir: str = "themes"):
        """
        테마 폴더에서 모든 테마 로드
        
        Args:
            themes_dir: 테마 폴더 경로
        """
        self.themes_dir = Path(themes_dir)
        
        if not self.themes_dir.exists():
            self.themes_dir.mkdir(parents=True)
            return
        
        # .yaml 파일 찾기
        for theme_file in self.themes_dir.glob("*.yaml"):
            theme_name = theme_file.stem
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = yaml.safe_load(f)
                    self.themes[theme_name] = theme_data
            except Exception as e:
                print(f"Failed to load theme '{theme_name}': {e}")
    
    def get_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        테마 가져오기
        
        Args:
            theme_name: 테마 이름
            
        Returns:
            Dict: 테마 데이터
        """
        return self.themes.get(theme_name)
    
    def set_current_theme(self, theme_name: str) -> bool:
        """
        현재 테마 설정
        
        Args:
            theme_name: 테마 이름
            
        Returns:
            bool: 성공 여부
        """
        if theme_name not in self.themes:
            return False
        
        self.current_theme = theme_name
        return True
    
    def get_current_theme(self) -> Optional[Dict[str, Any]]:
        """
        현재 테마 가져오기
        
        Returns:
            Dict: 현재 테마 데이터
        """
        if self.current_theme is None:
            return None
        return self.themes.get(self.current_theme)
    
    def list_themes(self) -> List[str]:
        """
        사용 가능한 테마 목록
        
        Returns:
            List[str]: 테마 이름 리스트
        """
        return list(self.themes.keys())
    
    def get_theme_info(self, theme_name: str) -> Optional[Dict[str, str]]:
        """
        테마 정보 가져오기
        
        Args:
            theme_name: 테마 이름
            
        Returns:
            Dict: 테마 정보 (이름, 설명, 렌더러)
        """
        theme = self.get_theme(theme_name)
        if theme is None:
            return None
        
        theme_meta = theme.get('theme', {})
        return {
            'name': theme_meta.get('name', theme_name),
            'description': theme_meta.get('description', ''),
            'renderer': theme_meta.get('renderer', 'BaseRenderer')
        }
    
    def create_default_themes(self):
        """기본 테마 생성 (테마 파일이 없을 때)"""
        default_themes = {
            'panel': self._create_panel_theme(),
            'transparent': self._create_transparent_theme(),
            'ticker': self._create_ticker_theme()
        }
        
        for theme_name, theme_data in default_themes.items():
            theme_path = self.themes_dir / f"{theme_name}.yaml"
            if not theme_path.exists():
                with open(theme_path, 'w', encoding='utf-8') as f:
                    yaml.dump(theme_data, f, default_flow_style=False, allow_unicode=True)
                self.themes[theme_name] = theme_data
    
    def _create_panel_theme(self) -> Dict[str, Any]:
        """패널형 테마 생성"""
        return {
            'theme': {
                'name': '패널형',
                'description': '우측 패널 형태의 자막',
                'renderer': 'PanelRenderer'
            },
            'window': {
                'width': 400,
                'height': 600,
                'position': 'right',
                'opacity': 0.9,
                'always_on_top': True,
                'click_through': False
            },
            'background': {
                'color': '#000000',
                'opacity': 0.7,
                'border_radius': 10
            },
            'layout': {
                'type': 'vertical',
                'padding': 20,
                'spacing': 10,
                'scroll': True
            },
            'caption': {
                'korean': {
                    'font_family': '맑은 고딕',
                    'font_size': 24,
                    'font_weight': 'bold',
                    'color': '#FFFFFF',
                    'alignment': 'left'
                },
                'english': {
                    'font_family': 'Arial',
                    'font_size': 20,
                    'font_weight': 'normal',
                    'color': '#FFFF00',
                    'alignment': 'left'
                },
                'max_lines': 10,
                'fade_duration': 0.5
            }
        }
    
    def _create_transparent_theme(self) -> Dict[str, Any]:
        """투명 오버레이 테마 생성"""
        return {
            'theme': {
                'name': '투명 오버레이',
                'description': '배경 없이 텍스트만 표시',
                'renderer': 'TransparentRenderer'
            },
            'window': {
                'width': 800,
                'height': 150,
                'position': 'bottom',
                'opacity': 1.0,
                'always_on_top': True,
                'click_through': True
            },
            'background': {
                'color': '#000000',
                'opacity': 0.0
            },
            'layout': {
                'type': 'vertical',
                'padding': 10,
                'spacing': 5,
                'scroll': False
            },
            'caption': {
                'korean': {
                    'font_family': '맑은 고딕',
                    'font_size': 28,
                    'font_weight': 'bold',
                    'color': '#FFFFFF',
                    'alignment': 'center',
                    'stroke_width': 3,
                    'stroke_color': '#000000'
                },
                'english': {
                    'font_family': 'Arial',
                    'font_size': 24,
                    'font_weight': 'normal',
                    'color': '#FFFF00',
                    'alignment': 'center',
                    'stroke_width': 3,
                    'stroke_color': '#000000'
                },
                'max_lines': 2,
                'fade_duration': 0.3
            }
        }
    
    def _create_ticker_theme(self) -> Dict[str, Any]:
        """뉴스 자막형 테마 생성"""
        return {
            'theme': {
                'name': '뉴스 자막형',
                'description': '화면 하단 배너 형태',
                'renderer': 'TickerRenderer'
            },
            'window': {
                'width': 1200,
                'height': 80,
                'position': 'bottom',
                'opacity': 0.95,
                'always_on_top': True,
                'click_through': False
            },
            'background': {
                'color': '#0066CC',
                'opacity': 0.8,
                'border_radius': 0
            },
            'layout': {
                'type': 'horizontal',
                'padding': 15,
                'spacing': 20,
                'scroll': False
            },
            'caption': {
                'korean': {
                    'font_family': '맑은 고딕',
                    'font_size': 22,
                    'font_weight': 'bold',
                    'color': '#FFFFFF',
                    'alignment': 'left'
                },
                'english': {
                    'font_family': 'Arial',
                    'font_size': 20,
                    'font_weight': 'normal',
                    'color': '#FFFF00',
                    'alignment': 'left'
                },
                'max_lines': 1,
                'fade_duration': 0.2
            }
        }
