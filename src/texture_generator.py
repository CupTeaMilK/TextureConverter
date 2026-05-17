# src/texture_generator.py
import random
from PIL import Image, ImageDraw, ImageFilter
import colorsys
import math
from typing import Dict, Any, Tuple

class SmartTextureGenerator:
    def __init__(self):
        """初始化智能材质生成器"""
        self.color_cache = {}
    
    def generate_smart_texture(self, item_data: Dict[str, Any], size: int = 16) -> Image.Image:
        """
        智能程序化生成材质
        
        Args:
            item_data: 物品数据
            size: 材质大小
            
        Returns:
            PIL.Image: 生成的材质
        """
        item_type = item_data.get("item_type", "block")
        color_hex = item_data.get("color", "#808080")
        
        # 根据物品类型选择生成方法
        if item_type == "ore":
            return self._generate_ore_texture(color_hex, size)
        elif item_type == "crystal":
            return self._generate_crystal_texture(color_hex, size)
        elif item_type == "plant":
            return self._generate_plant_texture(color_hex, size)
        elif item_type == "wood":
            return self._generate_wood_texture(color_hex, size)
        elif item_type == "metal":
            return self._generate_metal_texture(color_hex, size)
        elif item_type == "stone":
            return self._generate_stone_texture(color_hex, size)
        elif item_type == "tool" or item_type == "weapon":
            return self._generate_tool_texture(color_hex, size)
        else:
            return self._generate_default_texture(color_hex, size)
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """RGB转十六进制颜色"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _adjust_color_brightness(self, rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """调整颜色亮度"""
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        v = max(0, min(1, v * factor))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r*255), int(g*255), int(b*255))
    
    def _generate_ore_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成矿石纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.7)
        light_color = self._adjust_color_brightness(base_color, 1.3)
        
        img = Image.new('RGB', (size, size), dark_color)
        pixels = img.load()
        
        # 添加矿物斑点
        random.seed(hash(color_hex))
        for _ in range(size * 2):
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            
            if random.random() < 0.3:  # 亮色斑点
                color = light_color
            else:  # 基础色斑点
                color = base_color
            
            radius = random.randint(1, 2)
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        if dx*dx + dy*dy <= radius*radius:
                            pixels[nx, ny] = color
        
        return img
    
    def _generate_crystal_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成水晶纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.6)
        light_color = self._adjust_color_brightness(base_color, 1.4)
        
        img = Image.new('RGB', (size, size), dark_color)
        draw = ImageDraw.Draw(img)
        
        # 绘制水晶面
        center = size // 2
        points = []
        
        for i in range(6):
            angle = i * math.pi / 3
            radius = size // 2 - 1
            if i % 2 == 0:
                radius = radius * 0.7
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append((x, y))
        
        # 填充多边形
        draw.polygon(points, fill=base_color, outline=light_color)
        
        # 添加高光
        for i in range(3):
            x1 = center + (size//4) * math.cos(i * 2 * math.pi / 3)
            y1 = center + (size//4) * math.sin(i * 2 * math.pi / 3)
            draw.ellipse([x1-1, y1-1, x1+1, y1+1], fill=light_color)
        
        return img
    
    def _generate_wood_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成木头纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.8)
        light_color = self._adjust_color_brightness(base_color, 1.2)
        
        img = Image.new('RGB', (size, size), base_color)
        pixels = img.load()
        
        # 添加木纹
        random.seed(hash(color_hex))
        for x in range(size):
            # 创建波浪形木纹
            wave = int(math.sin(x * 0.5) * 1)
            for y in range(size):
                if (y + wave) % 4 == 0:
                    pixels[x, y] = dark_color
                elif (y + wave) % 4 == 2:
                    pixels[x, y] = light_color
        
        return img
    
    def _generate_stone_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成石头纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.7)
        light_color = self._adjust_color_brightness(base_color, 1.3)
        
        img = Image.new('RGB', (size, size), base_color)
        pixels = img.load()
        
        # 添加石头纹理
        random.seed(hash(color_hex))
        for x in range(size):
            for y in range(size):
                if random.random() < 0.3:
                    pixels[x, y] = dark_color
                elif random.random() < 0.1:
                    pixels[x, y] = light_color
        
        return img
    
    def _generate_metal_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成金属纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.5)
        light_color = self._adjust_color_brightness(base_color, 1.5)
        
        img = Image.new('RGB', (size, size), base_color)
        draw = ImageDraw.Draw(img)
        
        # 添加金属光泽
        for i in range(size//2):
            color = self._adjust_color_brightness(base_color, 0.5 + i/size)
            draw.line([(i, i), (size-i-1, i)], fill=color, width=1)
            draw.line([(i, i), (i, size-i-1)], fill=color, width=1)
            draw.line([(size-i-1, i), (size-i-1, size-i-1)], fill=color, width=1)
            draw.line([(i, size-i-1), (size-i-1, size-i-1)], fill=color, width=1)
        
        return img
    
    def _generate_plant_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成植物纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.6)
        light_color = self._adjust_color_brightness(base_color, 1.4)
        
        img = Image.new('RGB', (size, size), base_color)
        pixels = img.load()
        
        # 添加叶片纹理
        random.seed(hash(color_hex))
        for x in range(size):
            for y in range(size):
                if (x + y) % 3 == 0:
                    pixels[x, y] = dark_color
                elif (x + y) % 5 == 0:
                    pixels[x, y] = light_color
        
        return img
    
    def _generate_tool_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成工具纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.4)
        light_color = self._adjust_color_brightness(base_color, 1.6)
        
        img = Image.new('RGB', (size, size), base_color)
        draw = ImageDraw.Draw(img)
        
        # 绘制简单工具形状
        center = size // 2
        
        # 手柄
        draw.rectangle([center-1, 2, center, size-3], fill=dark_color)
        
        # 头部
        if size >= 8:
            draw.rectangle([center-3, 2, center+2, 5], fill=light_color)
            draw.rectangle([center-2, 5, center+1, 6], fill=base_color)
        
        return img
    
    def _generate_default_texture(self, color_hex: str, size: int) -> Image.Image:
        """生成默认纹理"""
        base_color = self._hex_to_rgb(color_hex)
        dark_color = self._adjust_color_brightness(base_color, 0.8)
        light_color = self._adjust_color_brightness(base_color, 1.2)
        
        img = Image.new('RGB', (size, size), base_color)
        pixels = img.load()
        
        # 添加简单纹理
        for x in range(size):
            for y in range(size):
                if (x + y) % 2 == 0:
                    pixels[x, y] = dark_color
                else:
                    pixels[x, y] = light_color
        
        return img
