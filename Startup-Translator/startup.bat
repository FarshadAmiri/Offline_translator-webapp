:: Start MySQL from XAMPP
start "" "C:\xampp\mysql\bin\mysqld.exe"

:: Wait a few seconds to ensure MySQL starts before Django
timeout /t 5 /nobreak >nul

:: Start Nginx
cd /d C:\nginx-1.24.0
start nginx.exe

:: Start Django App
cd /d D:
cd /d D:\Projects\venv2\Scripts
call activate.bat
cd /d D:\Projects\Offline_translator-webapp
echo Starting Django app with Nginx and Witress...
call py runserver.py
