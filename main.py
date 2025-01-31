import uvicorn
from src.utils.config import config
import argparse
import os

if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='One-TTS API Server')
    parser.add_argument('--debug', action='store_true', help='启用debug模式')
    args = parser.parse_args()

    # 优先使用环境变量，如果没有则使用配置文件
    host = os.getenv('API_HOST', config["api_server"]["host"])
    port = int(os.getenv('API_PORT', config["api_server"]["port"]))
    debug_mode = args.debug or \
                os.getenv('API_DEBUG', '').lower() == 'true' or \
                config["api_server"].get("debug", False)

    # 运行服务器
    uvicorn.run(
        "src.api:app",
        host=host,
        port=port,
        reload=debug_mode,
        log_level="debug" if debug_mode else "info"
    ) 