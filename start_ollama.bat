@echo off
REM Script pour demarrer Ollama avec Gemma 3 (Windows)

echo ==========================================
echo DEMARRAGE OLLAMA + GEMMA 3
echo ==========================================
echo.

REM Verifier que Ollama est installe
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Ollama n'est pas installe
    echo Telechargez-le sur: https://ollama.ai/download
    pause
    exit /b 1
)

echo [1] Verification de Gemma 3...
ollama list | findstr /C:"gemma3" >nul
if %errorlevel% neq 0 (
    echo [DOWNLOAD] Gemma 3 non trouve - Telechargement...
    ollama pull gemma3:latest

    if %errorlevel% neq 0 (
        echo ERROR: Erreur lors du telechargement de Gemma 3
        pause
        exit /b 1
    )
)

echo [OK] Gemma 3 trouve
echo.
echo [2] Demarrage du serveur Ollama...
echo      URL: http://localhost:11434
echo      Modele: Gemma 3
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

ollama serve
pause
