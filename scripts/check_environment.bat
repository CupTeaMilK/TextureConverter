@echo off
chcp 65001 >nul
title 检查环境
color 0A

echo ================================================
echo    环境检查工具
echo ================================================
echo.

echo 1. 检查Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装
) else (
    echo ✅ Python已安装
    python -c "import sys; print('   版本:', sys.version.split()[0])"
)
echo.

echo 2. 检查项目路径...
set PROJECT_DIR=%~dp0..
if exist "%PROJECT_DIR%" (
    echo ✅ 项目目录: %PROJECT_DIR%
) else (
    echo ❌ 项目目录不存在
)
echo.

echo 3. 检查配置文件...
if exist "%PROJECT_DIR%\config.json" (
    echo ✅ config.json 存在
) else (
    echo ❌ config.json 不存在
)
echo.

echo 4. 检查Python依赖...
python -c "
import sys
print('检查依赖库...')

deps = [
    ('torch', 'PyTorch'),
    ('diffusers', 'Diffusers'),
    ('transformers', 'Transformers'),
    ('numpy', 'NumPy'),
    ('PIL', 'Pillow'),
]

all_ok = True
for module, name in deps:
    try:
        if module == 'PIL':
            import PIL
            print(f'  ✅ {name}: 已安装')
        else:
            __import__(module)
            print(f'  ✅ {name}: 已安装')
    except ImportError:
        print(f'  ❌ {name}: 未安装')
        all_ok = False

if all_ok:
    print('✅ 所有依赖库已安装')
else:
    print('❌ 有依赖库未安装')
    print('   请运行: pip install -r requirements.txt')
"
echo.

echo 5. 检查AI模型...
set MODEL_DIR=D:\mc\TextureConverter_Github\ai_generator\models
if exist "%MODEL_DIR%\v1-5-pruned.safetensors" (
    echo ✅ AI模型已安装
    python -c "
import os
path = r'%MODEL_DIR%\v1-5-pruned.safetensors'
if os.path.exists(path):
    size = os.path.getsize(path) / (1024**3)
    print(f'   大小: {size:.1f} GB')
"
) else (
    echo ❌ AI模型未安装
    echo 运行: download_model.bat
)
echo.

echo ================================================
echo 检查完成！
echo 如果没有红色错误，可以正常运行程序
echo ================================================
echo.

pause