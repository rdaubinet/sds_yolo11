# Prevent Windows sleep during training
# Run this script before starting long training runs

Write-Host "Configuring power settings for training..." -ForegroundColor Green

# Get current power scheme
$currentScheme = powercfg /getactivescheme
Write-Host "Current power scheme: $currentScheme" -ForegroundColor Yellow

# Disable sleep and hibernation temporarily
Write-Host "`nDisabling sleep and hibernation..." -ForegroundColor Green
powercfg /change monitor-timeout-ac 0
powercfg /change standby-timeout-ac 0
powercfg /change disk-timeout-ac 0
powercfg /change hibernate-timeout-ac 0

Write-Host "`n✅ Power settings configured for training:" -ForegroundColor Green
Write-Host "  - Monitor timeout: Disabled" -ForegroundColor Cyan
Write-Host "  - Sleep timeout: Disabled" -ForegroundColor Cyan
Write-Host "  - Disk timeout: Disabled" -ForegroundColor Cyan
Write-Host "  - Hibernation: Disabled" -ForegroundColor Cyan

Write-Host "`n⚠️  Remember to run 'restore_power_settings.ps1' after training!" -ForegroundColor Yellow
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
