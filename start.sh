#!/bin/bash
echo "Minecraft AI材质包转换器"
echo "=========================="

# 检查Python
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    python --version >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "❌ 未找到Python，请先安装Python 3.8+"
        exit 1
    else
        PYTHON=python
    fi
else
    PYTHON=python3
fi

# 检查依赖
echo "检查依赖..."
$PYTHON -c "import PIL, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "请先安装依赖：pip install -r requirements.txt"
    exit 1
fi

# 运行主程序
$PYTHON main.py