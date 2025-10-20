"""
Face Recognition Module for Smart Home Automation

This module provides face enrollment, encoding, and identification capabilities
for recognizing people in camera feeds.
"""

from .face_encoder import FaceEncoder
from .face_identifier import FaceIdentifier
from .database import FaceDatabase

__all__ = ['FaceEncoder', 'FaceIdentifier', 'FaceDatabase']

