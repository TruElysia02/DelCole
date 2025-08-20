import cv2
import mediapipe as mp
import time
import math

class HandGestureDetector:
    def __init__(self):
        # 初始化mediapipe手部检测
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # 手部关键点
        self.hand_landmarks = None
        
    def detect_hands(self, frame):
        """
        检测手部并返回关键点
        """
        # 转换为RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 检测手部
        results = self.hands.process(rgb_frame)
        
        # 绘制手部关键点
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                self.hand_landmarks = hand_landmarks
                return True, hand_landmarks
        
        self.hand_landmarks = None
        return False, None
    
    def get_hand_position(self, hand_landmarks):
        """
        获取手部位置信息
        """
        if not hand_landmarks:
            return None
        
        # 获取手掌中心位置 (landmark 0)
        palm_center = hand_landmarks.landmark[0]
        
        # 获取食指指尖位置 (landmark 8)
        index_finger_tip = hand_landmarks.landmark[8]
        
        # 获取拇指指尖位置 (landmark 4)
        thumb_tip = hand_landmarks.landmark[4]
        
        return {
            'palm_center': (palm_center.x, palm_center.y),
            'index_finger_tip': (index_finger_tip.x, index_finger_tip.y),
            'thumb_tip': (thumb_tip.x, thumb_tip.y)
        }
    
    def is_fist(self, hand_landmarks):
        """
        检测是否为握拳状态
        """
        if not hand_landmarks:
            return False
        
        # 获取关键点
        palm_center = hand_landmarks.landmark[0]
        thumb_tip = hand_landmarks.landmark[4]
        index_finger_tip = hand_landmarks.landmark[8]
        middle_finger_tip = hand_landmarks.landmark[12]
        ring_finger_tip = hand_landmarks.landmark[16]
        pinky_finger_tip = hand_landmarks.landmark[20]
        
        # 计算指尖到手掌中心的距离
        thumb_dist = math.sqrt((thumb_tip.x - palm_center.x)**2 + (thumb_tip.y - palm_center.y)**2)
        index_dist = math.sqrt((index_finger_tip.x - palm_center.x)**2 + (index_finger_tip.y - palm_center.y)**2)
        middle_dist = math.sqrt((middle_finger_tip.x - palm_center.x)**2 + (middle_finger_tip.y - palm_center.y)**2)
        ring_dist = math.sqrt((ring_finger_tip.x - palm_center.x)**2 + (ring_finger_tip.y - palm_center.y)**2)
        pinky_dist = math.sqrt((pinky_finger_tip.x - palm_center.x)**2 + (pinky_finger_tip.y - palm_center.y)**2)
        
        # 计算手指弯曲程度（通过比较指尖和指关节的位置）
        index_finger_pip = hand_landmarks.landmark[6]
        middle_finger_pip = hand_landmarks.landmark[10]
        ring_finger_pip = hand_landmarks.landmark[14]
        pinky_finger_pip = hand_landmarks.landmark[18]
        
        index_bent = index_finger_tip.y > index_finger_pip.y
        middle_bent = middle_finger_tip.y > middle_finger_pip.y
        ring_bent = ring_finger_tip.y > ring_finger_pip.y
        pinky_bent = pinky_finger_tip.y > pinky_finger_pip.y
        
        # 如果大多数手指弯曲，则认为是握拳
        bent_count = sum([index_bent, middle_bent, ring_bent, pinky_bent])
        
        return bent_count >= 3
    
    def run(self):
        """
        主循环，从摄像头获取图像并处理
        """
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue
            
            # 检测手部
            hand_detected, hand_landmarks = self.detect_hands(frame)
            
            if hand_detected:
                # 获取手部位置
                hand_position = self.get_hand_position(hand_landmarks)
                
                # 检测是否握拳
                fist = self.is_fist(hand_landmarks)
                
                # 显示信息
                if hand_position:
                    # 在图像上显示手掌中心位置
                    h, w, _ = frame.shape
                    palm_x, palm_y = int(hand_position['palm_center'][0] * w), int(hand_position['palm_center'][1] * h)
                    cv2.circle(frame, (palm_x, palm_y), 10, (0, 255, 0), -1)
                    
                    # 显示状态信息
                    status = "Fist (Click)" if fist else "Open Hand"
                    cv2.putText(frame, status, (palm_x - 50, palm_y - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # 打印位置和状态信息
                    print(f"Hand Position: {hand_position['palm_center']}, Status: {status}")
            
            # 显示图像
            cv2.imshow('Hand Gesture Detection', frame)
            
            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = HandGestureDetector()
    detector.run()