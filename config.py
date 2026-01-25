"""
Configuration settings for the Hand Gesture Presenter.
"""

import dataclasses


@dataclasses.dataclass
class Config:
    """Configuration class for gesture detection and timing parameters."""

    # MediaPipe hand detection settings
    max_num_hands: int = 2
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.7

    # Timing intervals (in seconds)
    slide_interval: float = 1.0
    special_cooldown: float = 1.5
    toggle_cooldown: float = 1.5
    palm_hold_time: float = 0.6
    two_hand_hold_time: float = 1.0
    post_toggle_delay: float = 1.2
    two_hand_lock_time: float = 1.0

    # Camera settings
    camera_index: int = 0

    # Logging level
    log_level: str = "INFO"