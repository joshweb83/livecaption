"""
Live Caption - Main Entry Point
실시간 AI 자막 프로그램

Author: Manus AI
Version: 1.0.3
"""

import sys
import os
import argparse
import traceback
from pathlib import Path

# PyInstaller 환경에서 stdout/stderr 리다이렉션 문제 해결
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def show_error_dialog(title: str, message: str):
    """오류 대화상자 표시"""
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
    except Exception:
        # PyQt5가 없으면 콘솔에 출력
        print(f"ERROR: {title}\n{message}")


def main():
    """메인 함수"""
    try:
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
        
        # GUI 모듈 임포트
        from gui.app import LiveCaptionApp
        
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
            show_error_dialog("초기화 실패", "애플리케이션 초기화에 실패했습니다.")
            return 1
        
        # 자동 시작
        if not args.no_auto_start:
            if not app.start(device_index=args.device):
                show_error_dialog("시작 실패", "캡션 서비스 시작에 실패했습니다.")
                return 1
        
        # 애플리케이션 실행
        return app.run()
        
    except Exception as e:
        error_msg = f"오류 발생:\n{str(e)}\n\n상세:\n{traceback.format_exc()}"
        show_error_dialog("Live Caption 오류", error_msg)
        
        # 로그 파일에도 기록
        try:
            log_path = Path.home() / "LiveCaption_error.log"
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(error_msg)
        except Exception:
            pass
        
        return 1


if __name__ == '__main__':
    sys.exit(main())
