#!/usr/bin/env python3
"""
YOLO Model Downloader
Downloads required YOLO model files (weights, config, class names)
"""

import os
import sys
import urllib.request
import yaml
from pathlib import Path


class ModelDownloader:
    """Download and manage YOLO model files."""
    
    def __init__(self, config_path="config/config.yaml"):
        """Initialize the model downloader."""
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / config_path
        self.config = self.load_config()
        self.models_dir = self.project_root / "models"
        self.models_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            sys.exit(1)
    
    def download_file(self, url, destination, description="file"):
        """Download a file with progress indication."""
        try:
            print(f"\n📥 Downloading {description}...")
            print(f"   URL: {url}")
            print(f"   Destination: {destination}")
            
            def progress_hook(block_num, block_size, total_size):
                """Show download progress."""
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(downloaded * 100.0 / total_size, 100)
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    print(f"\r   Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='')
                else:
                    mb_downloaded = downloaded / (1024 * 1024)
                    print(f"\r   Downloaded: {mb_downloaded:.1f} MB", end='')
            
            urllib.request.urlretrieve(url, destination, progress_hook)
            print(f"\n   ✅ Downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"\n   ❌ Error downloading: {e}")
            return False
    
    def check_file_exists(self, filepath):
        """Check if a file exists and show its size."""
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"   ✅ Already exists ({size_mb:.1f} MB): {filepath.name}")
            return True
        return False
    
    def download_model(self, model_type):
        """Download all files for a specific YOLO model."""
        print(f"\n{'='*70}")
        print(f"Downloading YOLO Model: {model_type}")
        print(f"{'='*70}")
        
        if model_type not in self.config['model_files']:
            print(f"❌ Unknown model type: {model_type}")
            print(f"Available models: {list(self.config['model_files'].keys())}")
            return False
        
        model_info = self.config['model_files'][model_type]
        success = True
        
        # Download weights
        weights_path = self.project_root / model_info['weights']
        if not self.check_file_exists(weights_path):
            if not self.download_file(
                model_info['weights_url'],
                weights_path,
                f"{model_type} weights"
            ):
                success = False
        
        # Download config
        config_path = self.project_root / model_info['config']
        if not self.check_file_exists(config_path):
            if not self.download_file(
                model_info['config_url'],
                config_path,
                f"{model_type} config"
            ):
                success = False
        
        # Download class names
        names_path = self.project_root / model_info['names']
        if not self.check_file_exists(names_path):
            if not self.download_file(
                model_info['names_url'],
                names_path,
                "COCO class names"
            ):
                success = False
        
        return success
    
    def verify_model(self, model_type):
        """Verify that all model files exist and are valid."""
        print(f"\n🔍 Verifying {model_type} model files...")
        
        if model_type not in self.config['model_files']:
            print(f"❌ Unknown model type: {model_type}")
            return False
        
        model_info = self.config['model_files'][model_type]
        all_valid = True
        
        # Check weights
        weights_path = self.project_root / model_info['weights']
        if weights_path.exists() and weights_path.stat().st_size > 1000000:  # > 1MB
            print(f"   ✅ Weights file OK")
        else:
            print(f"   ❌ Weights file missing or invalid")
            all_valid = False
        
        # Check config
        config_path = self.project_root / model_info['config']
        if config_path.exists() and config_path.stat().st_size > 100:  # > 100 bytes
            print(f"   ✅ Config file OK")
        else:
            print(f"   ❌ Config file missing or invalid")
            all_valid = False
        
        # Check names
        names_path = self.project_root / model_info['names']
        if names_path.exists() and names_path.stat().st_size > 100:  # > 100 bytes
            print(f"   ✅ Names file OK")
        else:
            print(f"   ❌ Names file missing or invalid")
            all_valid = False
        
        return all_valid
    
    def list_available_models(self):
        """List all available YOLO models."""
        print("\n📋 Available YOLO Models:")
        print("-" * 70)
        for model_type in self.config['model_files'].keys():
            print(f"   • {model_type}")
        print("-" * 70)


def main():
    """Main function."""
    print("="*70)
    print("YOLO Model Downloader")
    print("="*70)
    
    downloader = ModelDownloader()
    
    # Get model type from config or command line
    model_type = downloader.config['model']['type']
    
    if len(sys.argv) > 1:
        model_type = sys.argv[1]
    
    print(f"\n🎯 Target model: {model_type}")
    
    # List available models
    downloader.list_available_models()
    
    # Download the model
    print(f"\n🚀 Starting download for {model_type}...")
    success = downloader.download_model(model_type)
    
    if success:
        # Verify the download
        if downloader.verify_model(model_type):
            print(f"\n{'='*70}")
            print(f"✅ SUCCESS! {model_type} model is ready to use!")
            print(f"{'='*70}")
            print(f"\nNext step: Run the object detector")
            print(f"   python scripts/detect_objects.py")
            return 0
        else:
            print(f"\n❌ Model verification failed. Please try downloading again.")
            return 1
    else:
        print(f"\n❌ Download failed. Please check your internet connection and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

