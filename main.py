"""
Live Caption - Main Entry Point
실시간 AI 자막 프로그램

Author: Manus AI
Version: 1.0.0
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from gui.app import LiveCaptionApp


def main():
    """메인 함수"""
    # 커맨드 라인 인자 파싱
    parser = argparse.ArgumentParser(
        description='Live Caption - 실시간 AI 음성 인식 및 번역 자막 프로그램'
    )
    
    parser.add_argument(
        '--theme',
        type=str,
        default='panel',
        choices=['panel', 'transparent', 'ticker'],
        help='자막 테마 (기본값: panel)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='설정 파일 경로 (기본값: config.yaml)'
    )
    
    parser.add_argument(
        '--device',
        type=int,
        default=None,
        help='오디오 디바이스 인덱스'
    )
    
    parser.add_argument(
        '--list-devices',
        action='store_true',
        help='사용 가능한 오디오 디바이스 목록 표시'
    )
    
    parser.add_argument(
        '--no-auto-start',
        action='store_true',
        help='자동 시작 비활성화 (GUI만 표시)'
    )
    
    args = parser.parse_args()
    
    # 애플리케이션 생성
    app = LiveCaptionApp(
        config_path=args.config,
        theme_name=args.theme
    )
    
    # 디바이스 목록 표시
    if args.list_devices:
        print("=== 사용 가능한 오디오 디바이스 ===")
        devices = app.list_audio_devices()
        for device in devices:
            print(f"  [{device['index']}] {device['name']}")
            print(f"      채널: {device['channels']}, 샘플레이트: {device['sample_rate']}Hz")
        print()
        return 0
    
    # 초기화
    if not app.initialize():
        print("❌ 초기화 실패")
        return 1
    
    # 자동 시작
    if not args.no_auto_start:
        if not app.start(device_index=args.device):
            print("❌ 시작 실패")
            return 1
    
    # 애플리케이션 실행
    return app.run()


if __name__ == '__main__':
    sys.exit(main())
