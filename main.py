# main.py
import os
import sys
import time
import traceback
from pathlib import Path
from converter import TexturePackConverter

def main():
    print("=" * 50)
    print("    Minecraft材质包转换器 - AI增强版")
    print("=" * 50)
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # ========== 第一步：设置AI模型路径 ==========
    # 获取项目根目录
    PROJECT_ROOT = Path(__file__).parent  # 修改了这里：从 .parent.parent 改为 .parent
    
    # 调试信息
    print(f"🔧 调试信息:")
    print(f"   当前文件: {__file__}")
    print(f"   父目录: {Path(__file__).parent}")
    print(f"   项目根目录: {PROJECT_ROOT}")
    print()
    
    # 使用相对路径设置AI模型路径
    AI_DIR = PROJECT_ROOT / "ai_generator"
    print(f"   AI目录: {AI_DIR}")
    print(f"   AI目录存在: {AI_DIR.exists()}")
    print()
    
    os.environ['HF_HOME'] = str(AI_DIR / "models")
    os.environ['TRANSFORMERS_CACHE'] = os.environ['HF_HOME']
    os.environ['DIFFUSERS_CACHE'] = os.environ['HF_HOME']
    
    # 确保AI目录存在
    AI_DIR.mkdir(parents=True, exist_ok=True)
    (AI_DIR / "models").mkdir(parents=True, exist_ok=True)
    
    # 检查AI模型是否存在
    ai_model_path = AI_DIR / "models" / "v1-5-pruned.safetensors"
    ai_available = ai_model_path.exists()
    
    print(f"   AI模型路径: {ai_model_path}")
    print(f"   AI模型存在: {ai_model_path.exists()}")
    if ai_model_path.exists():
        print(f"   AI模型大小: {ai_model_path.stat().st_size / 1024**3:.1f} GB")
    print()
    
    if ai_available:
        print("🤖 AI模型可用")
        print(f"   路径: {os.environ['HF_HOME']}")
        print(f"   大小: {ai_model_path.stat().st_size / 1024**3:.1f} GB")
    else:
        print("🤖 AI模型未找到，将使用智能程序化生成")
        print(f"   如果需要AI生成，请下载模型到: {AI_DIR / 'models'}")
    print()
    
    try:
        # 检查输入参数
        if len(sys.argv) > 1:
            # 命令行模式
            input_zip = sys.argv[1]
            if len(sys.argv) > 2:
                target_version = sys.argv[2]
            else:
                target_version = "1.21.11"
            
            # 检查是否有AI模式参数
            use_ai = False
            ai_model = "smart"
            if len(sys.argv) > 3:
                if sys.argv[3] == "--ai":
                    use_ai = True
                    ai_model = "ai"
                elif sys.argv[3] == "--smart":
                    use_ai = True
                    ai_model = "smart"
                elif sys.argv[3] == "--basic":
                    use_ai = False
                    ai_model = None
        else:
            # 交互模式
            print("📂 请将材质包.zip文件拖拽到此处，然后按Enter:")
            try:
                input_zip = input().strip('"')
            except KeyboardInterrupt:
                print("\n\n❌ 用户取消操作")
                input("按Enter键退出...")
                return
            
            print(f"🔍 检查文件是否存在: {input_zip}")
            
            if not os.path.exists(input_zip):
                print(f"❌ 文件不存在: {input_zip}")
                input("按Enter键退出...")
                return
            
            # 检查文件是否.zip格式
            if not input_zip.lower().endswith('.zip'):
                print(f"❌ 文件格式错误: 需要.zip文件")
                input("按Enter键退出...")
                return
            
            print("✅ 文件存在，继续...")
            
            # ========== 第二步：选择AI生成模式 ==========
            print("\n🎨 请选择材质生成模式:")
            
            if ai_available:
                print("  1) 🤖 AI深度学习生成 (高质量，速度慢)")
                print("  2) 🎯 智能程序化生成 (中等质量，速度快)")
                print("  3) ⚡ 基础占位符生成 (低质量，最快)")
            else:
                print("  1) 🎯 智能程序化生成 (中等质量，速度快)")
                print("  2) ⚡ 基础占位符生成 (低质量，最快)")
                print("  (AI功能不可用，需要下载AI模型)")
            
            try:
                gen_choice = input(f"请输入数字 (1-{'3' if ai_available else '2'}): ").strip()
            except KeyboardInterrupt:
                print("\n\n❌ 用户取消操作")
                input("按Enter键退出...")
                return
            
            # 设置AI参数
            if ai_available:
                if gen_choice == "1":
                    use_ai = True
                    ai_model = "ai"
                    print("🎨 已选择: AI深度学习生成")
                elif gen_choice == "2":
                    use_ai = True
                    ai_model = "smart"
                    print("🎨 已选择: 智能程序化生成")
                else:
                    use_ai = False
                    ai_model = None
                    print("🎨 已选择: 基础占位符生成")
            else:
                if gen_choice == "1":
                    use_ai = True
                    ai_model = "smart"
                    print("🎨 已选择: 智能程序化生成")
                else:
                    use_ai = False
                    ai_model = None
                    print("🎨 已选择: 基础占位符生成")
            
            print()
            
            # ========== 第三步：选择目标版本 ==========
            print("\n🎯 请选择目标版本:")
            print("  1) 1.16.5")
            print("  2) 1.17.1")
            print("  3) 1.18.2")
            print("  4) 1.19.4")
            print("  5) 1.20.6")
            print("  6) 1.21.5")
            print("  7) 1.21.11")
            print("  8) 自定义版本")
            
            try:
                choice = input("请输入数字 (1-8): ").strip()
            except KeyboardInterrupt:
                print("\n\n❌ 用户取消操作")
                input("按Enter键退出...")
                return
            
            version_map = {
                "1": "1.16.5",
                "2": "1.17.1",
                "3": "1.18.2",
                "4": "1.19.4",
                "5": "1.20.6",
                "6": "1.21.5",
                "7": "1.21.11"
            }
            
            if choice in version_map:
                target_version = version_map[choice]
            elif choice == "8":
                try:
                    target_version = input("请输入自定义版本号 (如 1.21.11): ").strip()
                except KeyboardInterrupt:
                    print("\n\n❌ 用户取消操作")
                    input("按Enter键退出...")
                    return
            else:
                target_version = "1.21.11"
        
        print(f"\n🔧 开始转换:")
        print(f"   输入: {input_zip}")
        print(f"   目标: {target_version}")
        if use_ai and ai_model == "ai":
            print(f"   模式: 🤖 AI生成")
        elif use_ai and ai_model == "smart":
            print(f"   模式: 🎯 智能生成")
        else:
            print(f"   模式: ⚡ 基础生成")
        print(f"   开始时间: {time.strftime('%H:%M:%S')}")
        print()
        
        # 创建转换器并执行
        converter = TexturePackConverter(use_ai=use_ai, ai_model=ai_model)
        
        print("⏳ 正在初始化转换器...")
        start_time = time.time()
        
        success = converter.convert(input_zip, target_version)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if success:
            print(f"\n✅ 转换成功！耗时: {elapsed:.2f}秒")
        else:
            print(f"\n❌ 转换失败！耗时: {elapsed:.2f}秒")
            
    except KeyboardInterrupt:
        print("\n\n❌ 转换被用户中断")
    except Exception as e:
        print(f"\n❌ 转换过程中发生错误: {e}")
        print("详细错误信息:")
        traceback.print_exc()
    finally:
        print(f"\n结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
    
    if len(sys.argv) <= 1:
        input("\n按Enter键退出...")

# 添加启动功能测试
def test_launch():
    """测试启动功能"""
    print("🔧 测试启动功能")
    print("-" * 30)
    
    # 打印路径信息
    PROJECT_ROOT = Path(__file__).parent  # 修改了这里：从 .parent.parent 改为 .parent
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"Python文件: {__file__}")
    
    # 检查必要目录
    ai_dir = PROJECT_ROOT / "ai_generator"
    print(f"AI目录: {ai_dir}")
    print(f"AI目录存在: {ai_dir.exists()}")
    
    if ai_dir.exists():
        models_dir = ai_dir / "models"
        print(f"模型目录: {models_dir}")
        print(f"模型目录存在: {models_dir.exists()}")
        
        if models_dir.exists():
            safetensors_files = list(models_dir.glob("*.safetensors"))
            print(f"找到.safetensors文件: {len(safetensors_files)} 个")
            for file in safetensors_files:
                print(f"  - {file.name} ({file.stat().st_size / 1024**3:.2f} GB)")
    
    print("-" * 30)
    print("测试完成，按Enter键启动主程序...")
    input()
    
    # 启动主程序
    main()

if __name__ == "__main__":
    # 检查是否在命令行模式下运行
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_launch()
    else:
        main()
