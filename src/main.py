import uvicorn
import argparse

if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='One-TTS API Server')
    parser.add_argument('--debug', action='store_true', help='启用debug模式')
    args = parser.parse_args()

    # 运行服务器
    uvicorn.run(
        "api:app",  # 使用导入字符串
        host="0.0.0.0", 
        port=8000,
        reload=args.debug,  # debug模式下启用热重载
        log_level="debug" if args.debug else "info"
    ) 