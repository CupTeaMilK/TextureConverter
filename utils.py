# utils.py
import os
import zipfile
import json
import shutil
from pathlib import Path

def extract_zip(zip_path, extract_to):
    """解压材质包zip文件"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ 已解压到: {extract_to}")
        return True
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False

def create_zip(source_dir, output_zip):
    """将目录打包为zip文件"""
    try:
        # 确保输出路径是绝对路径
        if not os.path.isabs(output_zip):
            output_zip = os.path.join(os.getcwd(), output_zip)
        
        print(f"📦 打包信息:")
        print(f"   源目录: {source_dir}")
        print(f"   输出文件: {output_zip}")
        
        # 检查源目录是否存在
        if not os.path.exists(source_dir):
            print(f"❌ 源目录不存在: {source_dir}")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_zip)
        if output_dir and not os.path.exists(output_dir):
            print(f"📁 创建输出目录: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        elif not output_dir:
            # 如果输出目录为空，说明output_zip是当前目录下的文件名
            output_zip = os.path.join(os.getcwd(), output_zip)
            print(f"📁 使用当前目录: {os.getcwd()}")
        
        # 检查是否有写入权限
        try:
            test_file = os.path.join(os.path.dirname(output_zip), ".test_write")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            print(f"❌ 没有写入权限: {e}")
            return False
        
        # 统计文件数量
        file_count = 0
        total_size = 0
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算在zip中的相对路径
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    file_count += 1
                    total_size += os.path.getsize(file_path)
                    
                    # 每100个文件显示一次进度
                    if file_count % 100 == 0:
                        print(f"   📦 已打包 {file_count} 个文件...")
        
        # 转换为MB
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"✅ 打包完成!")
        print(f"   文件数: {file_count}")
        print(f"   总大小: {total_size_mb:.2f} MB")
        print(f"   输出位置: {output_zip}")
        
        return True
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def read_json_file(file_path):
    """读取JSON文件 - 支持多种编码和BOM"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return None
    
    # 尝试不同编码
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
                # 如果文件是空的，返回空字典
                if not content.strip():
                    return {}
                    
                return json.loads(content)
                
        except UnicodeDecodeError:
            continue  # 尝试下一个编码
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败 [{encoding}]: {file_path}")
            print(f"   错误: {e}")
            
            # 显示文件内容前200字符帮助调试
            try:
                with open(file_path, 'rb') as f:
                    raw = f.read(500)
                    print(f"   文件内容(前500字节): {raw[:200]}")
            except:
                pass
                
            continue
    
    # 所有编码都失败
    print(f"❌ 无法读取JSON文件: {file_path}")
    
    # 显示文件原始内容
    try:
        with open(file_path, 'rb') as f:
            raw = f.read(1000)
            print(f"原始内容(16进制): {raw[:100].hex()}")
            print(f"尝试作为文本: {raw[:200].decode('ascii', errors='replace')}")
    except:
        pass
    
    return None

def write_json_file(file_path, data):
    """写入JSON文件"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ 写入JSON失败 {file_path}: {e}")
        return False

def get_pack_version(pack_dir):
    """从pack.mcmeta读取材质包版本"""
    mcmeta_path = os.path.join(pack_dir, "pack.mcmeta")
    
    if not os.path.exists(mcmeta_path):
        print("⚠️  未找到 pack.mcmeta 文件")
        return None
    
    data = read_json_file(mcmeta_path)
    if data and "pack" in data:
        version = data["pack"].get("pack_format")
        # 将pack_format转换为游戏版本
        game_version = convert_pack_format_to_version(version)
        return {
            "pack_format": version,
            "game_version": game_version,
            "description": data["pack"].get("description", "")
        }
    
    return None

def convert_pack_format_to_version(pack_format):
    """将pack_format转换为具体的Minecraft版本"""
    # 这里先简单映射，后续会完善
    version_map = {
        4: "1.13-1.14",
        5: "1.15",
        6: "1.16.1-1.16.5",
        7: "1.17-1.17.1",
        8: "1.18-1.18.1",
        9: "1.18.2",
        10: "1.19-1.19.2",
        11: "1.19.3",
        12: "1.19.4",
        13: "1.20-1.20.1",
        14: "1.20.2",
        15: "1.20.3-1.20.4",
        16: "1.20.5-1.20.6",
        17: "1.21-1.21.1",
        18: "1.21.2",
        19: "1.21.3",
        20: "1.21.4",
        21: "1.21.5",
        22: "1.21.6-1.21.8",
        23: "1.21.9-1.21.10",
        24: "1.21.11-1.21.12"
    }
    
    return version_map.get(pack_format, f"未知版本 (pack_format: {pack_format})")

def clean_directory(dir_path):
    """清空目录"""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
