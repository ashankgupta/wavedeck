"""
Main entry point for the Hand Gesture Presenter application.
"""

import logging
import cv2
import sys

from config import Config
from gesture_detector import GestureDetector
from presentation_controller import PresentationController


def setup_logging(config: Config):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main application loop."""
    config = Config()
    setup_logging(config)

    logger = logging.getLogger(__name__)
    logger.info("Starting Gesture Presenter (Two-Hand Lock Enabled)")

    gesture_detector = GestureDetector(config)
    controller = PresentationController(config, gesture_detector)

    cap = cv2.VideoCapture(config.camera_index)
    if not cap.isOpened():
        logger.error("Failed to open camera")
        sys.exit(1)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to read frame from camera")
                break

            frame = cv2.flip(frame, 1)  # Mirror the frame
            frame = controller.process_frame(frame)

            cv2.imshow("Gesture Presenter", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Application exited")


if __name__ == "__main__":
    main()

