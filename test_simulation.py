#!/usr/bin/env python3.11
"""
Live Caption Simulation Test
GUI 없이 설정, 테마, 파일 구조를 테스트합니다.
"""

import sys
import time
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).parent))

def test_config_loading():
    """설정 파일 로딩 테스트"""
    print("=" * 60)
    print("1. Config Loading Test")
    print("=" * 60)
    
    try:
        from core.config_manager import ConfigManager
        config_mgr = ConfigManager("config.yaml")
        
        # 기본 설정 확인
        profile = config_mgr.get('performance.profile')
        stt_model = config_mgr.get('stt.model')
        trans_model = config_mgr.get('translation.model')
        
        print(f"✅ Config loaded successfully")
        print(f"   Profile: {profile}")
        print(f"   STT Model: {stt_model}")
        print(f"   Translation Model: {trans_model}")
        
        # STT 설정 가져오기
        stt_config = config_mgr.get_stt_config()
        print(f"   STT Device: {stt_config.get('device')}")
        print(f"   STT Compute Type: {stt_config.get('compute_type')}")
        
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_theme_loading():
    """테마 파일 로딩 테스트"""
    print("\n" + "=" * 60)
    print("2. Theme Loading Test")
    print("=" * 60)
    
    try:
        import yaml
        themes_dir = Path(__file__).parent / 'themes'
        themes = ['panel', 'transparent', 'ticker']
        
        for theme_name in themes:
            theme_file = themes_dir / f"{theme_name}.yaml"
            if not theme_file.exists():
                print(f"❌ Theme file not found: {theme_file}")
                return False
            
            with open(theme_file, 'r', encoding='utf-8') as f:
                theme = yaml.safe_load(f)
            
            print(f"✅ Theme '{theme_name}' loaded")
            window_config = theme.get('window', {})
            print(f"   Window size: {window_config.get('width')}x{window_config.get('height')}")
            print(f"   Background: {window_config.get('background_color')}")
        
        return True
    except Exception as e:
        print(f"❌ Theme loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_renderer_loading():
    """렌더러 클래스 로딩 테스트"""
    print("\n" + "=" * 60)
    print("3. Renderer Loading Test")
    print("=" * 60)
    
    try:
        from gui.renderers.panel_renderer import PanelRenderer
        from gui.renderers.transparent_renderer import TransparentRenderer
        from gui.renderers.ticker_renderer import TickerRenderer
        from gui.renderers.renderer_factory import RendererFactory
        
        print(f"✅ PanelRenderer imported")
        print(f"✅ TransparentRenderer imported")
        print(f"✅ TickerRenderer imported")
        print(f"✅ RendererFactory imported")
        
        # Factory 패턴 테스트
        factory = RendererFactory()
        print(f"✅ RendererFactory instantiated")
        
        return True
    except Exception as e:
        print(f"❌ Renderer loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_service_imports():
    """서비스 클래스 임포트 테스트"""
    print("\n" + "=" * 60)
    print("4. Service Imports Test")
    print("=" * 60)
    
    try:
        # Base services
        from services.base_stt import BaseSTTService
        from services.base_translation import BaseTranslationService
        print(f"✅ Base service interfaces imported")
        
        # Implementations
        from implementations.whisper_stt import WhisperSTTService
        from implementations.opus_translation import OpusMTTranslationService
        from implementations.model_downloader import ModelDownloader
        print(f"✅ Service implementations imported")
        
        # Controller
        from core.controller import CaptionController
        print(f"✅ CaptionController imported")
        
        return True
    except Exception as e:
        print(f"❌ Service imports failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """파일 구조 확인"""
    print("\n" + "=" * 60)
    print("5. File Structure Test")
    print("=" * 60)
    
    required_files = [
        'config.yaml',
        'main.py',
        'LiveCaption.spec',
        'requirements.txt',
        'README.md',
        'themes/panel.yaml',
        'themes/transparent.yaml',
        'themes/ticker.yaml',
        'core/__init__.py',
        'core/controller.py',
        'core/config_manager.py',
        'services/__init__.py',
        'services/base_stt.py',
        'services/base_translation.py',
        'services/model_factory.py',
        'implementations/__init__.py',
        'implementations/whisper_stt.py',
        'implementations/opus_translation.py',
        'implementations/model_downloader.py',
        'gui/__init__.py',
        'gui/app.py',
        'gui/caption_window.py',
        'gui/settings_window.py',
        'gui/system_tray.py',
        'gui/renderers/__init__.py',
        'gui/renderers/base_renderer.py',
        'gui/renderers/panel_renderer.py',
        'gui/renderers/transparent_renderer.py',
        'gui/renderers/ticker_renderer.py',
        'gui/renderers/renderer_factory.py',
    ]
    
    all_exist = True
    missing_count = 0
    
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
            missing_count += 1
    
    if all_exist:
        print(f"\n✅ All {len(required_files)} files found")
    else:
        print(f"\n⚠️  {missing_count}/{len(required_files)} files missing")
    
    return all_exist

def test_config_profiles():
    """성능 프로필 설정 테스트"""
    print("\n" + "=" * 60)
    print("6. Performance Profiles Test")
    print("=" * 60)
    
    try:
        from core.config_manager import ConfigManager
        config_mgr = ConfigManager("config.yaml")
        
        # Lightweight 프로필
        print("\n📊 Lightweight Profile:")
        stt_config = config_mgr.get_stt_config('lightweight')
        trans_config = config_mgr.get_translation_config()
        
        print(f"   STT Model: {stt_config.get('model')}")
        print(f"   STT Device: {stt_config.get('device')}")
        print(f"   STT Compute: {stt_config.get('compute_type')}")
        print(f"   Translation Model: {trans_config.get('model')}")
        print(f"   Translation Device: {trans_config.get('device')}")
        
        # Standard 프로필
        print("\n📊 Standard Profile:")
        stt_config = config_mgr.get_stt_config('standard')
        trans_config = config_mgr.get_translation_config()
        
        print(f"   STT Model: {stt_config.get('model')}")
        print(f"   STT Device: {stt_config.get('device')}")
        print(f"   STT Compute: {stt_config.get('compute_type')}")
        print(f"   Translation Model: {trans_config.get('model')}")
        print(f"   Translation Device: {trans_config.get('device')}")
        
        print("\n✅ Both profiles configured correctly")
        return True
        
    except Exception as e:
        print(f"❌ Profile test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pyinstaller_spec():
    """PyInstaller spec 파일 검증"""
    print("\n" + "=" * 60)
    print("7. PyInstaller Spec Test")
    print("=" * 60)
    
    try:
        spec_file = Path(__file__).parent / 'LiveCaption.spec'
        
        if not spec_file.exists():
            print("❌ LiveCaption.spec not found")
            return False
        
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        # 필수 요소 확인
        checks = [
            ("main.py entry point", "'main.py'" in spec_content),
            ("config.yaml included", "'config.yaml'" in spec_content),
            ("themes directory included", "'themes'" in spec_content),
            ("PyQt5 hidden import", "'PyQt5'" in spec_content),
            ("faster_whisper import", "'faster_whisper'" in spec_content),
            ("transformers import", "'transformers'" in spec_content),
            ("Console disabled", "console=False" in spec_content),
            ("UPX compression", "upx=True" in spec_content),
        ]
        
        all_passed = True
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"{status} {check_name}")
            if not check_result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Spec file test failed: {e}")
        return False

def main():
    """메인 테스트 실행"""
    print("\n" + "=" * 60)
    print("Live Caption - Simulation Test")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {Path.cwd()}")
    print(f"Script Location: {Path(__file__).parent}")
    
    results = []
    
    # 테스트 실행
    results.append(("File Structure", test_file_structure()))
    results.append(("Config Loading", test_config_loading()))
    results.append(("Theme Loading", test_theme_loading()))
    results.append(("Renderer Loading", test_renderer_loading()))
    results.append(("Service Imports", test_service_imports()))
    results.append(("Config Profiles", test_config_profiles()))
    results.append(("PyInstaller Spec", test_pyinstaller_spec()))
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20s}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready for EXE build.")
        print("\n📦 Next steps:")
        print("   1. GitHub Actions will build the EXE automatically")
        print("   2. Check: https://github.com/joshweb83/livecaption/actions")
        print("   3. Download from: https://github.com/joshweb83/livecaption/releases")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix before building.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
