import uvicorn
from src.utils.config import config
import argparse

if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='One-TTS API Server')
    parser.add_argument('--debug', action='store_true', help='启用debug模式')
    args = parser.parse_args()

    # 运行服务器
    debug_mode = args.debug or config["api_server"].get("debug", False)
    uvicorn.run(
        "src.api:app",  # 使用正确的导入路径
        host=config["api_server"]["host"], 
        port=config["api_server"]["port"],
        reload=debug_mode,  # debug模式下启用热重载
        log_level="debug" if debug_mode else "info"
    ) 