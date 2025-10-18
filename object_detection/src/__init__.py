"""
YOLO Object Detection Package
Real-time object detection using YOLO and OpenCV.
"""

__version__ = "1.0.0"
__author__ = "Smart Home Automation"

from .detector import ObjectDetector
from .camera import CameraHandler
from .visualizer import Visualizer

__all__ = ['ObjectDetector', 'CameraHandler', 'Visualizer']

