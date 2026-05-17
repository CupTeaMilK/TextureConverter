# src/path_utils.py
import os
import json
from pathlib import Path
import sys

def get_project_root() -> Path:
    """获取项目根目录"""
    # 尝试从环境变量获取
    if 'TEXTURE_CONVERTER_ROOT' in os.environ:
        return Path(os.environ['TEXTURE_CONVERTER_ROOT'])
    
    # 尝试从配置文件获取
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        install_dir = config.get('paths', {}).get('install_dir', '')
        if install_dir:
            return Path(install_dir) / "Minecraft-Texture-Converter-AI"
    
    # 默认路径
    return Path(r"D:\mc\TextureConverter_Github\Minecraft-Texture-Converter-AI")

def get_ai_model_dir() -> Path:
    """获取AI模型目录"""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        models_dir = config.get('paths', {}).get('models_dir', '')
        if models_dir:
            return Path(models_dir)
    
    # 默认路径
    return get_project_root() / "ai_generator" / "models"

def get_output_dir() -> Path:
    """获取输出目录"""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        output_dir = config.get('paths', {}).get('output_dir', '')
        if output_dir:
            return Path(output_dir)
    
    # 默认路径
    return get_project_root() / "output"

def setup_environment():
    """设置环境变量"""
    ai_dir = get_ai_model_dir()
    
    # 创建目录
    ai_dir.mkdir(parents=True, exist_ok=True)
    get_output_dir().mkdir(parents=True, exist_ok=True)
    
    # 设置环境变量
    os.environ['HF_HOME'] = str(ai_dir)
    os.environ['TRANSFORMERS_CACHE'] = str(ai_dir)
    os.environ['DIFFUSERS_CACHE'] = str(ai_dir)
    
    return ai_dir
