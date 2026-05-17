@echo off
chcp 65001 >nul
title 下载AI模型
color 0A

echo ================================================
echo    AI模型下载器
echo    自动下载Stable Diffusion v1.5
echo ================================================
echo.

:: 设置项目路径
set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

echo 项目路径: %PROJECT_DIR%
echo.

:: 读取配置文件中的路径
for /f "tokens=2 delims=:" %%a in ('findstr "models_dir" config.json') do (
    set "MODEL_DIR=%%a"
    set MODEL_DIR=!MODEL_DIR:"=!
    set MODEL_DIR=!MODEL_DIR:,=!
    set MODEL_DIR=!MODEL_DIR: =!
)

echo AI模型将下载到: %MODEL_DIR%
echo.

:: 创建目录
if not exist "%MODEL_DIR%" (
    mkdir "%MODEL_DIR%"
    echo ✅ 创建模型目录
)

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未找到
    pause
    exit /b 1
)

:: 检查网络
echo 检查网络连接...
ping -n 1 www.baidu.com >nul
if %errorlevel% neq 0 (
    echo ❌ 网络连接失败
    pause
    exit /b 1
)

echo ✅ 网络正常
echo.

echo 开始下载AI模型...
echo 这将下载约4.3GB的文件
echo 需要稳定的网络连接，可能需要30-60分钟
echo 请勿关闭此窗口！
echo.

:: 设置环境变量
set HF_HOME=%MODEL_DIR%
set TRANSFORMERS_CACHE=%HF_HOME%
set DIFFUSERS_CACHE=%HF_HOME%

:: 运行Python下载脚本
python scripts\download_model.py

echo.
echo ================================================
echo 下载完成！
echo 模型已保存到: %MODEL_DIR%
echo ================================================
echo.

pause