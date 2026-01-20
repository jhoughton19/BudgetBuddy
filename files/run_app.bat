@echo off
REM BudgetBuddy Web App Launcher for Windows

echo ==========================================
echo   BudgetBuddy - County Budget Assistant
echo ==========================================
echo.
echo Starting web application...
echo Opening browser at http://localhost:8501
echo.
echo Press CTRL+C to stop the server
echo.

REM Install requirements if needed
pip install -r requirements.txt -q

REM Launch Streamlit
streamlit run app.py

pause
