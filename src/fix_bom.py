# src/fix_bom.py
import os
import codecs
from pathlib import Path
import sys

def remove_bom(filepath: str) -> bool:
    """
    移除文件的BOM（字节顺序标记）
    某些编辑器会在UTF-8文件开头添加BOM，可能导致JSON解析失败
    """
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # 检查是否有BOM
        if content.startswith(codecs.BOM_UTF8):
            # 移除BOM
            with open(filepath, 'wb') as f:
                f.write(content[3:])
            print(f"✅ 已移除BOM: {filepath}")
            return True
        else:
            return False
    
    except Exception as e:
        print(f"❌ 处理BOM失败 {filepath}: {e}")
        return False

def fix_json_files_in_directory(directory: str, recursive: bool = True) -> int:
    """
    修复目录中所有JSON文件的BOM问题
    
    Args:
        directory: 目录路径
        recursive: 是否递归处理子目录
    
    Returns:
        修复的文件数量
    """
    fixed_count = 0
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.json'):
                    filepath = os.path.join(root, file)
                    if remove_bom(filepath):
                        fixed_count += 1
    else:
        for file in os.listdir(directory):
            if file.lower().endswith('.json'):
                filepath = os.path.join(directory, file)
                if remove_bom(filepath):
                    fixed_count += 1
    
    return fixed_count

def check_file_encoding(filepath: str) -> str:
    """检查文件编码"""
    try:
        with open(filepath, 'rb') as f:
            raw = f.read(4)
            
        if raw.startswith(codecs.BOM_UTF8):
            return "UTF-8-BOM"
        elif raw.startswith(codecs.BOM_UTF16_LE):
            return "UTF-16-LE"
        elif raw.startswith(codecs.BOM_UTF16_BE):
            return "UTF-16-BE"
        elif raw.startswith(codecs.BOM_UTF32_LE):
            return "UTF-32-LE"
        elif raw.startswith(codecs.BOM_UTF32_BE):
            return "UTF-32-BE"
        else:
            # 尝试检测UTF-8
            try:
                raw.decode('utf-8')
                return "UTF-8"
            except:
                return "未知/二进制"
    
    except Exception as e:
        return f"检测失败: {e}"

def convert_to_utf8(filepath: str) -> bool:
    """将文件转换为UTF-8（无BOM）"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # 尝试不同编码
        encodings = ['utf-8', 'gbk', 'latin-1', 'cp1252']
        
        for enc in encodings:
            try:
                text = content.decode(enc)
                # 写入UTF-8（无BOM）
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✅ 已转换 {filepath} 到 UTF-8 (原编码: {enc})")
                return True
            except:
                continue
        
        print(f"❌ 无法确定文件编码: {filepath}")
        return False
    
    except Exception as e:
        print(f"❌ 转换文件失败 {filepath}: {e}")
        return False

def is_valid_json(filepath: str) -> bool:
    """检查文件是否是有效的JSON"""
    import json
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"❌ JSON解析失败 {filepath}: {e}")
        return False

def fix_all_json_files(project_dir: str = None) -> Dict[str, int]:
    """
    修复项目中的所有JSON文件
    
    Returns:
        修复统计
    """
    if project_dir is None:
        project_dir = os.getcwd()
    
    stats = {
        "total_files": 0,
        "bom_fixed": 0,
        "converted": 0,
        "invalid_json": 0
    }
    
    # 扫描所有JSON文件
    for root, dirs, files in os.walk(project_dir):
        # 跳过一些目录
        if '.git' in dirs:
            dirs.remove('.git')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        if 'temp_work' in dirs:
            dirs.remove('temp_work')
        
        for file in files:
            if file.lower().endswith('.json'):
                filepath = os.path.join(root, file)
                stats["total_files"] += 1
                
                # 检查编码
                encoding = check_file_encoding(filepath)
                print(f"检查: {filepath} [{encoding}]")
                
                # 修复BOM
                if encoding == "UTF-8-BOM":
                    if remove_bom(filepath):
                        stats["bom_fixed"] += 1
                
                # 检查JSON有效性
                if not is_valid_json(filepath):
                    stats["invalid_json"] += 1
                    # 尝试转换
                    if convert_to_utf8(filepath):
                        stats["converted"] += 1
                        # 再次检查
                        if is_valid_json(filepath):
                            stats["invalid_json"] -= 1
    
    return stats

def main():
    """主函数"""
    print("🔧 JSON文件修复工具")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("请输入要处理的目录（回车使用当前目录）: ").strip()
        if not target:
            target = os.getcwd()
    
    if not os.path.exists(target):
        print(f"❌ 目录不存在: {target}")
        return
    
    print(f"处理目录: {target}")
    print()
    
    # 修复文件
    stats = fix_all_json_files(target)
    
    print(f"\n📊 处理结果:")
    print(f"  总计文件: {stats['total_files']}")
    print(f"  修复BOM: {stats['bom_fixed']}")
    print(f"  转换编码: {stats['converted']}")
    print(f"  无效JSON: {stats['invalid_json']}")
    
    if stats['invalid_json'] > 0:
        print(f"\n⚠️  有 {stats['invalid_json']} 个JSON文件无法修复")
        print("   请手动检查这些文件")
    
    print("\n✅ 处理完成")

if __name__ == "__main__":
    main()
