"""
Gesture detection module using MediaPipe for hand tracking and gesture recognition.
"""

import mediapipe as mp
from typing import List, Optional, Tuple
import cv2


class GestureDetector:
    """Handles hand detection and gesture recognition using MediaPipe."""

    def __init__(self, config):
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=config.max_num_hands,
            min_detection_confidence=config.min_detection_confidence,
            min_tracking_confidence=config.min_tracking_confidence,
        )

    @staticmethod
    def index_up(lm) -> bool:
        """Check if index finger is raised."""
        return lm[8].y < lm[6].y

    @staticmethod
    def fingers_up(lm) -> int:
        """Count the number of raised fingers."""
        count = 0
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if lm[tip].y < lm[pip].y:
                count += 1
        return count

    @staticmethod
    def is_open_palm(lm) -> bool:
        """Check if the hand is an open palm (all fingers up)."""
        return GestureDetector.fingers_up(lm) == 4

    def process_frame(self, frame) -> Tuple[cv2.Mat, Optional[List], Optional[List]]:
        """Process a frame to detect hands and return landmarks and handedness."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        return frame, result.multi_hand_landmarks, result.multi_handedness

    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame."""
        if hand_landmarks:
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)