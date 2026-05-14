# ============================================
# Restore Power Settings Script
# ============================================
# Run this script AFTER training completes to restore original power settings
# Usage: Right-click -> "Run with PowerShell" OR .\restore_power_settings.ps1

Write-Host "============================================"
Write-Host "Restoring Original Power Settings"
Write-Host "============================================"
Write-Host ""

# Restore original settings (from before training)
Write-Host "Restoring settings..."
powercfg /change standby-timeout-ac 60      # Sleep after 60 minutes on AC
powercfg /change hibernate-timeout-ac 90    # Hibernate after 90 minutes on AC  
powercfg /change monitor-timeout-ac 10      # Display off after 10 minutes on AC

Write-Host ""
Write-Host "✅ Power settings restored to defaults:"
Write-Host "   - Sleep after: 60 minutes (AC power)"
Write-Host "   - Hibernate after: 90 minutes (AC power)"
Write-Host "   - Display timeout: 10 minutes (AC power)"
Write-Host ""
Write-Host "Original laptop power behavior restored!"
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
