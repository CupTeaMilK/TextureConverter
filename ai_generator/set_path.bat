@echo off
chcp 65001 >nul

:: 设置AI模型路径
set HF_HOME=D:\mc\TextureConverter\ai_generator\models
set TRANSFORMERS_CACHE=%HF_HOME%
set DIFFUSERS_CACHE=%HF_HOME%

echo ✅ AI模型路径: %HF_HOME%
echo 运行 python test_ai_generation.py 测试

pause
