# scripts/download_model.py
import os
import sys
import time
import json
from pathlib import Path

print("🤖 AI模型下载器")
print("=" * 60)

# 读取配置文件
config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 获取模型路径
model_dir = Path(config['paths']['models_dir'])
model_dir.mkdir(parents=True, exist_ok=True)

print(f"项目路径: {Path(__file__).parent.parent}")
print(f"模型目录: {model_dir}")
print()

# 设置环境变量
os.environ['HF_HOME'] = str(model_dir)
os.environ['TRANSFORMERS_CACHE'] = str(model_dir)
os.environ['DIFFUSERS_CACHE'] = str(model_dir)

# 检查依赖
print("🔍 检查依赖...")
try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
except ImportError:
    print("❌ PyTorch未安装")
    print("请先运行安装脚本")
    sys.exit(1)

try:
    import diffusers
    print(f"✅ diffusers: 已安装")
except ImportError:
    print("❌ diffusers未安装")
    print("请先运行安装脚本")
    sys.exit(1)

# 开始下载
print(f"\n🚀 开始下载AI模型...")
model_id = config['ai']['model_id']
print(f"模型: {model_id}")
print(f"大小: 约4.3GB")
print(f"保存到: {model_dir}")
print(f"请耐心等待，这需要较长时间...")
print()

try:
    from huggingface_hub import snapshot_download
    
    print(f"下载: {model_id}")
    print(f"使用镜像: https://hf-mirror.com")
    print()
    
    # 使用国内镜像
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    start_time = time.time()
    
    # 显示进度
    print("下载进度: [", end="", flush=True)
    
    # 下载模型
    snapshot_download(
        repo_id=model_id,
        cache_dir=str(model_dir),
        resume_download=True
    )
    
    end_time = time.time()
    
    print("] 100%")
    print()
    print(f"✅ 下载完成！")
    print(f"⏱️  耗时: {end_time - start_time:.1f}秒")
    
    # 验证文件
    print(f"\n🔍 验证文件...")
    safetensors = list(model_dir.rglob("*.safetensors"))
    if safetensors:
        size_gb = safetensors[0].stat().st_size / (1024**3)
        print(f"✅ 主模型文件: {size_gb:.1f} GB")
    
    index_file = list(model_dir.rglob("model_index.json"))
    if index_file:
        print(f"✅ 配置文件: 存在")
    
except KeyboardInterrupt:
    print("\n⚠️ 下载被中断")
    print("可以重新运行继续下载")
except Exception as e:
    print(f"\n❌ 下载失败: {e}")
    print(f"\n💡 解决方案:")
    print("1. 手动下载: https://hf-mirror.com/runwayml/stable-diffusion-v1-5")
    print("2. 下载文件: v1-5-pruned.safetensors 和 model_index.json")
    print(f"3. 保存到: {model_dir}")

print()
input("按Enter键退出...")
