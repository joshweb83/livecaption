# Live Caption - Windows 실행 파일 빌드 가이드

**Version**: 1.0.1  
**Last Updated**: 2026-01-28

---

## 📋 목차

1. [사전 요구사항](#사전-요구사항)
2. [방법 1: 자동 빌드 (권장)](#방법-1-자동-빌드-권장)
3. [방법 2: 수동 빌드](#방법-2-수동-빌드)
4. [빌드 결과물](#빌드-결과물)
5. [문제 해결](#문제-해결)

---

## 사전 요구사항

### 1. Python 3.11 설치

**다운로드**: https://www.python.org/downloads/

**설치 시 주의사항**:
- ✅ **"Add Python to PATH"** 반드시 체크!
- ✅ **"Install for all users"** 권장

**설치 확인**:
```cmd
python --version
```
출력: `Python 3.11.x`

### 2. Git 설치 (선택사항)

**다운로드**: https://git-scm.com/download/win

### 3. 하드웨어 요구사항

- **CPU**: Intel i5 이상
- **RAM**: 8GB 이상
- **저장공간**: 5GB 이상 (빌드 과정 중 임시 파일 포함)
- **OS**: Windows 10/11 (64-bit)

---

## 방법 1: 자동 빌드 (권장) ⭐

### 1단계: 코드 다운로드

#### Option A: GitHub에서 다운로드
```cmd
git clone https://github.com/joshweb83/livecaption.git
cd livecaption
```

#### Option B: ZIP 파일 다운로드
1. https://github.com/joshweb83/livecaption 접속
2. "Code" → "Download ZIP" 클릭
3. 압축 해제 후 폴더로 이동

### 2단계: 자동 빌드 실행

**`build.bat` 파일을 더블클릭**하거나, 명령 프롬프트에서:

```cmd
cd livecaption
build.bat
```

### 3단계: 빌드 완료 대기

빌드 과정:
1. ✅ 의존성 설치 (약 5분)
2. ✅ PyInstaller 설치
3. ✅ 실행 파일 빌드 (약 10분)
4. ✅ 완료!

### 4단계: 실행 파일 확인

```
dist/LiveCaption.exe  ← 이 파일이 최종 실행 파일입니다!
```

---

## 방법 2: 수동 빌드

### 1단계: 명령 프롬프트 열기

- `Win + R` → `cmd` 입력 → Enter
- 또는 프로젝트 폴더에서 주소창에 `cmd` 입력

### 2단계: 프로젝트 폴더로 이동

```cmd
cd C:\경로\livecaption
```

### 3단계: 의존성 설치

```cmd
pip install -r requirements.txt
```

**설치되는 패키지**:
- PyQt5 (GUI)
- faster-whisper (음성 인식)
- transformers (번역)
- torch (AI 모델)
- 기타 의존성

**예상 시간**: 5-10분

### 4단계: PyInstaller 설치

```cmd
pip install pyinstaller
```

### 5단계: 빌드 실행

```cmd
pyinstaller LiveCaption.spec
```

**빌드 과정**:
- 의존성 분석
- 파일 수집
- 실행 파일 생성
- UPX 압축 (선택사항)

**예상 시간**: 10-15분

### 6단계: 완료!

```
dist/LiveCaption.exe
```

---

## 빌드 결과물

### 디렉토리 구조

```
livecaption/
├── dist/
│   └── LiveCaption.exe       ← 최종 실행 파일 (약 200MB)
├── build/                     ← 임시 빌드 파일 (삭제 가능)
└── LiveCaption.spec           ← PyInstaller 설정 파일
```

### 배포 파일 준비

**최소 배포 파일**:
```
LiveCaption-v1.0.1/
├── LiveCaption.exe            ← 필수
├── config.yaml                ← 자동 생성됨 (선택사항)
└── README.md                  ← 사용 설명서 (선택사항)
```

**사용자에게 전달**:
- `LiveCaption.exe` 파일만 전달하면 됩니다!
- 첫 실행 시 AI 모델 자동 다운로드 (약 550MB)

---

## 문제 해결

### 문제 1: "python is not recognized"

**원인**: Python이 PATH에 추가되지 않음

**해결**:
1. Python 재설치 ("Add Python to PATH" 체크)
2. 또는 수동으로 PATH 추가:
   - 시스템 환경 변수 → Path 편집
   - `C:\Users\사용자명\AppData\Local\Programs\Python\Python311` 추가

### 문제 2: "pip install" 실패

**원인**: 네트워크 문제 또는 권한 부족

**해결**:
```cmd
# 관리자 권한으로 명령 프롬프트 실행
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### 문제 3: PyInstaller 빌드 실패

**원인**: 의존성 누락 또는 충돌

**해결**:
```cmd
# 가상 환경 사용 (권장)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller LiveCaption.spec
```

### 문제 4: 실행 파일이 너무 큼 (1GB 이상)

**원인**: 불필요한 의존성 포함

**해결**:
- `LiveCaption.spec` 파일에서 `excludes` 목록 확인
- UPX 압축 활성화 (이미 설정됨)

### 문제 5: 백신 프로그램이 차단

**원인**: PyInstaller로 만든 실행 파일의 일반적인 오탐지

**해결**:
- 백신 프로그램 예외 목록에 추가
- 또는 일시적으로 백신 비활성화 후 빌드

### 문제 6: 실행 시 "DLL not found" 오류

**원인**: Visual C++ 재배포 패키지 누락

**해결**:
- Visual C++ Redistributable 설치
- https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## 고급 옵션

### 빌드 최적화

**더 작은 실행 파일**:
```cmd
# spec 파일에서 수정
excludes=['matplotlib', 'scipy', 'numpy.tests']
```

**디버그 모드**:
```cmd
pyinstaller LiveCaption.spec --debug all
```

### 아이콘 변경

1. `.ico` 파일 준비 (256x256 권장)
2. `LiveCaption.spec` 파일 수정:
```python
icon='path/to/icon.ico'
```

### 단일 파일 vs 폴더

**현재 설정**: 단일 파일 (`onefile=True`)

**폴더 모드로 변경** (더 빠른 실행):
```python
# LiveCaption.spec
a = Analysis(...)
exe = EXE(
    pyz,
    a.scripts,
    # onefile=False로 변경
    exclude_binaries=True,  # 추가
    ...
)
coll = COLLECT(...)  # 추가
```

---

## 자동 빌드 (GitHub Actions)

### CI/CD 파이프라인 설정

`.github/workflows/build.yml` 파일 생성:

```yaml
name: Build Windows EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build EXE
        run: pyinstaller LiveCaption.spec
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: LiveCaption-Windows
          path: dist/LiveCaption.exe
```

**사용법**:
```cmd
git tag v1.0.1
git push origin v1.0.1
```

자동으로 빌드되어 GitHub Actions Artifacts에 업로드됩니다!

---

## 배포 체크리스트

빌드 후 확인사항:

- [ ] `LiveCaption.exe` 파일 생성 확인
- [ ] 파일 크기 확인 (200MB ~ 1GB)
- [ ] 실행 테스트 (더블클릭)
- [ ] 설정 창 열림 확인
- [ ] 마이크 입력 테스트
- [ ] 자막 표시 테스트
- [ ] 테마 변경 테스트
- [ ] 시스템 트레이 작동 확인

---

## 추가 리소스

- **PyInstaller 공식 문서**: https://pyinstaller.org/
- **Python 공식 사이트**: https://www.python.org/
- **프로젝트 GitHub**: https://github.com/joshweb83/livecaption
- **이슈 리포트**: https://github.com/joshweb83/livecaption/issues

---

**빌드 성공을 기원합니다! 🚀**

문제가 발생하면 GitHub Issues에 보고해주세요.
