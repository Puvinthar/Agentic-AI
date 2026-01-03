#!/usr/bin/env pwsh
# Force update and rebuild HF Space with latest code

Write-Host "
============================================================
🔄 Force Update HF Space - Agentic AI
============================================================
" -ForegroundColor Cyan

$HF_USERNAME = "lossleo"
$HF_SPACE_NAME = "Agentic-Ai-fullstack"
$HF_SPACE_URL = "https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE_NAME"
$DEPLOY_DIR = "hf-space-update"

Write-Host "🎯 Target Space: $HF_SPACE_URL" -ForegroundColor Yellow
Write-Host ""

# Clean up old directory if exists
if (Test-Path $DEPLOY_DIR) {
    Write-Host "🧹 Cleaning up old deployment directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $DEPLOY_DIR
}

Write-Host "
============================================================
Step 1: Cloning Your HF Space
============================================================
" -ForegroundColor Cyan

try {
    git clone $HF_SPACE_URL $DEPLOY_DIR
    Set-Location $DEPLOY_DIR
} catch {
    Write-Host "❌ Failed to clone. Error: $_" -ForegroundColor Red
    Write-Host "💡 Make sure you're logged in: git config credential.helper store" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Space cloned" -ForegroundColor Green

Write-Host "
============================================================
Step 2: Updating Files with Latest Code
============================================================
" -ForegroundColor Cyan

# Remove old files (except .git)
Get-ChildItem -Exclude ".git" | Remove-Item -Recurse -Force

# Copy fresh files from local
Write-Host "📁 Copying app-hf.py..." -ForegroundColor Gray
Copy-Item "..\app-hf.py" "." -Force

Write-Host "📁 Copying requirements-hf.txt..." -ForegroundColor Gray
Copy-Item "..\requirements-hf.txt" "." -Force

Write-Host "📁 Copying Dockerfile..." -ForegroundColor Gray
Copy-Item "..\Dockerfile.hf-combined" "Dockerfile" -Force

Write-Host "📁 Copying backend/..." -ForegroundColor Gray
Copy-Item -Recurse "..\backend" "." -Force

Write-Host "📁 Copying frontend/..." -ForegroundColor Gray
Copy-Item -Recurse "..\frontend" "." -Force

Write-Host "📁 Copying README..." -ForegroundColor Gray
Copy-Item "..\README-HF.md" "README.md" -Force

# Create/update .gitignore
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
agentic.db
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent

# Ensure uploads directory exists
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null
New-Item -ItemType File -Force -Path "uploads\.gitkeep" | Out-Null

Write-Host "✅ All files updated" -ForegroundColor Green

Write-Host "
============================================================
Step 3: Adding Build Timestamp to Force Rebuild
============================================================
" -ForegroundColor Cyan

# Add a comment with timestamp to Dockerfile to force rebuild
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$dockerfileContent = Get-Content "Dockerfile" -Raw
$dockerfileContent = "# Last updated: $timestamp`n" + $dockerfileContent
Set-Content -Path "Dockerfile" -Value $dockerfileContent

Write-Host "✅ Build timestamp added: $timestamp" -ForegroundColor Green

Write-Host "
============================================================
Step 4: Committing Changes
============================================================
" -ForegroundColor Cyan

git add -A
git status

$commitMsg = @"
🔄 Force Update: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

- Updated backend code
- Updated frontend code  
- Updated app-hf.py
- Updated requirements
- Force rebuild with timestamp
"@

git commit -m $commitMsg

Write-Host "✅ Changes committed" -ForegroundColor Green

Write-Host "
============================================================
Step 5: Pushing to HF Space (This triggers rebuild)
============================================================
" -ForegroundColor Cyan

git push --force

if ($LASTEXITCODE -ne 0) {
    Write-Host "
❌ Push failed. Authentication needed:
    
    Run these commands in the $DEPLOY_DIR folder:
    git config credential.helper store
    git push
    
    Enter your HF username and token when prompted.
    Get token from: https://huggingface.co/settings/tokens
" -ForegroundColor Red
    exit 1
}

Set-Location ..

Write-Host "
============================================================
✅ Update Pushed Successfully!
============================================================
" -ForegroundColor Green

Write-Host "
🎉 Your HF Space is now rebuilding with latest code!

📊 Monitor the rebuild:
   🔗 Logs: $HF_SPACE_URL/logs
   
⏱️  Build Time: ~3-5 minutes

📱 After rebuild completes:
   🔗 App: https://$HF_USERNAME-$HF_SPACE_NAME.hf.space
   
💡 What to check:
   ✅ Build completes without errors
   ✅ 'Running' status appears
   ✅ Test your latest features
   
🔑 If backend is offline after rebuild:
   1. Go to Settings → Repository secrets
   2. Verify GROQ_API_KEY is set
   3. Add OPENWEATHER_API_KEY if not present
   
============================================================
" -ForegroundColor Cyan

$cleanup = Read-Host "
Delete temporary update directory? (y/n)"
if ($cleanup -eq "y" -or $cleanup -eq "Y") {
    Remove-Item -Recurse -Force $DEPLOY_DIR
    Write-Host "✅ Cleanup complete" -ForegroundColor Green
} else {
    Write-Host "📁 Update files kept at: .\$DEPLOY_DIR" -ForegroundColor Yellow
}

Write-Host "
Done! 🚀
" -ForegroundColor Green
