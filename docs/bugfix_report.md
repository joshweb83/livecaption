# 버그 수정 보고서

**Date**: 2026-01-28  
**Bug ID**: #001  
**Severity**: Critical (프로그램 실행 불가)

---

## 문제 설명

### 증상
Windows에서 빌드된 `.exe` 파일 실행 시 다음 오류 발생:

```
Failed to execute script 'main' due to unhandled exception: 
ConfigManager.__new__() takes 1 positional argument but 2 were given

TypeError: ConfigManager.__new__() takes 1 positional argument but 2 were given
```

### 원인
`ConfigManager` 클래스가 Singleton 패턴으로 구현되어 있는데, `__new__()` 메서드가 인자를 받지 않도록 설계되어 있었습니다. 하지만 `LiveCaptionApp`과 `CaptionController`에서 `ConfigManager(config_path)`와 같이 인자를 전달하려고 시도하여 오류가 발생했습니다.

**문제 코드:**
```python
# 기존 코드 (문제)
class ConfigManager:
    def __new__(cls):  # ← 인자를 받지 않음
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):  # ← 인자를 받지 않음
        if self._initialized:
            return
        # ...

# 호출 시 (app.py)
self.config_mgr = ConfigManager(config_path)  # ← 인자 전달 시도 → 에러!
```

---

## 해결 방법

`__new__()` 및 `__init__()` 메서드가 `config_path` 인자를 받을 수 있도록 수정했습니다.

**수정된 코드:**
```python
class ConfigManager:
    def __new__(cls, config_path: Optional[str] = None):  # ← 인자 추가
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_path: Optional[str] = None):  # ← 인자 추가
        if self._initialized:
            # 이미 초기화되었지만 config_path가 제공되면 로드
            if config_path and not self.config:
                self.load_config(config_path)
            return
        
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[Path] = None
        self._initialized = True
        
        # config_path가 제공되면 자동 로드
        if config_path:
            self.load_config(config_path)
```

---

## 테스트 결과

모든 테스트 통과:

```
✅ 테스트 1 통과: ConfigManager() - 인자 없이 생성
✅ 테스트 2 통과: ConfigManager(config_path) - 인자와 함께 생성
✅ 테스트 3 통과: Singleton 패턴 확인
✅ 테스트 4 통과: 설정 로드 확인 (키 개수: 7)
✅ 테스트 5 통과: 설정 값 가져오기 (profile: light)

모든 테스트 통과! ✅
```

---

## 영향 범위

### 수정된 파일
- `core/config_manager.py`

### 영향받는 모듈
- `gui/app.py` (LiveCaptionApp)
- `core/controller.py` (CaptionController)
- 기타 ConfigManager를 사용하는 모든 모듈

### 호환성
- **이전 버전과 호환**: `ConfigManager()` (인자 없이) 호출도 여전히 작동
- **새로운 사용법**: `ConfigManager(config_path)` (인자와 함께) 호출 가능

---

## 재발 방지

### 1. 단위 테스트 추가
`tests/test_config_manager.py` 파일에 다음 테스트 추가:
- Singleton 패턴 검증
- 인자 없이 생성 테스트
- 인자와 함께 생성 테스트
- 설정 로드 테스트

### 2. CI/CD 통합
GitHub Actions에 자동 테스트 추가하여 빌드 전에 모든 테스트 실행

### 3. 코드 리뷰
Singleton 패턴 사용 시 `__new__()` 메서드 시그니처 확인

---

## 배포

### 수정된 버전
- **Version**: 1.0.1 (버그 수정)
- **Release Date**: 2026-01-28

### 배포 파일
- `live_caption_fixed.zip` (수정된 소스 코드)

### 사용자 공지
- 기존 v1.0.0 사용자에게 업데이트 권장
- 버그 수정 내용 공지

---

**작성자**: PM Manus  
**상태**: ✅ 해결 완료
