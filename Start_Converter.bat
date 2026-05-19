@echo off
chcp 65001 >nul
title Minecraft AI Texture Pack Converter
color 0A

echo ================================================
echo    Minecraft AI Texture Pack Converter
echo    Fixed Model Detection Issues
echo ================================================
echo.

:: 1. Check Python
echo [1/8] Checking Python environment...

:: Try to find Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_PATH=python
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_PATH=python3
    goto :python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_PATH=py
    goto :python_found
)

echo ❌ Python not found!
echo    Please install Python 3.8+ and add it to PATH
pause
exit /b 1

:python_found
echo ✅ Python found: %PYTHON_PATH%
%PYTHON_PATH% --version
echo.

:: 2. Set AI model paths
echo [2/8] Setting up AI model paths...

:: Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"
set "AI_DIR=%PROJECT_ROOT%ai_generator"
set "HF_HOME=%AI_DIR%\models"
set "TRANSFORMERS_CACHE=%HF_HOME%"
set "DIFFUSERS_CACHE=%HF_HOME%"

echo ✅ Script directory: %SCRIPT_DIR%
echo ✅ Project root: %PROJECT_ROOT%
echo ✅ AI model path: %AI_DIR%
echo.

:: 3. Check AI model directory
echo [3/8] Checking AI model directory...
if not exist "%HF_HOME%" (
    mkdir "%HF_HOME%" 2>nul
    if not exist "%HF_HOME%" (
        echo ❌ Cannot create AI model directory
    ) else (
        echo ✅ Created AI model directory
    )
) else (
    echo ✅ AI model directory exists
    echo    Content:
    dir "%HF_HOME%" 2>nul | find "file(s)" 2>nul || echo   (empty directory)
)
echo.

:: 4. Check AI model files
echo [4/8] Checking AI model files...
set "MODEL_FOUND=0"
set "SIZE_GB=0"

if exist "%HF_HOME%\v1-5-pruned.safetensors" (
    echo ✅ Found v1-5-pruned.safetensors
    set "MODEL_FOUND=1"
) else (
    echo ❌ v1-5-pruned.safetensors not found
    echo    You can download it manually to: %HF_HOME%
    set "MODEL_FOUND=0"
)

if exist "%HF_HOME%\model_index.json" (
    echo ✅ Found config file
) else (
    echo ❌ model_index.json not found
)

echo.

:: 5. Check basic dependencies
echo [5/8] Checking basic dependencies...

%PYTHON_PATH% -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Pillow not installed
) else (
    echo ✅ Pillow installed
)

%PYTHON_PATH% -c "import numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  numpy not installed
) else (
    echo ✅ numpy installed
)
echo.

:: 6. Check AI dependencies
echo [6/8] Checking AI dependencies...
if "%MODEL_FOUND%"=="1" (
    echo AI model detected, checking AI dependencies...
    
    %PYTHON_PATH% -c "import torch" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ PyTorch not installed
        set "AI_READY=0"
    ) else (
        echo ✅ PyTorch installed
        set "AI_READY=1"
    )
    
    %PYTHON_PATH% -c "import diffusers" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ diffusers not installed
        set "AI_READY=0"
    ) else (
        echo ✅ diffusers installed
        set "AI_READY=1"
    )
    
    if "%AI_READY%"=="1" (
        echo ✅ AI features ready
    ) else (
        echo ⚠️ AI features not available
    )
) else (
    echo ℹ️ AI model not found, will use smart procedural generation
)
echo.

:: 7. Check main program
echo [7/8] Checking main program file...
if not exist "main.py" (
    echo ❌ main.py not found
    pause
    exit /b 1
)
echo ✅ Found main.py
echo.

:: 8. Start program
echo [8/8] Starting Minecraft AI Texture Converter...
echo ================================================
echo.

if "%MODEL_FOUND%"=="1" (
    echo 🤖 AI model ready
    echo 💡 Tip: "AI Deep Learning Generation" option will be available
) else (
    echo 🤖 AI model not found
    echo 💡 Tip: "Smart Procedural Generation" and "Basic Placeholder Generation" options will be available
)
echo.

echo Starting program...
echo ================================================
echo.

:: Change to script directory
cd /d "%SCRIPT_DIR%"

%PYTHON_PATH% main.py

echo.
echo ================================================
echo Program finished
echo ================================================
echo.

pause