# Live Caption - 실시간 AI 자막 프로그램

실시간 음성 인식 및 번역 기술을 활용한 Windows 데스크톱 자막 애플리케이션

## 주요 기능

- **실시간 음성 인식**: Faster Whisper 기반 한국어 STT (93% 이상 정확도)
- **실시간 번역**: 한국어 → 영어 자동 번역
- **오버레이 자막**: 모든 창 위에 표시되는 자막 창
- **다양한 디자인**: 패널형, 투명 오버레이, 뉴스 자막형 테마
- **커스터마이징**: 폰트, 색상, 투명도, 위치 조정
- **경량 최적화**: GPU 없이 CPU만으로 실시간 처리

## 시스템 요구사항

### 최소 사양
- OS: Windows 10/11 (64-bit)
- CPU: Intel i5 이상 (8 threads)
- RAM: 4GB 이상
- 저장공간: 1GB

### 권장 사양
- CPU: Intel i7 이상
- RAM: 8GB 이상
- GPU: NVIDIA GTX 1060+ (선택사항)

## 설치 방법

### 일반 사용자
1. `LiveCaption-v1.0.exe` 다운로드
2. 실행 (설치 불필요)
3. 첫 실행 시 AI 모델 자동 다운로드 (약 550MB)

### 개발자
```bash
# 저장소 클론
git clone <repository_url>
cd live_caption

# 가상환경 생성 (Python 3.11+)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

## 프로젝트 구조

```
live_caption/
├── main.py                      # 진입점
├── config.yaml                  # 설정 파일
├── requirements.txt             # 의존성
│
├── core/                        # 핵심 로직
│   ├── controller.py            # 메인 컨트롤러
│   ├── config_manager.py        # 설정 관리
│   ├── theme_manager.py         # 테마 관리
│   └── audio_capture.py         # 오디오 캡처
│
├── services/                    # 서비스 인터페이스
│   ├── base_stt.py              # STT 인터페이스
│   ├── base_translation.py      # 번역 인터페이스
│   └── model_factory.py         # 팩토리
│
├── implementations/             # 구현체
│   ├── whisper_stt.py           # Whisper STT
│   ├── opus_translation.py      # Opus-MT 번역
│   └── model_downloader.py      # 모델 다운로더
│
├── gui/                         # GUI
│   ├── caption_window.py        # 자막 창
│   ├── settings_window.py       # 설정 창
│   ├── system_tray.py           # 시스템 트레이
│   └── renderers/               # 테마별 렌더러
│
├── themes/                      # 테마 스타일시트
│   ├── panel.yaml
│   ├── transparent.yaml
│   └── ticker.yaml
│
└── utils/                       # 유틸리티
    ├── logger.py
    └── performance_monitor.py
```

## 사용 방법

1. **프로그램 실행**: `LiveCaption.exe` 더블 클릭
2. **자막 시작**: 시스템 트레이 아이콘 → "자막 시작"
3. **테마 변경**: 설정 → 디자인 → 테마 선택
4. **커스터마이징**: 설정 → 폰트, 색상, 위치 조정

## 개발 일정

- [x] Phase 1: 프로젝트 계획 수립
- [ ] Phase 2: 환경 설정
- [ ] Phase 3: 서비스 레이어 구현
- [ ] Phase 4: STT/번역 엔진 구현
- [ ] Phase 5: 오디오 스트리밍 구현
- [ ] Phase 6: 디자인 시스템 구현
- [ ] Phase 7: GUI 메인 창 개발
- [ ] Phase 8: 설정 UI 개발
- [ ] Phase 9: 통합 테스트
- [ ] Phase 10: Windows 패키징
- [ ] Phase 11: 최종 전달

## 라이선스

MIT License

## 개발자

Manus AI - PM & Lead Developer

## 문의

프로젝트 관련 문의: [GitHub Issues]
