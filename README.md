# DelCole
# 手势位置与握拳状态识别

本项目使用OpenCV和MediaPipe实现手势位置信息获取和握拳状态识别功能。

## 功能特点

- 实时检测手部位置
- 识别握拳状态（用于模拟点击）
- 输出手部位置信息和点击状态
- 低性能需求，适合实时应用

## 环境要求

- Python 3.9
- OpenCV
- MediaPipe 0.10.3
- NumPy

## 安装步骤

1. 确保已安装Mamba（或Conda）
2. 运行环境设置脚本：
   ```
   setup_env.bat
   ```
3. 激活环境：
   ```
   mamba activate hand_gesture
   ```

## 使用方法

### 方法一：使用启动脚本（推荐）

直接双击运行 `run.bat` 文件，它会自动激活环境并启动程序。

### 方法二：手动启动

1. 首先激活环境：
   ```
   mamba activate hand_gesture
   ```

2. 然后运行主程序：
   ```
   python hand_gesture_detection.py
   ```

3. 程序将打开摄像头，实时检测手势
4. 按'q'键退出程序

**注意：** 每次手动运行程序前都需要先激活环境，否则会提示"ModuleNotFoundError: No module named 'mediapipe'"错误。

## 输出信息

程序会输出以下信息：
- 手部位置（手掌中心坐标）
- 状态（握拳/张开手）

## 握拳检测算法

握拳检测基于以下原理：
- 检测手指是否弯曲（比较指尖和指关节的Y坐标）
- 如果至少3个手指弯曲，则判定为握拳状态

## 性能优化

- 使用MediaPipe的轻量级手部检测模型
- 只检测单只手以减少计算量
- 适中的检测置信度阈值

## 自定义调整

可以通过修改以下参数来调整检测行为：
- `min_detection_confidence`: 检测置信度阈值
- `min_tracking_confidence`: 跟踪置信度阈值
- 握拳判定中的弯曲手指数量阈值
