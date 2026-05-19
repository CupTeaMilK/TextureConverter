# fix_bom.py
import os
import sys

def fix_json_bom(file_path):
    """修复JSON文件的BOM问题"""
    try:
        # 读取文件原始内容
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # 检查是否有BOM
        if content.startswith(b'\xef\xbb\xbf'):
            print(f"✅ 发现BOM，正在修复: {file_path}")
            # 去除BOM
            content = content[3:]
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"✅ 已修复: {file_path}")
            return True
        else:
            print(f"✅ 无BOM: {file_path}")
            return False
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            fix_json_bom(file_path)
        else:
            print(f"❌ 文件不存在: {file_path}")
    else:
        print("使用方法: python fix_bom.py <文件路径>")
        print("示例: python fix_bom.py MSL/材质包/pack.mcmeta")
