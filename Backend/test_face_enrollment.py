#!/usr/bin/env python3
"""
Test script to enroll a face using a sample image
"""

import requests
import json
import sys
from pathlib import Path

API_BASE_URL = "http://localhost:5000"

def test_enrollment_with_image(image_path, name, notes="Test enrollment"):
    """Test face enrollment with an image file"""
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    print(f"📸 Testing face enrollment with image: {image_path}")
    print(f"👤 Name: {name}")
    print(f"📝 Notes: {notes}")
    print()
    
    # Enroll face
    url = f"{API_BASE_URL}/api/faces/enroll"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'name': name,
            'notes': notes
        }
        
        print(f"🔄 Sending enrollment request to {url}...")
        response = requests.post(url, files=files, data=data)
    
    print(f"📡 Response status: {response.status_code}")
    print(f"📄 Response body:")
    print(json.dumps(response.json(), indent=2))
    print()
    
    if response.status_code == 201:
        print("✅ Face enrolled successfully!")
        return True
    else:
        print("❌ Face enrollment failed!")
        return False

def test_enrollment_from_camera(camera_id, name, notes="Test enrollment from camera"):
    """Test face enrollment from camera capture"""
    
    print(f"📸 Testing face enrollment from camera {camera_id}")
    print(f"👤 Name: {name}")
    print(f"📝 Notes: {notes}")
    print()
    
    url = f"{API_BASE_URL}/api/faces/enroll/capture"
    
    data = {
        'camera_id': camera_id,
        'name': name,
        'notes': notes
    }
    
    print(f"🔄 Sending enrollment request to {url}...")
    response = requests.post(url, json=data)
    
    print(f"📡 Response status: {response.status_code}")
    print(f"📄 Response body:")
    print(json.dumps(response.json(), indent=2))
    print()
    
    if response.status_code == 201:
        print("✅ Face enrolled successfully!")
        return True
    else:
        print("❌ Face enrollment failed!")
        return False

def list_enrolled_faces():
    """List all enrolled faces"""
    
    print("📋 Listing all enrolled faces...")
    url = f"{API_BASE_URL}/api/faces"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['count']} enrolled person(s):")
        print(json.dumps(data, indent=2))
        return data
    else:
        print(f"❌ Failed to list faces: {response.status_code}")
        return None

def get_stats():
    """Get face recognition statistics"""
    
    print("📊 Getting face recognition statistics...")
    url = f"{API_BASE_URL}/api/faces/stats"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Statistics:")
        print(json.dumps(data, indent=2))
        return data
    else:
        print(f"❌ Failed to get stats: {response.status_code}")
        return None

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Face Recognition Enrollment Test")
    print("=" * 70)
    print()
    
    # Check if image path is provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "Test Person"
        notes = sys.argv[3] if len(sys.argv) > 3 else "Test enrollment"
        
        # Test enrollment with image
        success = test_enrollment_with_image(image_path, name, notes)
        
        if success:
            print()
            print("=" * 70)
            list_enrolled_faces()
            print()
            print("=" * 70)
            get_stats()
            print()
            print("=" * 70)
    else:
        print("Usage:")
        print(f"  {sys.argv[0]} <image_path> [name] [notes]")
        print()
        print("Example:")
        print(f"  {sys.argv[0]} test_photo.jpg 'John Doe' 'Test user'")
        print()
        print("Or test with camera capture:")
        print("  Run this in Python:")
        print("  >>> from test_face_enrollment import test_enrollment_from_camera")
        print("  >>> test_enrollment_from_camera(1, 'John Doe', 'From camera')")

