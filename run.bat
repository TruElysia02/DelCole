@echo off
echo 激活环境并启动手势识别程序...
call mamba activate hand_gesture
python hand_gesture_detection.py
pause