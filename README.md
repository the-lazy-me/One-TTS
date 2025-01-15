# One-TTS

一个用于将多个TTS平台聚合管理调用的后端Python项目。

## 安装

1. 克隆项目：
```bash
git clone <repository_url>
cd one-tts
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行示例程序：
```bash
python src/main.py
```

这将执行以下操作：
- 获取可用的语音角色列表
- 生成示例语音
- 下载并保存音频文件

## 项目结构

```
one-tts/
├── src/                # 源代码目录
│   ├── platforms/      # 各个TTS平台的实现
│   ├── core/           # 核心功能模块
│   └── utils/          # 工具类
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## 支持的平台

- acgn_ttson
- ttson
- fish audio