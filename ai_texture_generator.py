import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np
import cv2
from texture_generator import SmartTextureGenerator

class AITextureGenerator:
    def __init__(self, use_gpu=True):
        # 动态计算项目根目录（假设脚本位于 src/ 目录下）
        self.project_root = Path(__file__).parent.parent  # 向上两级到项目根目录
        self.ai_dir = self.project_root / "ai_generator"   # AI模型根目录
        self.models_dir = self.ai_dir / "models"          # 模型存放目录
        self.output_dir = self.ai_dir / "test_output"     # 测试输出目录
        
        # 确保目录存在
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置环境变量（供HuggingFace库使用）
        os.environ["HF_HOME"] = str(self.models_dir)
        os.environ["TRANSFORMERS_CACHE"] = str(self.models_dir)
        os.environ["DIFFUSERS_CACHE"] = str(self.models_dir)
        
        # 初始化纹理生成器
        self.generator = SmartTextureGenerator()
        
    def generate_texture_with_ai(self, item_info, size=16):
        """使用AI生成材质（带后处理）"""
        # 1. 生成基础纹理（AI模型生成）
        base_texture = self._generate_base_texture(item_info, size)
        
        # 2. 后处理（颜色匹配、对比度增强等）
        target_color = self._hex_to_rgb(item_info.get("color", "#FFFFFF"))
        processed_texture = self._post_process_texture(base_texture, target_color, item_info.get("item_type", "block"))
        
        return processed_texture
    
    def _generate_base_texture(self, item_info, size):
        """调用AI模型生成基础纹理（示例逻辑，需根据实际模型调整）"""
        # 这里应调用实际的AI模型生成逻辑
        # 示例：使用SmartTextureGenerator作为回退
        return self.generator.generate_smart_texture(item_info, size)
    
    def _post_process_texture(self, image, target_color, item_type):
        """后处理生成的材质"""
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 调整颜色平衡
        img_array = self._adjust_color_balance(img_array, target_color)
        
        # 增强对比度
        img_array = self._enhance_contrast(img_array)
        
        # 锐化边缘
        img_array = self._sharpen_edges(img_array)
        
        # 像素化处理（针对方块/矿石）
        if item_type in ["ore", "block", "stone", "wood"]:
            img_array = self._pixelate(img_array, scale_factor=2)
        
        # 转换为PIL图像并调整大小
        result = Image.fromarray(img_array)
        return result.resize((16, 16), Image.Resampling.NEAREST)
    
    def _adjust_color_balance(self, image_array, target_color):
        """调整颜色平衡"""
        current_mean = image_array.mean(axis=(0, 1))
        color_shift = np.array(target_color) - current_mean
        adjusted = image_array.astype(np.float32) + color_shift * 0.3
        return np.clip(adjusted, 0, 255).astype(np.uint8)
    
    def _enhance_contrast(self, image_array):
        """增强对比度（使用CLAHE）"""
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)
        
        lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = enhanced_gray
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    def _sharpen_edges(self, image_array):
        """锐化边缘"""
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return np.clip(cv2.filter2D(image_array, -1, kernel), 0, 255)
    
    def _pixelate(self, image_array, scale_factor=2):
        """像素化处理"""
        h, w = image_array.shape[:2]
        small = cv2.resize(image_array, (w // scale_factor, h // scale_factor), 
                          interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    
    def _hex_to_rgb(self, hex_color):
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def test_ai_generator():
    """测试AI生成器（使用相对路径）"""
    print("🧪 测试修复版AI生成器（相对路径）")
    print("=" * 50)
    
    # 打印路径信息（调试用）
    print(f"项目根目录: {Path(__file__).parent.parent}")
    print(f"AI模型目录: {Path(__file__).parent.parent / 'ai_generator'}")
    print(f"模型存放目录: {Path(__file__).parent.parent / 'ai_generator' / 'models'}")
    
    # 检查模型目录是否存在
    models_dir = Path(__file__).parent.parent / "ai_generator" / "models"
    if models_dir.exists():
        print(f"✅ 模型目录已存在: {models_dir}")
        print("目录内容:", list(models_dir.iterdir()) if models_dir.iterdir() else "空")
    else:
        print(f"⚠️ 模型目录不存在，将自动创建: {models_dir}")
    
    # 初始化生成器
    try:
        generator = AITextureGenerator(use_gpu=True)
        
        # 测试数据
        test_item = {
            "id": "minecraft:test_copper_ore",
            "item_type": "ore",
            "color": "#D2691E",
            "similar_to": ["minecraft:iron_ore"]
        }
        
        print(f"\n尝试生成测试材质...")
        texture = generator.generate_texture_with_ai(test_item, size=16)
        
        # 保存测试结果
        output_path = generator.output_dir / "ai_test_result.png"
        texture.save(output_path)
        
        print(f"✅ 测试完成！结果保存至: {output_path}")
        print(f"   尺寸: {texture.size} | 模式: {texture.mode}")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_ai_generator()
    input("\n按Enter键退出...")
