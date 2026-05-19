# 🎮 Minecraft AI Texture Pack Converter

![GitHub](https://img.shields.io/badge/Python-3.8%2B-blue)
![GitHub](https://img.shields.io/badge/License-MIT-green)
![GitHub](https://img.shields.io/badge/Platform-Windows%20%7C%20MacOS%20%7C%20Linux-orange)

This is a powerful Minecraft texture pack conversion tool that can:

- 🔥 **AI-Enhanced Textures** - Uses Stable Diffusion to increase texture resolution
- 🧠 **Intelligent Completion** - Automatically generates missing texture files
- 🎨 **Batch Processing** - One-click conversion of entire texture packs
- 🏷️ **Version Adaptation** - Supports multiple Minecraft versions

## 🚨 IMPORTANT WARNING: MUST READ FOR NEW USERS! 🚨

**Before using this tool, you MUST complete the following two steps, otherwise the program will not run!**

### Step 1: Install Python 3.8+
1. Visit the [Python official website](https://www.python.org/downloads/) to download Python
2. **During installation, make sure to check "Add Python to PATH"** (adds Python to system path)
3. After installation, **restart your computer**

### Step 2: Download AI Model Files
1. Download the Stable Diffusion 1.5 model (e.g., `v1-5-pruned.safetensors`, approx. 4GB)
2. Find the `ai_generator/models/` folder in the project
3. Place the model file in this folder

**⚠️ Without Python, the program cannot run! Without AI model, AI features cannot be used! ⚠️**

### Author's Notes
1. AI model is optional, the program can run without it (but some features will be limited)
2. If you use the AI model, DO NOT change the directory structure! Relative paths are already set, do not modify them arbitrarily!
3. Generated texture packs are in the root directory
4. Due to Chinese encoding crash issues that bothered me for a long time, I made the launcher `.bat` file content entirely in English, but `main.py` and other main files remain in Chinese
5. Part of the code and comments were written with the help of AI (I went back to check halfway and found no comments QwQ, so I asked AI to add them)
6. Don't install Python versions that are too new or too old, otherwise plugins may be incompatible. Best to use the same version as me: 3.10.0

---

## 📦 Quick Start

### Method 1: One-Click Installation (Recommended for Beginners)
1. Download this project to your computer
2. Double-click to run `install_dependencies-chinese_version.bat`
3. Follow the prompts to select options
4. Wait for installation to complete

### Method 2: Manual Installation
bash
Install basic dependencies
pip install -r requirements.txt
Install AI-related dependencies (optional)
pip install -r requirements_ai.txt
---

## 🎯 Features

### 🤖 AI Enhancement Mode
- Automatically increases texture resolution (16x → 32x/64x/128x)
- Preserves original texture style
- Supports batch processing

### 🧩 Intelligent Completion
- Automatically detects missing textures
- Intelligently generates based on similar textures
- Supports custom generation rules

### 🔄 Batch Conversion
- One-click conversion of entire texture packs
- Supports multiple output formats
- Progress display and error handling

### ⚙️ Custom Configuration
- Adjust AI generation parameters
- Set output quality
- Select target versions

---

## 🖥️ Usage

### Basic Usage
1. Double-click `Start_Converter.bat`
2. Drag the texture pack `.zip` file into the window
3. Select processing mode:
   - 1: AI Enhancement Mode (requires model)
   - 2: Intelligent Completion Mode
   - 3: Hybrid Mode
4. Select output quality
5. Wait for processing to complete

### Command Line Usage
bash
Basic conversion
python main.py --input "texture_pack.zip"
AI enhancement mode
python main.py --input "texture_pack.zip" --mode ai
Specify output quality
python main.py --input "texture_pack.zip" --quality high
Batch process folder
python main.py --input "texture_pack_folder" --batch
### Advanced Parameters
bash
View all options
python main.py --help
Custom parameter example
python main.py \
--input "texture_pack.zip" \
--output "output_folder" \
--mode hybrid \
--quality ultra \
--scale 2 \
--device cuda
---

## 📁 Project Structure
TextureConverter/
├── core/ # Core conversion module
│ ├── converter.py # Main converter
│ └── texture_generation.py # Texture generation
├── ai_generator/ # AI generation module
│ ├── models/ # 【Place your AI model here】
│ ├── ai_texture_generator.py
│ └── init.py
├── utils/ # Utility functions
│ ├── file_utils.py
│ ├── image_utils.py
│ └── init.py
├── MSL/ # Material Standard Library
│ └── texture_library.json
├── Start_Converter.bat # Launcher script
├── main.py # Main program
├── requirements.txt # Basic dependencies
├── requirements_ai.txt # AI dependencies
├── install_dependencies-english_version.bat
├── 安装依赖-中文版.bat
└── README.md # This file
---

## ⚙️ Configuration

### AI Model Configuration
1. Place model files in `ai_generator/models/`
2. Supported formats: `.safetensors`, `.ckpt`, `.pth`
3. Recommended model: Stable Diffusion 1.5/2.1

### Hardware Requirements
- **Minimum**: 8GB RAM, 4GB VRAM (for AI mode)
- **Recommended**: 16GB RAM, 8GB+ VRAM
- **Storage**: At least 10GB free space

### Performance Optimization
python
Adjust in config.py
AI_CONFIG = {
"use_gpu": True, # Use GPU acceleration
"precision": "fp16", # Half-precision floating point
"batch_size": 1, # Batch size
"cache_models": True # Cache models
}
---

## ❓ Frequently Asked Questions

### Q1: "Python not found" error on startup
**A**: Python is not installed correctly or not added to PATH. Reinstall Python and check "Add Python to PATH".

### Q2: AI feature error "Model not found"
**A**: You haven't downloaded the AI model file. Please refer to Step 2 above and place the model in `ai_generator/models/`.

### Q3: Slow performance
**A**: Check if GPU is being used. Add `--device cuda` parameter in command line.

### Q4: Insufficient memory
**A**: Try reducing output quality or use CPU mode: `--device cpu --quality medium`

### Q5: Generated textures are blurry
**A**: Try increasing AI steps: `--steps 50` or use higher scaling: `--scale 4`

---

## 🐛 Issue Reporting

Encountered an issue? Please:

1. Check the log files in the `logs/` directory
2. Submit an issue on GitHub Issues
3. Include the following information:
   - Error message screenshot
   - Your system configuration
   - Model name used
   - Steps to reproduce

---

## 📄 License

This project uses the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the [Stable Diffusion](https://github.com/CompVis/stable-diffusion) team
- Thanks to [Hugging Face](https://huggingface.co/) for providing models
- Thanks to all testers and contributors

---

## ⭐ Supporting the Project

If this project helps you, please:

1. Give the project a Star ⭐
2. Share with other Minecraft players
3. Submit PRs or Issues to help improve

**Enjoy the visual feast of high-definition textures! 🎮✨**
