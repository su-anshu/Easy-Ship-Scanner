#!/usr/bin/env python3
"""
Quick camera performance test for the barcode scanner app
Run this to test your camera before using the main app
"""

import cv2
import time
import sys

def test_camera_performance():
    """Test camera performance and provide optimization suggestions"""
    print("🔍 Testing Camera Performance...")
    print("=" * 50)
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not open camera!")
        print("💡 Try:")
        print("   - Check if camera is being used by another app")
        print("   - Make sure camera drivers are installed")
        print("   - Try a different camera index (1, 2, etc.)")
        return False
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📷 Camera Properties:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Test frame capture speed
    print(f"\n⏱️  Testing frame capture speed...")
    
    frame_times = []
    test_frames = 30
    
    for i in range(test_frames):
        start_time = time.time()
        ret, frame = cap.read()
        end_time = time.time()
        
        if ret:
            frame_times.append(end_time - start_time)
        else:
            print(f"❌ Failed to capture frame {i+1}")
            break
        
        # Show progress
        if (i + 1) % 10 == 0:
            print(f"   Captured {i+1}/{test_frames} frames...")
    
    cap.release()
    
    if frame_times:
        avg_time = sum(frame_times) / len(frame_times)
        avg_fps = 1 / avg_time if avg_time > 0 else 0
        
        print(f"\n📊 Performance Results:")
        print(f"   Average frame time: {avg_time:.3f} seconds")
        print(f"   Average FPS: {avg_fps:.1f}")
        
        # Performance recommendations
        print(f"\n💡 Recommendations:")
        if avg_fps > 20:
            print("   ✅ Good performance! Camera should work well with the app.")
        elif avg_fps > 10:
            print("   ⚠️  Moderate performance. App will work but may be slightly slow.")
            print("   💭 Tips: Close other camera apps, ensure good lighting")
        else:
            print("   ❌ Poor performance. App may be very slow.")
            print("   💭 Tips:")
            print("      - Use external USB camera if possible")
            print("      - Close all other applications")
            print("      - Restart your computer")
            print("      - Update camera drivers")
        
        return True
    else:
        print("❌ Could not capture any frames!")
        return False

def test_pyzbar():
    """Test if pyzbar can decode barcodes"""
    print(f"\n🔍 Testing barcode detection...")
    
    try:
        from pyzbar import pyzbar
        print("✅ pyzbar library imported successfully")
        
        # Try to create a simple test
        import numpy as np
        
        # Create a simple test image (this won't actually have a barcode)
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        barcodes = pyzbar.decode(test_image)
        print("✅ pyzbar decode function works")
        
        return True
        
    except ImportError as e:
        print(f"❌ pyzbar import failed: {e}")
        print("💡 Install with: pip install pyzbar")
        return False
    except Exception as e:
        print(f"⚠️  pyzbar test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Barcode Scanner - Camera Performance Test")
    print("=" * 50)
    
    # Test camera
    camera_ok = test_camera_performance()
    
    # Test pyzbar
    pyzbar_ok = test_pyzbar()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    
    if camera_ok and pyzbar_ok:
        print("🎉 All tests passed! Your setup should work well.")
        print("\n🚀 Ready to run the barcode scanner app!")
        print("   Command: streamlit run app.py")
    else:
        print("⚠️  Some issues detected. Check the recommendations above.")
        if not camera_ok:
            print("   📷 Camera issues found")
        if not pyzbar_ok:
            print("   📦 Barcode detection library issues found")
    
    print("=" * 50)
    
    input("\nPress Enter to exit...")
