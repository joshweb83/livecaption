"""
Model Downloader
AI 모델 자동 다운로드 및 캐시 관리
"""

from pathlib import Path
from typing import Dict, Any, Optional, Callable
import os


class ModelDownloader:
    """모델 다운로더 클래스"""
    
    def __init__(self, cache_dir: str = "models"):
        """
        Args:
            cache_dir: 모델 캐시 디렉토리
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def download_whisper_model(
        self,
        model_size: str = "small",
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Whisper 모델 다운로드
        
        Args:
            model_size: 모델 크기 (small, large-v3-turbo)
            progress_callback: 진행 상황 콜백 함수
            
        Returns:
            bool: 다운로드 성공 여부
        """
        try:
            if progress_callback:
                progress_callback(f"Whisper {model_size} 모델 다운로드 중...")
            
            from faster_whisper import WhisperModel
            
            # 모델 로드 (자동 다운로드)
            whisper_cache = self.cache_dir / "whisper"
            whisper_cache.mkdir(parents=True, exist_ok=True)
            
            model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8",
                download_root=str(whisper_cache)
            )
            
            # 메모리 해제
            del model
            
            if progress_callback:
                progress_callback(f"✅ Whisper {model_size} 모델 다운로드 완료")
            
            return True
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ Whisper 모델 다운로드 실패: {e}")
            return False
    
    def download_translation_model(
        self,
        model_name: str = "Helsinki-NLP/opus-mt-ko-en",
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        번역 모델 다운로드
        
        Args:
            model_name: 모델 이름
            progress_callback: 진행 상황 콜백 함수
            
        Returns:
            bool: 다운로드 성공 여부
        """
        try:
            if progress_callback:
                progress_callback(f"번역 모델 다운로드 중...")
            
            from transformers import MarianMTModel, MarianTokenizer
            
            # 캐시 디렉토리
            translation_cache = self.cache_dir / "translation"
            translation_cache.mkdir(parents=True, exist_ok=True)
            
            # 토크나이저 다운로드
            tokenizer = MarianTokenizer.from_pretrained(
                model_name,
                cache_dir=str(translation_cache)
            )
            
            # 모델 다운로드
            model = MarianMTModel.from_pretrained(
                model_name,
                cache_dir=str(translation_cache)
            )
            
            # 메모리 해제
            del tokenizer
            del model
            
            if progress_callback:
                progress_callback(f"✅ 번역 모델 다운로드 완료")
            
            return True
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ 번역 모델 다운로드 실패: {e}")
            return False
    
    def download_all_models(
        self,
        profile: str = "light",
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        프로필에 따라 모든 필요한 모델 다운로드
        
        Args:
            profile: 성능 프로필 (light, standard)
            progress_callback: 진행 상황 콜백 함수
            
        Returns:
            bool: 다운로드 성공 여부
        """
        if progress_callback:
            progress_callback(f"=== {profile} 프로필 모델 다운로드 시작 ===")
        
        # Whisper 모델 크기 결정
        if profile == "light":
            whisper_size = "small"
        elif profile == "standard":
            whisper_size = "large-v3-turbo"
        else:
            whisper_size = "small"
        
        # Whisper 다운로드
        success1 = self.download_whisper_model(whisper_size, progress_callback)
        
        # 번역 모델 다운로드
        success2 = self.download_translation_model(
            "Helsinki-NLP/opus-mt-ko-en",
            progress_callback
        )
        
        if progress_callback:
            if success1 and success2:
                progress_callback("=== 모든 모델 다운로드 완료 ===")
            else:
                progress_callback("=== 일부 모델 다운로드 실패 ===")
        
        return success1 and success2
    
    def check_models_exist(self, profile: str = "light") -> Dict[str, bool]:
        """
        모델 존재 여부 확인
        
        Args:
            profile: 성능 프로필
            
        Returns:
            Dict: 모델별 존재 여부
        """
        whisper_cache = self.cache_dir / "whisper"
        translation_cache = self.cache_dir / "translation"
        
        # Whisper 모델 크기
        if profile == "light":
            whisper_size = "small"
        else:
            whisper_size = "large-v3-turbo"
        
        return {
            'whisper': whisper_cache.exists() and len(list(whisper_cache.glob("*"))) > 0,
            'translation': translation_cache.exists() and len(list(translation_cache.glob("*"))) > 0
        }
    
    def get_cache_size(self) -> Dict[str, float]:
        """
        캐시 크기 확인 (MB)
        
        Returns:
            Dict: 모델별 캐시 크기
        """
        def get_dir_size(path: Path) -> float:
            """디렉토리 크기 계산 (MB)"""
            if not path.exists():
                return 0.0
            total = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            return total / (1024 * 1024)  # MB
        
        whisper_cache = self.cache_dir / "whisper"
        translation_cache = self.cache_dir / "translation"
        
        return {
            'whisper': get_dir_size(whisper_cache),
            'translation': get_dir_size(translation_cache),
            'total': get_dir_size(self.cache_dir)
        }
    
    def clear_cache(self, model_type: Optional[str] = None):
        """
        캐시 삭제
        
        Args:
            model_type: 모델 타입 (whisper, translation, None=전체)
        """
        import shutil
        
        if model_type == "whisper":
            cache_path = self.cache_dir / "whisper"
            if cache_path.exists():
                shutil.rmtree(cache_path)
        elif model_type == "translation":
            cache_path = self.cache_dir / "translation"
            if cache_path.exists():
                shutil.rmtree(cache_path)
        else:
            # 전체 캐시 삭제
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
