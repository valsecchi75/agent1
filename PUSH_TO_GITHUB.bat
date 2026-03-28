@echo off
REM ========================================================================
REM Agent 1 Registry - Auto-rebuild and push to GitHub
REM Repository: github.com/valsecchi75/agent1
REM ========================================================================

setlocal enabledelayexpansion

REM Disable git pager so script never blocks waiting for user input
set "GIT_PAGER=cat"
set "GIT_TERMINAL_PROMPT=0"

set "GITHUB_USERNAME=valsecchi75"
set "REPO_NAME=agent1"
set "REMOTE_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git"

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%" >nul || (
    echo ERROR: Could not change to script directory
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo  Agent 1 Registry - Push to GitHub
echo  Repository: %GITHUB_USERNAME%/%REPO_NAME%
echo ========================================================================
echo.

REM Check Python (try python, then py, then python3)
set "PYTHON_CMD="
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)
py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :python_found
)
echo ERROR: Python not found. Install from https://www.python.org/downloads/
pause
exit /b 1

:python_found
echo [OK] Python found (%PYTHON_CMD%)

REM Check Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Install from https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git found

REM Initialize git repo if needed
if not exist ".git" (
    echo.
    echo Initializing Git repository...
    git init -b main >nul 2>&1
    if errorlevel 1 (
        git init >nul 2>&1
        git branch -m main >nul 2>&1
    )
    git remote add origin %REMOTE_URL% >nul 2>&1
    echo [OK] Git initialized with remote: %REMOTE_URL%
)
echo.

REM Step 1: Rebuild registry.json
echo Step 1: Rebuilding registry.json...
echo -----------------------------------------------
%PYTHON_CMD% rebuild_registry.py
if errorlevel 1 (
    echo ERROR: rebuild_registry.py failed
    pause
    exit /b 1
)
echo.

REM Step 2: Stage ALL changes (new templates, updated registry, deletions)
echo Step 2: Staging all changes...
echo -----------------------------------------------
git add -A
if errorlevel 1 (
    echo ERROR: git add failed
    pause
    exit /b 1
)

REM Check if there are changes to commit
git diff --cached --quiet >nul 2>&1
if %errorlevel% equ 0 (
    echo No new changes to commit.
    goto :check_push
)

REM Show what changed
echo.
echo Changes to commit:
git --no-pager diff --cached --stat
echo.

REM Step 3: Commit
echo Step 3: Committing...
echo -----------------------------------------------
set "COMMIT_MSG=Update registry: auto-rebuild %date% %time:~0,5%"
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo ERROR: git commit failed
    pause
    exit /b 1
)
echo [OK] Committed: %COMMIT_MSG%
echo.

:check_push
REM Step 4: Check for unpushed commits, then push
echo Step 4: Checking for unpushed commits...
echo -----------------------------------------------
git fetch origin main >nul 2>&1

REM Count commits ahead of origin/main
set "AHEAD=0"
for /f %%i in ('git rev-list --count origin/main..HEAD 2^>nul') do set "AHEAD=%%i"

if "%AHEAD%"=="0" (
    echo.
    echo Nothing to push. Everything is already up to date on GitHub.
    pause
    exit /b 0
)

echo Found %AHEAD% unpushed commit(s). Pushing...
echo.
git push -u origin main --force-with-lease
if errorlevel 1 (
    echo.
    echo Normal push failed, trying force push...
    git push -u origin main --force
    if errorlevel 1 (
        echo.
        echo ERROR: git push failed
        echo.
        echo If this is the first push, create the repo first:
        echo   gh repo create %REPO_NAME% --public --source=. --push
        echo.
        echo Or check your GitHub credentials.
        pause
        exit /b 1
    )
)
echo [OK] Pushed %AHEAD% commit(s) to GitHub
echo.

echo ========================================================================
echo  SUCCESS! Registry updated at:
echo  https://raw.githubusercontent.com/%GITHUB_USERNAME%/%REPO_NAME%/main/registry.json
echo ========================================================================
echo.
pause
exit /b 0
