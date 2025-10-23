@echo off
TITLE Sistema de Gestion NC Motors

echo ==============================================
echo     INICIANDO SISTEMA DE GESTION NC MOTORS
echo ==============================================
echo.

REM --- PASO 1: Activar el entorno virtual ---
REM Le decimos que suba un nivel (..) para encontrar 'virtual'
echo Activando entorno virtual...
CALL ..\virtual\Scripts\activate.bat

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ===================== ERROR =======================
    echo No se pudo encontrar el entorno virtual en '..\virtual'.
    echo.
    echo 1. Asegurate de que la carpeta 'virtual' este
    echo    un nivel ARRIBA de esta carpeta.
    echo ===================================================
    echo.
    pause
    exit /b
)
echo Entorno virtual activado.
echo.

REM --- PASO 2: Verificar que Python funciona ---
echo Verificando Python del entorno...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ===================== ERROR =======================
    echo El comando 'python' no funciona.
    echo Asegurate de que Python este instalado
    echo y de que el entorno virtual no este corrupto.
    echo ===================================================
    echo.
    pause
    exit /b
)
echo Python OK.
echo.

REM --- PASO 3: Iniciar el navegador ---
echo Abriendo el navegador en http://127.0.0.1:8000/login/
start http://127.0.0.1:8000/login/
echo.

REM --- PASO 4: Iniciar el servidor de Django ---
REM Este comando funcionara porque 'manage.py' SI esta en esta carpeta
echo Servidor en marcha en http://127.0.0.1:8000/
echo.
echo PUEDES CERRAR ESTA VENTANA PARA DETENER EL SISTEMA.
echo.

python manage.py runserver --noreload 127.0.0.1:8000

echo.
echo ===================================================
echo Servidor detenido o no pudo iniciar.
echo (Revisa si hay algun error aqui arriba)
echo ===================================================
echo.
pause

