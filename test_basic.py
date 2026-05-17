# test_basic.py
import os
import sys
import json
import tempfile
from pathlib import Path
import zipfile
import shutil

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_test_pack():
    """创建测试材质包"""
    with tempfile.TemporaryDirectory() as tmpdir:
        pack_dir = Path(tmpdir) / "test_pack"
        pack_dir.mkdir(parents=True)
        
        # 创建pack.mcmeta
        mcmeta = {
            "pack": {
                "pack_format": 6,
                "description": "测试材质包 v1.16.5"
            }
        }
        
        with open(pack_dir / "pack.mcmeta", "w", encoding="utf-8") as f:
            json.dump(mcmeta, f, indent=2)
        
        # 创建一些测试材质
        assets_dir = pack_dir / "assets" / "minecraft" / "textures" / "block"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        from PIL import Image
        # 创建简单的测试材质
        for name, color in [("stone", (128, 128, 128)), 
                           ("dirt", (139, 69, 19)), 
                           ("grass_block_top", (0, 128, 0))]:
            img = Image.new("RGB", (16, 16), color)
            img.save(assets_dir / f"{name}.png")
        
        # 创建ZIP文件
        zip_path = Path(tmpdir) / "test_pack.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in pack_dir.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(pack_dir)
                    zipf.write(file, arcname)
        
        # 复制到项目目录
        output_dir = project_root / "resources" / "example_pack"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(zip_path, output_dir / "test_pack_1.16.5.zip")
        print(f"✅ 测试材质包已创建: {output_dir / 'test_pack_1.16.5.zip'}")
        
        return output_dir / "test_pack_1.16.5.zip"

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    modules = [
        ("src.main", "主程序"),
        ("src.converter", "转换器"),
        ("src.ai_texture_generator", "AI生成器"),
        ("src.texture_generator", "智能生成器"),
        ("src.utils", "工具函数"),
        ("src.version_data", "版本数据"),
        ("src.path_utils", "路径工具"),
    ]
    
    all_passed = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {description}: 导入成功")
        except ImportError as e:
            print(f"  ❌ {description}: 导入失败 - {e}")
            all_passed = False
        except Exception as e:
            print(f"  ⚠️  {description}: 警告 - {e}")
    
    return all_passed

def test_path_config():
    """测试路径配置"""
    print("\n📍 测试路径配置...")
    
    try:
        config_path = project_root / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            print(f"  ✅ 配置文件加载成功")
            print(f"     项目名称: {config.get('project', {}).get('name', '未知')}")
            print(f"     版本: {config.get('project', {}).get('version', '未知')}")
            
            # 检查路径
            paths = config.get("paths", {})
            install_dir = Path(paths.get("install_dir", ""))
            if install_dir.exists():
                print(f"  ✅ 安装目录存在: {install_dir}")
            else:
                print(f"  ⚠️  安装目录不存在: {install_dir}")
            
            return True
        else:
            print("  ❌ 配置文件不存在")
            return False
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        return False

def test_converter():
    """测试转换器"""
    print("\n🧪 测试转换器...")
    
    try:
        from src.converter import TexturePackConverter
        
        # 测试三种模式
        print("  测试基础模式...")
        conv1 = TexturePackConverter(use_ai=False)
        print("    ✅ 基础模式初始化成功")
        
        print("  测试智能模式...")
        conv2 = TexturePackConverter(use_ai=True, ai_model="smart")
        print("    ✅ 智能模式初始化成功")
        
        # 检查AI模型是否存在
        ai_dir = Path(r"D:\mc\TextureConverter_Github\ai_generator\models")
        if (ai_dir / "v1-5-pruned.safetensors").exists():
            print("  测试AI模式...")
            conv3 = TexturePackConverter(use_ai=True, ai_model="ai")
            print("    ✅ AI模式初始化成功")
        else:
            print("  ⚠️  AI模式跳过（模型不存在）")
        
        return True
    except Exception as e:
        print(f"  ❌ 转换器测试失败: {e}")
        return False

def test_script_files():
    """测试脚本文件"""
    print("\n📜 测试脚本文件...")
    
    scripts = [
        ("scripts/install.bat", "安装脚本"),
        ("scripts/start.bat", "启动脚本"),
        ("scripts/download_model.bat", "下载脚本"),
        ("scripts/check_environment.bat", "环境检查脚本"),
    ]
    
    all_exist = True
    for script, description in scripts:
        script_path = project_root / script
        if script_path.exists():
            print(f"  ✅ {description}: 存在")
        else:
            print(f"  ❌ {description}: 不存在")
            all_exist = False
    
    return all_exist

def test_project_structure():
    """测试项目结构"""
    print("\n📁 测试项目结构...")
    
    required_dirs = [
        "src",
        "scripts", 
        "resources/example_pack",
        "ai_generator/models",
        "docs"
    ]
    
    required_files = [
        ".gitignore",
        "LICENSE",
        "README.md",
        "requirements.txt",
        "config.json",
        "src/__init__.py",
        "src/main.py",
        "src/converter.py",
        "src/ai_texture_generator.py",
        "src/texture_generator.py",
        "src/utils.py",
        "src/version_data.py",
        "src/fix_bom.py",
        "src/path_utils.py"
    ]
    
    all_good = True
    
    # 检查目录
    for dir_path in required_dirs:
        dir_full = project_root / dir_path
        if dir_full.exists():
            print(f"  ✅ 目录: {dir_path}")
        else:
            print(f"  ❌ 目录缺失: {dir_path}")
            all_good = False
    
    # 检查文件
    for file_path in required_files:
        file_full = project_root / file_path
        if file_full.exists():
            print(f"  ✅ 文件: {file_path}")
        else:
            print(f"  ❌ 文件缺失: {file_path}")
            all_good = False
    
    return all_good

def main():
    """主测试函数"""
    print("=" * 60)
    print("    Minecraft AI材质转换器 - 项目测试")
    print("=" * 60)
    print(f"项目路径: {project_root}")
    print()
    
    results = []
    
    # 1. 测试导入
    results.append(("模块导入", test_imports()))
    
    # 2. 测试项目结构
    results.append(("项目结构", test_project_structure()))
    
    # 3. 测试配置
    results.append(("路径配置", test_path_config()))
    
    # 4. 测试转换器
    results.append(("转换器", test_converter()))
    
    # 5. 测试脚本文件
    results.append(("脚本文件", test_script_files()))
    
    # 6. 创建测试材质包
    try:
        test_pack = create_test_pack()
        results.append(("测试材质包", True))
    except Exception as e:
        print(f"❌ 测试材质包创建失败: {e}")
        results.append(("测试材质包", False))
    
    # 显示结果
    print("\n" + "=" * 60)
    print("📊 测试结果:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！项目可以正常运行。")
        print("下一步:")
        print("1. 运行 scripts/install.bat 安装")
        print("2. 运行 scripts/start.bat 启动")
        print("3. 如需AI功能，运行 scripts/download_model.bat")
    else:
        print("⚠️  有测试失败，请检查错误信息。")
    
    print("=" * 60)
    
    # 等待用户按键
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()
