@echo off
chcp 65001 >nul
title 安装Python依赖
color 0A

echo ================================================
echo    安装Python依赖
echo ================================================
echo.

echo 1. 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未找到
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

echo 2. 升级pip...
python -m pip install --upgrade pip
echo.

echo 3. 检查当前目录...
echo 当前目录: %cd%
dir requirements.txt
if not exist "requirements.txt" (
    echo ❌ 找不到requirements.txt
    pause
    exit /b 1
)
echo.

echo 4. 读取依赖列表...
python -c "
with open('requirements.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    deps = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    print(f'找到 {len(deps)} 个依赖项')
    for dep in deps:
        print(f'  - {dep}')
"
echo.

echo 5. 安装依赖...
echo 这可能需要一些时间，请保持网络连接...
echo 使用国内镜像源加速下载...
echo.

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    echo 尝试使用备用镜像源...
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
)

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成
echo.

echo 6. 验证安装...
python scripts/verify_dependencies.py
if %errorlevel% neq 0 (
    echo ⚠️  验证失败
) else (
    echo ✅ 验证通过
)

echo.
echo ================================================
echo 安装完成!
echo 可以运行 scripts/start.bat 启动程序
echo ================================================
echo.

pause