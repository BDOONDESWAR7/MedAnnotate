@echo off
echo ==============================================
echo   Killing any existing Python Server processes
echo ==============================================
taskkill /F /IM python.exe >nul 2>&1

echo.
echo ==============================================
echo   Starting MedAnnotate Demo Server
echo ==============================================
python app.py
pause
