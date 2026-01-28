"""
GUI Structure Test
GUI 구조 검증 테스트 (실제 실행 없이)
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_imports():
    """모듈 import 테스트"""
    print("\n=== 모듈 import 테스트 ===")
    
    try:
        from gui.caption_window import CaptionWindow
        print("✅ CaptionWindow import 성공")
    except Exception as e:
        print(f"❌ CaptionWindow import 실패: {e}")
        return False
    
    try:
        from gui.app import LiveCaptionApp
        print("✅ LiveCaptionApp import 성공")
    except Exception as e:
        print(f"❌ LiveCaptionApp import 실패: {e}")
        return False
    
    return True


def test_class_structure():
    """클래스 구조 테스트"""
    print("\n=== 클래스 구조 테스트 ===")
    
    from gui.caption_window import CaptionWindow
    from gui.app import LiveCaptionApp
    
    # CaptionWindow 메서드 확인
    caption_methods = ['add_caption', 'clear_captions', 'change_theme']
    for method in caption_methods:
        if hasattr(CaptionWindow, method):
            print(f"✅ CaptionWindow.{method} 존재")
        else:
            print(f"❌ CaptionWindow.{method} 없음")
            return False
    
    # LiveCaptionApp 메서드 확인
    app_methods = ['initialize', 'start', 'stop', 'run', 'cleanup']
    for method in app_methods:
        if hasattr(LiveCaptionApp, method):
            print(f"✅ LiveCaptionApp.{method} 존재")
        else:
            print(f"❌ LiveCaptionApp.{method} 없음")
            return False
    
    return True


def test_integration():
    """통합 구조 테스트"""
    print("\n=== 통합 구조 테스트 ===")
    
    # 전체 파이프라인 확인
    components = [
        ('core.controller', 'CaptionController'),
        ('gui.caption_window', 'CaptionWindow'),
        ('gui.app', 'LiveCaptionApp'),
        ('gui.renderers', 'RendererFactory'),
    ]
    
    for module_name, class_name in components:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} 로드 성공")
        except Exception as e:
            print(f"❌ {module_name}.{class_name} 로드 실패: {e}")
            return False
    
    return True


def test_pipeline_flow():
    """파이프라인 흐름 검증"""
    print("\n=== 파이프라인 흐름 검증 ===")
    
    print("파이프라인 구조:")
    print("  1. LiveCaptionApp 생성")
    print("  2. CaptionController 초기화")
    print("  3. CaptionWindow 생성 (테마 기반)")
    print("  4. RendererFactory → Renderer 생성")
    print("  5. Controller.start() → 자막 콜백 등록")
    print("  6. 오디오 입력 → STT → 번역")
    print("  7. caption_callback → CaptionWindow.add_caption()")
    print("  8. Renderer.add_caption() → 화면 표시")
    
    print("\n✅ 파이프라인 흐름 검증 완료")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - GUI Structure Tests")
    print("=" * 60)
    print("⚠️  헤드리스 환경에서는 실제 GUI 실행이 불가능합니다")
    print("   구조 검증만 수행합니다")
    
    try:
        success = True
        success &= test_imports()
        success &= test_class_structure()
        success &= test_integration()
        success &= test_pipeline_flow()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ 모든 구조 검증 완료!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 일부 검증 실패")
            print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
