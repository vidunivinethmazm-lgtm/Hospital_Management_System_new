@echo off
echo Stopping all Hospital Management services...
taskkill /FI "WINDOWTITLE eq Patient Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Doctor Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Appointment Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Department Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Medicine Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Bill Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq API Gateway*" /F >nul 2>&1
echo All services stopped.
pause
