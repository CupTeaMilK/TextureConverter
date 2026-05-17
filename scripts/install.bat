@echo off
chcp 65001 >nul
title Minecraft AI材质转换器 - 一键安装程序
color 0A

echo ================================================
echo    Minecraft AI材质转换器 - 一键安装
echo ================================================
echo.

echo 版本: 1.0.0
echo 作者: YourName
echo 项目: https://github.com/yourname/Minecraft-Texture-Converter-AI
echo.

echo 1. 检查系统要求...
echo   操作系统: Windows 10/11
echo   内存: 最低8GB，推荐16GB
echo   磁盘空间: 最低20GB
echo   显卡: 支持CUDA的NVIDIA显卡（可选，CPU也可运行）
echo.

echo 2. 检查Python环境...
set PYTHON310=C:\Users\DELL\AppData\Local\Programs\Python\Python310\python.exe
set PYTHON_PATH=%PYTHON310%

if not exist "%PYTHON_PATH%" (
    echo ⚠️  找不到指定Python路径，尝试使用系统Python...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 找不到Python！
        echo 请确保Python 3.8+已安装并添加到PATH
        echo 从 https://www.python.org/downloads/ 下载Python
        echo 安装时务必勾选"Add Python to PATH"
        echo.
        pause
        exit /b 1
    )
    set PYTHON_PATH=python
    echo ✅ 使用系统Python
) else (
    echo ✅ 找到Python 3.10: %PYTHON_PATH%
)

"%PYTHON_PATH%" --version
echo.

echo 3. 设置安装路径...
echo   默认安装到: D:\mc\TextureConverter_Github
echo   如需更改，请修改脚本中的 INSTALL_DIR 变量
echo.

set INSTALL_DIR=D:\mc\TextureConverter_Github
set PROJECT_DIR=%INSTALL_DIR%\Minecraft-Texture-Converter-AI

echo 安装到: %PROJECT_DIR%
echo.

set /p CONTINUE=是否继续? (y/n): 
if /i not "%CONTINUE%"=="y" (
    echo 安装已取消
    pause
    exit /b
)
echo.

echo 4. 创建目录结构...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✅ 创建安装目录: %INSTALL_DIR%
)

if not exist "%PROJECT_DIR%" (
    mkdir "%PROJECT_DIR%"
    echo ✅ 创建项目目录: %PROJECT_DIR%
) else (
    echo ⚠️  项目目录已存在
    set /p OVERWRITE=是否覆盖现有文件? (y/n): 
    if /i "%OVERWRITE%"=="y" (
        echo 正在备份旧文件...
        if exist "%PROJECT_DIR%\backup" (
            rmdir /s /q "%PROJECT_DIR%\backup"
        )
        mkdir "%PROJECT_DIR%\backup"
        xcopy "%PROJECT_DIR%\*.*" "%PROJECT_DIR%\backup\" /E /Y /Q
        echo ✅ 已备份到: %PROJECT_DIR%\backup\
    ) else (
        echo 安装已取消
        pause
        exit /b
    )
)
echo.

echo 5. 复制项目文件...
echo 正在复制，请稍候...

:: 复制当前目录的所有文件到项目目录
set "SOURCE_DIR=%~dp0"

echo 源目录: %SOURCE_DIR%
echo 目标目录: %PROJECT_DIR%
echo.

:: 复制根目录文件
for %%F in (
    "README.md"
    "LICENSE"
    "requirements.txt"
    "config.json"
    ".gitignore"
    "test_basic.py"
    "check_project.py"
    "clean_for_upload.py"
) do (
    if exist "%%~F" (
        copy "%%~F" "%PROJECT_DIR%\" >nul
        echo ✅ 复制: %%~F
    )
)

:: 创建必要的子目录
mkdir "%PROJECT_DIR%\ai_generator" 2>nul
mkdir "%PROJECT_DIR%\ai_generator\models" 2>nul
mkdir "%PROJECT_DIR%\resources" 2>nul
mkdir "%PROJECT_DIR%\resources\example_pack" 2>nul
mkdir "%PROJECT_DIR%\docs" 2>nul
mkdir "%PROJECT_DIR%\scripts" 2>nul
mkdir "%PROJECT_DIR%\src" 2>nul
mkdir "%PROJECT_DIR%\output" 2>nul

echo ✅ 目录结构创建完成
echo.

:: 复制脚本目录
if exist "scripts" (
    xcopy "scripts" "%PROJECT_DIR%\scripts\" /E /Y /Q
    echo ✅ 复制: scripts/ 目录
)

:: 复制源代码目录
if exist "src" (
    xcopy "src" "%PROJECT_DIR%\src\" /E /Y /Q
    echo ✅ 复制: src/ 目录
)

:: 复制文档目录
if exist "docs" (
    xcopy "docs" "%PROJECT_DIR%\docs\" /E /Y /Q
    echo ✅ 复制: docs/ 目录
)

:: 复制示例资源
if exist "resources" (
    xcopy "resources" "%PROJECT_DIR%\resources\" /E /Y /Q
    echo ✅ 复制: resources/ 目录
)
echo.

echo 6. 安装Python依赖...
echo 这可能需要几分钟，请保持网络连接...
echo 如果安装失败，可以手动运行: cd "%PROJECT_DIR%" && pip install -r requirements.txt
echo.

:: 切换到项目目录
cd /d "%PROJECT_DIR%"

:: 先升级pip
echo 升级pip...
"%PYTHON_PATH%" -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

:: 安装依赖
echo 安装依赖库...
"%PYTHON_PATH%" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，尝试使用备用镜像源...
    "%PYTHON_PATH%" -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败，请手动安装
        echo 运行: cd "%PROJECT_DIR%" && pip install -r requirements.txt
    ) else (
        echo ✅ 依赖安装完成
    )
) else (
    echo ✅ 依赖安装完成
)
echo.

:: 验证安装
echo 验证依赖安装...
"%PYTHON_PATH%" -c "
import sys
print('Python版本:', sys.version.split()[0])

deps = [
    ('torch', 'PyTorch'),
    ('diffusers', 'Diffusers'),
    ('transformers', 'Transformers'),
    ('PIL', 'Pillow'),
    ('numpy', 'NumPy'),
    ('requests', 'Requests'),
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
    print('✅ 所有核心依赖已安装')
else:
    print('❌ 有依赖未安装，请手动安装')
"
echo.

echo 7. 创建桌面快捷方式...
set SHORTCUT_NAME=Minecraft AI材质转换器
set SHORTCUT_PATH=%USERPROFILE%\Desktop\%SHORTCUT_NAME%.lnk
set TARGET_PATH=%PROJECT_DIR%\scripts\start.bat
set WORKING_DIR=%PROJECT_DIR%
set ICON_PATH=

echo 快捷方式: %SHORTCUT_PATH%
echo 目标: %TARGET_PATH%
echo 工作目录: %WORKING_DIR%
echo.

:: 创建快捷方式的VBS脚本
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%WORKING_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "Minecraft AI材质转换器" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs" >nul
del "%TEMP%\create_shortcut.vbs"

if exist "%SHORTCUT_PATH%" (
    echo ✅ 桌面快捷方式已创建
) else (
    echo ⚠️  快捷方式创建失败，请手动创建
)
echo.

:: 创建下载AI模型的快捷方式
set SHORTCUT_NAME2=下载AI模型
set SHORTCUT_PATH2=%USERPROFILE%\Desktop\%SHORTCUT_NAME2%.lnk
set TARGET_PATH2=%PROJECT_DIR%\scripts\download_model.bat

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut2.vbs"
echo sLinkFile = "%SHORTCUT_PATH2%" >> "%TEMP%\create_shortcut2.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut2.vbs"
echo oLink.TargetPath = "%TARGET_PATH2%" >> "%TEMP%\create_shortcut2.vbs"
echo oLink.WorkingDirectory = "%WORKING_DIR%" >> "%TEMP%\create_shortcut2.vbs"
echo oLink.Description = "下载AI模型" >> "%TEMP%\create_shortcut2.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut2.vbs"

cscript //nologo "%TEMP%\create_shortcut2.vbs" >nul
del "%TEMP%\create_shortcut2.vbs"

if exist "%SHORTCUT_PATH2%" (
    echo ✅ 创建快捷方式: 下载AI模型
) else (
    echo ⚠️  快捷方式创建失败
)
echo.

echo 8. 设置环境变量...
:: 设置用户环境变量
setx TEXTURE_CONVERTER_ROOT "%PROJECT_DIR%" >nul
if %errorlevel% equ 0 (
    echo ✅ 已设置环境变量: TEXTURE_CONVERTER_ROOT=%PROJECT_DIR%
) else (
    echo ⚠️  环境变量设置失败，请手动设置
)
echo.

echo 9. 创建配置文件...
if not exist "%PROJECT_DIR%\config.json" (
    (
        echo {
        echo   "project": {
        echo     "name": "Minecraft-Texture-Converter-AI",
        echo     "version": "1.0.0",
        echo     "description": "Minecraft材质包转换器，支持AI生成材质"
        echo   },
        echo   "paths": {
        echo     "install_dir": "D:\\mc\\TextureConverter_Github",
        echo     "models_dir": "D:\\mc\\TextureConverter_Github\\ai_generator\\models",
        echo     "output_dir": "D:\\mc\\TextureConverter_Github\\output"
        echo   },
        echo   "ai": {
        echo     "model_id": "runwayml/stable-diffusion-v1-5",
        echo     "use_gpu": true,
        echo     "cache_dir": "D:\\mc\\TextureConverter_Github\\ai_generator\\models"
        echo   },
        echo   "generation": {
        echo     "default_size": 16,
        echo     "ai_steps": 20,
        echo     "ai_guidance_scale": 7.5
        echo   }
        echo }
    ) > "%PROJECT_DIR%\config.json"
    echo ✅ 已创建配置文件: config.json
) else (
    echo ✅ 配置文件已存在
)
echo.

echo 10. 运行基本测试...
echo 正在测试项目是否可运行...
cd /d "%PROJECT_DIR%"
"%PYTHON_PATH%" -c "
import sys
sys.path.insert(0, '.')
try:
    from src.converter import TexturePackConverter
    print('  ✅ 转换器导入成功')
    
    # 测试初始化
    converter = TexturePackConverter(use_ai=True, ai_model='smart')
    print('  ✅ 转换器初始化成功')
    
    # 检查AI模型目录
    import os
    ai_dir = r'D:\mc\TextureConverter_Github\ai_generator\models'
    if os.path.exists(ai_dir):
        print(f'  ✅ AI模型目录存在: {ai_dir}')
    else:
        print(f'  ⚠️  AI模型目录不存在，需要下载AI模型')
        
    print('  ✅ 基本测试通过')
except Exception as e:
    print(f'  ❌ 测试失败: {e}')
    import traceback
    traceback.print_exc()
"
echo.

echo 11. 安装完成！
echo ================================================
echo 🎉 安装成功完成！
echo.
echo 📁 项目路径: %PROJECT_DIR%
echo 🤖 AI模型路径: %PROJECT_DIR%\ai_generator\models
echo 📦 输出路径: %PROJECT_DIR%\output
echo 🖥️  桌面快捷方式: Minecraft AI材质转换器
echo.
echo 🔧 使用方法:
echo 1. 双击桌面"Minecraft AI材质转换器"快捷方式
echo 2. 如需AI功能，先运行"下载AI模型"快捷方式
echo 3. 将材质包.zip文件拖拽到程序窗口
echo 4. 选择生成模式和目标版本
echo 5. 开始转换
echo.
echo 💡 注意事项:
echo 1. 首次运行AI功能需要下载约4.3GB的模型
echo 2. 下载AI模型时请确保网络稳定
echo 3. 转换过程需要一些时间，请耐心等待
echo 4. 输出文件保存在项目目录的output文件夹
echo ================================================
echo.

echo 是否现在启动程序? (y/n)
set /p LAUNCH= 
if /i "%LAUNCH%"=="y" (
    echo 启动程序...
    timeout /t 2 >nul
    start "" "%TARGET_PATH%"
) else (
    echo 您可以稍后从桌面快捷方式启动程序
)

echo.
pause