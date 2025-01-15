from abc import ABC, abstractmethod
from typing import List, Dict, Optional, BinaryIO

class TTSPlatform(ABC):
    """TTS平台的基础抽象类"""
    
    @abstractmethod
    def get_characters(self) -> List[Dict]:
        """获取所有可用的语音角色"""
        pass
    
    @abstractmethod
    def generate(self, text: str, voice_id: int, **kwargs) -> bytes:
        """生成语音文件"""
        pass

class TTSManager:
    """TTS平台管理器"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TTSManager, cls).__new__(cls)
            cls._instance._platforms = {}
        return cls._instance
    
    def register_platform(self, name: str, platform: TTSPlatform):
        """注册TTS平台"""
        self._platforms[name] = platform
        
    def get_platform(self, name: str) -> Optional[TTSPlatform]:
        """获取指定的TTS平台"""
        return self._platforms.get(name)
    
    def list_platforms(self) -> List[str]:
        """列出所有已注册的平台"""
        return list(self._platforms.keys()) 