"""
📷 CAMERA-ONLY BARCODE SCANNER
=============================

Simplified version focused only on live camera scanning
Uses different WebRTC approach for better compatibility
"""

import streamlit as st
import pandas as pd
import cv2
import numpy as np
from pyzbar import pyzbar
from datetime import datetime
import time
from typing import Set

# Simplified page config
st.set_page_config(
    page_title="📷 Camera Scanner",
    page_icon="📷",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    if 'valid_barcodes' not in st.session_state:
        st.session_state.valid_barcodes = set()
    if 'scanned_barcodes' not in st.session_state:
        st.session_state.scanned_barcodes = []
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'scanning_active' not in st.session_state:
        st.session_state.scanning_active = False

def load_barcodes_from_file(uploaded_file) -> Set[str]:
    """Load barcodes from uploaded Excel or CSV file"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
        
        if df.empty:
            raise ValueError("Empty file")
        
        # Check for tracking-id column
        if 'tracking-id' in df.columns:
            st.success("✅ Using 'tracking-id' column")
            barcode_column = df['tracking-id'].dropna().astype(str).str.strip()
        elif 'tracking_id' in df.columns:
            st.success("✅ Using 'tracking_id' column")
            barcode_column = df['tracking_id'].dropna().astype(str).str.strip()
        else:
            st.info("ℹ️ Using first column")
            barcode_column = df.iloc[:, 0].dropna().astype(str).str.strip()
        
        barcode_set = set(barcode_column.tolist())
        barcode_set.discard('')
        
        return barcode_set
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return set()

def simple_camera_scanner():
    """Simplified camera scanner using HTML5 video"""
    
    st.markdown("""
    <div style="text-align: center;">
        <h3>📷 Camera Scanner</h3>
        <p>Point your camera at a barcode and click "Capture & Scan"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # HTML5 Camera access
    camera_html = """
    <div style="text-align: center;">
        <video id="video" width="640" height="480" autoplay></video><br><br>
        <canvas id="canvas" width="640" height="480" style="display: none;"></canvas><br>
        <button onclick="captureImage()" style="padding: 10px 20px; font-size: 16px; background: #ff4b4b; color: white; border: none; border-radius: 5px;">
            📸 Capture & Scan
        </button><br><br>
        <img id="capturedImage" style="max-width: 400px; border: 2px solid #ccc; display: none;">
    </div>
    
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const capturedImage = document.getElementById('capturedImage');
        const ctx = canvas.getContext('2d');
        
        // Access camera
        navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: 640, 
                height: 480,
                facingMode: 'environment' // Use back camera on mobile
            } 
        })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error('Camera error:', err);
            alert('Camera access failed: ' + err.message);
        });
        
        function captureImage() {
            // Draw video frame to canvas
            ctx.drawImage(video, 0, 0, 640, 480);
            
            // Convert to data URL
            const dataURL = canvas.toDataURL('image/png');
            
            // Show captured image
            capturedImage.src = dataURL;
            capturedImage.style.display = 'block';
            
            // Send image data to Streamlit (you'll need to handle this)
            console.log('Image captured');
            
            // For now, just show success message
            alert('Image captured! (Integration with barcode detection needed)');
        }
    </script>
    """
    
    st.components.v1.html(camera_html, height=700)

def main():
    initialize_session_state()
    
    st.title("📷 Camera-Only Barcode Scanner")
    st.markdown("**Live camera scanning focused solution**")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Barcode List")
        
        uploaded_file = st.file_uploader(
            "Excel/CSV with tracking IDs",
            type=['xlsx', 'xls', 'csv']
        )
        
        if uploaded_file:
            barcodes = load_barcodes_from_file(uploaded_file)
            if barcodes:
                st.session_state.valid_barcodes = barcodes
                st.session_state.file_uploaded = True
                st.success(f"✅ {len(barcodes)} tracking IDs loaded")
    
    # Main camera area
    if st.session_state.file_uploaded:
        
        # Camera method selection
        st.subheader("🔧 Choose Camera Method")
        
        method = st.radio(
            "Select scanning approach:",
            [
                "🔧 Diagnostics First (Recommended)",
                "📷 HTML5 Camera (Experimental)", 
                "🔄 Try Original WebRTC",
                "💻 OpenCV Direct (Advanced)"
            ]
        )
        
        if method == "🔧 Diagnostics First (Recommended)":
            st.info("👇 **Run camera diagnostics first to fix issues:**")
            st.code("streamlit run camera_diagnostics.py")
            st.markdown("This will test your camera and provide specific fixes.")
            
        elif method == "📷 HTML5 Camera (Experimental)":
            st.warning("⚠️ This is experimental - may not work on all browsers")
            simple_camera_scanner()
            
        elif method == "🔄 Try Original WebRTC":
            st.info("🔄 **Go back to main app with these fixes:**")
            st.markdown("""
            1. **Use Chrome browser**
            2. **Close all other camera apps**
            3. **Refresh the page** (F5)
            4. **Allow camera permissions**
            5. **Check "I'm using mobile device" if on phone**
            """)
            st.code("streamlit run app.py")
            
        elif method == "💻 OpenCV Direct (Advanced)":
            st.warning("⚠️ Advanced method - requires technical setup")
            st.markdown("""
            **This method captures frames directly but requires custom integration.**
            
            **Steps:**
            1. Install additional packages: `pip install opencv-python-headless`
            2. Use system camera directly
            3. Manual frame capture and processing
            
            **Note:** This bypasses browser limitations but is more complex.
            """)
    
    else:
        st.warning("👈 Upload your tracking ID file first!")
        st.info("Use the sidebar to upload your Excel/CSV file with tracking IDs")

if __name__ == "__main__":
    main()
