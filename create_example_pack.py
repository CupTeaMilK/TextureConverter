# create_example_pack.py
import os
import json
import zipfile
from pathlib import Path
from PIL import Image

def create_simple_pack():
    """创建简单的示例材质包"""
    project_root = Path(__file__).parent
    output_dir = project_root / "resources" / "example_pack"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        pack_dir = Path(tmpdir) / "SimplePack_1.16.5"
        pack_dir.mkdir(parents=True)
        
        # 创建pack.mcmeta
        mcmeta = {
            "pack": {
                "pack_format": 6,
                "description": "§a简单测试材质包 §7(v1.16.5)"
            }
        }
        
        with open(pack_dir / "pack.mcmeta", "w", encoding="utf-8") as f:
            json.dump(mcmeta, f, indent=2, ensure_ascii=False)
        
        # 创建assets结构
        assets_dir = pack_dir / "assets" / "minecraft"
        textures_dir = assets_dir / "textures"
        
        # 创建block材质
        block_dir = textures_dir / "block"
        block_dir.mkdir(parents=True, exist_ok=True)
        
        blocks = [
            ("stone", (128, 128, 128)),
            ("dirt", (139, 69, 19)),
            ("grass_block_top", (102, 153, 51)),
            ("grass_block_side", (128, 180, 77)),
            ("oak_planks", (168, 136, 85)),
            ("cobblestone", (128, 128, 128)),
        ]
        
        for name, color in blocks:
            img = Image.new("RGB", (16, 16), color)
            # 添加简单纹理
            pixels = img.load()
            for x in range(16):
                for y in range(16):
                    if (x + y) % 3 == 0:
                        pixels[x, y] = tuple(max(0, c-20) for c in color)
            img.save(block_dir / f"{name}.png")
        
        # 创建item材质
        item_dir = textures_dir / "item"
        item_dir.mkdir(parents=True, exist_ok=True)
        
        items = [
            ("apple", (255, 0, 0)),
            ("diamond", (102, 229, 252)),
            ("iron_ingot", (220, 220, 220)),
            ("gold_ingot", (255, 215, 0)),
        ]
        
        for name, color in items:
            img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制简单图标
            draw.ellipse([3, 3, 13, 13], fill=color)
            if name == "apple":
                draw.rectangle([7, 2, 9, 4], fill=(0, 128, 0))
            
            img.save(item_dir / f"{name}.png")
        
        # 创建ZIP文件
        zip_path = output_dir / "SimplePack_1.16.5.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in pack_dir.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(pack_dir)
                    zipf.write(file, arcname)
        
        print(f"✅ 示例材质包已创建: {zip_path}")
        print(f"   大小: {zip_path.stat().st_size / 1024:.1f} KB")
        
        return zip_path

if __name__ == "__main__":
    import tempfile
    from PIL import ImageDraw
    
    create_simple_pack()
