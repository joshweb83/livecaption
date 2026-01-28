"""
Implementations Module
STT 및 번역 구현체 모듈
"""

from services.model_factory import ModelFactory
from implementations.whisper_stt import WhisperLightSTT, WhisperStandardSTT
from implementations.opus_translation import OpusMTTranslationService


# STT 구현체 등록
ModelFactory.register_stt('whisper_light', WhisperLightSTT)
ModelFactory.register_stt('whisper_standard', WhisperStandardSTT)

# 번역 구현체 등록
ModelFactory.register_translation('opus_mt', OpusMTTranslationService)


__all__ = [
    'WhisperLightSTT',
    'WhisperStandardSTT',
    'OpusMTTranslationService',
    'ModelFactory'
]
