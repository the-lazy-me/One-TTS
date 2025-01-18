# One-TTS

一个用于将多个TTS平台聚合管理调用的后端Python项目。

## 安装

1. 克隆项目：
```bash
git clone https://github.com/the-lazy-me/One-TTS.git
cd One-TTS
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 配置文件`config/config.yaml`

   ```yaml
   # API服务配置
   api_server:
     host: "0.0.0.0"
     port: 5555
     base_url: "http://localhost:5555"
     debug: false # 默认关闭debug模式
   
   # TTS平台配置
   platforms:
     # 海豚Ai配音，地址：https://www.ttson.cn/
     ttson:
       base_url: "https://ht.ttson.cn:37284"
       token: "your_token_here"
       network_proxies:
         http: null
         https: null
   
     # TTS-Online，实际也是海豚Ai的，地址：https://acgn.ttson.cn/
     acgn_ttson:
       base_url: "https://ht.ttson.cn:37284"
       token: "your_token_here"
       network_proxies:
         http: null
         https: null
   
     # Fish Audio，地址：https://fish.audio/
     fish_audio:
       base_url: "https://api.fish.audio"
       token: "your_token_here"
       network_proxies:
         http: "http://127.0.0.1:7890"
         https: "http://127.0.0.1:7890"
   ```

2. 运行示例程序：
```bash
python main.py
```


## 支持的平台

- [x] 支持[海豚配音 TTS Online 二次元音色](https://www.ttson.cn/?source=thelazy)
- [x] 支持[海豚Ai配音](https://www.ttson.cn/?source=thelazy)
- [x] 支持[Fish Audio](https://fish.audio/zh-CN/discovery/)
- [ ] 支持[ChatTTS](https://github.com/2noise/ChatTTS)
- [ ] 支持[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- [ ] 支持[Kokoro TTS](https://kokorotts.net/zh)
