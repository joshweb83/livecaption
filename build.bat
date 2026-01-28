@echo off
REM Live Caption - Windows Build Script
REM Version: 1.0.1

echo ========================================
echo Live Caption - Windows Build Script
echo ========================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.11 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
python --version
echo.

REM Install dependencies
echo [2/4] Installing dependencies...
echo This may take 5-10 minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

REM Install PyInstaller
echo [3/4] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller!
    pause
    exit /b 1
)
echo.

REM Build executable
echo [4/4] Building executable...
echo This may take 10-15 minutes...
pyinstaller LiveCaption.spec
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

REM Success
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable location: dist\LiveCaption.exe
echo.
echo You can now distribute the LiveCaption.exe file.
echo First run will download AI models (~550MB).
echo.
pause
