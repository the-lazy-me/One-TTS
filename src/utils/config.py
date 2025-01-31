import yaml
from pathlib import Path
import os

def load_config():
    """加载配置文件，并用环境变量覆盖配置"""
    # 加载基础配置
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 从环境变量更新配置
    # TTSON配置
    if os.getenv('TTSON_BASE_URL'):
        config['platforms']['ttson']['base_url'] = os.getenv('TTSON_BASE_URL')
    if os.getenv('TTSON_TOKEN'):
        config['platforms']['ttson']['token'] = os.getenv('TTSON_TOKEN')
    if os.getenv('TTSON_HTTP_PROXY'):
        config['platforms']['ttson']['network_proxies']['http'] = os.getenv('TTSON_HTTP_PROXY')
    if os.getenv('TTSON_HTTPS_PROXY'):
        config['platforms']['ttson']['network_proxies']['https'] = os.getenv('TTSON_HTTPS_PROXY')

    # ACGN TTSON配置
    if os.getenv('ACGN_TTSON_BASE_URL'):
        config['platforms']['acgn_ttson']['base_url'] = os.getenv('ACGN_TTSON_BASE_URL')
    if os.getenv('ACGN_TTSON_TOKEN'):
        config['platforms']['acgn_ttson']['token'] = os.getenv('ACGN_TTSON_TOKEN')
    if os.getenv('ACGN_TTSON_HTTP_PROXY'):
        config['platforms']['acgn_ttson']['network_proxies']['http'] = os.getenv('ACGN_TTSON_HTTP_PROXY')
    if os.getenv('ACGN_TTSON_HTTPS_PROXY'):
        config['platforms']['acgn_ttson']['network_proxies']['https'] = os.getenv('ACGN_TTSON_HTTPS_PROXY')

    # Fish Audio配置
    if os.getenv('FISH_AUDIO_BASE_URL'):
        config['platforms']['fish_audio']['base_url'] = os.getenv('FISH_AUDIO_BASE_URL')
    if os.getenv('FISH_AUDIO_TOKEN'):
        config['platforms']['fish_audio']['token'] = os.getenv('FISH_AUDIO_TOKEN')
    if os.getenv('FISH_AUDIO_HTTP_PROXY'):
        config['platforms']['fish_audio']['network_proxies']['http'] = os.getenv('FISH_AUDIO_HTTP_PROXY')
    if os.getenv('FISH_AUDIO_HTTPS_PROXY'):
        config['platforms']['fish_audio']['network_proxies']['https'] = os.getenv('FISH_AUDIO_HTTPS_PROXY')

    return config

config = load_config() 