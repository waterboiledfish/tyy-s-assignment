@echo off
chcp 65001 >nul
title 传媒资讯交互数据分析平台

echo 正在启动：传媒资讯交互数据分析平台
echo.

python --version >nul 2>nul
if errorlevel 1 (
    echo 未检测到 Python。
    echo 请先安装 Python 3.10 或更高版本，并在安装时勾选 Add Python to PATH。
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo 正在检查 Matplotlib 依赖...
python -c "import matplotlib" >nul 2>nul
if errorlevel 1 (
    echo 未安装 Matplotlib，正在自动安装，请稍等...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Matplotlib 自动安装失败。
        echo 可以手动执行：python -m pip install matplotlib
        echo.
        pause
        exit /b 1
    )
)

echo 依赖检查完成，正在打开程序...
echo.
python media_insight_platform.py

echo.
echo 程序已关闭。
pause
