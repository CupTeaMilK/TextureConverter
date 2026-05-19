# version_data.py
# 增强版版本差异数据库

# 详细的 pack_format 到版本映射
PACK_FORMAT_MAP = {
    1: "1.6.1-1.8.9",
    2: "1.9-1.10.2",
    3: "1.11-1.12.2",
    4: "1.13-1.14.4",
    5: "1.15-1.16.1",
    6: "1.16.2-1.16.5",
    7: "1.17-1.17.1",
    8: "1.18-1.18.1",
    9: "1.18.2",
    10: "1.19-1.19.2",
    11: "1.19.3",
    12: "1.19.4",
    13: "1.20-1.20.1",
    14: "1.20.2",
    15: "1.20.3-1.20.4",
    16: "1.20.5-1.20.6",
    17: "1.21-1.21.1",
    18: "1.21.2",
    19: "1.21.3",
    20: "1.21.4",
    21: "1.21.5",
    22: "1.21.6-1.21.8",
    23: "1.21.9-1.21.10",
    24: "1.21.11-1.21.12",
    25: "1.22-1.22.2"  # 预留未来版本
}

# 完整的版本差异数据库
VERSION_DIFFERENCES = {
    # 1.16.5 -> 1.17 (洞穴与山崖第一部分)
    "1.16.5_to_1.17": {
        "added_blocks": [
            {"id": "minecraft:copper_ore", "texture": "textures/block/copper_ore.png", 
             "similar_to": ["minecraft:iron_ore"], "color": "#D2691E", "type": "ore"},
            {"id": "minecraft:deepslate_copper_ore", "texture": "textures/block/deepslate_copper_ore.png",
             "similar_to": ["minecraft:copper_ore"], "color": "#4A4A4A", "type": "ore"},
            {"id": "minecraft:copper_block", "texture": "textures/block/copper_block.png",
             "similar_to": ["minecraft:iron_block"], "color": "#D2691E", "type": "block"},
            {"id": "minecraft:cut_copper", "texture": "textures/block/cut_copper.png",
             "similar_to": ["minecraft:copper_block"], "color": "#B5651D", "type": "block"},
            {"id": "minecraft:exposed_copper", "texture": "textures/block/exposed_copper.png",
             "similar_to": ["minecraft:copper_block"], "color": "#8F6C4B", "type": "block"},
            {"id": "minecraft:weathered_copper", "texture": "textures/block/weathered_copper.png",
             "similar_to": ["minecraft:copper_block"], "color": "#556B2F", "type": "block"},
            {"id": "minecraft:oxidized_copper", "texture": "textures/block/oxidized_copper.png",
             "similar_to": ["minecraft:copper_block"], "color": "#2F4F4F", "type": "block"},
            {"id": "minecraft:raw_copper_block", "texture": "textures/block/raw_copper_block.png",
             "similar_to": ["minecraft:copper_block"], "color": "#CD853F", "type": "block"},
            {"id": "minecraft:amethyst_block", "texture": "textures/block/amethyst_block.png",
             "similar_to": ["minecraft:diamond_block"], "color": "#9966CC", "type": "crystal"},
            {"id": "minecraft:budding_amethyst", "texture": "textures/block/budding_amethyst.png",
             "similar_to": ["minecraft:amethyst_block"], "color": "#9370DB", "type": "crystal"},
            {"id": "minecraft:calcite", "texture": "textures/block/calcite.png",
             "similar_to": ["minecraft:diorite"], "color": "#F5F5DC", "type": "stone"},
            {"id": "minecraft:tuff", "texture": "textures/block/tuff.png",
             "similar_to": ["minecraft:stone"], "color": "#696969", "type": "stone"},
            {"id": "minecraft:dripstone_block", "texture": "textures/block/dripstone_block.png",
             "similar_to": ["minecraft:stone"], "color": "#8B7355", "type": "stone"},
            {"id": "minecraft:pointed_dripstone", "texture": "textures/block/pointed_dripstone.png",
             "similar_to": ["minecraft:dripstone_block"], "color": "#8B7355", "type": "stone"},
            {"id": "minecraft:azalea", "texture": "textures/block/azalea.png",
             "similar_to": ["minecraft:oak_leaves"], "color": "#228B22", "type": "plant"},
            {"id": "minecraft:flowering_azalea", "texture": "textures/block/flowering_azalea.png",
             "similar_to": ["minecraft:azalea"], "color": "#FF69B4", "type": "plant"},
            {"id": "minecraft:spore_blossom", "texture": "textures/block/spore_blossom.png",
             "similar_to": ["minecraft:poppy"], "color": "#FF1493", "type": "plant"},
            {"id": "minecraft:moss_block", "texture": "textures/block/moss_block.png",
             "similar_to": ["minecraft:grass_block"], "color": "#2E8B57", "type": "plant"},
            {"id": "minecraft:glow_lichen", "texture": "textures/block/glow_lichen.png",
             "similar_to": ["minecraft:vine"], "color": "#7FFF00", "type": "plant"},
            {"id": "minecraft:rooted_dirt", "texture": "textures/block/rooted_dirt.png",
             "similar_to": ["minecraft:dirt"], "color": "#8B4513", "type": "dirt"},
            {"id": "minecraft:hanging_roots", "texture": "textures/block/hanging_roots.png",
             "similar_to": ["minecraft:roots"], "color": "#8B4513", "type": "plant"},
            {"id": "minecraft:powder_snow", "texture": "textures/block/powder_snow.png",
             "similar_to": ["minecraft:snow_block"], "color": "#F0FFFF", "type": "snow"},
            {"id": "minecraft:sculk_sensor", "texture": "textures/block/sculk_sensor.png",
             "similar_to": ["minecraft:observer"], "color": "#1C1C1C", "type": "redstone"},
            {"id": "minecraft:light", "texture": "textures/block/light.png",
             "similar_to": ["minecraft:glowstone"], "color": "#FFD700", "type": "light"},
            {"id": "minecraft:candle", "texture": "textures/block/candle.png",
             "similar_to": ["minecraft:torch"], "color": "#FFFFF0", "type": "light"},
            {"id": "minecraft:small_amethyst_bud", "texture": "textures/block/small_amethyst_bud.png",
             "similar_to": ["minecraft:amethyst_block"], "color": "#9370DB", "type": "crystal"},
            {"id": "minecraft:medium_amethyst_bud", "texture": "textures/block/medium_amethyst_bud.png",
             "similar_to": ["minecraft:amethyst_block"], "color": "#9370DB", "type": "crystal"},
            {"id": "minecraft:large_amethyst_bud", "texture": "textures/block/large_amethyst_bud.png",
             "similar_to": ["minecraft:amethyst_block"], "color": "#9370DB", "type": "crystal"},
            {"id": "minecraft:amethyst_cluster", "texture": "textures/block/amethyst_cluster.png",
             "similar_to": ["minecraft:amethyst_block"], "color": "#9370DB", "type": "crystal"},
        ],
        "added_items": [
            {"id": "minecraft:raw_copper", "texture": "textures/item/raw_copper.png",
             "similar_to": ["minecraft:iron_ingot"], "color": "#D2691E", "type": "material"},
            {"id": "minecraft:raw_iron", "texture": "textures/item/raw_iron.png",
             "similar_to": ["minecraft:iron_ingot"], "color": "#C0C0C0", "type": "material"},
            {"id": "minecraft:raw_gold", "texture": "textures/item/raw_gold.png",
             "similar_to": ["minecraft:gold_ingot"], "color": "#FFD700", "type": "material"},
            {"id": "minecraft:amethyst_shard", "texture": "textures/item/amethyst_shard.png",
             "similar_to": ["minecraft:diamond"], "color": "#9966CC", "type": "material"},
            {"id": "minecraft:spyglass", "texture": "textures/item/spyglass.png",
             "similar_to": ["minecraft:compass"], "color": "#8B7355", "type": "tool"},
            {"id": "minecraft:glow_ink_sac", "texture": "textures/item/glow_ink_sac.png",
             "similar_to": ["minecraft:ink_sac"], "color": "#7FFF00", "type": "material"},
            {"id": "minecraft:glow_item_frame", "texture": "textures/item/glow_item_frame.png",
             "similar_to": ["minecraft:item_frame"], "color": "#7FFF00", "type": "decor"},
            {"id": "minecraft:glow_berries", "texture": "textures/item/glow_berries.png",
             "similar_to": ["minecraft:sweet_berries"], "color": "#7FFF00", "type": "food"},
            {"id": "minecraft:axolotl_bucket", "texture": "textures/item/axolotl_bucket.png",
             "similar_to": ["minecraft:water_bucket"], "color": "#FF69B4", "type": "mob"},
            {"id": "minecraft:bundle", "texture": "textures/item/bundle.png",
             "similar_to": ["minecraft:shulker_box"], "color": "#8B4513", "type": "storage"},
        ],
        "texture_changes": {
            "textures/block/stone.png": "textures/block/deepslate.png",  # 深层板岩替代石头
        }
    },
    
    # 1.17 -> 1.18 (洞穴与山崖第二部分)
    "1.17_to_1.18": {
        "added_blocks": [
            {"id": "minecraft:deepslate", "texture": "textures/block/deepslate.png",
             "similar_to": ["minecraft:stone"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:cobbled_deepslate", "texture": "textures/block/cobbled_deepslate.png",
             "similar_to": ["minecraft:cobblestone"], "color": "#363636", "type": "stone"},
            {"id": "minecraft:polished_deepslate", "texture": "textures/block/polished_deepslate.png",
             "similar_to": ["minecraft:stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:deepslate_bricks", "texture": "textures/block/deepslate_bricks.png",
             "similar_to": ["minecraft:stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:deepslate_tiles", "texture": "textures/block/deepslate_tiles.png",
             "similar_to": ["minecraft:stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:chiseled_deepslate", "texture": "textures/block/chiseled_deepslate.png",
             "similar_to": ["minecraft:chiseled_stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:cracked_deepslate_bricks", "texture": "textures/block/cracked_deepslate_bricks.png",
             "similar_to": ["minecraft:cracked_stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:cracked_deepslate_tiles", "texture": "textures/block/cracked_deepslate_tiles.png",
             "similar_to": ["minecraft:cracked_stone_bricks"], "color": "#2F4F4F", "type": "stone"},
            {"id": "minecraft:sculk", "texture": "textures/block/sculk.png",
             "similar_to": ["minecraft:black_wool"], "color": "#1C1C1C", "type": "sculk"},
            {"id": "minecraft:sculk_catalyst", "texture": "textures/block/sculk_catalyst.png",
             "similar_to": ["minecraft:sculk"], "color": "#1C1C1C", "type": "sculk"},
            {"id": "minecraft:sculk_shrieker", "texture": "textures/block/sculk_shrieker.png",
             "similar_to": ["minecraft:sculk"], "color": "#1C1C1C", "type": "sculk"},
            {"id": "minecraft:sculk_vein", "texture": "textures/block/sculk_vein.png",
             "similar_to": ["minecraft:sculk"], "color": "#1C1C1C", "type": "sculk"},
        ],
        "added_items": [],
        "texture_changes": {}
    },
    
    # 1.20 -> 1.21 (试炼更新)
    "1.20_to_1.21": {
        "added_blocks": [
            {"id": "minecraft:copper_grate", "texture": "textures/block/copper_grate.png",
             "similar_to": ["minecraft:iron_bars"], "color": "#D2691E", "type": "block"},
            {"id": "minecraft:exposed_copper_grate", "texture": "textures/block/exposed_copper_grate.png",
             "similar_to": ["minecraft:copper_grate"], "color": "#8F6C4B", "type": "block"},
            {"id": "minecraft:weathered_copper_grate", "texture": "textures/block/weathered_copper_grate.png",
             "similar_to": ["minecraft:copper_grate"], "color": "#556B2F", "type": "block"},
            {"id": "minecraft:oxidized_copper_grate", "texture": "textures/block/oxidized_copper_grate.png",
             "similar_to": ["minecraft:copper_grate"], "color": "#2F4F4F", "type": "block"},
            {"id": "minecraft:copper_bulb", "texture": "textures/block/copper_bulb.png",
             "similar_to": ["minecraft:redstone_lamp"], "color": "#D2691E", "type": "light"},
            {"id": "minecraft:exposed_copper_bulb", "texture": "textures/block/exposed_copper_bulb.png",
             "similar_to": ["minecraft:copper_bulb"], "color": "#8F6C4B", "type": "light"},
            {"id": "minecraft:weathered_copper_bulb", "texture": "textures/block/weathered_copper_bulb.png",
             "similar_to": ["minecraft:copper_bulb"], "color": "#556B2F", "type": "light"},
            {"id": "minecraft:oxidized_copper_bulb", "texture": "textures/block/oxidized_copper_bulb.png",
             "similar_to": ["minecraft:copper_bulb"], "color": "#2F4F4F", "type": "light"},
            {"id": "minecraft:chiseled_copper", "texture": "textures/block/chiseled_copper.png",
             "similar_to": ["minecraft:chiseled_stone_bricks"], "color": "#D2691E", "type": "block"},
            {"id": "minecraft:exposed_chiseled_copper", "texture": "textures/block/exposed_chiseled_copper.png",
             "similar_to": ["minecraft:chiseled_copper"], "color": "#8F6C4B", "type": "block"},
            {"id": "minecraft:weathered_chiseled_copper", "texture": "textures/block/weathered_chiseled_copper.png",
             "similar_to": ["minecraft:chiseled_copper"], "color": "#556B2F", "type": "block"},
            {"id": "minecraft:oxidized_chiseled_copper", "texture": "textures/block/oxidized_chiseled_copper.png",
             "similar_to": ["minecraft:chiseled_copper"], "color": "#2F4F4F", "type": "block"},
            {"id": "minecraft:tuff_bricks", "texture": "textures/block/tuff_bricks.png",
             "similar_to": ["minecraft:stone_bricks"], "color": "#696969", "type": "stone"},
            {"id": "minecraft:chiseled_tuff", "texture": "textures/block/chiseled_tuff.png",
             "similar_to": ["minecraft:chiseled_stone_bricks"], "color": "#696969", "type": "stone"},
            {"id": "minecraft:polished_tuff", "texture": "textures/block/polished_tuff.png",
             "similar_to": ["minecraft:polished_diorite"], "color": "#696969", "type": "stone"},
            {"id": "minecraft:tuff_slab", "texture": "textures/block/tuff_slab.png",
             "similar_to": ["minecraft:stone_slab"], "color": "#696969", "type": "stone"},
        ],
        "added_items": [
            {"id": "minecraft:wind_charge", "texture": "textures/item/wind_charge.png",
             "similar_to": ["minecraft:fire_charge"], "color": "#87CEEB", "type": "projectile"},
            {"id": "minecraft:mace", "texture": "textures/item/mace.png",
             "similar_to": ["minecraft:iron_sword"], "color": "#C0C0C0", "type": "weapon"},
            {"id": "minecraft:breeze_rod", "texture": "textures/item/breeze_rod.png",
             "similar_to": ["minecraft:blaze_rod"], "color": "#87CEEB", "type": "material"},
            {"id": "minecraft:trial_key", "texture": "textures/item/trial_key.png",
             "similar_to": ["minecraft:gold_ingot"], "color": "#FFD700", "type": "key"},
        ],
        "texture_changes": {}
    },
}

# 合并所有版本差异
def get_all_version_differences(source_version, target_version):
    """获取两个版本之间的所有差异"""
    all_differences = {
        "added_blocks": [],
        "added_items": [],
        "texture_changes": {}
    }
    
    # 版本升级顺序
    version_order = [
        "1.16.5_to_1.17",
        "1.17_to_1.18", 
        "1.18_to_1.19",
        "1.19_to_1.20",
        "1.20_to_1.21",
        "1.21_to_1.21.11"
    ]
    
    # 如果是1.16.5到1.21.11，包含所有中间版本
    if "1.16" in source_version and "1.21.11" in target_version:
        for version_key in version_order:
            if version_key in VERSION_DIFFERENCES:
                diff = VERSION_DIFFERENCES[version_key]
                all_differences["added_blocks"].extend(diff.get("added_blocks", []))
                all_differences["added_items"].extend(diff.get("added_items", []))
                all_differences["texture_changes"].update(diff.get("texture_changes", {}))
    
    return all_differences

def get_added_items(source_version, target_version):
    """获取新增的物品（兼容旧接口）"""
    differences = get_all_version_differences(source_version, target_version)
    
    # 转换为旧格式
    result = []
    for block in differences["added_blocks"]:
        result.append({
            "id": block["id"],
            "type": "block",
            "texture": block["texture"],
            "similar_to": block.get("similar_to", []),
            "color": block.get("color", "#808080"),
            "item_type": block.get("type", "block")
        })
    
    for item in differences["added_items"]:
        result.append({
            "id": item["id"],
            "type": "item",
            "texture": item["texture"],
            "similar_to": item.get("similar_to", []),
            "color": item.get("color", "#808080"),
            "item_type": item.get("type", "item")
        })
    
    return result

def get_pack_format_for_version(version):
    """根据游戏版本获取对应的pack_format"""
    for pack_format, ver_range in PACK_FORMAT_MAP.items():
        if version in ver_range:
            return pack_format
    
    # 近似匹配
    if "1.12" in version:
        return 3
    elif "1.13" in version or "1.14" in version:
        return 4
    elif "1.15" in version or "1.16" in version:
        return 5
    elif "1.17" in version:
        return 7
    elif "1.18" in version:
        return 8 if "1.18.2" not in version else 9
    elif "1.19" in version:
        if "1.19.4" in version:
            return 12
        elif "1.19.3" in version:
            return 11
        else:
            return 10
    elif "1.20" in version:
        if "1.20.2" in version:
            return 14
        elif "1.20.3" in version or "1.20.4" in version:
            return 15
        elif "1.20.5" in version or "1.20.6" in version:
            return 16
        else:
            return 13
    elif "1.21" in version:
        if "1.21.11" in version or "1.21.12" in version:
            return 24
        elif "1.21.9" in version or "1.21.10" in version:
            return 23
        elif "1.21.6" in version or "1.21.7" in version or "1.21.8" in version:
            return 22
        elif "1.21.5" in version:
            return 21
        elif "1.21.4" in version:
            return 20
        elif "1.21.3" in version:
            return 19
        elif "1.21.2" in version:
            return 18
        else:
            return 17
    
    return 24  # 默认最新
