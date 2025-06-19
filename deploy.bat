@echo off
echo 🚀 Preparing Barcode Scanner App for Deployment...
echo ==================================================

REM Check if git is initialized
if not exist ".git" (
    echo 📂 Initializing Git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

REM Add all files
echo 📁 Adding files to git...
git add .

REM Commit files
echo 💾 Committing files...
git commit -m "Barcode Scanner App - Ready for deployment"

echo.
echo 🎉 Your app is ready for deployment!
echo.
echo 📋 Next Steps:
echo 1. Create a GitHub repository
echo 2. Add remote: git remote add origin https://github.com/yourusername/barcode-scanner
echo 3. Push code: git push -u origin main
echo 4. Deploy on Streamlit Cloud: https://share.streamlit.io
echo.
echo ⚠️  Important Notes:
echo - Camera requires HTTPS (automatic on Streamlit Cloud)
echo - Users need to allow camera permissions
echo - Image upload mode works as backup
echo.
echo 🔗 Deployment Guide: See DEPLOYMENT_GUIDE.md for detailed instructions
echo ==================================================

pause
