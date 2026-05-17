@echo off
chcp 65001 >nul
title Minecraft AI材质转换器
color 0A

echo ================================================
echo    Minecraft AI材质转换器
echo    版本 1.0.0
echo ================================================
echo.

:: 设置项目路径
set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

echo 项目路径: %PROJECT_DIR%
echo.

:: 读取配置文件中的路径
for /f "tokens=2 delims=:" %%a in ('findstr "install_dir" config.json') do (
    set "INSTALL_DIR=%%a"
    set INSTALL_DIR=!INSTALL_DIR:"=!
    set INSTALL_DIR=!INSTALL_DIR:,=!
    set INSTALL_DIR=!INSTALL_DIR: =!
)

:: 设置AI模型路径
set MODEL_DIR=%INSTALL_DIR%\ai_generator\models
set HF_HOME=%MODEL_DIR%
set TRANSFORMERS_CACHE=%HF_HOME%
set DIFFUSERS_CACHE=%HF_HOME%

echo AI模型路径: %HF_HOME%
echo.

:: 检查AI模型
if exist "%HF_HOME%\v1-5-pruned.safetensors" (
    echo ✅ AI模型已安装
) else (
    echo ❌ AI模型未安装
    echo 如需AI生成，请先下载AI模型
    echo 运行: scripts\download_model.bat
)
echo.

:: 检查Python环境
echo 检查环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未找到
    pause
    exit /b 1
)

echo ✅ 环境正常
echo.

:: 启动主程序
echo 启动主程序...
echo ================================================
echo.

python src\main.py

echo.
echo ================================================
echo 程序运行结束
echo ================================================
echo.

pause