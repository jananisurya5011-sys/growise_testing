@echo off
rem Starts the GroWise backend and website in their own windows, then opens the site.
cd /d "%~dp0"

start "GroWise Backend" cmd /k "cd /d "%~dp0backend" && venv_local\Scripts\python.exe app.py"
start "GroWise Website" cmd /k "cd /d "%~dp0website" && npm run dev"

echo Waiting for the servers to start...
ping 127.0.0.1 -n 8 >nul
start "" http://localhost:5173
