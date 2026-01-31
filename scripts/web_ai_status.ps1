param (
    [string]$RepoDir = (Get-Location).Path
)

Set-Location $RepoDir

Write-Host "# 📊 Virtual Company - 実行状況レポート"
Write-Host ""
Write-Host "**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")"
Write-Host ""

# 実行履歴 (JSON) を読み込む
$LogFile = "results\gemini\execution_log.json"
$Log = @()
if (Test-Path $LogFile) {
    try {
        $Log = Get-Content $LogFile -Raw | ConvertFrom-Json
    } catch {
        $Log = @()
    }
}

if ($Log) {
    $Latest = $Log | Sort-Object timestamp -Descending | Select-Object -First 1
    
    if ($Latest) {
        Write-Host "## ✨ 最新の実行"
        Write-Host ""
        Write-Host "- **ファイル**: ``$($Latest.instructions_file)``"
        Write-Host "- **実行日時**: $($Latest.timestamp)"
        Write-Host "- **ステータス**: $($Latest.status)"
        Write-Host ""
    }
    
    Write-Host "## 📜 最近の実行履歴（直近5件）"
    Write-Host ""
    Write-Host "| 日時 | 指示書 | ステータス |"
    Write-Host "|------|--------|-----------|"
    
    $Recent = $Log | Sort-Object timestamp -Descending | Select-Object -First 5
    foreach ($Entry in $Recent) {
        $ShortFile = [System.IO.Path]::GetFileName($Entry.instructions_file)
        if ($ShortFile.Length -gt 30) { $ShortFile = $ShortFile.Substring(0, 27) + "..." }
        Write-Host "| $($Entry.timestamp.Substring(5, 11)) | ``$ShortFile`` | $($Entry.status) |"
    }
    Write-Host ""
    
    $Stats = @{
        Total = $Log.Count
        Success = ($Log | Where-Object { $_.status -like "*SUCCESS*" }).Count
        Failed = ($Log | Where-Object { $_.status -like "*FAILED*" }).Count
    }
    
    Write-Host "## 📈 統計情報"
    Write-Host ""
    Write-Host "- **総実行数**: $($Stats.Total)"
    Write-Host "- **成功**: $($Stats.Success)"
    Write-Host "- **失敗**: $($Stats.Failed)"
    if ($Stats.Total -gt 0) {
        $Rate = [int]($Stats.Success * 100 / $Stats.Total)
        Write-Host "- **成功率**: $Rate%"
    }
    Write-Host ""
}

Write-Host "## 📋 未実行の指示書"
Write-Host ""

$PendingCount = 0
$PendingFiles = @()
Get-ChildItem instructions -Filter "order_*.md" | ForEach-Object {
    $BaseName = $_.BaseName
    $AlreadyRun = $false
    foreach ($Entry in $Log) {
        if ($Entry.instructions_file -like "*$BaseName*") {
            $AlreadyRun = $true
            break
        }
    }
    if (-not $AlreadyRun) {
        Write-Host "- $($_.Name)"
        $PendingFiles += $_.Name
        $PendingCount++
    }
}

if ($PendingCount -eq 0) {
    Write-Host "✅ すべての指示書が実行済みです"
}

Write-Host ""
Write-Host "## 🎯 次のアクション"
Write-Host ""
Write-Host "### 未実行の指示書を実行してください"
Write-Host ""
Write-Host " \`\`\`powershell"
foreach ($File in $PendingFiles) {
    Write-Host ".\scripts\gemini_wrapper.ps1 instructions\$File"
}
Write-Host " \`\`\` "
