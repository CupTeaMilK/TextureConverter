# src/ai_texture_generator.py
import os
import sys
import torch
from pathlib import Path
from PIL import Image
import numpy as np
from typing import Dict, Any, Optional
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.path_utils import get_ai_model_dir, setup_environment

class AITextureGenerator:
    def __init__(self, use_gpu=True, model_id="runwayml/stable-diffusion-v1-5"):
        """
        初始化AI材质生成器
        
        Args:
            use_gpu: 是否使用GPU加速
            model_id: 模型ID
        """
        self.use_gpu = use_gpu
        self.model_id = model_id
        self.model_loaded = False
        self.pipe = None
        
        # 设置环境
        self.ai_dir = setup_environment()
        
        # 检查是否有模型文件
        self.model_path = self.ai_dir / "v1-5-pruned.safetensors"
        self.config_path = self.ai_dir / "model_index.json"
        
        if not self.model_path.exists() or not self.config_path.exists():
            print("⚠️  AI模型文件不完整")
            print(f"   请运行 scripts/download_model.bat 下载模型")
            print(f"   或手动下载文件到: {self.ai_dir}")
            self.model_available = False
        else:
            self.model_available = True
        
    def load_models(self):
        """加载AI模型"""
        if not self.model_available:
            raise Exception("AI模型不可用，请先下载模型")
        
        if self.model_loaded:
            return
        
        print("🤖 正在加载AI模型，这需要一些时间...")
        start_time = time.time()
        
        try:
            from diffusers import StableDiffusionPipeline
            
            # 设置设备
            device = "cuda" if (self.use_gpu and torch.cuda.is_available()) else "cpu"
            print(f"   使用设备: {device}")
            
            # 加载模型
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                cache_dir=str(self.ai_dir),
                safety_checker=None
            )
            
            # 移动到设备
            self.pipe.to(device)
            
            # 启用注意力切片以节省内存
            if device == "cuda":
                self.pipe.enable_attention_slicing()
            
            self.model_loaded = True
            end_time = time.time()
            print(f"✅ AI模型加载完成，耗时: {end_time - start_time:.1f}秒")
            
        except Exception as e:
            print(f"❌ AI模型加载失败: {e}")
            raise
    
    def generate_texture_with_ai(self, item_data: Dict[str, Any], size: int = 16, 
                                num_inference_steps: int = 20) -> Image.Image:
        """
        使用AI生成材质
        
        Args:
            item_data: 物品数据
            size: 生成图片大小
            num_inference_steps: 推理步数
            
        Returns:
            PIL.Image: 生成的材质图片
        """
        if not self.model_loaded:
            self.load_models()
        
        # 生成提示词
        prompt = self._create_prompt(item_data)
        
        print(f"🎨 AI生成: {item_data['id']}")
        print(f"   提示词: {prompt}")
        print(f"   大小: {size}x{size}")
        
        try:
            # 生成图片
            image = self.pipe(
                prompt=prompt,
                negative_prompt="ugly, blurry, low quality, distorted, watermark, text",
                height=size,
                width=size,
                num_inference_steps=num_inference_steps,
                guidance_scale=7.5
            ).images[0]
            
            # 调整大小到标准材质尺寸
            if image.size != (size, size):
                image = image.resize((size, size), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            print(f"❌ AI生成失败: {e}")
            # 返回占位符图片
            return self._create_fallback_texture(item_data, size)
    
    def _create_prompt(self, item_data: Dict[str, Any]) -> str:
        """根据物品数据创建提示词"""
        item_id = item_data.get("id", "")
        item_type = item_data.get("item_type", "block")
        color_hex = item_data.get("color", "#808080")
        
        # 基础描述
        if "ore" in item_id or item_type == "ore":
            base = "Minecraft ore texture"
        elif "block" in item_id or item_type == "block":
            base = "Minecraft block texture"
        elif "crystal" in item_id or item_type == "crystal":
            base = "Minecraft crystal texture"
        elif "plant" in item_id or item_type == "plant":
            base = "Minecraft plant texture"
        elif "wood" in item_id or item_type == "wood":
            base = "Minecraft wood texture"
        elif "metal" in item_id or item_type == "metal":
            base = "Minecraft metal texture"
        elif "tool" in item_id or item_type == "tool":
            base = "Minecraft tool texture"
        elif "weapon" in item_id or item_type == "weapon":
            base = "Minecraft weapon texture"
        else:
            base = "Minecraft texture"
        
        # 颜色描述
        color_name = self._get_color_name(color_hex)
        
        # 风格描述
        style = "pixel art, 16x16 texture, Minecraft style, clean edges, no aliasing"
        
        # 组合提示词
        prompt = f"{base}, {color_name} color, {style}, high quality texture"
        
        return prompt
    
    def _get_color_name(self, hex_color: str) -> str:
        """获取颜色名称"""
        color_map = {
            "#FF0000": "red",
            "#00FF00": "green", 
            "#0000FF": "blue",
            "#FFFF00": "yellow",
            "#FF00FF": "magenta",
            "#00FFFF": "cyan",
            "#FFA500": "orange",
            "#800080": "purple",
            "#A52A2A": "brown",
            "#000000": "black",
            "#FFFFFF": "white",
            "#808080": "gray",
            "#C0C0C0": "silver",
            "#FFD700": "gold",
            "#D2691E": "copper",
            "#228B22": "forest green",
            "#696969": "dark gray",
            "#8B4513": "saddle brown",
            "#9966CC": "amethyst"
        }
        return color_map.get(hex_color.upper(), "colored")
    
    def _create_fallback_texture(self, item_data: Dict[str, Any], size: int) -> Image.Image:
        """创建回退纹理"""
        from PIL import ImageDraw
        
        img = Image.new('RGB', (size, size), (128, 128, 128))
        draw = ImageDraw.Draw(img)
        
        # 画一个简单的X
        draw.line([(0, 0), (size-1, size-1)], fill=(255, 0, 0), width=1)
        draw.line([(size-1, 0), (0, size-1)], fill=(255, 0, 0), width=1)
        
        return img
    
    def check_model_status(self) -> Dict[str, Any]:
        """检查模型状态"""
        return {
            "model_available": self.model_available,
            "model_loaded": self.model_loaded,
            "model_path": str(self.model_path),
            "model_exists": self.model_path.exists(),
            "config_exists": self.config_path.exists(),
            "ai_dir": str(self.ai_dir)
        }
