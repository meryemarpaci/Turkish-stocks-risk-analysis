@echo off
echo ================================
echo BIST30 Risk Analizi Baslatiliyor
echo ================================
echo.
echo Python paketleri kontrol ediliyor...
pip install -r requirements.txt --quiet
echo.
echo BIST30 analizi calistiriliyor...
python bist30_analysis.py
echo.
echo Analiz tamamlandi!
echo Sonuclari plots/ ve reports/ klasorlerinde bulabilirsiniz.
echo.
pause 