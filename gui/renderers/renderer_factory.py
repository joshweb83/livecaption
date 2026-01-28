"""
Renderer Factory
렌더러 팩토리
"""

from typing import Dict, Any, Type
from gui.renderers.base_renderer import BaseRenderer
from gui.renderers.panel_renderer import PanelRenderer
from gui.renderers.transparent_renderer import TransparentRenderer
from gui.renderers.ticker_renderer import TickerRenderer


class RendererFactory:
    """렌더러 팩토리"""
    
    _renderers: Dict[str, Type[BaseRenderer]] = {
        'PanelRenderer': PanelRenderer,
        'TransparentRenderer': TransparentRenderer,
        'TickerRenderer': TickerRenderer
    }
    
    @classmethod
    def register_renderer(cls, name: str, renderer_class: Type[BaseRenderer]):
        """
        렌더러 등록
        
        Args:
            name: 렌더러 이름
            renderer_class: 렌더러 클래스
        """
        cls._renderers[name] = renderer_class
    
    @classmethod
    def create_renderer(cls, theme_config: Dict[str, Any]) -> BaseRenderer:
        """
        테마 설정을 기반으로 렌더러 생성
        
        Args:
            theme_config: 테마 설정
            
        Returns:
            BaseRenderer: 렌더러 인스턴스
            
        Raises:
            ValueError: 렌더러를 찾을 수 없는 경우
        """
        renderer_name = theme_config.get('theme', {}).get('renderer', 'PanelRenderer')
        
        if renderer_name not in cls._renderers:
            raise ValueError(f"렌더러를 찾을 수 없습니다: {renderer_name}")
        
        renderer_class = cls._renderers[renderer_name]
        return renderer_class(theme_config)
    
    @classmethod
    def list_renderers(cls) -> list:
        """
        등록된 렌더러 목록
        
        Returns:
            list: 렌더러 이름 리스트
        """
        return list(cls._renderers.keys())
