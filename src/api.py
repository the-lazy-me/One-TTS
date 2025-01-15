from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from src.core.tts_manager import TTSManager, TTSPlatform
from src.platforms.acgn_ttson import ACGNTtson
from src.platforms.ttson import Ttson
from src.platforms.fish_audio import FishAudio
from typing import Dict, Any
from pydantic import BaseModel
import io
import time
from src.utils.config import config

# 平台映射字典
PLATFORM_MAP = {
    "ttson": Ttson,
    "acgn_ttson": ACGNTtson,
    "fish_audio": FishAudio
}

app = FastAPI(title="One-TTS API")

# 初始化TTS管理器
tts_manager = TTSManager()

# 从配置文件获取base_url并注册平台
acgn_platform = ACGNTtson(config["platforms"]["acgn_ttson"]["base_url"])
tts_manager.register_platform("acgn_ttson", acgn_platform)

ttson_platform = Ttson(config["platforms"]["ttson"]["base_url"])
tts_manager.register_platform("ttson", ttson_platform)

fish_audio_platform = FishAudio(
    base_url=config["platforms"]["fish_audio"]["base_url"],
    token=config["platforms"]["fish_audio"]["token"],
    network_proxies=config["platforms"]["fish_audio"]["network_proxies"]
)
tts_manager.register_platform("fish_audio", fish_audio_platform)

# 请求模型定义
class CharacterRequest(BaseModel):
    platform: str
    token: str = None  # token变为可选参数

class TTSRequest(BaseModel):
    platform: str
    text: str
    character: str
    token: str = None  # token变为可选参数
    options: Dict[str, Any] = {}

@app.get("/platforms")
def list_platforms():
    """获取所有支持的平台列表"""
    return {"platforms": tts_manager.list_platforms()}

@app.post("/characters")
def get_characters(request: CharacterRequest):
    """获取指定平台的所有可用语音角色"""
    platform = tts_manager.get_platform(request.platform)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    try:
        # 优先使用请求中的token,否则使用配置文件中的token
        token = request.token or config["platforms"][request.platform]["token"]
        platform.set_token(token)
        return {"characters": platform.get_characters()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/emotions")
def get_emotions(platform: str = Query(..., description="Platform name")):
    """获取指定平台的所有可用情感(仅TTSON平台支持)"""
    if platform != "ttson":
        raise HTTPException(status_code=400, detail="Only TTSON platform supports emotions")
    
    platform_instance = tts_manager.get_platform(platform)
    if not platform_instance:
        raise HTTPException(status_code=404, detail="Platform not found")
        
    return {"emotions": platform_instance.get_emotions()}

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """统一的文本转语音接口"""
    platform = tts_manager.get_platform(request.platform)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    try:
        # 优先使用请求中的token,否则使用配置文件中的token
        token = request.token or config["platforms"][request.platform]["token"]
        platform.set_token(token)
        
        # 根据不同平台处理character参数
        voice_id = request.character
        if request.platform in ["ttson", "acgn_ttson"]:
            voice_id = int(request.character)
            
        audio_data = platform.generate(
            text=request.text,
            voice_id=voice_id,
            **request.options
        )
        
        filename = f"{request.platform}_tts_{int(time.time())}.mp3"
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

def init_platform(name: str, config: Dict) -> TTSPlatform:
    """初始化指定的TTS平台"""
    platform_class = PLATFORM_MAP.get(name)
    if not platform_class:
        raise ValueError(f"Unsupported platform: {name}")
        
    return platform_class(
        base_url=config['base_url'],
        token=config.get('token'),
        network_proxies=config.get('network_proxies')
    ) 