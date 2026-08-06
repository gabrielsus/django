@echo off
echo ==========================================
echo Configurando el entorno de desarrollo...
echo ==========================================

:: 1. (Opcional) Crea un entorno virtual si no existe
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

:: 2. Activa el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

:: 3. Actualiza pip por las dudas
echo Actualizando pip...
python -m pip install --upgrade pip

:: 4. Instala las dependencias
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo ==========================================
echo ¡Listo! Entorno preparado con exito.
echo ==========================================
pause