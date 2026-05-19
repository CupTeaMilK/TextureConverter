# texture_generator.py
import os
import colorsys
import random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

class SmartTextureGenerator:
    def __init__(self, reference_textures_dir=None):
        """初始化智能材质生成器"""
        self.reference_dir = reference_textures_dir
        
    def hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        """将RGB转换为十六进制颜色"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
    def generate_smart_texture(self, item_info, size=16):
        """生成智能材质"""
        item_id = item_info.get("id", "unknown")
        item_type = item_info.get("item_type", "block")
        base_color = self.hex_to_rgb(item_info.get("color", "#808080"))
        similar_items = item_info.get("similar_to", [])
        
        print(f"  🎨 生成智能材质: {item_id} ({item_type})")
        
        # 根据物品类型使用不同的生成算法
        if item_type == "ore":
            return self._generate_ore_texture(base_color, size)
        elif item_type == "block":
            return self._generate_block_texture(base_color, size)
        elif item_type == "crystal":
            return self._generate_crystal_texture(base_color, size)
        elif item_type == "plant":
            return self._generate_plant_texture(base_color, size)
        elif item_type == "stone":
            return self._generate_stone_texture(base_color, size)
        elif item_type == "wood":
            return self._generate_wood_texture(base_color, size)
        elif item_type == "metal":
            return self._generate_metal_texture(base_color, size)
        elif item_type == "tool" or item_type == "weapon":
            return self._generate_tool_texture(base_color, size)
        elif item_type == "material":
            return self._generate_material_texture(base_color, size)
        elif item_type == "food":
            return self._generate_food_texture(base_color, size)
        else:
            return self._generate_generic_texture(base_color, item_id, size)
    
    def _generate_ore_texture(self, base_color, size=16):
        """生成矿石纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建基础矿石颜色
        ore_color = tuple(max(0, min(255, c - 20)) for c in base_color)
        
        # 填充背景
        for x in range(size):
            for y in range(size):
                # 添加一些随机噪点
                noise = random.randint(-15, 15)
                r = max(0, min(255, ore_color[0] + noise))
                g = max(0, min(255, ore_color[1] + noise))
                b = max(0, min(255, ore_color[2] + noise))
                img.putpixel((x, y), (r, g, b, 255))
        
        # 添加矿物斑点
        draw = ImageDraw.Draw(img)
        mineral_color = tuple(min(255, c + 50) for c in base_color)
        
        for _ in range(random.randint(3, 8)):
            x = random.randint(2, size-3)
            y = random.randint(2, size-3)
            radius = random.randint(1, 2)
            
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    if 0 <= x+dx < size and 0 <= y+dy < size:
                        if dx*dx + dy*dy <= radius*radius:
                            # 矿物斑点更亮
                            r = min(255, mineral_color[0] + random.randint(-10, 10))
                            g = min(255, mineral_color[1] + random.randint(-10, 10))
                            b = min(255, mineral_color[2] + random.randint(-10, 10))
                            img.putpixel((x+dx, y+dy), (r, g, b, 255))
        
        return img
    
    def _generate_block_texture(self, base_color, size=16):
        """生成方块纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建基础纹理
        for x in range(size):
            for y in range(size):
                # 添加轻微的渐变和噪点
                gradient = (x + y) / (size * 2) * 20
                noise = random.randint(-5, 5)
                
                r = max(0, min(255, base_color[0] - int(gradient) + noise))
                g = max(0, min(255, base_color[1] - int(gradient) + noise))
                b = max(0, min(255, base_color[2] - int(gradient) + noise))
                
                img.putpixel((x, y), (r, g, b, 255))
        
        # 添加简单的纹理细节
        draw = ImageDraw.Draw(img)
        for i in range(0, size, 4):
            draw.line([(i, 0), (i, size-1)], fill=(0, 0, 0, 30), width=1)
            draw.line([(0, i), (size-1, i)], fill=(0, 0, 0, 30), width=1)
        
        return img
    
    def _generate_crystal_texture(self, base_color, size=16):
        """生成水晶/宝石纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建闪烁效果
        for x in range(size):
            for y in range(size):
                # 创建菱形图案
                center_x, center_y = size/2, size/2
                distance = abs(x - center_x) + abs(y - center_y)
                
                # 根据距离调整亮度
                brightness = 1.0 - (distance / (size/2)) * 0.5
                brightness = max(0.3, min(1.0, brightness))
                
                # 添加随机闪烁
                sparkle = random.random() * 0.3 + 0.7
                
                r = int(base_color[0] * brightness * sparkle)
                g = int(base_color[1] * brightness * sparkle)
                b = int(base_color[2] * brightness * sparkle)
                
                # 边缘透明
                alpha = 255
                if distance > size/2 - 2:
                    alpha = int(255 * (1.0 - (distance - size/2 + 2) / 2))
                
                img.putpixel((x, y), (r, g, b, alpha))
        
        return img
    
    def _generate_plant_texture(self, base_color, size=16):
        """生成植物纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建叶子纹理
        leaf_color = base_color
        stem_color = tuple(max(0, c - 40) for c in base_color)
        
        # 绘制叶子形状
        draw = ImageDraw.Draw(img)
        
        # 主叶脉
        draw.line([(size//2, 2), (size//2, size-3)], fill=stem_color, width=1)
        
        # 侧叶脉
        for i in range(3, size-3, 3):
            angle = random.uniform(0.3, 0.7)
            length = random.randint(3, 6)
            
            # 左侧叶脉
            draw.line([(size//2, i), (int(size//2 - length * angle), i)], fill=stem_color, width=1)
            # 右侧叶脉
            draw.line([(size//2, i), (int(size//2 + length * angle), i)], fill=stem_color, width=1)
        
        # 填充叶肉
        for x in range(size):
            for y in range(size):
                # 检查是否在叶子范围内
                if abs(x - size//2) < size//2 - 2 and 2 < y < size-2:
                    # 距离叶脉的距离
                    dist_to_vein = min(abs(x - size//2), size//2)
                    
                    # 根据距离调整颜色
                    fade = 1.0 - (dist_to_vein / (size//2)) * 0.3
                    noise = random.randint(-10, 10)
                    
                    r = int(leaf_color[0] * fade + noise)
                    g = int(leaf_color[1] * fade + noise)
                    b = int(leaf_color[2] * fade + noise)
                    
                    # 确保颜色在有效范围内
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    
                    img.putpixel((x, y), (r, g, b, 255))
        
        return img
    
    def _generate_stone_texture(self, base_color, size=16):
        """生成石头纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建石头纹理
        for x in range(size):
            for y in range(size):
                # 添加大量的噪点
                noise = random.randint(-25, 25)
                
                r = max(0, min(255, base_color[0] + noise))
                g = max(0, min(255, base_color[1] + noise))
                b = max(0, min(255, base_color[2] + noise))
                
                img.putpixel((x, y), (r, g, b, 255))
        
        # 添加一些裂纹
        draw = ImageDraw.Draw(img)
        for _ in range(random.randint(1, 3)):
            start_x = random.randint(2, size-3)
            start_y = random.randint(2, size-3)
            
            for i in range(random.randint(2, 5)):
                end_x = start_x + random.randint(-2, 2)
                end_y = start_y + random.randint(-2, 2)
                
                if 0 <= end_x < size and 0 <= end_y < size:
                    crack_color = tuple(max(0, c - 30) for c in base_color)
                    draw.line([(start_x, start_y), (end_x, end_y)], fill=crack_color, width=1)
                
                start_x, start_y = end_x, end_y
        
        return img
    
    def _generate_metal_texture(self, base_color, size=16):
        """生成金属纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建金属光泽
        for x in range(size):
            for y in range(size):
                # 创建渐变效果
                gradient = (x + y) / (size * 2) * 100
                
                # 金属光泽
                if (x + y) % 3 == 0:
                    highlight = 30
                else:
                    highlight = 0
                
                r = max(0, min(255, base_color[0] - int(gradient) + highlight))
                g = max(0, min(255, base_color[1] - int(gradient) + highlight))
                b = max(0, min(255, base_color[2] - int(gradient) + highlight))
                
                img.putpixel((x, y), (r, g, b, 255))
        
        return img
    
    def _generate_tool_texture(self, base_color, size=16):
        """生成工具/武器纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 工具通常是金属材质
        tool_color = base_color
        handle_color = tuple(max(0, c - 80) for c in base_color)  # 手柄颜色较深
        
        draw = ImageDraw.Draw(img)
        
        # 绘制工具轮廓（简单的剑/工具形状）
        # 手柄
        draw.rectangle([(size//2-1, 2), (size//2+1, size-4)], fill=handle_color)
        
        # 工具头部
        if random.choice([True, False]):
            # 剑形状
            draw.polygon([(size//2, 2), (size//2-3, 8), (size//2+3, 8)], fill=tool_color)
        else:
            # 工具头
            draw.rectangle([(size//2-2, 2), (size//2+2, 6)], fill=tool_color)
        
        return img
    
    def _generate_material_texture(self, base_color, size=16):
        """生成材料纹理（锭、宝石等）"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建锭/宝石形状
        draw = ImageDraw.Draw(img)
        
        # 绘制一个菱形（类似宝石）或矩形（类似锭）
        if random.choice([True, False]):
            # 菱形（宝石）
            points = [
                (size//2, 2),           # 上
                (size-3, size//2),      # 右
                (size//2, size-3),      # 下
                (2, size//2)            # 左
            ]
            draw.polygon(points, fill=tuple(base_color))
            
            # 添加高光
            highlight_color = tuple(min(255, c + 50) for c in base_color)
            draw.polygon([(size//2, 4), (size-5, size//2), (size//2, size-5), (4, size//2)], 
                        fill=highlight_color)
        else:
            # 矩形（锭）
            draw.rectangle([(3, 4), (size-4, size-3)], fill=tuple(base_color))
            
            # 添加3D效果
            draw.rectangle([(3, 4), (size-4, 6)], fill=tuple(min(255, c + 30) for c in base_color))  # 上边
            draw.rectangle([(size-6, 4), (size-4, size-3)], fill=tuple(min(255, c + 20) for c in base_color))  # 右边
        
        return img
    
    def _generate_food_texture(self, base_color, size=16):
        """生成食物纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建圆形食物
        center_x, center_y = size//2, size//2
        radius = size//2 - 2
        
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形食物
        draw.ellipse([(center_x-radius, center_y-radius), 
                     (center_x+radius, center_y+radius)], 
                     fill=tuple(base_color))
        
        # 添加纹理细节
        for _ in range(random.randint(3, 6)):
            x = random.randint(center_x-radius+2, center_x+radius-2)
            y = random.randint(center_y-radius+2, center_y+radius-2)
            
            if (x-center_x)**2 + (y-center_y)**2 < (radius-2)**2:
                spot_color = tuple(max(0, c + random.randint(-20, 20)) for c in base_color)
                draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=spot_color)
        
        return img
    
    def _generate_generic_texture(self, base_color, item_id, size=16):
        """生成通用纹理"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 简单的网格纹理
        for x in range(size):
            for y in range(size):
                # 添加轻微噪点
                noise = random.randint(-10, 10)
                
                r = max(0, min(255, base_color[0] + noise))
                g = max(0, min(255, base_color[1] + noise))
                b = max(0, min(255, base_color[2] + noise))
                
                img.putpixel((x, y), (r, g, b, 255))
        
        # 添加物品名称缩写
        draw = ImageDraw.Draw(img)
        item_name = item_id.split(':')[-1]
        
        if len(item_name) > 4:
            text = item_name[:4]
        else:
            text = item_name
        
        try:
            # 计算文字颜色（对比色）
            brightness = (base_color[0] * 0.299 + base_color[1] * 0.587 + base_color[2] * 0.114)
            text_color = (255, 255, 255, 255) if brightness < 128 else (0, 0, 0, 255)
            
            # 尝试绘制文字
            bbox = draw.textbbox((0, 0), text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2)
            
            draw.text(position, text, fill=text_color)
        except:
            # 如果绘制失败，添加一个简单的X
            draw.line([(4, 4), (size-5, size-5)], fill=(255, 255, 255, 255), width=1)
            draw.line([(size-5, 4), (4, size-5)], fill=(255, 255, 255, 255), width=1)
        
        return img
