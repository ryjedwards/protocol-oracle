@echo off
echo ===============================================
echo PROTOCOL: GIT INITIALIZATION
echo ===============================================
echo.

REM Initialize Git repository
echo [1/6] Initializing Git repository...
git init

REM Add all files
echo [2/6] Adding project files...
git add .

REM Create initial commit
echo [3/6] Creating initial commit...
git commit -m "Initial commit: PROTOCOL ORACLE_v1 - AI-Powered Tarot Reader"

echo.
echo ===============================================
echo NEXT STEP: Create GitHub Repository
echo ===============================================
echo.
echo 1. Go to https://github.com/new
echo 2. Repository name: protocol-oracle
echo 3. Description: AI-Powered Cyberpunk Tarot Reader
echo 4. Keep it PUBLIC (Streamlit Cloud requires public repos for free tier)
echo 5. DO NOT initialize with README, .gitignore, or license
echo 6. Click "Create repository"
echo.
echo After creating the repo, copy the URL that looks like:
echo   https://github.com/YOUR_USERNAME/protocol-oracle.git
echo.
pause

set /p REPO_URL="Paste your GitHub repository URL here: "

echo.
echo [4/6] Adding GitHub remote...
git remote add origin %REPO_URL%

echo [5/6] Renaming branch to main...
git branch -M main

echo [6/6] Pushing to GitHub...
git push -u origin main

echo.
echo ===============================================
echo SUCCESS! Your code is now on GitHub!
echo ===============================================
echo.
echo NEXT: Deploy to Streamlit Cloud
echo 1. Go to https://share.streamlit.io
echo 2. Click "New app"
echo 3. Select your repository: protocol-oracle
echo 4. Set main file: main.py
echo 5. In Settings ^> Secrets, add:
echo    GOOGLE_API_KEY = "your-api-key-here"
echo 6. Click "Deploy"
echo.
pause
