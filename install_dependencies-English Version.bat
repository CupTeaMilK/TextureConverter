@echo off
chcp 65001 >nul
title Minecraft AI Texture Pack Converter - Dependency Installer
color 0A

echo ================================================
echo    Minecraft AI Texture Pack Converter
echo         Dependency Installation Tool
echo ================================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  It is recommended to run this script as administrator
    echo     to avoid permission-related issues
    echo.
    set /p RUN_AS_ADMIN="Continue anyway? (y/n): "
    if /i "%RUN_AS_ADMIN%" neq "y" (
        echo Installation cancelled
        pause
        exit /b
    )
)
echo.

:: Check Python
echo [1/4] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        py --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ Python not found!
            echo.
            echo Please install Python 3.8 or higher:
            echo 1. Visit https://www.python.org/downloads/
            echo 2. Download and install Python
            echo 3. Make sure to check "Add Python to PATH"
            echo.
            echo After installation, run this script again
            pause
            exit /b 1
        )
    )
)

python --version 2>nul && set PYTHON=python
python3 --version 2>nul && set PYTHON=python3
py --version 2>nul && set PYTHON=py

echo ✅ Found Python: %PYTHON%
%PYTHON% --version
echo.

:: Check pip
echo [2/4] Checking pip tool...
%PYTHON% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    echo Installing pip...
    %PYTHON% -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pip
        echo Please install pip manually: %PYTHON% -m ensurepip
        pause
        exit /b 1
    )
)
%PYTHON% -m pip --version
echo.

:: Select installation options
echo [3/4] Select installation options
echo.
echo Please select Python package source:
echo 1) Default source (Official, recommended for international network)
echo 2) Tsinghua source (Recommended for China, fast)
echo 3) Aliyun source (Recommended for China)
echo 4) Custom source
echo.

set /p MIRROR_CHOICE="Please choose (1-4, default 1): "
if "%MIRROR_CHOICE%"=="" set MIRROR_CHOICE=1

if "%MIRROR_CHOICE%"=="1" (
    echo Using default source
    set PIP_SOURCE=
    set PYTORCH_SOURCE=
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="2" (
    echo Using Tsinghua source
    set PIP_SOURCE=-i https://pypi.tuna.tsinghua.edu.cn/simple
    set EXTRA_SOURCE=--trusted-host pypi.tuna.tsinghua.edu.cn
    set PYTORCH_SOURCE=-i https://pypi.tuna.tsinghua.edu.cn/simple
    set PYTORCH_EXTRA=--trusted-host pypi.tuna.tsinghua.edu.cn
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="3" (
    echo Using Aliyun source
    set PIP_SOURCE=-i https://mirrors.aliyun.com/pypi/simple
    set EXTRA_SOURCE=--trusted-host mirrors.aliyun.com
    set PYTORCH_SOURCE=-i https://mirrors.aliyun.com/pypi/simple
    set PYTORCH_EXTRA=--trusted-host mirrors.aliyun.com
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="4" (
    echo Custom configuration
    set /p CUSTOM_SOURCE="Please enter mirror URL: "
    set PIP_SOURCE=-i %CUSTOM_SOURCE%
    set PYTORCH_SOURCE=-i %CUSTOM_SOURCE%
) else (
    echo Using default source
    set PIP_SOURCE=
    set PYTORCH_SOURCE=
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
)

echo.

:: Select PyTorch version
echo Please select PyTorch version:
echo 1) CPU version (No GPU acceleration, works on all computers)
echo 2) CUDA 11.8 (NVIDIA GPU, recommended for RTX 20/30/40 series)
echo 3) CUDA 12.1 (Latest NVIDIA GPU)
echo.

set /p TORCH_CHOICE="Please choose (1-3, default 1): "
if "%TORCH_CHOICE%"=="" set TORCH_CHOICE=1

if "%TORCH_CHOICE%"=="1" (
    echo Installing PyTorch CPU version
    set TORCH_CMD=pip install torch torchvision torchaudio
) else if "%TORCH_CHOICE%"=="2" (
    echo Installing PyTorch CUDA 11.8 version
    set TORCH_CMD=pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
) else if "%TORCH_CHOICE%"=="3" (
    echo Installing PyTorch CUDA 12.1 version
    set TORCH_CMD=pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
) else (
    echo Installing PyTorch CPU version
    set TORCH_CMD=pip install torch torchvision torchaudio
)

echo.

:: Confirm installation
echo [4/4] Confirm installation
echo.
echo The following packages will be installed:
echo 1. PyTorch (AI deep learning framework)
echo 2. Pillow (Image processing library)
echo 3. NumPy (Mathematical computing library)
echo 4. Diffusers (Diffusion models library)
echo 5. Transformers (Transformer models library)
echo 6. Other necessary dependencies
echo.
echo Python command: %PYTHON%
echo Pip source: %PIP_SOURCE%
echo PyTorch version: %TORCH_CHOICE%
echo.

set /p CONFIRM="Start installation? (y/n): "
if /i "%CONFIRM%" neq "y" (
    echo Installation cancelled
    pause
    exit /b
)

echo.
echo ================================================
echo Starting dependency installation...
echo ================================================
echo.

:: 1. Install PyTorch
echo [1/6] Installing PyTorch...
%PYTHON% -m %TORCH_CMD% %PYTORCH_SOURCE% %PYTORCH_EXTRA%
if %errorlevel% neq 0 (
    echo ⚠️  PyTorch installation may have failed, continuing...
)
echo.

:: 2. Install Pillow and NumPy
echo [2/6] Installing Pillow and NumPy...
%PYTHON% -m pip install Pillow numpy opencv-python scikit-image %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Pillow/NumPy installation failed
    pause
    exit /b 1
)
echo.

:: 3. Install Diffusers
echo [3/6] Installing Diffusers...
%PYTHON% -m pip install diffusers %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Diffusers installation failed
    pause
    exit /b 1
)
echo.

:: 4. Install Transformers
echo [4/6] Installing Transformers...
%PYTHON% -m pip install transformers %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Transformers installation failed
    pause
    exit /b 1
)
echo.

:: 5. Install other dependencies
echo [5/6] Installing other dependencies...
%PYTHON% -m pip install accelerate safetensors %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ⚠️  Some dependencies failed to install, continuing...
)
echo.

:: 6. Verify installation
echo [6/6] Verifying installation...
echo.

echo Verifying Python version...
%PYTHON% --version
echo.

echo Verifying Pillow...
%PYTHON% -c "from PIL import Image; print('✅ Pillow installed successfully')"
if %errorlevel% neq 0 echo ❌ Pillow installation failed
echo.

echo Verifying NumPy...
%PYTHON% -c "import numpy; print('✅ NumPy installed successfully')"
if %errorlevel% neq 0 echo ❌ NumPy installation failed
echo.

echo Verifying PyTorch...
%PYTHON% -c "import torch; print(f'✅ PyTorch installed successfully, version: {torch.__version__}'); print(f'   CUDA available: {torch.cuda.is_available()}')"
if %errorlevel% neq 0 echo ❌ PyTorch installation failed
echo.

echo Verifying Diffusers...
%PYTHON% -c "import diffusers; print('✅ Diffusers installed successfully')"
if %errorlevel% neq 0 echo ❌ Diffusers installation failed
echo.

echo Verifying Transformers...
%PYTHON% -c "import transformers; print('✅ Transformers installed successfully')"
if %errorlevel% neq 0 echo ❌ Transformers installation failed
echo.

echo ================================================
echo Dependency installation completed!
echo ================================================
echo.
echo Installation summary:
echo ✅ Python: Installed
echo ✅ pip: Installed
echo ✅ Pillow: For image processing
echo ✅ NumPy: For mathematical computing
echo ✅ PyTorch: For AI computing
echo ✅ Diffusers: For diffusion models
echo ✅ Transformers: For transformer models
echo.
echo Next steps:
echo 1. Download AI model files (if AI features are needed)
echo 2. Run Start_Converter.bat
echo.
echo If any component failed to install, you can:
echo 1. Run this script again
echo 2. Install manually: pip install package_name
echo 3. Check network connection
echo.

pause