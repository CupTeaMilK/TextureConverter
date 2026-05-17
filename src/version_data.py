# src/version_data.py
from typing import Dict, List, Any, Optional
from datetime import datetime

# Minecraft版本之间的物品差异
VERSION_DIFFERENCES = {
    "1.16.5": {
        "added": [],
        "removed": []
    },
    "1.17.1": {
        "added": [
            {
                "id": "minecraft:copper_ore",
                "type": "ore",
                "texture": "minecraft/textures/block/copper_ore.png",
                "color": "#D2691E",
                "item_type": "ore"
            },
            {
                "id": "minecraft:deepslate",
                "type": "block", 
                "texture": "minecraft/textures/block/deepslate.png",
                "color": "#404040",
                "item_type": "stone"
            },
            {
                "id": "minecraft:raw_copper",
                "type": "item",
                "texture": "minecraft/textures/item/raw_copper.png",
                "color": "#D2691E",
                "item_type": "material"
            }
        ],
        "removed": []
    },
    "1.18.2": {
        "added": [
            {
                "id": "minecraft:sculk",
                "type": "block",
                "texture": "minecraft/textures/block/sculk.png",
                "color": "#0C0C1C",
                "item_type": "block"
            },
            {
                "id": "minecraft:sculk_catalyst",
                "type": "block",
                "texture": "minecraft/textures/block/sculk_catalyst.png",
                "color": "#0A0A1A",
                "item_type": "block"
            }
        ],
        "removed": []
    },
    "1.19.4": {
        "added": [
            {
                "id": "minecraft:mangrove_planks",
                "type": "block",
                "texture": "minecraft/textures/block/mangrove_planks.png",
                "color": "#A52A2A",
                "item_type": "wood"
            },
            {
                "id": "minecraft:recovery_compass",
                "type": "item",
                "texture": "minecraft/textures/item/recovery_compass.png",
                "color": "#FFD700",
                "item_type": "tool"
            }
        ],
        "removed": []
    },
    "1.20.6": {
        "added": [
            {
                "id": "minecraft:armadillo_scute",
                "type": "item",
                "texture": "minecraft/textures/item/armadillo_scute.png",
                "color": "#D2B48C",
                "item_type": "material"
            },
            {
                "id": "minecraft:wind_charge",
                "type": "item",
                "texture": "minecraft/textures/item/wind_charge.png",
                "color": "#87CEEB",
                "item_type": "material"
            }
        ],
        "removed": []
    },
    "1.21.5": {
        "added": [
            {
                "id": "minecraft:breeze_rod",
                "type": "item",
                "texture": "minecraft/textures/item/breeze_rod.png",
                "color": "#87CEEB",
                "item_type": "material"
            },
            {
                "id": "minecraft:trial_key",
                "type": "item",
                "texture": "minecraft/textures/item/trial_key.png",
                "color": "#FFD700",
                "item_type": "tool"
            }
        ],
        "removed": []
    },
    "1.21.11": {
        "added": [
            {
                "id": "minecraft:heavy_core",
                "type": "item",
                "texture": "minecraft/textures/item/heavy_core.png",
                "color": "#FF6347",
                "item_type": "material"
            },
            {
                "id": "minecraft:ominous_bottle",
                "type": "item",
                "texture": "minecraft/textures/item/ominous_bottle.png",
                "color": "#8A2BE2",
                "item_type": "material"
            }
        ],
        "removed": []
    }
}

# 版本升级链
VERSION_UPGRADE_CHAIN = [
    "1.16.5", "1.17.1", "1.18.2", "1.19.4", "1.20.6", "1.21.5", "1.21.11"
]

def get_added_items(from_version: str, to_version: str) -> List[Dict[str, Any]]:
    """
    获取从某个版本升级到另一个版本时新增的物品
    
    Args:
        from_version: 源版本
        to_version: 目标版本
    
    Returns:
        新增物品列表
    """
    # 标准化版本
    from_version = normalize_version(from_version)
    to_version = normalize_version(to_version)
    
    # 如果目标版本比源版本旧，返回空列表
    if get_version_index(from_version) >= get_version_index(to_version):
        return []
    
    added_items = []
    
    # 获取所有中间版本
    start_index = get_version_index(from_version)
    end_index = get_version_index(to_version)
    
    if start_index == -1 or end_index == -1:
        return []
    
    # 收集新增物品
    for i in range(start_index + 1, end_index + 1):
        version = VERSION_UPGRADE_CHAIN[i]
        if version in VERSION_DIFFERENCES:
            added_items.extend(VERSION_DIFFERENCES[version]["added"])
    
    return added_items

def get_removed_items(from_version: str, to_version: str) -> List[Dict[str, Any]]:
    """
    获取从某个版本升级到另一个版本时移除的物品
    """
    from_version = normalize_version(from_version)
    to_version = normalize_version(to_version)
    
    if get_version_index(from_version) >= get_version_index(to_version):
        return []
    
    removed_items = []
    
    start_index = get_version_index(from_version)
    end_index = get_version_index(to_version)
    
    if start_index == -1 or end_index == -1:
        return []
    
    for i in range(start_index + 1, end_index + 1):
        version = VERSION_UPGRADE_CHAIN[i]
        if version in VERSION_DIFFERENCES:
            removed_items.extend(VERSION_DIFFERENCES[version]["removed"])
    
    return removed_items

def normalize_version(version: str) -> str:
    """标准化版本号"""
    # 移除可能的空格
    version = version.strip()
    
    # 如果是已知版本，直接返回
    if version in VERSION_UPGRADE_CHAIN:
        return version
    
    # 尝试匹配主版本
    for v in VERSION_UPGRADE_CHAIN:
        if v.startswith(version):
            return v
    
    # 默认返回最新版本
    return VERSION_UPGRADE_CHAIN[-1]

def get_version_index(version: str) -> int:
    """获取版本在升级链中的索引"""
    normalized = normalize_version(version)
    try:
        return VERSION_UPGRADE_CHAIN.index(normalized)
    except ValueError:
        return -1

def get_latest_version() -> str:
    """获取最新版本"""
    return VERSION_UPGRADE_CHAIN[-1]

def get_supported_versions() -> List[str]:
    """获取支持的版本列表"""
    return VERSION_UPGRADE_CHAIN.copy()

def get_version_info(version: str) -> Dict[str, Any]:
    """获取版本信息"""
    normalized = normalize_version(version)
    
    return {
        "version": normalized,
        "index": get_version_index(normalized),
        "display_name": f"Minecraft {normalized}",
        "release_date": get_version_release_date(normalized),
        "pack_format": get_pack_format_for_version(normalized)
    }

def get_version_release_date(version: str) -> str:
    """获取版本发布日期（示例）"""
    dates = {
        "1.16.5": "2021-01-15",
        "1.17.1": "2021-07-06", 
        "1.18.2": "2021-12-10",
        "1.19.4": "2023-03-14",
        "1.20.6": "2024-05-13",
        "1.21.5": "2024-08-20",
        "1.21.11": "2025-01-15"
    }
    return dates.get(version, "未知")

def get_pack_format_for_version(version: str) -> int:
    """根据版本获取pack_format"""
    from src.utils import get_pack_format_for_version as utils_get_pack_format
    return utils_get_pack_format(version)

def is_version_supported(version: str) -> bool:
    """检查版本是否支持"""
    normalized = normalize_version(version)
    return normalized in VERSION_UPGRADE_CHAIN

def get_next_version(current_version: str) -> Optional[str]:
    """获取下一个版本"""
    index = get_version_index(current_version)
    if index >= 0 and index < len(VERSION_UPGRADE_CHAIN) - 1:
        return VERSION_UPGRADE_CHAIN[index + 1]
    return None

def get_previous_version(current_version: str) -> Optional[str]:
    """获取上一个版本"""
    index = get_version_index(current_version)
    if index > 0:
        return VERSION_UPGRADE_CHAIN[index - 1]
    return None

def get_version_difference_summary(from_version: str, to_version: str) -> Dict[str, Any]:
    """获取版本差异摘要"""
    added = get_added_items(from_version, to_version)
    removed = get_removed_items(from_version, to_version)
    
    return {
        "from_version": from_version,
        "to_version": to_version,
        "added_count": len(added),
        "removed_count": len(removed),
        "added_items": [item["id"] for item in added[:10]],  # 只显示前10个
        "removed_items": [item["id"] for item in removed[:10]]
    }

# 测试函数
if __name__ == "__main__":
    print("🔍 测试版本数据")
    
    # 测试版本标准化
    test_versions = ["1.16", "1.17.1", "1.20", "1.21.11", "unknown"]
    for v in test_versions:
        normalized = normalize_version(v)
        print(f"  {v} -> {normalized}")
    
    # 测试获取新增物品
    print(f"\n从 1.16.5 升级到 1.21.11 新增物品:")
    added = get_added_items("1.16.5", "1.21.11")
    for item in added:
        print(f"  - {item['id']} ({item.get('item_type', 'block')})")
    
    print(f"\n共新增 {len(added)} 个物品")
    
    # 测试版本信息
    print(f"\n版本信息:")
    for v in ["1.16.5", "1.21.11"]:
        info = get_version_info(v)
        print(f"  {v}: pack_format={info['pack_format']}, 发布日期={info['release_date']}")
    
    print("✅ 版本数据测试完成")
