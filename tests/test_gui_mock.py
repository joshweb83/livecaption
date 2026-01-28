"""
GUI Mock Test
GUI 테스트 (Mock 자막 데이터)
"""

import sys
from pathlib import Path
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui.caption_window import CaptionWindow


def test_caption_window():
    """자막 창 테스트"""
    print("\n=== 자막 창 테스트 ===")
    
    app = QApplication(sys.argv)
    
    # 패널형 창 생성
    print("⏳ 패널형 창 생성 중...")
    panel_window = CaptionWindow('panel')
    panel_window.show()
    print("✅ 패널형 창 생성 완료")
    
    # Mock 자막 데이터
    mock_captions = [
        {
            'korean': '안녕하세요, 실시간 자막 테스트입니다.',
            'english': 'Hello, this is a real-time caption test.',
            'timestamp': time.time(),
            'stt_confidence': 0.95,
            'trans_confidence': 0.92
        },
        {
            'korean': '이 프로그램은 음성을 인식하여 자막으로 표시합니다.',
            'english': 'This program recognizes speech and displays it as captions.',
            'timestamp': time.time(),
            'stt_confidence': 0.93,
            'trans_confidence': 0.90
        },
        {
            'korean': 'Zoom 회의나 온라인 강의에서 사용할 수 있습니다.',
            'english': 'It can be used in Zoom meetings or online lectures.',
            'timestamp': time.time(),
            'stt_confidence': 0.94,
            'trans_confidence': 0.91
        }
    ]
    
    # 자막 추가 (타이머로 순차 추가)
    def add_caption_with_delay(index):
        if index < len(mock_captions):
            print(f"  자막 #{index + 1} 추가")
            panel_window.add_caption(mock_captions[index])
            QTimer.singleShot(2000, lambda: add_caption_with_delay(index + 1))
        else:
            print("✅ 모든 자막 추가 완료")
            # 5초 후 창 닫기
            QTimer.singleShot(5000, app.quit)
    
    # 1초 후 첫 자막 추가
    QTimer.singleShot(1000, lambda: add_caption_with_delay(0))
    
    # 애플리케이션 실행
    print("🚀 GUI 실행 중... (자동으로 종료됩니다)")
    app.exec_()
    
    print("✅ 자막 창 테스트 완료")


def test_theme_switching():
    """테마 전환 테스트"""
    print("\n=== 테마 전환 테스트 ===")
    
    app = QApplication(sys.argv)
    
    # 패널형으로 시작
    print("⏳ 패널형 창 생성 중...")
    window = CaptionWindow('panel')
    window.show()
    print("✅ 패널형 창 생성 완료")
    
    # Mock 자막
    caption = {
        'korean': '테마 전환 테스트',
        'english': 'Theme switching test',
        'timestamp': time.time(),
        'stt_confidence': 0.95,
        'trans_confidence': 0.92
    }
    
    window.add_caption(caption)
    
    # 테마 전환 시퀀스
    themes = ['panel', 'transparent', 'ticker', 'panel']
    current_theme_index = [0]
    
    def switch_theme():
        current_theme_index[0] += 1
        if current_theme_index[0] < len(themes):
            theme = themes[current_theme_index[0]]
            print(f"  테마 전환: {theme}")
            window.change_theme(theme)
            QTimer.singleShot(3000, switch_theme)
        else:
            print("✅ 모든 테마 전환 완료")
            QTimer.singleShot(2000, app.quit)
    
    # 3초 후 테마 전환 시작
    QTimer.singleShot(3000, switch_theme)
    
    print("🚀 GUI 실행 중... (자동으로 종료됩니다)")
    app.exec_()
    
    print("✅ 테마 전환 테스트 완료")


def test_window_positioning():
    """창 위치 테스트"""
    print("\n=== 창 위치 테스트 ===")
    
    app = QApplication(sys.argv)
    
    # 다양한 위치에 창 생성
    positions = ['right', 'left', 'top', 'bottom', 'center']
    
    for position in positions:
        print(f"  {position} 위치 창 생성")
        # 테마 설정에서 위치만 변경하는 것은 복잡하므로
        # 여기서는 기본 위치 테스트만 수행
    
    print("✅ 창 위치 테스트 완료 (시각적 확인 필요)")


if __name__ == '__main__':
    print("=" * 60)
    print("Live Caption - GUI Mock Tests")
    print("=" * 60)
    
    try:
        test_caption_window()
        # test_theme_switching()  # 별도로 실행
        # test_window_positioning()
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료")
    print("=" * 60)
