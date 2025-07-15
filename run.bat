@echo off
REM Run script for QA RAG Chatbot

echo Starting QA RAG Chatbot...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found
    echo Please copy .env.example to .env and configure your settings
    pause
)

REM Run the application
echo Launching Streamlit app...
streamlit run app.py

pause
