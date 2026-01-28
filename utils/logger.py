"""
Logger Utility
로깅 설정 및 유틸리티
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional


class Logger:
    """로거 클래스 (Singleton)"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.logger = logger
    
    def setup(
        self,
        level: str = "INFO",
        log_file: Optional[str] = None,
        max_size: str = "10MB",
        backup_count: int = 3
    ):
        """
        로거 설정
        
        Args:
            level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
            log_file: 로그 파일 경로
            max_size: 최대 파일 크기
            backup_count: 백업 파일 개수
        """
        # 기존 핸들러 제거
        self.logger.remove()
        
        # 콘솔 핸들러 추가
        self.logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=level,
            colorize=True
        )
        
        # 파일 핸들러 추가
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.add(
                log_file,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                level=level,
                rotation=max_size,
                retention=backup_count,
                compression="zip",
                encoding="utf-8"
            )
    
    def get_logger(self):
        """로거 인스턴스 반환"""
        return self.logger
    
    @staticmethod
    def debug(message: str):
        """디버그 로그"""
        logger.debug(message)
    
    @staticmethod
    def info(message: str):
        """정보 로그"""
        logger.info(message)
    
    @staticmethod
    def warning(message: str):
        """경고 로그"""
        logger.warning(message)
    
    @staticmethod
    def error(message: str):
        """에러 로그"""
        logger.error(message)
    
    @staticmethod
    def critical(message: str):
        """치명적 에러 로그"""
        logger.critical(message)


# 전역 로거 인스턴스
_logger_instance = Logger()


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 3
):
    """
    로거 설정 (전역 함수)
    
    Args:
        level: 로그 레벨
        log_file: 로그 파일 경로
        max_size: 최대 파일 크기
        backup_count: 백업 파일 개수
    """
    _logger_instance.setup(level, log_file, max_size, backup_count)


def get_logger():
    """로거 인스턴스 가져오기"""
    return _logger_instance.get_logger()
