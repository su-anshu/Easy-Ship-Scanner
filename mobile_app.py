"""
📱 MOBILE-OPTIMIZED BARCODE SCANNER
===================================

This version is specifically designed for mobile phones and tablets.
No camera streaming - only image upload for maximum compatibility.

Run with: streamlit run mobile_app.py
"""

import streamlit as st
import pandas as pd
import cv2
import numpy as np
from pyzbar import pyzbar
import base64
import io
from datetime import datetime
import PIL.Image
from typing import Set

# Page configuration for mobile
st.set_page_config(
    page_title="📱 Mobile Barcode Scanner",
    page_icon="📱",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed"  # Start with sidebar closed on mobile
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'valid_barcodes' not in st.session_state:
        st.session_state.valid_barcodes = set()
    if 'scanned_barcodes' not in st.session_state:
        st.session_state.scanned_barcodes = []
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

# File handling functions
def load_barcodes_from_file(uploaded_file) -> Set[str]:
    """Load barcodes from uploaded Excel or CSV file"""
    try:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel file.")
        
        if df.empty:
            raise ValueError("The uploaded file is empty.")
        
        # Check for 'tracking-id' column first, then fall back to first column
        if 'tracking-id' in df.columns:
            st.success("✅ Found 'tracking-id' column - using that for barcodes!")
            barcode_column = df['tracking-id'].dropna().astype(str).str.strip()
        elif 'tracking_id' in df.columns:
            st.success("✅ Found 'tracking_id' column - using that for barcodes!")
            barcode_column = df['tracking_id'].dropna().astype(str).str.strip()
        elif 'Tracking ID' in df.columns:
            st.success("✅ Found 'Tracking ID' column - using that for barcodes!")
            barcode_column = df['Tracking ID'].dropna().astype(str).str.strip()
        else:
            st.info("ℹ️ No 'tracking-id' column found - using first column")
            barcode_column = df.iloc[:, 0].dropna().astype(str).str.strip()
        
        barcode_set = set(barcode_column.tolist())
        barcode_set.discard('')
        
        return barcode_set
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return set()

# Barcode detection function
def detect_barcodes(frame):
    """Detect and decode barcodes in the given frame"""
    barcodes = pyzbar.decode(frame)
    detected_codes = []
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        (x, y, w, h) = barcode.rect
        
        detected_codes.append({
            'data': barcode_data,
            'type': barcode_type,
            'location': (x, y, w, h)
        })
    
    return detected_codes

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("📱 Mobile Barcode Scanner")
    st.markdown("**Optimized for phones and tablets**")
    st.markdown("---")
    
    # Step 1: File Upload
    st.header("📂 Step 1: Upload Your Barcode List")
    
    uploaded_file = st.file_uploader(
        "Choose Excel or CSV file with tracking IDs",
        type=['xlsx', 'xls', 'csv'],
        help="Upload file with 'tracking-id' column or barcodes in first column"
    )
    
    if uploaded_file is not None:
        with st.spinner("Loading barcodes..."):
            valid_barcodes = load_barcodes_from_file(uploaded_file)
            
        if valid_barcodes:
            st.session_state.valid_barcodes = valid_barcodes
            st.session_state.file_uploaded = True
            st.success(f"✅ Loaded {len(valid_barcodes)} valid tracking IDs!")
            
            # Show preview
            with st.expander("👀 Preview loaded tracking IDs"):
                preview_list = list(valid_barcodes)[:5]
                for i, barcode in enumerate(preview_list, 1):
                    st.text(f"{i}. {barcode}")
                if len(valid_barcodes) > 5:
                    st.text(f"... and {len(valid_barcodes) - 5} more")
    
    # Step 2: Scanning (only if file uploaded)
    if st.session_state.file_uploaded:
        st.markdown("---")
        st.header("📸 Step 2: Scan Your Barcodes")
        
        st.markdown("""
        ### 📱 **How to scan with your phone:**
        1. **Take a clear photo** of the barcode/tracking ID
        2. **Ensure good lighting** - avoid shadows and glare
        3. **Hold phone steady** and get barcode in focus
        4. **Upload the photo** below for instant results!
        """)
        
        uploaded_image = st.file_uploader(
            "📷 Take a photo and upload it here",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            help="Use your phone camera to take a photo of the barcode"
        )
        
        if uploaded_image is not None:
            # Display uploaded image
            image = PIL.Image.open(uploaded_image)
            st.image(image, caption="📸 Your uploaded image", use_column_width=True)
            
            # Process image
            with st.spinner("🔍 Scanning for barcodes..."):
                # Convert PIL image to cv2 format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Detect barcodes
                detected_barcodes = detect_barcodes(opencv_image)
                
            if detected_barcodes:
                st.success("🎉 Barcode(s) found!")
                
                for barcode_info in detected_barcodes:
                    barcode_data = barcode_info['data']
                    
                    # Display found barcode
                    st.code(f"Found: {barcode_data}")
                    
                    # Check if barcode is valid
                    if (barcode_data in st.session_state.valid_barcodes and 
                        barcode_data not in [scan['barcode'] for scan in st.session_state.scanned_barcodes]):
                        
                        # Valid and new barcode
                        st.session_state.scanned_barcodes.append({
                            'barcode': barcode_data,
                            'timestamp': datetime.now(),
                            'status': 'Valid'
                        })
                        st.success(f"✅ **VALID TRACKING ID!** - {barcode_data}")
                        st.balloons()
                        
                    elif barcode_data in st.session_state.valid_barcodes:
                        st.warning(f"⚠️ **ALREADY SCANNED** - {barcode_data}")
                        
                    else:
                        st.error(f"❌ **INVALID TRACKING ID** - {barcode_data}")
                        st.info("This tracking ID is not in your uploaded list.")
            else:
                st.error("❌ No barcodes detected in the image")
                st.info("💡 **Tips:** Ensure good lighting, clear focus, and try different angles")
        
        # Step 3: Results and History
        if st.session_state.scanned_barcodes:
            st.markdown("---")
            st.header("📊 Step 3: Scan Results")
            
            # Statistics
            total_valid = len(st.session_state.valid_barcodes)
            total_scanned = len(st.session_state.scanned_barcodes)
            progress = (total_scanned / total_valid) * 100 if total_valid > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Total", total_valid)
            with col2:
                st.metric("✅ Scanned", total_scanned)
            with col3:
                st.metric("📊 Progress", f"{progress:.1f}%")
            
            # Progress bar
            st.progress(progress / 100)
            
            # Scan history
            st.subheader("📋 Scan History")
            df_history = pd.DataFrame(st.session_state.scanned_barcodes)
            df_history['timestamp'] = df_history['timestamp'].dt.strftime('%H:%M:%S')
            
            st.dataframe(
                df_history[['timestamp', 'barcode', 'status']],
                column_config={
                    'timestamp': 'Time',
                    'barcode': 'Tracking ID',
                    'status': 'Status'
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Export and clear buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export Results", type="primary"):
                    csv = df_history.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🗑️ Clear History", type="secondary"):
                    st.session_state.scanned_barcodes = []
                    st.rerun()
    
    else:
        st.info("👆 Please upload your tracking ID file first to start scanning!")

if __name__ == "__main__":
    main()
