param (
    [string]$InstructionsFile
)

$RepoRoot = Resolve-Path "$PSScriptRoot\.."
$ResultsDir = Join-Path $RepoRoot "results\gemini"
$LogFile = Join-Path $ResultsDir "execution_log.json"

if (-not $InstructionsFile) {
    Write-Host "Usage: .\scripts\gemini_wrapper.ps1 <instructions_file.md>"
    exit 1
}

if (-not (Test-Path $InstructionsFile)) {
    Write-Host "ERROR: File not found: $InstructionsFile"
    exit 1
}

if (-not (Test-Path $ResultsDir)) {
    New-Item -ItemType Directory -Path $ResultsDir -Force
}

$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$BaseName = [System.IO.Path]::GetFileNameWithoutExtension($InstructionsFile)
$OutputFile = Join-Path $ResultsDir "$($Timestamp)_$($BaseName).md"
$TempStdout = Join-Path $env:TEMP "gemini_stdout_$($PID).txt"
$TempStderr = Join-Path $env:TEMP "gemini_stderr_$($PID).txt"

Write-Host "========================================="
Write-Host "Gemini CLI Wrapper (PowerShell)"
Write-Host "========================================="
Write-Host "Time: $(Get-Date)"
Write-Host "Instruction: $InstructionsFile"
Write-Host "Output: $OutputFile"
Write-Host "========================================="
Write-Host ""

$StartTime = Get-Date
$ExitCode = 0

Write-Host "Executing instruction..."
$FullInstrPath = (Resolve-Path $InstructionsFile).Path
gemini --yolo "$FullInstrPath" > "$TempStdout" 2> "$TempStderr"
$ExitCode = $LASTEXITCODE

$Status = "FAILED"
if ($ExitCode -eq 0) {
    $Status = "SUCCESS"
}

$EndTime = Get-Date
$Duration = [int]($EndTime - $StartTime).TotalSeconds

$StdoutContent = ""
if (Test-Path $TempStdout) { $StdoutContent = Get-Content $TempStdout -Raw }
$StderrContent = ""
if (Test-Path $TempStderr) { $StderrContent = Get-Content $TempStderr -Raw }
$InstrContent = Get-Content $FullInstrPath -Raw

$NextAction = "Check results."
if ($ExitCode -eq 0) {
    $NextAction = "Execution successful. Verify changes and commit."
} else {
    $NextAction = "Execution failed. Check error output."
}

$Report = "
# Gemini CLI Execution Result

## Execution Information

| Item | Content |
|------|------|
| **Status** | $Status |
| **Time** | $(Get-Date) |
| **Instruction** | $InstructionsFile |
| **Duration** | ${Duration}s |
| **Exit Code** | $ExitCode |

---

## Instruction Content

$InstrContent

---

## stdout

$StdoutContent

---

## stderr

$StderrContent

---

## Next Action

$NextAction

---

Generated: $(Get-Date)
"

$Report | Set-Content -Path $OutputFile -Encoding UTF8

if (Test-Path "$RepoRoot\scripts\log_result.py") {
    python "$RepoRoot\scripts\log_result.py" "$RepoRoot" "$InstructionsFile" "$OutputFile" "$Status" "$ExitCode" "$Duration"
}

if ($ExitCode -eq 0) {
    Write-Host "Committing result to Git..."
    git add "$OutputFile" "$LogFile"
    git commit -m "chore: Add Gemini CLI execution result - $([System.IO.Path]::GetFileNameWithoutExtension($OutputFile))"
}

Write-Host ""
Write-Host "========================================="
Write-Host "Finished: $Status"
Write-Host "========================================="
Write-Host "Status: $Status"
Write-Host "Duration: ${Duration}s"
Write-Host "Result file: $OutputFile"
Write-Host "========================================="

if (Test-Path $TempStdout) { Remove-Item $TempStdout -ErrorAction SilentlyContinue }
if (Test-Path $TempStderr) { Remove-Item $TempStderr -ErrorAction SilentlyContinue }

exit $ExitCode