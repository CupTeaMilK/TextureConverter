# 🎮 Minecraft AI 材质包转换器

![GitHub](https://img.shields.io/badge/Python-3.8%2B-blue)
![GitHub](https://img.shields.io/badge/License-MIT-green)
![GitHub](https://img.shields.io/badge/Platform-Windows%20%7C%20MacOS%20%7C%20Linux-orange)

这是一个强大的 Minecraft 材质包转换工具，可以：
- 🔥 **AI增强材质** - 使用 Stable Diffusion 提升材质分辨率
- 🧠 **智能补全** - 自动生成缺失的材质文件
- 🎨 **批量处理** - 一键转换整个材质包
- 🏷️ **版本适配** - 支持多种 Minecraft 版本

## 🚨 重要警告：新用户必读！🚨

**在使用本工具前，你必须完成以下两个步骤，否则程序无法运行！**

### 第一步：安装 Python 3.8+
1. 访问 [Python官网](https://www.python.org/downloads/) 下载 Python
2. **安装时务必勾选 "Add Python to PATH"**（将Python添加到系统路径）
3. 安装完成后，**重启电脑**

### 第二步：下载 AI 模型文件
1. 下载 Stable Diffusion 1.5 模型（如 `v1-5-pruned.safetensors`，约4GB）
2. 在项目中找到 `ai_generator/models/` 文件夹
3. 将模型文件放入此文件夹

**⚠️ 没有Python无法运行！没有AI模型无法使用AI功能！⚠️**

### 作者提醒
1.AI模型可选，没有不影响运行（但影响功能）   
2.如果使用，文件包目录结构不要动！！！相对路径已经设置好，不要随意更改路径！！！     
3.生成的材质包在根目录下    
4.由于中文编码闪退问题困扰我许久，所以我把启动器.bat文件内容全英文了，但main.py等其他主要文件依旧中文awa    
5.文件代码部分请教AI，还有内容注释（打代码打到一半回去检查发现没有注释QwQ，让AI帮我注释了）   
6.python不要安装太新，也不要太旧，否则插件不兼容，最好和我的一样3.10.0    

---

## 📦 快速开始

### 方法一：一键安装（推荐新手）
1. 下载本项目到你的电脑
2. 双击运行 `安装依赖-中文版.bat`
3. 按照提示选择选项
4. 等待安装完成

### 方法二：手动安装
bash
安装基础依赖
pip install -r requirements.txt
安装AI相关依赖（可选）
pip install -r requirements_ai.txt
---

## 🎯 功能特色

### 🤖 AI 增强模式
- 自动提升材质分辨率（16x → 32x/64x/128x）
- 保持原材质风格
- 支持批量处理

### 🧩 智能补全
- 自动检测缺失的材质
- 基于相似材质智能生成
- 支持自定义生成规则

### 🔄 批量转换
- 一键转换整个材质包
- 支持多种输出格式
- 进度显示和错误处理

### ⚙️ 自定义配置
- 调整AI生成参数
- 设置输出质量
- 选择目标版本

---

## 🖥️ 使用方法

### 基本使用
1. 双击 `Start_Converter.bat`
2. 将材质包 `.zip` 文件拖入窗口
3. 选择处理模式：
   - 1: AI增强模式（需要模型）
   - 2: 智能补全模式
   - 3: 混合模式
4. 选择输出质量
5. 等待处理完成

### 命令行使用
bash
基本转换
python main.py --input "材质包.zip"
AI增强模式
python main.py --input "材质包.zip" --mode ai
指定输出质量
python main.py --input "材质包.zip" --quality high
批量处理文件夹
python main.py --input "材质包文件夹" --batch
### 高级参数
bash
查看所有选项
python main.py --help
自定义参数示例
python main.py \
--input "材质包.zip" \
--output "输出文件夹" \
--mode hybrid \
--quality ultra \
--scale 2 \
--device cuda
---


## ⚙️ 配置说明

### AI 模型配置
1. 在 `ai_generator/models/` 中放入模型文件
2. 支持格式：`.safetensors`, `.ckpt`, `.pth`
3. 推荐模型：Stable Diffusion 1.5/2.1

### 硬件要求
- **最低配置**: 8GB RAM, 4GB VRAM (AI模式)
- **推荐配置**: 16GB RAM, 8GB+ VRAM
- **存储空间**: 至少10GB可用空间

### 性能优化
python
在 config.py 中调整
AI_CONFIG = {
"use_gpu": True, # 使用GPU加速
"precision": "fp16", # 半精度浮点
"batch_size": 1, # 批处理大小
"cache_models": True # 缓存模型
}
---

## ❓ 常见问题

### Q1: 启动时提示 "Python not found"
**A**: Python没有正确安装或没有添加到PATH。请重新安装Python并勾选"Add Python to PATH"。

### Q2: AI功能报错 "Model not found"
**A**: 你还没有下载AI模型文件。请参考上面的【第二步】，将模型放入 `ai_generator/models/`。

### Q3: 运行速度很慢
**A**: 检查是否使用了GPU。在命令行中添加 `--device cuda` 参数。

### Q4: 内存不足
**A**: 尝试降低输出质量或使用CPU模式：`--device cpu --quality medium`

### Q5: 生成的材质模糊
**A**: 尝试提高AI步数：`--steps 50` 或使用更高的缩放比例：`--scale 4`

---

## 🐛 问题反馈

遇到问题？请：

1. 查看 `logs/` 目录下的日志文件
2. 在GitHub Issues中提交问题
3. 包含以下信息：
   - 错误信息截图
   - 你的系统配置
   - 使用的模型名称
   - 操作步骤

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 [Stable Diffusion](https://github.com/CompVis/stable-diffusion) 团队
- 感谢 [Hugging Face](https://huggingface.co/) 提供的模型
- 感谢所有测试者和贡献者

---

## ⭐ 支持项目

如果这个项目对你有帮助，请：
1. 给项目点个Star ⭐
2. 分享给其他Minecraft玩家
3. 提交PR或Issue帮助改进

**享受高清材质带来的视觉盛宴吧！🎮✨**


