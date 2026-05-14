# Resume Training Helper Script
# This script helps you resume interrupted training sessions

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🔄 Training Resume Helper" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Check for recent training runs
Write-Host "📁 Searching for recent training runs..." -ForegroundColor Green
Write-Host ""

$trainingRuns = Get-ChildItem "runs\train\" -Directory -ErrorAction SilentlyContinue | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 10

if ($trainingRuns.Count -eq 0) {
    Write-Host "❌ No training runs found in runs\train\" -ForegroundColor Red
    Write-Host ""
    Write-Host "Start a new training session with:" -ForegroundColor Yellow
    Write-Host "  python sds_yolo11\train.py --config <config> --data <data>" -ForegroundColor White
    exit
}

# Display found runs
Write-Host "Found $($trainingRuns.Count) recent training run(s):" -ForegroundColor Green
Write-Host ""

$index = 1
foreach ($run in $trainingRuns) {
    $lastPt = Join-Path $run.FullName "weights\last.pt"
    $hasCheckpoint = Test-Path $lastPt
    
    $status = if ($hasCheckpoint) { "✅ Has checkpoint" } else { "❌ No checkpoint" }
    $color = if ($hasCheckpoint) { "Green" } else { "Red" }
    
    Write-Host "[$index] " -NoNewline -ForegroundColor White
    Write-Host "$($run.Name) " -NoNewline -ForegroundColor Cyan
    Write-Host "- $status" -ForegroundColor $color
    Write-Host "    Last modified: $($run.LastWriteTime)" -ForegroundColor Gray
    
    if ($hasCheckpoint) {
        # Try to read the results.csv to get epoch info
        $resultsFile = Join-Path $run.FullName "results.csv"
        if (Test-Path $resultsFile) {
            $lines = Get-Content $resultsFile
            if ($lines.Count -gt 1) {
                $lastEpoch = $lines.Count - 2  # Subtract header and 0-based indexing
                Write-Host "    Last epoch: $lastEpoch" -ForegroundColor Gray
            }
        }
    }
    Write-Host ""
    $index++
}

# Ask user which run to resume
Write-Host ""
Write-Host "Which training run would you like to resume? (1-$($trainingRuns.Count), or 0 to cancel): " -NoNewline -ForegroundColor Yellow
$selection = Read-Host

if ($selection -eq "0" -or $selection -eq "") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

$selectedIndex = [int]$selection - 1
if ($selectedIndex -lt 0 -or $selectedIndex -ge $trainingRuns.Count) {
    Write-Host "❌ Invalid selection!" -ForegroundColor Red
    exit
}

$selectedRun = $trainingRuns[$selectedIndex]
$checkpointPath = Join-Path $selectedRun.FullName "weights\last.pt"

if (-not (Test-Path $checkpointPath)) {
    Write-Host "❌ No checkpoint found for this run!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "Selected: $($selectedRun.Name)" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Try to detect which training script was used
$argsFile = Join-Path $selectedRun.FullName "args.yaml"
$useTrainPy = $true  # Default

if (Test-Path $argsFile) {
    Write-Host "📄 Found training configuration in args.yaml" -ForegroundColor Green
    Get-Content $argsFile | Select-Object -First 10
    Write-Host ""
}

# Ask which script to use
Write-Host "Which training script should be used?" -ForegroundColor Yellow
Write-Host "  [1] train.py (default)" -ForegroundColor White
Write-Host "  [2] train_with_milestones.py" -ForegroundColor White
Write-Host ""
Write-Host "Select (1 or 2): " -NoNewline -ForegroundColor Yellow
$scriptChoice = Read-Host

$scriptName = if ($scriptChoice -eq "2") { "train_with_milestones.py" } else { "train.py" }

# Build resume command
Write-Host ""
Write-Host "🚀 To resume training, run:" -ForegroundColor Green
Write-Host ""

if ($scriptChoice -eq "2") {
    # For train_with_milestones.py, we need to specify the name
    Write-Host "python sds_yolo11\$scriptName --name $($selectedRun.Name) --resume" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Note: You may need to add other parameters like --config, --data, --epochs, etc." -ForegroundColor Gray
} else {
    # For train.py, it can auto-detect from the last run
    Write-Host "python sds_yolo11\$scriptName --resume" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or with specific parameters:" -ForegroundColor Gray
    Write-Host "python sds_yolo11\$scriptName --config <your_config> --data <your_data> --name $($selectedRun.Name) --resume" -ForegroundColor Gray
}

Write-Host ""
Write-Host "💡 Tip: Run .\sds_yolo11\prevent_sleep.ps1 first to prevent sleep during training" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to resume now
Write-Host "Would you like to resume training now? (y/n): " -NoNewline -ForegroundColor Yellow
$resumeNow = Read-Host

if ($resumeNow -eq "y" -or $resumeNow -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Resuming training..." -ForegroundColor Green
    Write-Host ""
    
    # Check if venv is activated
    if (-not $env:VIRTUAL_ENV) {
        Write-Host "⚠️  Virtual environment not activated. Activating..." -ForegroundColor Yellow
        & "sds_yolo11\venv_cuda\Scripts\Activate.ps1"
    }
    
    # Run the training
    if ($scriptChoice -eq "2") {
        python "sds_yolo11\$scriptName" --name $selectedRun.Name --resume
    } else {
        python "sds_yolo11\$scriptName" --resume
    }
} else {
    Write-Host "You can resume manually when ready." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
