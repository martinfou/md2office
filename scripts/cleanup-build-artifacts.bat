@echo off
REM Script to remove build artifacts from git tracking
REM Run this script to clean up build artifacts that were accidentally committed

echo Removing build artifacts from git tracking...

REM Remove build directories
if exist build (
    echo Removing build\ directory from git tracking...
    git rm -r --cached build\ 2>nul || echo   build\ not tracked or already removed
)

REM Remove dist directories
if exist dist (
    echo Removing dist\ directory from git tracking...
    git rm -r --cached dist\ 2>nul || echo   dist\ not tracked or already removed
)

REM Remove venv directory
if exist venv (
    echo Removing venv\ directory from git tracking...
    git rm -r --cached venv\ 2>nul || echo   venv\ not tracked or already removed
)

REM Remove egg-info directories (using PowerShell for find)
for /d /r %%d in (*.egg-info) do (
    echo Removing %%d from git tracking...
    git rm -r --cached "%%d" 2>nul
)

REM Remove __pycache__ directories
for /d /r %%d in (__pycache__) do (
    echo Removing %%d from git tracking...
    git rm -r --cached "%%d" 2>nul
)

echo.
echo Done! Build artifacts have been removed from git tracking.
echo These files are now ignored by .gitignore and won't be committed in the future.
echo.
echo Next steps:
echo   1. Review the changes: git status
echo   2. Commit the removal: git commit -m "chore: remove build artifacts from git tracking"
echo   3. Verify .gitignore is working: git status (should not show build artifacts)

