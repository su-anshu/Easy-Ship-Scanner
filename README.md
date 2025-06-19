# 📱 Barcode Scanner Streamlit App

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Use the app:**
   - Upload your Excel file with 'tracking-id' column (or any CSV/Excel file)
   - Allow camera permissions when prompted
   - Point camera at barcodes/tracking IDs
   - See real-time scanning results with audio feedback!

## ✨ Features

- 📁 **Smart Excel/CSV upload** - Automatically detects 'tracking-id' column or uses first column
- 📷 **Optimized webcam scanning** - Reduced lag for laptop cameras
- ✅ **Visual feedback** - Green ✓ for valid, red ✗ for invalid barcodes
- 🔊 **Audio feedback** - Success/failure sounds for scan results
- 📊 **Real-time progress tracking** - Statistics and completion percentage
- 📋 **Complete scan history** - Timestamped log with export functionality
- 📥 **Export scan results** - Download results to CSV
- 🎯 **Duplicate prevention** - Won't scan the same barcode twice
- ⚡ **Performance optimized** - Frame skipping and resolution scaling for smooth operation

## 📋 Requirements

- Python 3.8+
- Webcam access
- Modern web browser (Chrome/Firefox recommended)

## 🔧 Supported Barcode Formats

- Code 128, Code 39
- EAN-13/UPC-A, EAN-8/UPC-E
- QR Code, Data Matrix
- PDF417 and more...

## 🆘 Troubleshooting

### Camera Issues
- **Camera not working?** Run `python test_camera.py` to diagnose issues
- **Lag/slow performance?** Close other camera apps, ensure good lighting
- **"Camera not found"?** Check browser permissions, try different browser

### Barcode Detection
- **Barcode not detected?** Ensure good lighting and steady positioning
- **Hold tracking ID steady** 5-10cm from camera for 1-2 seconds
- **Try different angles** if barcode is hard to read

### File Upload Issues
- **Excel not loading?** Ensure 'tracking-id' column exists or put barcodes in first column
- **Column not found?** App will show available columns - check spelling

### Performance Tips
- **Use external USB camera** for better performance than laptop camera
- **Close other applications** to free up camera resources
- **Good lighting is crucial** - avoid shadows and glare

---
**Made with ❤️ using Streamlit**