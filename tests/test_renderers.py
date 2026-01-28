"""
Renderer Tests
렌더러 단위 테스트
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.theme_manager import ThemeManager
from gui.renderers import RendererFactory


def test_renderer_factory():
    """렌더러 팩토리 테스트"""
    print("\n=== 렌더러 팩토리 테스트 ===")
    
    # 등록된 렌더러 목록
    renderers = RendererFactory.list_renderers()
    print(f"✅ 등록된 렌더러: {renderers}")
    
    assert 'PanelRenderer' in renderers
    assert 'TransparentRenderer' in renderers
    assert 'TickerRenderer' in renderers
    
    print("✅ 렌더러 팩토리 테스트 통과")


def test_theme_to_renderer():
    """테마 → 렌더러 생성 테스트"""
    print("\n=== 테마 → 렌더러 생성 테스트 ===")
    
    theme_mgr = ThemeManager()
    theme_mgr.load_themes('themes')
    
    # 패널형 테마
    panel_theme = theme_mgr.get_theme('panel')
    panel_renderer = RendererFactory.create_renderer(panel_theme)
    print(f"✅ 패널형 렌더러 생성: {panel_renderer.__class__.__name__}")
    
    # 투명 오버레이 테마
    transparent_theme = theme_mgr.get_theme('transparent')
    transparent_renderer = RendererFactory.create_renderer(transparent_theme)
    print(f"✅ 투명 오버레이 렌더러 생성: {transparent_renderer.__class__.__name__}")
    
    # 뉴스 자막형 테마
    ticker_theme = theme_mgr.get_theme('ticker')
    ticker_renderer = RendererFactory.create_renderer(ticker_theme)
    print(f"✅ 뉴스 자막형 렌더러 생성: {ticker_renderer.__class__.__name__}")
    
    print("✅ 테마 → 렌더러 생성 테스트 통과")


def test_renderer_config():
    """렌더러 설정 테스트"""
    print("\n=== 렌더러 설정 테스트 ===")
    
    theme_mgr = ThemeManager()
    theme_mgr.load_themes('themes')
    
    # 패널형 테마 로드
    panel_theme = theme_mgr.get_theme('panel')
    panel_renderer = RendererFactory.create_renderer(panel_theme)
    
    # 창 설정
    window_config = panel_renderer.get_window_config()
    print(f"✅ 창 설정: {window_config}")
    assert window_config['width'] == 400
    assert window_config['height'] == 600
    assert window_config['position'] == 'right'
    
    # 자막 설정
    caption_config = panel_renderer.get_caption_config()
    print(f"✅ 자막 설정: {caption_config}")
    assert caption_config['max_lines'] == 10
    
    # 레이아웃 설정
    layout_config = panel_renderer.get_layout_config()
    print(f"✅ 레이아웃 설정: {layout_config}")
    assert layout_config['type'] == 'vertical'
    
    # 배경 설정
    bg_config = panel_renderer.get_background_config()
    print(f"✅ 배경 설정: {bg_config}")
    assert bg_config['opacity'] == 0.7
    
    print("✅ 렌더러 설정 테스트 통과")


def test_stylesheet_generation():
    """스타일시트 생성 테스트"""
    print("\n=== 스타일시트 생성 테스트 ===")
    
    theme_mgr = ThemeManager()
    theme_mgr.load_themes('themes')
    panel_theme = theme_mgr.get_theme('panel')
    panel_renderer = RendererFactory.create_renderer(panel_theme)
    
    # 스타일시트 생성
    stylesheet = panel_renderer.build_stylesheet()
    print(f"✅ 스타일시트 생성 완료 (길이: {len(stylesheet)})")
    
    # 스타일시트 내용 확인
    assert 'QWidget#CaptionWidget' in stylesheet
    assert 'QLabel#KoreanCaption' in stylesheet
    assert 'QLabel#EnglishCaption' in stylesheet
    
    print("✅ 스타일시트 생성 테스트 통과")


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - Renderer Tests")
    print("=" * 60)
    
    try:
        test_renderer_factory()
        test_theme_to_renderer()
        test_renderer_config()
        test_stylesheet_generation()
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료")
    print("=" * 60)
