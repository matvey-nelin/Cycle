<#
.SYNOPSIS
    Автоматическая настройка окружения и сборка Android (APK/AAB) для Flet.
.NOTES
    Сохраняйте файл в кодировке UTF-8 (без BOM) во избежание ошибок парсинга PowerShell.
#>

param(
    [string]$SdkDir = "C:\Android\Sdk",
    [string]$JavaDir = "C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot",
    [ValidateSet("apk", "aab")]
    [string]$BuildType = "apk"
)

$env:SERIOUS_PYTHON_USE_SYSTEM_PYTHON = "1"

$ErrorActionPreference = "Stop"
Write-Host "Configuring Android build environment ($BuildType)..." -ForegroundColor Cyan

# 1. Проверка путей
if (-not (Test-Path $SdkDir)) {
    throw "Android SDK not found: $SdkDir. Specify path: .\build_android.ps1 -SdkDir 'C:\your\path'"
}
if (-not (Test-Path $JavaDir)) {
    throw "Java JDK not found: $JavaDir. Install JDK 17 and specify path."
}

# 2. Установка переменных окружения (только для текущей сессии)
$env:ANDROID_HOME = $SdkDir
$env:JAVA_HOME = $JavaDir
$env:Path = "$JavaDir\bin;$SdkDir\platform-tools;$SdkDir\cmdline-tools\latest\bin;$env:Path"

Write-Host "JAVA_HOME = $env:JAVA_HOME" -ForegroundColor Green
Write-Host "ANDROID_HOME = $env:ANDROID_HOME" -ForegroundColor Green

# 3. Безопасная проверка версии Java (java -version пишет в stderr)
$oldPref = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$javaVerOutput = (java -version 2>&1 | Out-String).Trim()
$ErrorActionPreference = $oldPref

if ($javaVerOutput -match '"(\d+)\.') {
    $majorVer = $matches[1]
    if ($majorVer -ne "17") {
        Write-Warning "Java version detected: $javaVerOutput. JDK 17 is required for stable builds."
    } else {
        Write-Host "Java version OK: $javaVerOutput" -ForegroundColor Green
    }
} else {
    Write-Host "Java detected (manual version check recommended)" -ForegroundColor Yellow
}

# 4. Принятие лицензий Android SDK
Write-Host "Checking Android SDK licenses..." -ForegroundColor Yellow
$licCmd = "$SdkDir\cmdline-tools\latest\bin\sdkmanager.bat --licenses"
if (Test-Path $licCmd) {
    # Автоматически отвечаем 'y' на все лицензии
    echo y | & $licCmd 2>&1 | Out-Null
    Write-Host "Licenses processed." -ForegroundColor Green
} else {
    Write-Warning "sdkmanager.bat not found. Install 'Android SDK Command-line Tools (latest)' via SDK Manager."
}

# 5. Очистка артефактов
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build, dist, .flet, __pycache__ -ErrorAction SilentlyContinue
Write-Host "Cleaned." -ForegroundColor Green

# 6. Запуск сборки Flet
Write-Host "Starting flet build $BuildType --verbose..." -ForegroundColor Cyan
flet build $BuildType --verbose
$exitCode = $LASTEXITCODE

# 7. Итог
if ($exitCode -eq 0) {
    Write-Host "`nBuild successful!" -ForegroundColor Green
    $outDir = if ($BuildType -eq "aab") {
        "build\flutter\build\app\outputs\bundle\release"
    } else {
        "build\flutter\build\app\outputs\flutter-apk"
    }
    if (Test-Path $outDir) {
        $file = Get-ChildItem $outDir -Filter "app-release.*" | Select-Object -First 1
        if ($file) { Write-Host "Output file: $($file.FullName)" -ForegroundColor Cyan }
    }
} else {
    Write-Host "`nBuild failed (code: $exitCode)" -ForegroundColor Red
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host " - Ensure JDK 17 is installed and JAVA_HOME is correct"
    Write-Host " - Install Android SDK Platform 34 & Build-Tools 34.0.0 via SDK Manager"
    Write-Host " - Install 'Android SDK Command-line Tools (latest)' in SDK Manager"
    Write-Host " - Do not write to assets/ at runtime; use app data dir"
    exit 1
}