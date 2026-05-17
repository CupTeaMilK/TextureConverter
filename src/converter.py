# src/converter.py
import os
import shutil
import sys
import time
import traceback
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import colorsys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.path_utils import get_project_root, get_ai_model_dir, get_output_dir
from src.utils import *
from src.version_data import *

class TexturePackConverter:
    def __init__(self, use_ai=True, ai_model="smart"):
        """
        初始化转换器
        
        Args:
            use_ai: 是否使用智能/AI生成
            ai_model: 生成模型类型 
                - "smart": 智能程序化生成
                - "ai": 深度学习AI生成
                - None: 基础占位符生成
        """
        self.work_dir = "temp_work"
        self.source_dir = None
        self.target_dir = None
        self.start_time = None
        self.conversion_success = False
        
        # 生成器设置
        self.use_ai = use_ai
        self.ai_model = ai_model
        
        # 获取AI模型路径
        self.ai_dir = get_ai_model_dir()
        
        # 检查AI模型文件
        if use_ai and ai_model == "ai":
            ai_model_path = self.ai_dir / "v1-5-pruned.safetensors"
            
            if not ai_model_path.exists():
                print("⚠️  AI模型未找到，将使用智能程序化生成")
                self.use_ai = True
                self.ai_model = "smart"
            else:
                print("🤖 AI生成器已启用")
        
        # 初始化生成器
        if use_ai and ai_model == "ai":
            try:
                from src.ai_texture_generator import AITextureGenerator
                self.ai_generator = AITextureGenerator(use_gpu=True)
                self.ai_generator.load_models()
                self.smart_generator = None
                print("✅ AI生成器初始化成功")
            except Exception as e:
                print(f"❌ AI生成器初始化失败: {e}")
                print("⚠️  将回退到智能程序化生成")
                self.use_ai = True
                self.ai_model = "smart"
                from src.texture_generator import SmartTextureGenerator
                self.smart_generator = SmartTextureGenerator()
                self.ai_generator = None
        elif use_ai and ai_model == "smart":
            try:
                from src.texture_generator import SmartTextureGenerator
                self.smart_generator = SmartTextureGenerator()
                self.ai_generator = None
                print("🎯 智能程序化生成已启用")
            except Exception as e:
                print(f"❌ 智能生成器初始化失败: {e}")
                self.use_ai = False
                self.smart_generator = None
                self.ai_generator = None
                print("🔄 使用基础占位符生成")
        else:
            self.smart_generator = None
            self.ai_generator = None
            if not use_ai:
                print("⚡ 使用基础占位符生成")
    
    def log_step(self, step_name, message=""):
        """记录步骤日志"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            time_str = f"[{elapsed:.1f}s] "
        else:
            time_str = ""
        
        if message:
            print(f"{time_str}↳ {step_name}: {message}")
        else:
            print(f"{time_str}✓ {step_name}")
    
    def convert(self, input_zip, target_version, output_path=None):
        """
        主转换函数
        Args:
            input_zip: 输入材质包zip路径
            target_version: 目标版本（如"1.21.11"）
            output_path: 输出zip路径（可选）
        """
        self.start_time = time.time()
        self.conversion_success = False
        
        print("=" * 60)
        if self.use_ai and self.ai_model == "ai":
            print("      Minecraft材质包转换器 v1.0 - AI深度学习版")
        elif self.use_ai and self.ai_model == "smart":
            print("      Minecraft材质包转换器 v1.0 - 智能程序化版")
        else:
            print("      Minecraft材质包转换器 v1.0 - 基础版")
        print("=" * 60)
        print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.use_ai and self.ai_model == "ai":
            print("🤖 使用AI深度学习生成材质")
        elif self.use_ai and self.ai_model == "smart":
            print("🎯 使用智能程序化生成材质")
        else:
            print("🔷 使用基础占位符生成材质")
        
        print()
        
        try:
            # 1. 验证输入文件
            self.log_step("验证输入文件")
            if not os.path.exists(input_zip):
                raise FileNotFoundError(f"输入文件不存在: {input_zip}")
            
            if not input_zip.lower().endswith('.zip'):
                raise ValueError(f"输入文件不是.zip格式: {input_zip}")
            
            file_size = os.path.getsize(input_zip) / (1024 * 1024)  # MB
            self.log_step("", f"文件大小: {file_size:.1f} MB")
            
            # 2. 准备工作目录
            self._prepare_workspace()
            
            # 3. 解压源材质包
            self.log_step("解压源材质包")
            source_extract = os.path.join(self.work_dir, "source")
            
            if not extract_zip(input_zip, source_extract):
                raise Exception("解压文件失败")
            
            self.source_dir = source_extract
            
            # 4. 检测源版本
            self.log_step("检测材质包版本")
            source_info = get_pack_version(source_extract)
            
            if not source_info:
                # 尝试手动查找pack.mcmeta
                self._debug_pack_structure(source_extract)
                raise Exception("无法检测源材质包版本，请检查pack.mcmeta文件")
            
            source_version = source_info["game_version"]
            self.log_step("", f"源版本: {source_version} (pack_format: {source_info['pack_format']})")
            if source_info.get('description'):
                desc = source_info['description'][:50]
                if len(source_info['description']) > 50:
                    desc += "..."
                self.log_step("", f"描述: {desc}")
            
            # 5. 创建目标目录结构
            self.log_step("创建目标目录")
            self.target_dir = os.path.join(self.work_dir, "target")
            clean_directory(self.target_dir)
            
            # 6. 复制基础文件
            self._copy_base_files()
            
            # 7. 更新pack.mcmeta
            self._update_pack_format(target_version)
            
            # 8. 分析版本差异
            self.log_step("分析版本差异")
            added_items = get_added_items(source_version, target_version)
            
            if added_items:
                self.log_step("", f"检测到 {len(added_items)} 个新增物品/方块")
                for i, item in enumerate(added_items[:5]):  # 只显示前5个
                    item_type = item.get("item_type", item.get("type", "block"))
                    self.log_step("", f"  {i+1}. {item['id']} ({item_type})")
                if len(added_items) > 5:
                    self.log_step("", f"  ... 还有 {len(added_items)-5} 个")
            else:
                self.log_step("", "无新增物品需要处理")
            
            # 9. 复制已有材质
            self._copy_existing_textures()
            
            # 10. 生成缺失材质
            if added_items:
                if self.use_ai and self.ai_model == "ai":
                    self.log_step("🤖 AI深度学习生成材质")
                elif self.use_ai and self.ai_model == "smart":
                    self.log_step("🎯 智能程序化生成材质")
                else:
                    self.log_step("🔷 生成基础占位符材质")
                
                self._generate_missing_textures(added_items)
            
            # 11. 打包输出
            self.log_step("打包转换结果")
            if output_path is None:
                input_name = os.path.splitext(os.path.basename(input_zip))[0]
                # 清理文件名中的特殊字符
                clean_name = ''.join(c for c in input_name if c.isalnum() or c in ' _-')
    
                # 如果清理后名称为空，使用默认名称
                if not clean_name.strip():
                    clean_name = "converted_pack"
    
                target_clean = target_version.replace('.', '_')
    
                # 确保在当前目录下创建输出文件
                current_dir = os.getcwd()
                output_filename = f"{clean_name}_to_{target_clean}.zip"
                output_path = os.path.join(current_dir, output_filename)
    
                self.log_step("", f"输出路径: {output_path}")
            
            if create_zip(self.target_dir, output_path):
                output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                self.log_step("", f"输出大小: {output_size:.1f} MB")
                
                # 12. 清理临时文件
                self._cleanup()
                
                # 显示最终信息
                print(f"\n🎉 转换成功完成!")
                print(f"📁 输出文件: {os.path.abspath(output_path)}")
                print(f"📦 文件大小: {output_size:.1f} MB")
                print(f"⏱️  总耗时: {time.time() - self.start_time:.2f}秒")
                
                self.conversion_success = True
                return True
            else:
                raise Exception("打包失败")
                
        except KeyboardInterrupt:
            print("\n\n❌ 转换被用户中断")
            self._emergency_cleanup()
            return False
            
        except Exception as e:
            print(f"\n❌ 转换过程中发生错误: {e}")
            print("\n详细错误信息:")
            traceback.print_exc()
            
            # 显示有用的调试信息
            self._show_debug_info()
            
            self._emergency_cleanup()
            return False
    
    def _prepare_workspace(self):
        """准备工作目录"""
        try:
            if os.path.exists(self.work_dir):
                self.log_step("清理旧的工作目录")
                shutil.rmtree(self.work_dir)
            
            os.makedirs(self.work_dir, exist_ok=True)
            self.log_step("", f"工作目录: {self.work_dir}")
            
        except Exception as e:
            raise Exception(f"创建工作目录失败: {e}")
    
    def _debug_pack_structure(self, pack_dir):
        """调试材质包结构"""
        print("\n🔍 调试 - 材质包结构:")
        print(f"目录: {pack_dir}")
        
        if not os.path.exists(pack_dir):
            print("❌ 解压目录不存在")
            return
        
        # 列出目录内容
        print("\n目录内容:")
        for item in os.listdir(pack_dir):
            item_path = os.path.join(pack_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                print(f"  📄 {item} ({size} bytes)")
        
        # 查找可能的pack.mcmeta文件
        mcmeta_path = os.path.join(pack_dir, "pack.mcmeta")
        if os.path.exists(mcmeta_path):
            print(f"\n✅ 找到 pack.mcmeta: {mcmeta_path}")
            try:
                with open(mcmeta_path, 'rb') as f:
                    content = f.read(1000)
                    print(f"文件内容(前1000字节):")
                    print(content.decode('utf-8', errors='ignore'))
            except Exception as e:
                print(f"读取文件失败: {e}")
        else:
            print("\n❌ 未找到 pack.mcmeta")
            
            # 搜索所有.mcmeta文件
            print("\n搜索所有.mcmeta文件:")
            for root, dirs, files in os.walk(pack_dir):
                for file in files:
                    if file.endswith('.mcmeta'):
                        print(f"  📄 {os.path.join(root, file)}")
    
    def _copy_base_files(self):
        """复制基础文件（非材质文件）"""
        self.log_step("复制基础文件")
        
        try:
            # 复制 pack.mcmeta
            source_mcmeta = os.path.join(self.source_dir, "pack.mcmeta")
            target_mcmeta = os.path.join(self.target_dir, "pack.mcmeta")
            
            if os.path.exists(source_mcmeta):
                shutil.copy2(source_mcmeta, target_mcmeta)
                self.log_step("", "pack.mcmeta")
            else:
                # 如果没有pack.mcmeta，创建一个默认的
                default_mcmeta = {
                    "pack": {
                        "pack_format": 6,
                        "description": "转换后的材质包"
                    }
                }
                write_json_file(target_mcmeta, default_mcmeta)
                self.log_step("", "创建默认 pack.mcmeta")
            
            # 复制 pack.png（图标）
            source_png = os.path.join(self.source_dir, "pack.png")
            target_png = os.path.join(self.target_dir, "pack.png")
            
            if os.path.exists(source_png):
                shutil.copy2(source_png, target_png)
                self.log_step("", "pack.png")
            
            # 复制其他配置文件
            config_files = ["LICENSE", "README.txt", "README.md", "credits.txt"]
            for file in config_files:
                source_file = os.path.join(self.source_dir, file)
                if os.path.exists(source_file):
                    shutil.copy2(source_file, os.path.join(self.target_dir, file))
                    self.log_step("", file)
                    
        except Exception as e:
            raise Exception(f"复制基础文件失败: {e}")
    
    def _update_pack_format(self, target_version):
        """更新pack.mcmeta中的pack_format"""
        try:
            mcmeta_path = os.path.join(self.target_dir, "pack.mcmeta")
            if not os.path.exists(mcmeta_path):
                self.log_step("", "⚠️ 没有pack.mcmeta可更新")
                return
            
            data = read_json_file(mcmeta_path)
            if data and "pack" in data:
                new_format = get_pack_format_for_version(target_version)
                data["pack"]["pack_format"] = new_format
                write_json_file(mcmeta_path, data)
                self.log_step("", f"更新pack_format: {new_format} ({target_version})")
            else:
                self.log_step("", "⚠️ pack.mcmeta格式不正确")
                
        except Exception as e:
            raise Exception(f"更新pack_format失败: {e}")
    
    def _copy_existing_textures(self):
        """复制已有的材质文件"""
        self.log_step("复制已有材质")
        
        try:
            # 源材质包目录
            source_assets = os.path.join(self.source_dir, "assets")
            target_assets = os.path.join(self.target_dir, "assets")
            
            if not os.path.exists(source_assets):
                self.log_step("", "⚠️ 未找到assets目录")
                return
            
            # 统计文件数量
            file_count = 0
            for root, dirs, files in os.walk(source_assets):
                file_count += len(files)
            
            self.log_step("", f"发现 {file_count} 个文件")
            
            if file_count > 1000:
                self.log_step("", f"⏳ 大量文件处理中，请稍候...")
            
            # 复制整个assets目录
            if os.path.exists(target_assets):
                shutil.rmtree(target_assets)
            
            shutil.copytree(source_assets, target_assets)
            self.log_step("", f"✅ 已复制 {file_count} 个文件")
            
        except Exception as e:
            raise Exception(f"复制材质文件失败: {e}")
    
    def _generate_missing_textures(self, missing_items):
        """生成缺失的材质"""
        try:
            generated_count = 0
            ai_generated = 0
            smart_generated = 0
            fallback_count = 0
            
            for i, item in enumerate(missing_items):
                texture_path = os.path.join(self.target_dir, "assets", item["texture"])
                
                # 显示进度
                if i % 5 == 0 or i == len(missing_items) - 1:
                    progress = (i + 1) / len(missing_items) * 100
                    if self.use_ai and self.ai_model == "ai":
                        self.log_step("", f"🤖 AI生成进度: {progress:.0f}% ({i+1}/{len(missing_items)})")
                    elif self.use_ai and self.ai_model == "smart":
                        self.log_step("", f"🎯 智能生成进度: {progress:.0f}% ({i+1}/{len(missing_items)})")
                    else:
                        self.log_step("", f"🔷 基础生成进度: {progress:.0f}% ({i+1}/{len(missing_items)})")
                
                # 创建目录
                os.makedirs(os.path.dirname(texture_path), exist_ok=True)
                
                try:
                    if self.use_ai and self.ai_model == "ai" and hasattr(self, 'ai_generator') and self.ai_generator:
                        # 使用AI生成器
                        # 确保item有必要的字段
                        if 'color' not in item:
                            item['color'] = item.get('color', self._get_color_by_type(item.get("item_type", "block")))
                        if 'similar_to' not in item:
                            item['similar_to'] = []
                        if 'item_type' not in item:
                            item['item_type'] = item.get("type", "block")
                        
                        # 使用AI生成材质
                        texture_img = self.ai_generator.generate_texture_with_ai(
                            item, 
                            size=16,
                            num_inference_steps=20
                        )
                        ai_generated += 1
                    elif self.use_ai and self.ai_model == "smart" and hasattr(self, 'smart_generator') and self.smart_generator:
                        # 使用智能生成器
                        if 'color' not in item:
                            item['color'] = item.get('color', self._get_color_by_type(item.get("item_type", "block")))
                        if 'similar_to' not in item:
                            item['similar_to'] = []
                        if 'item_type' not in item:
                            item['item_type'] = item.get("type", "block")
                        
                        texture_img = self.smart_generator.generate_smart_texture(item)
                        smart_generated += 1
                    else:
                        # 使用基础占位符
                        texture_img = self._create_placeholder_texture(item["id"], item.get("item_type", "block"))
                        fallback_count += 1
                    
                    # 保存图片
                    texture_img.save(texture_path, "PNG")
                    generated_count += 1
                    
                except Exception as e:
                    print(f"⚠️  生成失败 {item['id']}: {e}")
                    # 回退到基础占位符
                    texture_img = self._create_placeholder_texture(item["id"], item.get("item_type", "block"))
                    texture_img.save(texture_path, "PNG")
                    generated_count += 1
                    fallback_count += 1
            
            # 显示生成统计
            if self.use_ai and self.ai_model == "ai":
                if ai_generated > 0:
                    self.log_step("", f"✅ AI深度学习生成: {ai_generated} 个材质")
            elif self.use_ai and self.ai_model == "smart":
                if smart_generated > 0:
                    self.log_step("", f"✅ 智能程序化生成: {smart_generated} 个材质")
            else:
                self.log_step("", f"✅ 基础占位符生成: {generated_count} 个材质")
                
            if fallback_count > 0:
                self.log_step("", f"⚠️  回退到占位符: {fallback_count} 个")
            
            self.log_step("", f"总计生成 {generated_count} 个材质")
            
        except Exception as e:
            raise Exception(f"生成材质失败: {e}")
    
    def _create_placeholder_texture(self, item_id, item_type="block"):
        """创建占位符材质图片"""
        try:
            # 根据物品类型选择颜色
            color_map = {
                "ore": "#D2691E",  # 矿石棕
                "block": "#808080",  # 方块灰
                "crystal": "#9966CC",  # 水晶紫
                "plant": "#228B22",  # 植物绿
                "stone": "#696969",  # 石头灰
                "wood": "#8B4513",  # 木头棕
                "metal": "#C0C0C0",  # 金属银
                "tool": "#FFD700",  # 工具金
                "weapon": "#B22222",  # 武器红
                "material": "#00CED1",  # 材料青
                "food": "#FF6347",  # 食物橙
            }
            
            # 获取基础颜色
            base_color_hex = color_map.get(item_type, "#808080")
            base_color = self._hex_to_rgb(base_color_hex)
            
            # 根据物品ID添加随机种子
            random.seed(hash(item_id))
            
            # 创建16x16的图片
            img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 填充基础颜色
            for x in range(16):
                for y in range(16):
                    # 添加轻微噪点
                    noise = random.randint(-10, 10)
                    r = max(0, min(255, base_color[0] + noise))
                    g = max(0, min(255, base_color[1] + noise))
                    b = max(0, min(255, base_color[2] + noise))
                    img.putpixel((x, y), (r, g, b, 255))
            
            # 添加网格线
            for i in range(0, 16, 4):
                draw.line([(i, 0), (i, 15)], fill=(0, 0, 0, 100), width=1)
                draw.line([(0, i), (15, i)], fill=(0, 0, 0, 100), width=1)
            
            # 添加物品类型缩写
            type_abbr = item_type[:3].upper() if len(item_type) >= 3 else item_type.upper()
            
            try:
                # 计算文字颜色（对比色）
                brightness = (base_color[0] * 0.299 + base_color[1] * 0.587 + base_color[2] * 0.114)
                text_color = (255, 255, 255, 255) if brightness < 128 else (0, 0, 0, 255)
                
                # 绘制类型缩写
                bbox = draw.textbbox((0, 0), type_abbr)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                position = ((16 - text_width) // 2, (16 - text_height) // 2)
                
                draw.text(position, type_abbr, fill=text_color)
            except:
                # 如果绘制失败，画个X
                draw.line([(4, 4), (12, 12)], fill=(255, 255, 255, 255), width=1)
                draw.line([(12, 4), (4, 12)], fill=(255, 255, 255, 255), width=1)
            
            return img
            
        except Exception as e:
            print(f"⚠️ 创建占位符失败 {item_id}: {e}")
            # 创建最简单的红色占位符
            return Image.new('RGB', (16, 16), (255, 0, 0))
    
    def _get_color_by_type(self, item_type):
        """根据物品类型获取颜色"""
        color_map = {
            "ore": "#D2691E",  # 矿石棕
            "block": "#808080",  # 方块灰
            "crystal": "#9966CC",  # 水晶紫
            "plant": "#228B22",  # 植物绿
            "stone": "#696969",  # 石头灰
            "wood": "#8B4513",  # 木头棕
            "metal": "#C0C0C0",  # 金属银
            "tool": "#FFD700",  # 工具金
            "weapon": "#B22222",  # 武器红
            "material": "#00CED1",  # 材料青
            "food": "#FF6347",  # 食物橙
        }
        return color_map.get(item_type, "#808080")
    
    def _hex_to_rgb(self, hex_color):
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _cleanup(self):
        """清理临时文件"""
        try:
            if os.path.exists(self.work_dir):
                shutil.rmtree(self.work_dir, ignore_errors=True)
                self.log_step("", "清理临时文件")
        except Exception as e:
            print(f"⚠️ 清理临时文件失败: {e}")
    
    def _emergency_cleanup(self):
        """紧急清理（发生错误时）"""
        print("\n⚠️ 正在执行紧急清理...")
        try:
            if os.path.exists(self.work_dir):
                shutil.rmtree(self.work_dir, ignore_errors=True)
                print("✅ 已清理临时文件")
        except Exception as e:
            print(f"⚠️ 清理失败: {e}")
    
    def _show_debug_info(self):
        """显示调试信息"""
        print("\n🔧 调试信息:")
        print(f"Python版本: {sys.version}")
        print(f"当前目录: {os.getcwd()}")
        print(f"临时目录: {self.work_dir}")
        
        if os.path.exists(self.work_dir):
            print(f"\n临时目录内容:")
            for item in os.listdir(self.work_dir):
                item_path = os.path.join(self.work_dir, item)
                if os.path.isdir(item_path):
                    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(item_path) for f in fn) / 1024
                    print(f"  📁 {item}/ ({size:.1f} KB)")
                else:
                    size = os.path.getsize(item_path) / 1024
                    print(f"  📄 {item} ({size:.1f} KB)")

# 测试函数
def test_converter():
    """测试转换器功能"""
    print("🧪 测试转换器功能")
    print("=" * 50)
    
    # 测试不同的模式
    modes = [
        (True, "ai", "🤖 AI深度学习模式"),
        (True, "smart", "🎯 智能程序化模式"),
        (False, None, "🔷 基础占位符模式")
    ]
    
    for use_ai, ai_model, description in modes:
        print(f"\n测试: {description}")
        print("-" * 30)
        
        try:
            converter = TexturePackConverter(use_ai=use_ai, ai_model=ai_model)
            print("✅ 初始化成功")
            
            # 测试占位符生成
            test_item = {
                "id": "minecraft:test_item",
                "item_type": "ore",
                "color": "#D2691E"
            }
            
            if use_ai and ai_model == "ai" and hasattr(converter, 'ai_generator') and converter.ai_generator:
                print("🎨 测试AI生成器...")
                try:
                    texture = converter.ai_generator.generate_texture_with_ai(test_item, size=16)
                    print(f"  ✅ AI生成成功，大小: {texture.size}")
                except Exception as e:
                    print(f"  ❌ AI生成失败: {e}")
            
            elif use_ai and ai_model == "smart" and hasattr(converter, 'smart_generator') and converter.smart_generator:
                print("🎨 测试智能生成器...")
                try:
                    texture = converter.smart_generator.generate_smart_texture(test_item)
                    print(f"  ✅ 智能生成成功，大小: {texture.size}")
                except Exception as e:
                    print(f"  ❌ 智能生成失败: {e}")
            
            else:
                print("🎨 测试基础占位符生成...")
                try:
                    texture = converter._create_placeholder_texture(test_item["id"], test_item["item_type"])
                    print(f"  ✅ 基础生成成功，大小: {texture.size}")
                except Exception as e:
                    print(f"  ❌ 基础生成失败: {e}")
                    
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成!")
    input("按Enter退出...")

if __name__ == "__main__":
    test_converter()
