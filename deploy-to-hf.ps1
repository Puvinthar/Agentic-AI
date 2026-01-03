#!/usr/bin/env pwsh
# PowerShell script to deploy Agentic AI to Hugging Face Spaces
# Usage: .\deploy-to-hf.ps1

Write-Host "
============================================================
🤖 Agentic AI - Hugging Face Spaces Deployment
============================================================
" -ForegroundColor Cyan

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Get user input
Write-Host "📝 Enter your Hugging Face details:" -ForegroundColor Yellow
$HF_USERNAME = Read-Host "HF Username"
$HF_SPACE_NAME = Read-Host "HF Space Name (e.g., agentic-ai)"

if ([string]::IsNullOrWhiteSpace($HF_USERNAME) -or [string]::IsNullOrWhiteSpace($HF_SPACE_NAME)) {
    Write-Host "❌ Error: Username and Space Name are required!" -ForegroundColor Red
    exit 1
}

$HF_SPACE_URL = "https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE_NAME"

Write-Host "
============================================================
📋 Deployment Plan
============================================================
🔗 Space URL: $HF_SPACE_URL
📁 Local Path: .\hf-deployment-temp
============================================================
" -ForegroundColor Green

# Confirm before proceeding
$confirm = Read-Host "Continue with deployment? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Create temporary directory for deployment
$DEPLOY_DIR = "hf-deployment-temp"
if (Test-Path $DEPLOY_DIR) {
    Write-Host "⚠️  Removing existing deployment directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $DEPLOY_DIR
}

Write-Host "
============================================================
Step 1: Cloning HF Space Repository
============================================================
" -ForegroundColor Cyan

try {
    git clone $HF_SPACE_URL $DEPLOY_DIR
    if (-not $?) {
        Write-Host "❌ Failed to clone repository. Make sure:" -ForegroundColor Red
        Write-Host "   1. The space exists at: $HF_SPACE_URL" -ForegroundColor Red
        Write-Host "   2. You are logged in to HF: git config credential.helper store" -ForegroundColor Red
        Write-Host "   3. You have access to the space" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error cloning repository: $_" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Repository cloned successfully" -ForegroundColor Green

Write-Host "
============================================================
Step 2: Copying Application Files
============================================================
" -ForegroundColor Cyan

# Copy main files
Copy-Item ".\app-hf.py" "$DEPLOY_DIR\app-hf.py" -Force
Copy-Item ".\requirements-hf.txt" "$DEPLOY_DIR\requirements-hf.txt" -Force
Copy-Item ".\Dockerfile.hf-combined" "$DEPLOY_DIR\Dockerfile" -Force
Copy-Item ".\README-HF.md" "$DEPLOY_DIR\README.md" -Force

# Copy directories
Copy-Item ".\backend" "$DEPLOY_DIR\backend" -Recurse -Force
Copy-Item ".\frontend" "$DEPLOY_DIR\frontend" -Recurse -Force

# Create .gitignore if it doesn't exist
$gitignoreContent = @"
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.local
.venv/
venv/
*.egg-info/
.DS_Store
.vscode/
uploads/*.txt
uploads/*.pdf
uploads/*.docx
!uploads/.gitkeep
*.log
"@

Set-Content -Path "$DEPLOY_DIR\.gitignore" -Value $gitignoreContent

# Create uploads directory with .gitkeep
New-Item -ItemType Directory -Force -Path "$DEPLOY_DIR\uploads" | Out-Null
New-Item -ItemType File -Force -Path "$DEPLOY_DIR\uploads\.gitkeep" | Out-Null

Write-Host "✅ Files copied successfully" -ForegroundColor Green

Write-Host "
============================================================
Step 3: Committing Changes
============================================================
" -ForegroundColor Cyan

Set-Location $DEPLOY_DIR

# Configure git if not already configured
$gitUserName = git config user.name
if ([string]::IsNullOrWhiteSpace($gitUserName)) {
    git config user.name $HF_USERNAME
    git config user.email "$HF_USERNAME@users.noreply.huggingface.co"
}

# Add and commit
git add .
git commit -m "Deploy: Agentic AI combined frontend + backend

- Combined app running on port 7860
- Backend API on port 8000
- Frontend interface with streaming chat
- Document upload and RAG support
- Weather and web search capabilities
- Meeting scheduler with SQLite
"

Write-Host "✅ Changes committed" -ForegroundColor Green

Write-Host "
============================================================
Step 4: Pushing to Hugging Face
============================================================
" -ForegroundColor Cyan

git push

if (-not $?) {
    Write-Host "❌ Push failed. You may need to authenticate:" -ForegroundColor Red
    Write-Host "   Run: git config credential.helper store" -ForegroundColor Yellow
    Write-Host "   Then: git push" -ForegroundColor Yellow
    Write-Host "   Enter your HF username and token when prompted" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

Set-Location ..

Write-Host "
============================================================
✅ Deployment Successful!
============================================================
" -ForegroundColor Green

Write-Host "
🚀 Your app is now deploying at:
   $HF_SPACE_URL

📊 Next Steps:
   1. Go to your space page
   2. Click 'Settings' → 'Repository secrets'
   3. Add these secrets:
      • GROQ_API_KEY = your_groq_api_key
      • OPENWEATHER_API_KEY = your_weather_key (optional)
   4. Wait 3-5 minutes for build to complete
   5. Check the 'Logs' tab if there are any issues

📝 Build Status:
   Watch at: $HF_SPACE_URL/logs

🌐 Once ready, access your app at:
   https://$HF_USERNAME-$HF_SPACE_NAME.hf.space

============================================================
" -ForegroundColor Cyan

Write-Host "💡 Tip: To update your space later, just run this script again!" -ForegroundColor Yellow

# Ask if user wants to clean up temp directory
$cleanup = Read-Host "
Delete temporary deployment directory? (y/n)"
if ($cleanup -eq "y" -or $cleanup -eq "Y") {
    Remove-Item -Recurse -Force $DEPLOY_DIR
    Write-Host "✅ Cleanup complete" -ForegroundColor Green
} else {
    Write-Host "📁 Deployment files kept at: .\$DEPLOY_DIR" -ForegroundColor Yellow
}

Write-Host "
🎉 Deployment process complete!
" -ForegroundColor Green
