@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py setup_local.py
  if errorlevel 1 goto failed
  py -m unittest discover -s tests -v
  if errorlevel 1 goto failed
  py -m unittest discover -s bulk/tests -v
  if errorlevel 1 goto failed
) else (
  python setup_local.py
  if errorlevel 1 goto failed
  python -m unittest discover -s tests -v
  if errorlevel 1 goto failed
  python -m unittest discover -s bulk/tests -v
  if errorlevel 1 goto failed
)
echo.
echo Setup and both sets of tests passed.
pause
exit /b 0
:failed
echo.
echo Setup or tests failed. Check the error above.
pause
exit /b 1
