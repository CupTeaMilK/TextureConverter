# Minecraft-Texture-Converter-AI-mixed-
A new generation Minecraft texture pack converter, supporting the conversion of high-version texture packs, and innovatively integrating AI generation technology (for the specific use of AI, please refer to the project's README.md).


# 🎮 Minecraft AI Texture Converter(English version)  中文在下面

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A powerful Minecraft texture pack converter that uses AI to intelligently generate textures, allowing you to convert older texture packs to newer versions.

## ✨ Features

- 🤖 **AI Deep Learning Generation** - Uses Stable Diffusion to generate high-quality textures
- 🎯 **Smart Procedural Generation** - Algorithmically generates textures matching vanilla style
- ⚡ **Basic Placeholder Generation** - Quickly generates simple placeholder textures
- 🔄 **Version Conversion** - Supports conversion from 1.16.5 to 1.21.11
- 📦 **Batch Processing** - Automatically processes all missing textures
- 🎨 **Color Matching** - Intelligently matches colors based on item types
- 📁 **Complete Preservation** - Retains all existing files from the original texture pack

## 📦 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 64-bit
- **Processor**: Intel i5 or equivalent
- **RAM**: 8GB
- **Disk Space**: 20GB free space
- **Python**: 3.8 or higher

### Recommended Requirements
- **Operating System**: Windows 11 64-bit
- **Processor**: Intel i7 or equivalent
- **RAM**: 16GB
- **Disk Space**: 50GB free space
- **Graphics Card**: NVIDIA GPU (CUDA-capable, for AI acceleration)
- **Python**: 3.10 or higher

## 🚀 Quick Start

### 1. Download the Project
bash
Clone with Git
git clone https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git
cd Minecraft-Texture-Converter-AI
Or download ZIP directly
Download latest release from the Releases page
### 2. One-Click Installation
Double-click `scripts/install.bat`

The installer will automatically:
- Check Python environment
- Install required dependencies
- Create desktop shortcuts
- Set up project paths

### 3. Download AI Models (Optional)
To use AI generation features, run:
bash
Run the download script
scripts\download_model.bat
Or use the "Download AI Models" desktop shortcut
> ⚠️ **Note**: AI models are approximately 4.3GB and may take a while to download

### 4. Start Using
1. Double-click the `Minecraft AI Texture Converter` desktop shortcut
2. Drag and drop your texture pack `.zip` file into the window
3. Select generation mode
4. Choose target version
5. Start conversion

## 📁 Project Structure
Minecraft-Texture-Converter-AI/
├── src/ # Source code
│ ├── main.py # Main program entry
│ ├── converter.py # Core converter
│ ├── ai_texture_generator.py # AI texture generator
│ ├── texture_generator.py # Smart texture generator
│ ├── utils.py # Utility functions
│ ├── version_data.py # Version data
│ ├── fix_bom.py # File repair utilities
│ ├── path_utils.py # Path utilities
│ └── init.py # Package definition
│
├── scripts/ # Scripts directory
│ ├── install.bat # One-click installer
│ ├── start.bat # Startup script
│ ├── download_model.bat # AI model downloader
│ ├── download_model.py # Python download script
│ └── check_environment.bat # Environment checker
│
├── resources/ # Resources directory
│ └── example_pack/ # Example texture packs
│
├── docs/ # Documentation
│ └── tutorial_en.md # English tutorial
│
├── ai_generator/ # AI models directory (user downloads)
│ └── models/ # Stable Diffusion models
│
├── .gitignore # Git ignore file
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
├── README.md # Project documentation
├── config.json # Configuration file
└── test_basic.py # Test script
## ⚙️ Configuration

### Path Configuration
Project uses fixed path: `D:\mc\TextureConverter_Github\Minecraft-Texture-Converter-AI`

To modify, edit `config.json`:
json
{
"paths": {
"install_dir": "D:\mc\TextureConverter_Github",
"models_dir": "D:\mc\TextureConverter_Github\ai_generator\models",
"output_dir": "D:\mc\TextureConverter_Github\output"
}
}
### Generation Modes
Three generation modes are available:

| Mode | Quality | Speed | Requires AI Model |
|------|---------|-------|-------------------|
| 🤖 AI Deep Learning | High | Slow | Yes |
| 🎯 Smart Procedural | Medium | Medium | No |
| ⚡ Basic Placeholder | Low | Fast | No |

### Supported Versions
- 1.16.5
- 1.17.1
- 1.18.2
- 1.19.4
- 1.20.6
- 1.21.5
- 1.21.11
- Custom versions

## 🔧 Advanced Usage

### Command Line Mode
bash
Basic usage
python src\main.py "texture_pack.zip" "1.21.11"
Specify output path
python src\main.py "texture_pack.zip" "1.21.11" "output_path.zip"
### Developer Usage
bash
Clone the project
git clone https://github.com/yourname/Minecraft-Texture-Converter-AI.git
cd Minecraft-Texture-Converter-AI
Create virtual environment
python -m venv venv
venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run tests
python test_basic.py
Run directly
python src\main.py
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

- 🐛 [Issue Tracker](https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git/issues)
- 💬 [Discussions](https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git/discussions)
- 📧 Email: cupteamilk@163.com

## 🙏 Acknowledgments

- [Stable Diffusion](https://stability.ai/stable-diffusion) - For AI generation
- [Hugging Face](https://huggingface.co) - For model hosting
- [PyTorch](https://pytorch.org) - Deep learning framework
- [Pillow](https://python-pillow.org) - Image processing library

## 📈 Changelog

### v1.0.0 (2024-XX-XX)
- ✅ Initial release
- ✅ Three generation modes supported
- ✅ Version conversion functionality
- ✅ One-click installer
- ✅ AI model downloader

---

**Made with ❤️ for the Minecraft community**














# 🎮 Minecraft AI材质转换器(中文版)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个功能强大的Minecraft材质包转换工具，支持AI智能生成材质，可将旧版材质包转换为新版。

## ✨ 特性

- 🤖 **AI深度学习生成** - 使用Stable Diffusion生成高质量材质
- 🎯 **智能程序化生成** - 算法生成匹配原版风格的材质
- ⚡ **基础占位符生成** - 快速生成简单材质
- 🔄 **版本转换** - 支持1.16.5到1.21.11的版本转换
- 📦 **批量处理** - 自动处理所有缺失材质
- 🎨 **颜色匹配** - 根据物品类型智能匹配颜色
- 📁 **完整保留** - 保留原材质包的所有已有文件

## 📦 系统要求

### 最低配置
- **操作系统**: Windows 10/11 64位
- **处理器**: Intel i5 或同等性能
- **内存**: 8GB RAM
- **磁盘空间**: 20GB 可用空间
- **Python**: 3.8 或更高版本

### 推荐配置
- **操作系统**: Windows 11 64位
- **处理器**: Intel i7 或同等性能
- **内存**: 16GB RAM
- **磁盘空间**: 50GB 可用空间
- **显卡**: NVIDIA GPU (支持CUDA，用于AI加速)
- **Python**: 3.10 或更高版本

## 🚀 快速开始

### 1. 下载项目
bash
使用Git下载
git clone https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git
cd Minecraft-Texture-Converter-AI
或直接下载ZIP包
从Releases页面下载最新版本
### 2. 一键安装
双击运行 `scripts/install.bat`

安装程序会自动：
- 检查Python环境
- 安装所需依赖
- 创建桌面快捷方式
- 设置项目路径

### 3. 下载AI模型（可选）
如需使用AI生成功能，运行：
bash
运行下载脚本
scripts\download_model.bat
或双击桌面快捷方式中的"下载AI模型"
> ⚠️ **注意**: AI模型约4.3GB，下载需要较长时间

### 4. 开始使用
1. 双击桌面上的 `Minecraft AI材质转换器` 快捷方式
2. 将材质包.zip文件拖拽到窗口
3. 选择生成模式
4. 选择目标版本
5. 开始转换

## 📁 项目结构
Minecraft-Texture-Converter-AI/
├── src/ # 源代码目录
│ ├── main.py # 主程序入口
│ ├── converter.py # 核心转换器
│ ├── ai_texture_generator.py # AI生成器
│ ├── texture_generator.py # 智能生成器
│ ├── utils.py # 工具函数
│ ├── version_data.py # 版本数据
│ ├── fix_bom.py # 文件修复
│ ├── path_utils.py # 路径工具
│ └── init.py # 包定义
│
├── scripts/ # 脚本目录
│ ├── install.bat # 一键安装
│ ├── start.bat # 启动程序
│ ├── download_model.bat # 下载AI模型
│ ├── download_model.py # Python下载脚本
│ └── check_environment.bat # 环境检查
│
├── resources/ # 资源目录
│ └── example_pack/ # 示例材质包
│
├── docs/ # 文档目录
│ └── tutorial_zh.md # 中文教程
│
├── ai_generator/ # AI模型目录（用户下载）
│ └── models/ # Stable Diffusion模型
│
├── .gitignore # Git忽略文件
├── requirements.txt # Python依赖
├── LICENSE # MIT许可证
├── README.md # 项目说明
├── config.json # 配置文件
└── test_basic.py # 测试脚本
## ⚙️ 配置说明

### 路径配置
项目使用固定路径：`D:\mc\TextureConverter_Github\Minecraft-Texture-Converter-AI`

如需修改，请编辑 `config.json`：
json
{
"paths": {
"install_dir": "D:\mc\TextureConverter_Github",
"models_dir": "D:\mc\TextureConverter_Github\ai_generator\models",
"output_dir": "D:\mc\TextureConverter_Github\output"
}
}
### 生成模式
程序提供三种生成模式：

| 模式 | 质量 | 速度 | 需要AI模型 |
|------|------|------|------------|
| 🤖 AI深度学习生成 | 高 | 慢 | 是 |
| 🎯 智能程序化生成 | 中 | 中 | 否 |
| ⚡ 基础占位符生成 | 低 | 快 | 否 |

### 支持版本
- 1.16.5
- 1.17.1
- 1.18.2
- 1.19.4
- 1.20.6
- 1.21.5
- 1.21.11
- 自定义版本

## 🔧 高级使用

### 命令行模式
bash
基本用法
python src\main.py "材质包.zip" "1.21.11"
指定输出路径
python src\main.py "材质包.zip" "1.21.11" "输出路径.zip"
### 开发者使用
bash
克隆项目
git clone https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git
cd Minecraft-Texture-Converter-AI
创建虚拟环境
python -m venv venv
venv\Scripts\activate
安装依赖
pip install -r requirements.txt
运行测试
python test_basic.py
直接运行
python src\main.py
## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 支持

- 🐛 [问题报告](https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git/issues)
- 💬 [讨论区](https://github.com/CupTeaMilK/Minecraft-Texture-Converter-AI-mixed-.git/discussions)
- 📧 邮箱: cupteamilk@163.com

## 🙏 致谢

- [Stable Diffusion](https://stability.ai/stable-diffusion) - 用于AI生成
- [Hugging Face](https://huggingface.co) - 模型托管
- [PyTorch](https://pytorch.org) - 深度学习框架
- [Pillow](https://python-pillow.org) - 图像处理库

## 📈 更新日志

### v1.0.0 (2024-XX-XX)
- ✅ 初始版本发布
- ✅ 支持三种生成模式
- ✅ 版本转换功能
- ✅ 一键安装脚本
- ✅ AI模型下载

---

**Made with ❤️ for the Minecraft community**
