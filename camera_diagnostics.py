"""
🔧 CAMERA-ONLY BARCODE SCANNER TROUBLESHOOTING
=============================================

Run this to diagnose and fix camera issues
"""

import streamlit as st
import cv2
import numpy as np
from pyzbar import pyzbar
import time

def test_camera_direct():
    """Test camera using OpenCV directly"""
    st.subheader("🔧 Direct Camera Test")
    
    if st.button("Test Camera Access"):
        try:
            # Try to open camera with OpenCV
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Camera not accessible via OpenCV")
                st.info("💡 Try: Close other camera apps, check drivers")
                return False
            
            # Capture a frame
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                st.success("✅ Camera works with OpenCV!")
                st.image(frame, channels="BGR", caption="Camera Test Frame")
                
                # Test barcode detection on this frame
                barcodes = pyzbar.decode(frame)
                if barcodes:
                    st.success(f"🎉 Found {len(barcodes)} barcode(s) in test frame!")
                    for barcode in barcodes:
                        st.code(f"Detected: {barcode.data.decode('utf-8')}")
                else:
                    st.info("📷 No barcodes in test frame (that's normal)")
                
                return True
            else:
                st.error("❌ Could not capture frame")
                return False
                
        except Exception as e:
            st.error(f"❌ Camera error: {str(e)}")
            return False

def main():
    st.title("🔧 Camera Diagnostics")
    st.markdown("Let's fix your camera scanning issues!")
    
    # Test direct camera access
    camera_works = test_camera_direct()
    
    st.markdown("---")
    
    # Show recommendations
    st.subheader("💡 Recommendations")
    
    if camera_works:
        st.success("✅ Your camera works! The issue is likely with streamlit-webrtc.")
        st.markdown("""
        **Solutions to try:**
        
        1. **Use different browser** - Chrome works best
        2. **Restart Streamlit** - Close and run `streamlit run app.py` again  
        3. **Clear browser cache** - Ctrl+Shift+Delete
        4. **Allow camera permissions** - Check browser settings
        5. **Close other camera apps** - Zoom, Skype, etc.
        """)
    else:
        st.error("❌ Camera access issues detected")
        st.markdown("""
        **Fixes to try:**
        
        1. **Close other apps** using camera (Zoom, Teams, Skype)
        2. **Restart your computer** - Refreshes camera drivers
        3. **Check camera drivers** - Update if needed
        4. **Try external USB camera** - Often works better
        5. **Run as administrator** - Some cameras need elevated permissions
        """)
    
    # Browser-specific advice
    st.markdown("---")
    st.subheader("🌐 Browser-Specific Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Chrome (Recommended):**
        - Best WebRTC support
        - Go to chrome://settings/content/camera
        - Allow camera for localhost
        """)
    
    with col2:
        st.markdown("""
        **⚠️ Other Browsers:**
        - Firefox: Limited WebRTC support
        - Safari: Often blocks camera
        - Edge: Try compatibility mode
        """)

if __name__ == "__main__":
    main()
