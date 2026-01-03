#!/usr/bin/env pwsh
# Deploy with PostgreSQL/Neon DB support

Write-Host "
============================================================
🐘 Deploying with PostgreSQL/Neon DB Support
============================================================
" -ForegroundColor Cyan

$HF_USERNAME = "lossleo"
$HF_SPACE_NAME = "Agentic-Ai-fullstack"
$HF_SPACE_URL = "https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE_NAME"
$DEPLOY_DIR = "hf-postgres-deploy"

if (Test-Path $DEPLOY_DIR) {
    Remove-Item -Recurse -Force $DEPLOY_DIR
}

Write-Host "📥 Cloning space..." -ForegroundColor Gray
git clone $HF_SPACE_URL $DEPLOY_DIR 2>$null
Set-Location $DEPLOY_DIR

Write-Host "📦 Updating files..." -ForegroundColor Gray
Copy-Item "..\backend\database.py" "backend\database.py" -Force
Copy-Item "..\requirements-hf.txt" "requirements-hf.txt" -Force

Write-Host "💾 Committing..." -ForegroundColor Gray
git add backend/database.py requirements-hf.txt
git commit -m "Add PostgreSQL support for Neon DB

- Added asyncpg and psycopg2-binary to requirements
- Database now supports both PostgreSQL (Neon) and SQLite fallback
- Will use DATABASE_URL from HF Spaces secrets if provided
"

Write-Host "🚀 Pushing..." -ForegroundColor Gray
git push

Set-Location ..

Write-Host "
============================================================
✅ PostgreSQL Support Added!
============================================================
" -ForegroundColor Green

Write-Host "
📋 NEXT STEPS - Configure Your Neon DB:

1️⃣  Go to HF Space Settings:
   🔗 https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE_NAME/settings

2️⃣  Click 'Repository secrets' → 'New secret'

3️⃣  Add these secrets:
   
   Secret 1:
   Name:  DATABASE_URL
   Value: postgresql+asyncpg://[user]:[password]@[host]/[dbname]
   
   Example from your .env:
   postgresql+asyncpg://postgres:postgres@localhost:5432/agentic_db
   
   For Neon DB, it looks like:
   postgresql+asyncpg://[user]:[password]@ep-xxx.us-east-2.aws.neon.tech/neondb

   Secret 2:
   Name:  SYNC_DATABASE_URL  
   Value: postgresql://[user]:[password]@[host]/[dbname]
   (Same as above but without '+asyncpg')

4️⃣  Your existing secrets (keep these):
   ✅ GROQ_API_KEY
   ✅ OPENWEATHER_API_KEY

============================================================
💡 Get Your Neon DB Connection String:
============================================================

If using Neon DB:
1. Go to https://console.neon.tech
2. Select your project
3. Click 'Connection string'
4. Copy the connection string
5. Replace 'postgresql://' with 'postgresql+asyncpg://' for DATABASE_URL
6. Use as-is 'postgresql://' for SYNC_DATABASE_URL

============================================================
🔄 After adding secrets:
============================================================

Your space will auto-rebuild and connect to Neon DB!

📊 Monitor: $HF_SPACE_URL/logs
🌐 App: https://$HF_USERNAME-$HF_SPACE_NAME.hf.space

If you DON'T add DATABASE_URL secret:
→ It will use SQLite as fallback (still works!)

============================================================
" -ForegroundColor Cyan

Remove-Item -Recurse -Force $DEPLOY_DIR

Write-Host "Done! 🚀" -ForegroundColor Green
