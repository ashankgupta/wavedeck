"""
Presentation controller module for managing gesture-based presentation control.
"""

import time
import cv2
from typing import Optional
from input_control import send_next, send_prev, send_start, send_exit
import logging


class PresentationController:
    """Manages the overall state and logic for gesture-controlled presentations."""

    def __init__(self, config, gesture_detector):
        self.config = config
        self.gesture_detector = gesture_detector
        self.logger = logging.getLogger(__name__)

        # State
        self.gestures_enabled = True
        self.active_mode = None

        # Timers
        self.last_slide_time = 0.0
        self.last_special_time = 0.0
        self.last_toggle_time = 0.0

        self.palm_start_time: Optional[float] = None
        self.two_hand_start_time: Optional[float] = None

        self.gesture_resume_time = 0.0
        self.two_hand_lock_until = 0.0

    def process_frame(self, frame) -> cv2.Mat:
        """Process a single frame and update presentation state."""
        now = time.time()
        frame, multi_hand_landmarks, multi_handedness = self.gesture_detector.process_frame(frame)

        # Handle two-hand detection (highest priority)
        self._handle_two_hand_gesture(now, multi_hand_landmarks)

        # Handle single-hand logic if enabled and not locked
        if (
            self.gestures_enabled
            and now > self.two_hand_lock_until
            and now > self.gesture_resume_time
            and multi_hand_landmarks
            and multi_handedness
        ):
            self._handle_single_hand_gesture(now, multi_hand_landmarks[0], multi_handedness[0])
            self.gesture_detector.draw_landmarks(frame, multi_hand_landmarks[0])
        else:
            self.active_mode = None
            self.palm_start_time = None

        # Auto slide execution
        self._execute_auto_slide(now)

        # Update HUD
        self._update_hud(frame)

        return frame

    def _handle_two_hand_gesture(self, now: float, multi_hand_landmarks):
        """Handle two-hand gestures for toggling recognition."""
        if multi_hand_landmarks and len(multi_hand_landmarks) == 2:
            self.two_hand_lock_until = now + self.config.two_hand_lock_time

            lm1 = multi_hand_landmarks[0].landmark
            lm2 = multi_hand_landmarks[1].landmark

            if self.gesture_detector.is_open_palm(lm1) and self.gesture_detector.is_open_palm(lm2):
                if self.two_hand_start_time is None:
                    self.two_hand_start_time = now

                if (
                    (now - self.two_hand_start_time) >= self.config.two_hand_hold_time
                    and (now - self.last_toggle_time) > self.config.toggle_cooldown
                ):
                    self.gestures_enabled = not self.gestures_enabled
                    state = "ENABLED" if self.gestures_enabled else "DISABLED"
                    self.logger.info(f"Gestures {state}")

                    self.gesture_resume_time = now + self.config.post_toggle_delay
                    self.active_mode = None
                    self.palm_start_time = None

                    self.last_toggle_time = now
                    self.two_hand_start_time = None
            else:
                self.two_hand_start_time = None
        else:
            self.two_hand_start_time = None

    def _handle_single_hand_gesture(self, now: float, hand, handedness):
        """Handle single-hand gestures for navigation and special actions."""
        lm = hand.landmark
        hand_label = handedness.classification[0].label

        # Start/Exit gestures
        if self.gesture_detector.is_open_palm(lm):
            if self.palm_start_time is None:
                self.palm_start_time = now

            if (
                (now - self.palm_start_time) >= self.config.palm_hold_time
                and (now - self.last_special_time) > self.config.special_cooldown
            ):
                if hand_label == "Right":
                    send_start()
                    self.logger.info("START SLIDESHOW")
                else:
                    send_exit()
                    self.logger.info("EXIT SLIDESHOW")

                self.last_special_time = now
                self.palm_start_time = None
        else:
            self.palm_start_time = None

        # Navigation gestures
        if self.gesture_detector.index_up(lm):
            self.active_mode = "NEXT" if hand_label == "Right" else "PREV"
        else:
            self.active_mode = None

    def _execute_auto_slide(self, now: float):
        """Execute slide navigation if active mode is set and interval passed."""
        if (
            self.gestures_enabled
            and self.active_mode
            and (now - self.last_slide_time) > self.config.slide_interval
        ):
            if self.active_mode == "NEXT":
                send_next()
                self.logger.info("AUTO NEXT")
            elif self.active_mode == "PREV":
                send_prev()
                self.logger.info("AUTO PREV")

            self.last_slide_time = now

    def _update_hud(self, frame):
        """Update the on-screen heads-up display."""
        status = "ENABLED" if self.gestures_enabled else "DISABLED"
        cv2.putText(
            frame,
            f"Gestures: {status}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0) if self.gestures_enabled else (0, 0, 255),
            2,
        )