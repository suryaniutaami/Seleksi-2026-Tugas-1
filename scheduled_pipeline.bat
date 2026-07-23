@echo off
setlocal

@REM Untuk Automated Schedulling.
@REM Sebelum menjalankan file ini,
@REM 1. Lakukan Initial Setup Database (jalankan "Data Storing/src/exercise.sql")
@REM 2. Setting config pipeline.cnf 

set "DB_CONFIG=%USERPROFILE%\.mariadb\pipeline.cnf"
if not exist "%DB_CONFIG%" (
    echo [ERROR] File konfigurasi pipeline.cnf tidak ditemukan: %DB_CONFIG%
    echo Salin config\pipeline.cnf.example ke: %USERPROFILE%\.mariadb\pipeline.cnf
    exit /b 1
)
set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
    echo [ERROR] Python virtual environment tidak ditemukan: %PYTHON%
    exit /b 1
)

for /f "delims=" %%i in ('powershell.exe -NoProfile -Command "[DateTime]::Now.ToString(\"yyyyMMdd_HHmmss\")"') do set "BATCH_ID=%%i"
if not defined BATCH_ID (
    echo [ERROR] Gagal membuat Batch ID.
    goto :error
)

echo === SCHEDULED UPDATE ===
echo Batch ID: %BATCH_ID%

cd /d "%~dp0Data Scraping"
if errorlevel 1 goto :error
"%PYTHON%" -m src.scraper.main
if errorlevel 1 goto :error

"%PYTHON%" -m src.transform.main
if errorlevel 1 goto :error

cd /d "%~dp0Data Storing"
if errorlevel 1 goto :error
"%PYTHON%" -m src.seeder.main
if errorlevel 1 goto :error

@REM UPDATE DATABASE exercise

cd /d "%~dp0Data Storing\src"
if errorlevel 1 goto :error
mariadb --defaults-extra-file="%DB_CONFIG%" exercise < "seed\seed.sql"
if errorlevel 1 goto :error

@REM ARSIP hasil ekstraksi 

set "RAW_DIR=%~dp0Data Scraping\data\raw"
set "ARCHIVE_DIR=%RAW_DIR%\history\%BATCH_ID%"
if not exist "%ARCHIVE_DIR%" (
    mkdir "%ARCHIVE_DIR%"
    if errorlevel 1 goto :error
)
copy "%RAW_DIR%\target_areas.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error
copy "%RAW_DIR%\filters.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error
copy "%RAW_DIR%\listings.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error
copy "%RAW_DIR%\workouts.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error
copy "%RAW_DIR%\programs.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error
copy "%RAW_DIR%\program_workouts.json" "%ARCHIVE_DIR%\" >nul
if errorlevel 1 goto :error

echo.
echo === SCHEDULED UPDATE BERHASIL ===
echo Batch ID: %BATCH_ID%
echo Arsip: %ARCHIVE_DIR%

exit /b 0

:error
echo.
echo === [ERROR] SCHEDULED UPDATE GAGAL ===
echo Batch ID: %BATCH_ID%

exit /b 1