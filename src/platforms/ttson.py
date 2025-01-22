from typing import List, Dict, BinaryIO
from src.core.tts_manager import TTSPlatform
from src.utils.http_client import HTTPClient

class Ttson(TTSPlatform):
    """TTSON平台实现"""
    
    def __init__(self, base_url: str, token: str = None, network_proxies: Dict = None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.http_client = HTTPClient(proxies=network_proxies)
        
    def set_token(self, token: str):
        """设置token"""
        self.token = token
        
    def get_characters(self) -> List[Dict]:
        """获取所有可用的语音角色"""
        if not self.token:
            raise ValueError("Token is required for getting characters")
            
        url = f"{self.base_url}/flashsummary/voices"
        params = {
            'token': self.token
        }
        headers = {
            'Pragma': 'no-cache'
        }
        
        response = self.http_client.get(url, params=params, headers=headers)
        return response.json()
    
    def get_emotions(self) -> List[Dict]:
        """获取所有可用的情感"""
        url = f"{self.base_url}/flashsummary/emotions"
        headers = {
            'Pragma': 'no-cache'
        }
        
        response = self.http_client.get(url, headers=headers)
        return response.json()
    
    def generate_speech(self, text: str, voice_id: int, **kwargs) -> Dict:
        """生成语音"""
        if not self.token:
            raise ValueError("Token is required for generating speech")
            
        url = f"{self.base_url}/flashsummary/tts"
        
        payload = {
            "voice_id": voice_id,
            "text": text,
            "to_lang": kwargs.get('to_lang', 'auto'),
            "format": "wav",
            "speed_factor": kwargs.get('speed_factor', 1),
            "pitch_factor": kwargs.get('pitch_factor', 0),
            "volume_change_dB": kwargs.get('volume_change_dB', 0),
            "emotion": kwargs.get('emotion', 1),
            "code": kwargs.get('code', '')
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {'token': self.token}
        
        response = self.http_client.post(
            url=url,
            json=payload,
            headers=headers,
            params=params
        )
        
        return response.json()
    
    def download_audio(self, result: Dict) -> bytes:
        """下载生成的音频文件
        result: 生成语音返回的结果，包含 url, port, voice_path
        """
        if not self.token:
            raise ValueError("Token is required for downloading audio")
        
        # 从结果中构建完整的URL
        base_url = f"{result['url']}:{result['port']}"
        url = f"{base_url}/flashsummary/retrieveFileData"
        
        # 设置请求参数
        params = {
            'stream': True,
            'token': self.token,
            'voice_audio_path': result['voice_path']
        }
        
        # 设置请求头
        headers = {
            'Pragma': 'no-cache',
            'Range': 'bytes=0-'
        }
        
        # 发送请求并返回响应内容
        response = self.http_client.get(url, params=params, headers=headers)
        return response.content 
    
    def generate(self, text: str, voice_id: int, **kwargs) -> bytes:
        """生成语音文件
        
        Args:
            text: 要转换的文本
            voice_id: 语音角色ID
            **kwargs: 其他参数，包括:
                - to_lang: 目标语言，默认'auto'
                - speed_factor: 速度因子，默认1
                - pitch_factor: 音调因子，默认0
                - volume_change_dB: 音量变化，默认0
                - emotion: 情感，默认1
                - code: 代码，默认''
                
        Returns:
            bytes: 音频文件的二进制数据
            
        Raises:
            ValueError: 当token未设置时抛出
        """
        # 首先生成语音
        result = self.generate_speech(text, voice_id, **kwargs)
        
        # 然后下载音频
        return self.download_audio(result)