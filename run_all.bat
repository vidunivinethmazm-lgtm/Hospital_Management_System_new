@echo off
echo ============================================
echo  Hospital Management System - Starting All
echo ============================================

echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting Auth Service        (port 8007)...
start "Auth Service"        cmd /k "cd auth_service && python main.py"

echo Starting Patient Service     (port 8001)...
start "Patient Service"     cmd /k "cd patient_service && python main.py"

echo Starting Doctor Service      (port 8002)...
start "Doctor Service"      cmd /k "cd doctor_service && python main.py"

echo Starting Appointment Service (port 8003)...
start "Appointment Service" cmd /k "cd appointment_service && python main.py"

echo Starting Department Service  (port 8004)...
start "Department Service"  cmd /k "cd department_service && python main.py"

echo Starting Medicine Service    (port 8005)...
start "Medicine Service"    cmd /k "cd medicine_service && python main.py"

echo Starting Bill Service        (port 8006)...
start "Bill Service"        cmd /k "cd bill_service && python main.py"

timeout /t 3 /nobreak >nul

echo Starting API Gateway         (port 8000)...
start "API Gateway"         cmd /k "cd api_gateway && python main.py"

echo.
echo ============================================
echo  All services started!
echo ============================================
echo.
echo  STEP 1 - Register:  POST http://localhost:8000/auth/register
echo  STEP 2 - Login:     POST http://localhost:8000/auth/login
echo  STEP 3 - Use token in Postman: Authorization - Bearer Token
echo.
echo  Gateway Swagger: http://localhost:8000/docs
echo  Health Check:    http://localhost:8000/health
echo ============================================
pause
