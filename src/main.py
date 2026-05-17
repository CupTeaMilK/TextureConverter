# src/main.py
import os
import sys
import time
import traceback
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.path_utils import get_project_root, get_ai_model_dir, setup_environment
from src.converter import TexturePackConverter

def main():
    print("=" * 50)
    print("    Minecraft材质包转换器 - AI增强版")
    print("=" * 50)
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # 设置环境
    ai_dir = setup_environment()
    
    # 检查AI模型是否存在
    ai_model_path = ai_dir / "v1-5-pruned.safetensors"
    ai_available = ai_model_path.exists()
    
    if ai_available:
        print("🤖 AI模型可用")
        print(f"   路径: {ai_dir}")
        print(f"   大小: {ai_model_path.stat().st_size / 1024**3:.1f} GB")
    else:
        print("🤖 AI模型未找到，将使用智能程序化生成")
        print(f"   如果需要AI生成，请下载模型到: {ai_dir}")
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
            use_ai = False  # 命令行模式默认不使用AI
            ai_model = "smart"
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
            
            print("✅ 文件存在，继续...")
            
            # 选择AI生成模式
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
            
            # 选择目标版本
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
        if ai_available and use_ai:
            print(f"   模式: {'🤖 AI生成' if ai_model == 'ai' else '🎯 智能生成'}")
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
    
    if len(sys.argv) <= 1:
        input("\n按Enter键退出...")

if __name__ == "__main__":
    main()
