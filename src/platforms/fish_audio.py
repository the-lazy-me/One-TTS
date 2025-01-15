from typing import List, Dict
from src.core.tts_manager import TTSPlatform
from src.utils.http_client import HTTPClient
import ormsgpack  # 需要安装：pip install ormsgpack

class FishAudio(TTSPlatform):
    """Fish Audio平台实现"""
    
    def __init__(self, base_url: str = "https://api.fish.audio", token: str = None, network_proxies: Dict = None):
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
            
        url = f"{self.base_url}/v1/voices"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        response = self.http_client.get(url, headers=headers)
        return response.json()['data']
    
    def generate(self, text: str, voice_id: str, **kwargs) -> bytes:
        """生成语音文件"""
        if not self.token:
            raise ValueError("Token is required for generating speech")
            
        url = f"{self.base_url}/v1/tts"
        
        # 构建请求数据
        request_data = {
            "text": text,
            "reference_id": voice_id,
            "chunk_length": kwargs.get("chunk_length", 200),
            "format": kwargs.get("format", "mp3"),
            "mp3_bitrate": kwargs.get("mp3_bitrate", 128),
            "normalize": kwargs.get("normalize", True),
            "latency": kwargs.get("latency", "normal"),
            "references": []  # 暂不支持参考音频
        }
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/msgpack'
        }
        
        # 使用 msgpack 序列化请求数据
        payload = ormsgpack.packb(
            request_data, 
            option=ormsgpack.OPT_SERIALIZE_PYDANTIC
        )
        
        # 发送请求并获取音频数据
        response = self.http_client.post(
            url=url,
            data=payload,  # 使用 data 而不是 json
            headers=headers
        )
        
        # 收集所有音频数据
        audio_data = b''
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                audio_data += chunk
                
        return audio_data