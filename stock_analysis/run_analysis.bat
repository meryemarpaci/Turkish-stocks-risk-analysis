@echo off
echo Turk Hisse Analizi Programi Baslatiliyor...
echo ----------------------------------------------

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python'u yukleyin.
    pause
    exit /b
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip bulunamadi! Python kurulumunuzu kontrol edin.
    pause
    exit /b
)

echo Gerekli kutuphaneler yukleniyor...
pip install -r requirements.txt

echo.
echo Analiz baslatiliyor...
python stock_analysis.py

echo.
echo ----------------------------------------------
echo Islem tamamlandi!
pause 