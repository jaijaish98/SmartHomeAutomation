"""
Visualizer Module
Handles drawing bounding boxes, labels, and overlays on frames.
"""

import cv2
import numpy as np


class Visualizer:
    """Handles visualization of detection results."""
    
    def __init__(self, config):
        """
        Initialize visualizer.
        
        Args:
            config (dict): Display configuration
        """
        self.config = config
        self.colors = self._generate_colors(80)  # 80 COCO classes
        
    def _generate_colors(self, num_classes):
        """
        Generate distinct colors for each class.
        
        Args:
            num_classes (int): Number of classes
            
        Returns:
            list: List of BGR color tuples
        """
        np.random.seed(42)  # For consistent colors
        colors = []
        for i in range(num_classes):
            hue = int(180 * i / num_classes)
            color = cv2.cvtColor(
                np.uint8([[[hue, 255, 255]]]),
                cv2.COLOR_HSV2BGR
            )[0][0]
            colors.append(tuple(map(int, color)))
        return colors
    
    def draw_detection(self, frame, detection, class_name, class_id):
        """
        Draw a single detection on the frame.
        
        Args:
            frame: Input frame
            detection: Detection tuple (x, y, w, h, confidence)
            class_name: Name of detected class
            class_id: ID of detected class
            
        Returns:
            Modified frame
        """
        x, y, w, h, confidence = detection
        
        # Get color for this class
        color = self.colors[class_id % len(self.colors)]
        
        # Draw bounding box
        thickness = self.config.get('box_thickness', 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        
        # Prepare label
        if self.config.get('show_confidence', True):
            label = f"{class_name}: {confidence:.2f}"
        else:
            label = class_name
        
        # Calculate label size and position
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = self.config.get('font_scale', 0.6)
        font_thickness = self.config.get('font_thickness', 2)
        
        (label_width, label_height), baseline = cv2.getTextSize(
            label, font, font_scale, font_thickness
        )
        
        # Draw label background
        label_y = max(y - 10, label_height + 10)
        cv2.rectangle(
            frame,
            (x, label_y - label_height - baseline - 5),
            (x + label_width + 5, label_y + baseline),
            color,
            -1  # Filled
        )
        
        # Draw label text
        cv2.putText(
            frame,
            label,
            (x + 2, label_y - 5),
            font,
            font_scale,
            (255, 255, 255),  # White text
            font_thickness,
            cv2.LINE_AA
        )
        
        return frame
    
    def draw_detections(self, frame, detections, class_names):
        """
        Draw all detections on the frame.
        
        Args:
            frame: Input frame
            detections: List of (class_id, class_name, confidence, x, y, w, h)
            class_names: List of all class names
            
        Returns:
            Modified frame
        """
        for detection in detections:
            class_id, class_name, confidence, x, y, w, h = detection
            self.draw_detection(
                frame,
                (x, y, w, h, confidence),
                class_name,
                class_id
            )
        
        return frame
    
    def draw_info_overlay(self, frame, detections, fps=0):
        """
        Draw information overlay on the frame.
        
        Args:
            frame: Input frame
            detections: List of detections
            fps: Current FPS
            
        Returns:
            Modified frame
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        color = (0, 255, 0)  # Green
        y_offset = 30
        
        # Draw object count
        if self.config.get('show_count', True):
            count_text = f"Objects detected: {len(detections)}"
            cv2.putText(
                frame, count_text, (10, y_offset),
                font, font_scale, color, font_thickness, cv2.LINE_AA
            )
            y_offset += 35
        
        # Draw FPS
        if self.config.get('show_fps', True) and fps > 0:
            fps_text = f"FPS: {fps:.1f}"
            cv2.putText(
                frame, fps_text, (10, y_offset),
                font, font_scale, color, font_thickness, cv2.LINE_AA
            )
            y_offset += 35
        
        # Draw class breakdown
        if len(detections) > 0 and len(detections) <= 10:
            class_counts = {}
            for detection in detections:
                class_name = detection[1]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            breakdown_text = "Detected: " + ", ".join(
                [f"{name}({count})" for name, count in class_counts.items()]
            )
            
            # Use smaller font for breakdown
            cv2.putText(
                frame, breakdown_text, (10, y_offset),
                font, 0.5, color, 1, cv2.LINE_AA
            )
        
        # Draw instructions at bottom
        instructions = "Press 'q' or ESC to exit | 's' to save frame"
        text_size = cv2.getTextSize(instructions, font, 0.5, 1)[0]
        text_x = 10
        text_y = frame.shape[0] - 10
        
        cv2.putText(
            frame, instructions, (text_x, text_y),
            font, 0.5, (255, 255, 255), 1, cv2.LINE_AA
        )
        
        return frame
    
    def create_detection_summary(self, detections):
        """
        Create a text summary of detections.
        
        Args:
            detections: List of detections
            
        Returns:
            str: Summary text
        """
        if not detections:
            return "No objects detected"
        
        class_counts = {}
        for detection in detections:
            class_name = detection[1]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        summary_parts = []
        for class_name, count in sorted(class_counts.items()):
            summary_parts.append(f"{count} {class_name}{'s' if count > 1 else ''}")
        
        return "Detected: " + ", ".join(summary_parts)

