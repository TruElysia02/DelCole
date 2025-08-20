@echo off
echo 创建手势识别虚拟环境...
mamba create -n hand_gesture python=3.9 -y
echo 激活环境...
call mamba activate hand_gesture
echo 安装依赖...
mamba install -c conda-forge opencv numpy -y
pip install mediapipe==0.10.3
echo 环境设置完成！
echo.
echo 使用方法：
echo 1. 激活环境：mamba activate hand_gesture
echo 2. 运行程序：python hand_gesture_detection.py
echo.
echo 或者直接运行本脚本启动程序：
call mamba activate hand_gesture && python hand_gesture_detection.py