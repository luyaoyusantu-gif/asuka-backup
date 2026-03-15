$ErrorActionPreference = 'Stop'

$backupRoot = 'E:\openclaw_backups'
$sourcePath = 'C:\Users\10798\.openclaw'

# Create root backup directory if it doesn't exist
if (-not (Test-Path $backupRoot)) {
    New-Item -Path $backupRoot -ItemType Directory
}

# Generate timestamp and create timestamped subdirectory
$timestamp = (Get-Date).ToString('yyyy-MM-dd_HHmmss')
$backupPath = Join-Path $backupRoot $timestamp
New-Item -Path $backupPath -ItemType Directory

# Copy OpenClaw data
Copy-Item -Path $sourcePath -Destination $backupPath -Recurse -Force

Write-Host "OpenClaw core data backup completed successfully to $backupPath"
