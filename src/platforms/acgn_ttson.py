from typing import List, Dict, BinaryIO
from src.core.tts_manager import TTSPlatform
from src.utils.http_client import HTTPClient

class ACGNTtson(TTSPlatform):
    """ACGN TTSON平台实现"""
    
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.http_client = HTTPClient()
        
    def set_token(self, token: str):
        """设置token"""
        self.token = token
        
    def get_characters(self) -> List[Dict]:
        """获取所有可用的语音角色"""
        url = f"{self.base_url}/flashsummary/voices"
        params = {
            'language': 'zh-CN',
            'tag_id': 1
        }
        headers = {
            'Pragma': 'no-cache'
        }
        
        response = self.http_client.get(url, params=params, headers=headers)
        return response.json()
    
    def generate(self, text: str, voice_id: int, **kwargs) -> bytes:
        """生成语音文件
        
        Args:
            text: 要转换的文本
            voice_id: 语音角色ID
            **kwargs: 其他参数，包括:
                - to_lang: 目标语言，默认'ZH'
                - auto_translate: 是否自动翻译，默认0
                - voice_speed: 语音速度，默认'0%'
                - speed_factor: 速度因子，默认1
                - pitch_factor: 音调因子，默认0
                - rate: 语速率，默认'1.0'
                - emotion: 情感，默认1
                
        Returns:
            bytes: 音频文件的二进制数据
            
        Raises:
            ValueError: 当token未设置时抛出
        """
        # 首先生成语音
        result = self.generate_speech(text, voice_id, **kwargs)
        
        # 然后下载音频
        return self.download_audio(result)
    
    def generate_speech(self, text: str, voice_id: int, **kwargs) -> Dict:
        """生成语音（内部使用）"""
        if not self.token:
            raise ValueError("Token is required for generating speech")
            
        url = f"{self.base_url}/flashsummary/tts"
        
        payload = {
            "voice_id": voice_id,
            "text": text,
            "format": "wav",
            "to_lang": kwargs.get('to_lang', 'ZH'),
            "auto_translate": kwargs.get('auto_translate', 0),
            "voice_speed": kwargs.get('voice_speed', '0%'),
            "speed_factor": kwargs.get('speed_factor', 1),
            "pitch_factor": kwargs.get('pitch_factor', 0),
            "rate": kwargs.get('rate', '1.0'),
            "client_ip": "ACGN",
            "emotion": kwargs.get('emotion', 1)
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
        """下载生成的音频文件（内部使用）"""
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
        return response.content  # 直接返回二进制内容