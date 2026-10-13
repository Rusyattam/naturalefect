@echo off
chcp 65001 >nul
cd /d "%~dp0"
py clone_originals.py
if errorlevel 1 (
  echo.
  echo Some files did not download. Check clone_report.txt.
) else (
  echo.
  echo Original pages and downloadable assets are now saved to site-1 and site-2.
)
echo.
pause
