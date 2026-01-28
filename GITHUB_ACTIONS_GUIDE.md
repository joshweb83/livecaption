# GitHub Actions로 자동 EXE 빌드하기

**Version**: 1.0.1  
**Last Updated**: 2026-01-28

---

## 📋 개요

GitHub Actions를 사용하면 **로컬 PC 없이** GitHub 클라우드에서 자동으로 Windows 실행 파일을 빌드할 수 있습니다.

### 장점
- ✅ **Windows PC 불필요** - GitHub 클라우드에서 빌드
- ✅ **자동화** - 태그 푸시 시 자동 빌드
- ✅ **무료** - Public 저장소는 무료
- ✅ **릴리스 자동 생성** - EXE 파일 자동 첨부

---

## 🚀 사용 방법

### 방법 1: 태그로 자동 빌드 (권장) ⭐

#### 1단계: 버전 태그 생성

로컬 PC 또는 GitHub 웹에서:

```bash
# 로컬에서
git tag v1.0.1
git push origin v1.0.1
```

또는 **GitHub 웹에서**:
1. https://github.com/joshweb83/livecaption 접속
2. "Releases" → "Create a new release" 클릭
3. "Choose a tag" → `v1.0.1` 입력 (새 태그 생성)
4. "Publish release" 클릭

#### 2단계: 자동 빌드 시작

- 태그가 푸시되면 **자동으로 빌드 시작**
- "Actions" 탭에서 진행 상황 확인
- 약 **10-15분** 소요

#### 3단계: EXE 다운로드

- 빌드 완료 후 "Releases" 탭으로 이동
- 새로 생성된 릴리스에서 **`LiveCaption.exe`** 다운로드

---

### 방법 2: 수동 빌드

GitHub 웹에서 수동으로 빌드를 트리거할 수 있습니다.

#### 1단계: Actions 탭 접속

https://github.com/joshweb83/livecaption/actions

#### 2단계: 워크플로우 선택

- "Build Windows EXE" 워크플로우 클릭

#### 3단계: 수동 실행

- "Run workflow" 버튼 클릭
- 브랜치 선택 (main)
- "Run workflow" 확인

#### 4단계: Artifact 다운로드

- 빌드 완료 후 워크플로우 실행 결과 클릭
- "Artifacts" 섹션에서 **`LiveCaption-dev-xxxxx`** 다운로드
- ZIP 파일 압축 해제하여 EXE 파일 확인

---

## 📊 빌드 프로세스

### 자동화 단계

1. **코드 체크아웃** - 최신 코드 가져오기
2. **Python 설치** - Python 3.11 설치
3. **의존성 설치** - requirements.txt 패키지 설치
4. **PyInstaller 설치** - 빌드 도구 설치
5. **EXE 빌드** - LiveCaption.spec 실행
6. **릴리스 생성** - GitHub Release에 EXE 첨부

### 예상 시간

| 단계 | 시간 |
|------|------|
| 코드 체크아웃 | 10초 |
| Python 설치 | 30초 |
| 의존성 설치 | 5분 |
| PyInstaller 설치 | 30초 |
| EXE 빌드 | 10분 |
| **총 소요 시간** | **약 15분** |

---

## 🔍 빌드 상태 확인

### Actions 탭에서 확인

1. https://github.com/joshweb83/livecaption/actions 접속
2. 최신 워크플로우 실행 클릭
3. 각 단계별 로그 확인

### 빌드 상태 배지

README.md에 추가하여 빌드 상태 표시:

```markdown
![Build Status](https://github.com/joshweb83/livecaption/actions/workflows/build-windows.yml/badge.svg)
```

---

## 📦 릴리스 관리

### 버전 관리 규칙

**Semantic Versioning** 사용:
- `v1.0.0` - 메이저 버전 (큰 변경)
- `v1.1.0` - 마이너 버전 (기능 추가)
- `v1.0.1` - 패치 버전 (버그 수정)

### 릴리스 생성 예시

```bash
# 버그 수정
git tag v1.0.2
git push origin v1.0.2

# 기능 추가
git tag v1.1.0
git push origin v1.1.0

# 메이저 업데이트
git tag v2.0.0
git push origin v2.0.0
```

---

## 🛠️ 워크플로우 설정

### 파일 위치

`.github/workflows/build-windows.yml`

### 트리거 조건

```yaml
on:
  push:
    tags:
      - 'v*'  # v로 시작하는 모든 태그
  workflow_dispatch:  # 수동 실행 가능
```

### 빌드 환경

- **OS**: Windows Server 2022 (latest)
- **Python**: 3.11
- **Runner**: GitHub-hosted

---

## 💡 고급 설정

### 1. 빌드 최적화

캐싱을 사용하여 빌드 시간 단축:

```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~\AppData\Local\pip\Cache
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 2. 멀티 플랫폼 빌드

Windows, macOS, Linux 동시 빌드:

```yaml
strategy:
  matrix:
    os: [windows-latest, macos-latest, ubuntu-latest]
runs-on: ${{ matrix.os }}
```

### 3. 자동 테스트 추가

빌드 전 테스트 실행:

```yaml
- name: Run tests
  run: |
    pip install pytest
    pytest tests/
```

### 4. 코드 서명

Windows 실행 파일에 디지털 서명:

```yaml
- name: Sign executable
  run: |
    signtool sign /f certificate.pfx /p ${{ secrets.CERT_PASSWORD }} dist/LiveCaption.exe
```

---

## 🔒 보안

### Secrets 관리

민감한 정보는 GitHub Secrets에 저장:

1. 저장소 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 이름과 값 입력

### 사용 예시

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

---

## 📊 비용

### GitHub Actions 무료 한도

| 계정 유형 | 월간 무료 시간 |
|-----------|----------------|
| Public 저장소 | **무제한** ✅ |
| Private 저장소 (Free) | 2,000분 |
| Private 저장소 (Pro) | 3,000분 |

**현재 프로젝트**: Public 저장소 → **무료 무제한** 🎉

---

## 🐛 문제 해결

### 빌드 실패

#### 1. 의존성 설치 실패

**원인**: requirements.txt 오류

**해결**:
```yaml
- name: Install dependencies
  run: |
    pip install --no-cache-dir -r requirements.txt
```

#### 2. PyInstaller 빌드 실패

**원인**: spec 파일 오류

**해결**:
- 로컬에서 먼저 테스트
- 로그 확인하여 누락된 모듈 추가

#### 3. 릴리스 생성 실패

**원인**: GITHUB_TOKEN 권한 부족

**해결**:
1. 저장소 Settings → Actions → General
2. "Workflow permissions" → "Read and write permissions" 선택

### 로그 확인

Actions 탭 → 실패한 워크플로우 → 빨간색 단계 클릭

---

## 📚 추가 리소스

- **GitHub Actions 공식 문서**: https://docs.github.com/en/actions
- **PyInstaller 문서**: https://pyinstaller.org/
- **워크플로우 예시**: https://github.com/actions/starter-workflows

---

## 🎯 빠른 참조

### 새 버전 릴리스

```bash
# 1. 코드 수정 및 커밋
git add .
git commit -m "Fix: 버그 수정"

# 2. 태그 생성
git tag v1.0.2

# 3. 푸시 (자동 빌드 시작)
git push origin main
git push origin v1.0.2

# 4. 10-15분 후 Releases에서 EXE 다운로드
```

### 수동 빌드

1. https://github.com/joshweb83/livecaption/actions
2. "Build Windows EXE" → "Run workflow"
3. Artifacts에서 다운로드

---

## ✅ 체크리스트

릴리스 전:
- [ ] 코드 테스트 완료
- [ ] 버전 번호 결정 (Semantic Versioning)
- [ ] CHANGELOG 업데이트
- [ ] README 업데이트

릴리스 후:
- [ ] Actions 탭에서 빌드 성공 확인
- [ ] Releases에서 EXE 다운로드 테스트
- [ ] 실행 파일 테스트
- [ ] 릴리스 노트 작성

---

**GitHub Actions로 손쉽게 EXE 파일을 빌드하세요! 🚀**

문제가 발생하면 Actions 탭의 로그를 확인하거나 GitHub Issues에 보고해주세요.
