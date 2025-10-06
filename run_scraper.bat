@echo off
echo South Carolina Courts Scraper
echo ============================
echo.
echo This scraper requires US-based IP addresses to work.
echo.
echo Options:
echo 1. Run without proxy (will likely fail due to geo-blocking)
echo 2. Run with proxy support
echo 3. Test a proxy
echo 4. Add a proxy
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running scraper without proxy...
    python sc_courts_scraper.py
) else if "%choice%"=="2" (
    echo Running scraper with proxy support...
    python sc_courts_scraper.py --proxy
) else if "%choice%"=="3" (
    set /p proxy="Enter proxy (ip:port): "
    python test_proxy.py %proxy%
) else if "%choice%"=="4" (
    set /p proxy="Enter proxy (ip:port): "
    python add_proxy.py %proxy%
) else (
    echo Invalid choice
)

pause
