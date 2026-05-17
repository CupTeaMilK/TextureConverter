# src/utils.py
import os
import json
import zipfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
import re

def read_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """读取JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"❌ 读取JSON文件失败 {filepath}: {e}")
        return None

def write_json_file(filepath: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """写入JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"❌ 写入JSON文件失败 {filepath}: {e}")
        return False

def extract_zip(zip_path: str, extract_dir: str) -> bool:
    """解压ZIP文件"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return True
    except Exception as e:
        print(f"❌ 解压文件失败 {zip_path}: {e}")
        return False

def create_zip(source_dir: str, zip_path: str) -> bool:
    """创建ZIP文件"""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        return True
    except Exception as e:
        print(f"❌ 创建ZIP文件失败 {zip_path}: {e}")
        return False

def clean_directory(dir_path: str) -> None:
    """清空目录（如果存在）"""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

def get_pack_version(pack_dir: str) -> Optional[Dict[str, Any]]:
    """获取材质包版本信息"""
    mcmeta_path = os.path.join(pack_dir, "pack.mcmeta")
    
    if not os.path.exists(mcmeta_path):
        # 尝试在父目录中查找
        for root, dirs, files in os.walk(pack_dir):
            for file in files:
                if file == "pack.mcmeta":
                    mcmeta_path = os.path.join(root, file)
                    break
    
    if not os.path.exists(mcmeta_path):
        return None
    
    data = read_json_file(mcmeta_path)
    if not data or "pack" not in data:
        return None
    
    pack_info = data["pack"]
    pack_format = pack_info.get("pack_format", 1)
    
    # 根据pack_format推断游戏版本
    version_map = {
        1: "1.6.1-1.8.9",
        2: "1.9-1.10.2",
        3: "1.11-1.12.2",
        4: "1.13-1.14.4",
        5: "1.15-1.16.1",
        6: "1.16.2-1.16.5",
        7: "1.17-1.17.1",
        8: "1.18-1.18.2",
        9: "1.19-1.19.2",
        10: "1.19.3",
        11: "1.19.4",
        12: "1.20-1.20.1",
        13: "1.20.2-1.20.4",
        14: "1.20.5-1.20.6",
        15: "1.21-1.21.4",
        16: "1.21.5",
        18: "1.21.11"
    }
    
    game_version = version_map.get(pack_format, f"未知(pack_format={pack_format})")
    
    return {
        "pack_format": pack_format,
        "game_version": game_version,
        "description": pack_info.get("description", "")
    }

def get_pack_format_for_version(version: str) -> int:
    """根据版本获取pack_format"""
    version_map = {
        "1.16.5": 6,
        "1.17.1": 7,
        "1.18.2": 8,
        "1.19.4": 11,
        "1.20.6": 14,
        "1.21.5": 16,
        "1.21.11": 18
    }
    
    # 尝试精确匹配
    if version in version_map:
        return version_map[version]
    
    # 尝试主版本匹配
    for v, fmt in version_map.items():
        if version.startswith(v.split('.')[0]):
            return fmt
    
    # 默认
    return 6

def normalize_path(path: str) -> str:
    """规范化路径（统一斜杠）"""
    return path.replace('\\', '/')

def is_texture_file(filename: str) -> bool:
    """检查是否是材质文件"""
    texture_extensions = {'.png', '.jpg', '.jpeg', '.tga', '.bmp'}
    return any(filename.lower().endswith(ext) for ext in texture_extensions)

def get_file_size_mb(filepath: str) -> float:
    """获取文件大小（MB）"""
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    return 0.0

def copy_directory(src: str, dst: str) -> bool:
    """复制整个目录"""
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return True
    except Exception as e:
        print(f"❌ 复制目录失败 {src} -> {dst}: {e}")
        return False

def get_relative_texture_path(namespace: str, item_id: str) -> str:
    """获取相对材质路径"""
    # 转换物品ID为路径
    # 例如: minecraft:stone -> textures/block/stone.png
    parts = item_id.split(':')
    if len(parts) == 2:
        namespace, item_name = parts
    else:
        namespace = "minecraft"
        item_name = parts[0]
    
    # 猜测类型
    if "ore" in item_name:
        item_type = "block"
    elif "block" in item_name:
        item_type = "block"
    elif "item" in item_name or "ingot" in item_name or "gem" in item_name:
        item_type = "item"
    elif "sword" in item_name or "pickaxe" in item_name or "axe" in item_name:
        item_type = "item"
    else:
        item_type = "block"  # 默认
    
    return f"{namespace}/textures/{item_type}/{item_name}.png"

def ensure_directory_exists(dirpath: str) -> None:
    """确保目录存在"""
    os.makedirs(dirpath, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """清理文件名中的非法字符"""
    # 移除非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(illegal_chars, '_', filename)
    
    # 限制长度
    if len(sanitized) > 200:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:200-len(ext)] + ext
    
    return sanitized

def get_texture_resolution(pack_dir: str) -> int:
    """检测材质包分辨率（16x, 32x, 64x等）"""
    # 查找第一个材质文件
    for root, dirs, files in os.walk(pack_dir):
        for file in files:
            if file.lower().endswith('.png'):
                try:
                    from PIL import Image
                    img_path = os.path.join(root, file)
                    with Image.open(img_path) as img:
                        width, height = img.size
                        if width == height:
                            return width
                except:
                    pass
    
    return 16  # 默认

def count_files(directory: str) -> int:
    """统计目录中的文件数量"""
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

def get_minecraft_versions() -> List[str]:
    """获取支持的Minecraft版本列表"""
    return [
        "1.16.5",
        "1.17.1", 
        "1.18.2",
        "1.19.4",
        "1.20.6",
        "1.21.5",
        "1.21.11"
    ]

def print_progress_bar(iteration: int, total: int, prefix: str = '', 
                      suffix: str = '', length: int = 50, fill: str = '█'):
    """打印进度条"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    
    if iteration == total: 
        print()

# 测试代码
if __name__ == "__main__":
    print("🔧 测试工具函数")
    
    # 测试JSON函数
    test_data = {"test": 123, "name": "测试"}
    write_json_file("test.json", test_data)
    loaded = read_json_file("test.json")
    print(f"JSON测试: {loaded}")
    
    if os.path.exists("test.json"):
        os.remove("test.json")
    
    # 测试其他函数
    print(f"清理文件名: {sanitize_filename('test:file?name*.png')}")
    print(f"相对路径: {get_relative_texture_path('minecraft', 'stone')}")
    print(f"版本列表: {get_minecraft_versions()}")
    
    print("✅ 工具函数测试完成")
