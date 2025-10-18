"""
Object Detector Module
Core YOLO object detection functionality.
"""

import cv2
import numpy as np
from pathlib import Path


class ObjectDetector:
    """YOLO-based object detector."""
    
    def __init__(self, config):
        """
        Initialize object detector.
        
        Args:
            config (dict): Model configuration
        """
        self.config = config
        self.model_config = config['model']
        self.net = None
        self.class_names = []
        self.output_layers = []
        self.is_initialized = False
        
    def load_model(self, weights_path, config_path, names_path):
        """
        Load YOLO model from files.
        
        Args:
            weights_path (str): Path to weights file
            config_path (str): Path to config file
            names_path (str): Path to class names file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\n🤖 Loading YOLO model...")
            print(f"   Model type: {self.model_config['type']}")
            
            # Check if files exist
            weights_path = Path(weights_path)
            config_path = Path(config_path)
            names_path = Path(names_path)
            
            if not weights_path.exists():
                raise FileNotFoundError(f"Weights file not found: {weights_path}")
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
            if not names_path.exists():
                raise FileNotFoundError(f"Names file not found: {names_path}")
            
            # Load class names
            with open(names_path, 'r') as f:
                self.class_names = [line.strip() for line in f.readlines()]
            
            print(f"   ✅ Loaded {len(self.class_names)} class names")
            
            # Load YOLO network
            self.net = cv2.dnn.readNetFromDarknet(
                str(config_path),
                str(weights_path)
            )
            
            # Set backend and target
            backend = self.config.get('performance', {}).get('backend', 'opencv')
            target = self.config.get('performance', {}).get('target', 'cpu')
            
            if backend == 'cuda' and cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                print(f"   ✅ Using CUDA backend")
            else:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                print(f"   ✅ Using CPU backend")
            
            # Get output layer names
            layer_names = self.net.getLayerNames()
            self.output_layers = [
                layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()
            ]
            
            print(f"   ✅ Model loaded successfully")
            print(f"   📊 Output layers: {len(self.output_layers)}")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"   ❌ Error loading model: {e}")
            return False
    
    def detect(self, frame):
        """
        Detect objects in a frame.
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            list: List of detections (class_id, class_name, confidence, x, y, w, h)
        """
        if not self.is_initialized:
            return []
        
        height, width = frame.shape[:2]
        
        # Prepare input blob
        input_size = self.model_config.get('input_size', 416)
        blob = cv2.dnn.blobFromImage(
            frame,
            1/255.0,
            (input_size, input_size),
            swapRB=True,
            crop=False
        )
        
        # Run forward pass
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        
        # Process detections
        detections = self._process_detections(outputs, width, height)
        
        return detections
    
    def _process_detections(self, outputs, width, height):
        """
        Process YOLO outputs into detections.
        
        Args:
            outputs: YOLO network outputs
            width: Frame width
            height: Frame height
            
        Returns:
            list: Processed detections
        """
        class_ids = []
        confidences = []
        boxes = []
        
        confidence_threshold = self.model_config.get('confidence_threshold', 0.5)
        
        # Parse outputs
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > confidence_threshold:
                    # Check if class is in filter (if filtering is enabled)
                    if self._should_detect_class(class_id):
                        # Get bounding box coordinates
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        # Calculate top-left corner
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
        
        # Apply Non-Maximum Suppression
        nms_threshold = self.model_config.get('nms_threshold', 0.4)
        indices = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            confidence_threshold,
            nms_threshold
        )
        
        # Build final detections list
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                class_id = class_ids[i]
                class_name = self.class_names[class_id]
                
                detections.append((
                    class_id,
                    class_name,
                    confidence,
                    x, y, w, h
                ))
        
        return detections
    
    def _should_detect_class(self, class_id):
        """
        Check if a class should be detected based on filter settings.
        
        Args:
            class_id: Class ID to check
            
        Returns:
            bool: True if class should be detected
        """
        filter_config = self.config.get('filter', {})
        
        if not filter_config.get('enabled', False):
            return True
        
        allowed_classes = filter_config.get('classes', [])
        if not allowed_classes:
            return True
        
        class_name = self.class_names[class_id]
        return class_name in allowed_classes
    
    def get_class_names(self):
        """Get list of all class names."""
        return self.class_names
    
    def get_model_info(self):
        """
        Get model information.
        
        Returns:
            dict: Model information
        """
        return {
            'type': self.model_config['type'],
            'num_classes': len(self.class_names),
            'confidence_threshold': self.model_config['confidence_threshold'],
            'nms_threshold': self.model_config['nms_threshold'],
            'input_size': self.model_config['input_size'],
            'is_initialized': self.is_initialized
        }

