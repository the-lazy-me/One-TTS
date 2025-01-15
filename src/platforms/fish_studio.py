from typing import List, Dict
from src.core.tts_manager import TTSPlatform
from src.utils.http_client import HTTPClient

class FishStudio(TTSPlatform):
    """Fish Audio平台实现"""
    
    def __init__(self, base_url: str = "https://api.fish.audio", token: str = None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.http_client = HTTPClient()
        
    def set_token(self, token: str):
        """设置token"""
        self.token = token
        
    def get_characters(self) -> List[Dict]:
        """获取所有可用的语音角色"""
        if not self.token:
            raise ValueError("Token is required for getting characters")
            
        url = f"{self.base_url}/model"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        response = self.http_client.get(url, headers=headers)
        return response.json()
    
    def generate(self, text: str, voice_id: str, **kwargs) -> bytes:
        """生成语音文件
        
        Args:
            text: 要转换的文本
            voice_id: 语音角色ID (reference_id)
            **kwargs: 其他参数（Fish Audio目前没有其他可选参数）
                
        Returns:
            bytes: 音频文件的二进制数据
            
        Raises:
            ValueError: 当token未设置时抛出
        """
        if not self.token:
            raise ValueError("Token is required for generating speech")
            
        url = f"{self.base_url}/v1/tts"
        
        payload = {
            "text": text,
            "reference_id": voice_id
        }
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        response = self.http_client.post(
            url=url,
            json=payload,
            headers=headers
        )
        
        return response.content  # Fish Studio直接返回音频数据