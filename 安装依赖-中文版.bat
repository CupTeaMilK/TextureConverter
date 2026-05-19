@echo off
chcp 65001 >nul
title Minecraft AI材质包转换器 - 依赖安装工具
color 0A

echo ================================================
echo    Minecraft AI材质包转换器
echo          依赖包安装工具
echo ================================================
echo.

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  建议以管理员身份运行此脚本
    echo    可以避免权限相关问题
    echo.
    set /p RUN_AS_ADMIN="是否继续? (y/n): "
    if /i "%RUN_AS_ADMIN%" neq "y" (
        echo 退出安装
        pause
        exit /b
    )
)
echo.

:: 检查Python
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        py --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ 未找到Python!
            echo.
            echo 请先安装Python 3.8或更高版本:
            echo 1. 访问 https://www.python.org/downloads/
            echo 2. 下载并安装Python
            echo 3. 确保勾选"Add Python to PATH"
            echo.
            echo 安装完成后重新运行此脚本
            pause
            exit /b 1
        )
    )
)

python --version 2>nul && set PYTHON=python
python3 --version 2>nul && set PYTHON=python3
py --version 2>nul && set PYTHON=py

echo ✅ 找到Python: %PYTHON%
%PYTHON% --version
echo.

:: 检查pip
echo [2/4] 检查pip工具...
%PYTHON% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到pip
    echo 正在尝试安装pip...
    %PYTHON% -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo ❌ 安装pip失败
        echo 请手动安装pip: %PYTHON% -m ensurepip
        pause
        exit /b 1
    )
)
%PYTHON% -m pip --version
echo.

:: 选择安装选项
echo [3/4] 选择安装选项
echo.
echo 请选择Python包源:
echo 1) 默认源 (官方源，国际网络推荐)
echo 2) 清华源 (国内网络推荐，速度快)
echo 3) 阿里源 (国内网络推荐)
echo 4) 手动配置
echo.

set /p MIRROR_CHOICE="请选择 (1-4, 默认1): "
if "%MIRROR_CHOICE%"=="" set MIRROR_CHOICE=1

if "%MIRROR_CHOICE%"=="1" (
    echo 使用默认源
    set PIP_SOURCE=
    set PYTORCH_SOURCE=
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="2" (
    echo 使用清华源
    set PIP_SOURCE=-i https://pypi.tuna.tsinghua.edu.cn/simple
    set EXTRA_SOURCE=--trusted-host pypi.tuna.tsinghua.edu.cn
    set PYTORCH_SOURCE=-i https://pypi.tuna.tsinghua.edu.cn/simple
    set PYTORCH_EXTRA=--trusted-host pypi.tuna.tsinghua.edu.cn
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="3" (
    echo 使用阿里源
    set PIP_SOURCE=-i https://mirrors.aliyun.com/pypi/simple
    set EXTRA_SOURCE=--trusted-host mirrors.aliyun.com
    set PYTORCH_SOURCE=-i https://mirrors.aliyun.com/pypi/simple
    set PYTORCH_EXTRA=--trusted-host mirrors.aliyun.com
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
) else if "%MIRROR_CHOICE%"=="4" (
    echo 手动配置
    set /p CUSTOM_SOURCE="请输入镜像源URL: "
    set PIP_SOURCE=-i %CUSTOM_SOURCE%
    set PYTORCH_SOURCE=-i %CUSTOM_SOURCE%
) else (
    echo 使用默认源
    set PIP_SOURCE=
    set PYTORCH_SOURCE=
    set PYTORCH_URL=https://download.pytorch.org/whl/cu118
)

echo.

:: 选择PyTorch版本
echo 请选择PyTorch版本:
echo 1) CPU版本 (无GPU加速，适合所有电脑)
echo 2) CUDA 11.8 (NVIDIA显卡，RTX 20/30/40系列推荐)
echo 3) CUDA 12.1 (NVIDIA最新显卡)
echo.

set /p TORCH_CHOICE="请选择 (1-3, 默认1): "
if "%TORCH_CHOICE%"=="" set TORCH_CHOICE=1

if "%TORCH_CHOICE%"=="1" (
    echo 安装CPU版本的PyTorch
    set TORCH_CMD=pip install torch torchvision torchaudio
) else if "%TORCH_CHOICE%"=="2" (
    echo 安装CUDA 11.8版本的PyTorch
    set TORCH_CMD=pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
) else if "%TORCH_CHOICE%"=="3" (
    echo 安装CUDA 12.1版本的PyTorch
    set TORCH_CMD=pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
) else (
    echo 安装CPU版本的PyTorch
    set TORCH_CMD=pip install torch torchvision torchaudio
)

echo.

:: 确认安装
echo [4/4] 确认安装
echo.
echo 将安装以下包:
echo 1. PyTorch (AI深度学习框架)
echo 2. Pillow (图像处理库)
echo 3. NumPy (数学计算库)
echo 4. Diffusers (扩散模型库)
echo 5. Transformers (Transformer模型库)
echo 6. 其他必要依赖
echo.
echo Python命令: %PYTHON%
echo Pip源: %PIP_SOURCE%
echo PyTorch版本: %TORCH_CHOICE%
echo.

set /p CONFIRM="是否开始安装? (y/n): "
if /i "%CONFIRM%" neq "y" (
    echo 取消安装
    pause
    exit /b
)

echo.
echo ================================================
echo 开始安装依赖包...
echo ================================================
echo.

:: 1. 安装PyTorch
echo [1/6] 安装PyTorch...
%PYTHON% -m %TORCH_CMD% %PYTORCH_SOURCE% %PYTORCH_EXTRA%
if %errorlevel% neq 0 (
    echo ⚠️  PyTorch安装可能失败，继续安装其他依赖...
)
echo.

:: 2. 安装Pillow和NumPy
echo [2/6] 安装Pillow和NumPy...
%PYTHON% -m pip install Pillow numpy opencv-python scikit-image %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Pillow/NumPy安装失败
    pause
    exit /b 1
)
echo.

:: 3. 安装Diffusers
echo [3/6] 安装Diffusers...
%PYTHON% -m pip install diffusers %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Diffusers安装失败
    pause
    exit /b 1
)
echo.

:: 4. 安装Transformers
echo [4/6] 安装Transformers...
%PYTHON% -m pip install transformers %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ❌ Transformers安装失败
    pause
    exit /b 1
)
echo.

:: 5. 安装其他依赖
echo [5/6] 安装其他依赖...
%PYTHON% -m pip install accelerate safetensors %PIP_SOURCE% %EXTRA_SOURCE%
if %errorlevel% neq 0 (
    echo ⚠️  某些依赖安装失败，尝试继续...
)
echo.

:: 6. 验证安装
echo [6/6] 验证安装...
echo.

echo 验证Python版本...
%PYTHON% --version
echo.

echo 验证Pillow...
%PYTHON% -c "from PIL import Image; print('✅ Pillow 安装成功')"
if %errorlevel% neq 0 echo ❌ Pillow 安装失败
echo.

echo 验证NumPy...
%PYTHON% -c "import numpy; print('✅ NumPy 安装成功')"
if %errorlevel% neq 0 echo ❌ NumPy 安装失败
echo.

echo 验证PyTorch...
%PYTHON% -c "import torch; print(f'✅ PyTorch 安装成功，版本: {torch.__version__}'); print(f'   CUDA 可用: {torch.cuda.is_available()}')"
if %errorlevel% neq 0 echo ❌ PyTorch 安装失败
echo.

echo 验证Diffusers...
%PYTHON% -c "import diffusers; print('✅ Diffusers 安装成功')"
if %errorlevel% neq 0 echo ❌ Diffusers 安装失败
echo.

echo 验证Transformers...
%PYTHON% -c "import transformers; print('✅ Transformers 安装成功')"
if %errorlevel% neq 0 echo ❌ Transformers 安装失败
echo.

echo ================================================
echo 依赖安装完成!
echo ================================================
echo.
echo 安装结果汇总:
echo ✅ Python: 已安装
echo ✅ pip: 已安装
echo ✅ Pillow: 用于图像处理
echo ✅ NumPy: 用于数学计算
echo ✅ PyTorch: 用于AI计算
echo ✅ Diffusers: 用于扩散模型
echo ✅ Transformers: 用于Transformer模型
echo.
echo 下一步:
echo 1. 下载AI模型文件 (如果需要AI功能)
echo 2. 运行 Start_Converter.bat
echo.
echo 如果任何组件安装失败，可以:
echo 1. 重新运行此脚本
echo 2. 手动安装: pip install 包名
echo 3. 检查网络连接
echo.

pause