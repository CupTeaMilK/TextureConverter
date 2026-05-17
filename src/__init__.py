# src/__init__.py
"""
Minecraft AI材质转换器 - 核心模块
版本: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "YourName"
__description__ = "Minecraft材质包转换器，支持AI生成材质"

# 导出常用类和函数
from .converter import TexturePackConverter
from .ai_texture_generator import AITextureGenerator
from .texture_generator import SmartTextureGenerator
from .main import main
from .path_utils import get_project_root, get_ai_model_dir, setup_environment

# 导出工具函数
from .utils import (
    read_json_file, write_json_file,
    extract_zip, create_zip, clean_directory,
    get_pack_version, get_pack_format_for_version
)

# 导出版本数据
from .version_data import (
    get_added_items, get_removed_items,
    normalize_version, get_latest_version,
    get_supported_versions, is_version_supported
)
