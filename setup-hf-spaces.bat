@echo off
REM HF Spaces Setup Script for Windows PowerShell
REM Follow these steps to deploy Agentic AI to Hugging Face Spaces

echo.
echo ============================================================
echo Agentic AI Frontend - Hugging Face Spaces Setup
echo ============================================================
echo.

REM Step 1: Create HF Space
echo STEP 1: Create a new Space on Hugging Face
echo ============================================================
echo 1. Go to https://huggingface.co/spaces
echo 2. Click "Create new Space"
echo 3. Give it a name (e.g., agentic-ai-frontend)
echo 4. Choose Space type: "Docker"
echo 5. Click "Create Space"
echo 6. On your space page, copy the repository URL
echo.
pause

REM Step 2: Ask for HF username and space name
set /p HF_USERNAME="Enter your HF username: "
set /p HF_SPACE_NAME="Enter your Space name: "

echo.
echo STEP 2: Clone Your Space Repository
echo ============================================================
set HF_SPACE_URL=https://huggingface.co/spaces/%HF_USERNAME%/%HF_SPACE_NAME%
echo Cloning from: %HF_SPACE_URL%
git clone %HF_SPACE_URL%
cd %HF_SPACE_NAME%

echo.
echo STEP 3: Copy Files from Agentic Backend
echo ============================================================
copy ..\app.py .
copy ..\requirements-hf.txt requirements.txt
copy ..\Dockerfile.hf Dockerfile
xcopy ..\frontend\templates templates\ /E /I
xcopy ..\frontend\static static\ /E /I

echo.
echo STEP 4: Create .gitignore
echo ============================================================
(
echo __pycache__/
echo *.pyc
echo *.pyo
echo .env
echo .env.local
echo uploads/
echo .DS_Store
echo *.egg-info/
) > .gitignore

echo.
echo STEP 5: Commit and Push to HF
echo ============================================================
git add .
git commit -m "Initial commit: Agentic AI Frontend on HF Spaces"
git push

echo.
echo ============================================================
echo SUCCESS! Your space is deploying...
echo ============================================================
echo.
echo Your frontend will be available at:
echo https://%HF_USERNAME%-%HF_SPACE_NAME%.hf.space
echo.
echo NOTE: You still need to deploy the backend separately.
echo Options:
echo   1. Railway (railway.app) - Recommended
echo   2. Render (render.com)
echo   3. Keep running locally with ngrok
echo.
echo After backend is deployed, add the BACKEND_URL to your
echo HF Space secrets:
echo   1. Go to Settings ^> Repository secrets
echo   2. Add: BACKEND_URL = https://your-backend-url.com
echo   3. Space will auto-redeploy
echo.
pause
