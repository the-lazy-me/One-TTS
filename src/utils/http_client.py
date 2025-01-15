import requests
from typing import Dict, Any, Optional

class HTTPClient:
    """HTTP客户端工具类"""
    
    def __init__(self, proxies=None):
        self.proxies = proxies
        
    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Any:
        """发送GET请求"""
        if self.proxies:
            kwargs = {'proxies': self.proxies}
        else:
            kwargs = {}
        response = requests.get(url, params=params, headers=headers, stream=True, **kwargs)
        response.raise_for_status()
        return response
    
    def post(self, url: str, data: Optional[Dict] = None, json: Optional[Dict] = None,
            headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """发送POST请求"""
        if self.proxies:
            kwargs = {'proxies': self.proxies}
        else:
            kwargs = {}
        response = requests.post(url, data=data, json=json, headers=headers, params=params, **kwargs)
        response.raise_for_status()
        return response 