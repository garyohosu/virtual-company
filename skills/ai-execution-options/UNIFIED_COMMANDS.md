# skills/ai-execution-options/UNIFIED_COMMANDS.md

**対象**: Virtual Company の全 AI エージェント
**目的**: すべての CLI を統一コマンドで実行
**更新日**: 2026-01-31

---

## 🎯 問題：オプション名がバラバラ

```
Codex CLI:    --yolo
Gemini CLI:   --yolo
Claude CLI:   --dangerously-skip-permissions
Codex Code:   ??? 
ChatGPT CLI:  ???

→ 覚えられない！
```

---

## ✅ 解決：Windows PowerShell で統一エイリアス

```powershell
# $PROFILE に追加

# ========================================
# 統一エイリアス：すべての CLI を --yolo で実行
# ========================================

# Codex CLI
Set-Alias -Name cyx -Value 'codex --yolo'

# Gemini CLI  
Set-Alias -Name gym -Value 'gemini --yolo'

# Claude CLI（長いので関数でラップ）
function claude-yolo {
    claude --dangerously-skip-permissions @args
}
Set-Alias -Name cly -Value claude-yolo

# Genspark（確認後追加）
# Set-Alias -Name gspark -Value 'genspark --yolo'

# ========================================
# 統一実行関数
# ========================================

function Run-Order {
    param(
        [string]$File,
        [string]$AI = "auto"
    )
    
    if (-not (Test-Path $File)) {
        Write-Host "❌ ファイルが見つかりません: $File"
        return
    }
    
    switch ($AI) {
        "codex"  { 
            Write-Host "✅ Codex で実行"
            cyx $File
            break 
        }
        "gemini" { 
            Write-Host "✅ Gemini で実行"
            gym $File
            break 
        }
        "claude" { 
            Write-Host "✅ Claude で実行"
            cly $File
            break 
        }
        "auto"   {
            $size = (Get-Item $File).Length
            $sizeMB = [math]::Round($size / 1MB, 2)
            
            if ($size -gt 100KB) {
                Write-Host "📄 ファイルサイズ: $sizeMB MB → Gemini で実行"
                gym $File
            } else {
                Write-Host "📄 ファイルサイズ: $sizeMB MB → Codex で実行"
                cyx $File
            }
            break
        }
        default {
            Write-Host "❌ 不明な AI: $AI"
            Write-Host "使い方: run-order order.md [codex|gemini|claude|auto]"
        }
    }
}

Set-Alias -Name run-order -Value Run-Order
```

---

## 🚀 使い方

```powershell
# Codex で実行（短時間）
cyx order_short.md

# Gemini で実行（中時間）
gym order_medium.md

# Claude で実行（高品質）
cly order_complex.md

# 自動選択
run-order order.md

# 指定 AI で実行
run-order order.md -AI claude
run-order order.md -AI gemini
run-order order.md -AI codex
```

---

## 📊 統一後のコマンド表

| 用途 | 実行コマンド | 実際のコマンド | 制限 |
|------|-----------|-------------|------|
| Codex 直接 | `cyx order.md` | `codex --yolo order.md` | 5h |
| Gemini 直接 | `gym order.md` | `gemini --yolo order.md` | 無制限 |
| Claude 直接 | `cly order.md` | `claude --dangerously-skip-permissions order.md` | 無制限 |
| 自動選択 | `run-order order.md` | ファイルサイズで判定 | - |
| 指定実行 | `run-order order.md -AI claude` | Claude で実行 | - |

---

## 💡 PowerShell プロファイルの場所

```
Windows (PowerShell 5):
C:\Users\[ユーザー名]\Documents\WindowsPowerShell\profile.ps1

Windows (PowerShell 7):
C:\Users\[ユーザー名]\Documents\PowerShell\profile.ps1

Mac/Linux:
~/.config/powershell/profile.ps1
```

**開き方**:
```powershell
notepad $PROFILE
```

---

## ✅ セットアップ手順

1. **PowerShell プロファイルを開く**
   ```powershell
   notepad $PROFILE
   ```

2. **上記のコードを追加**

3. **保存して PowerShell を再起動**

4. **テスト**
   ```powershell
   cyx --help
   gym --help
   cly --help
   run-order --help
   ```

---

## 🎓 設計思想

```
複数 CLI の統一：
- すべてを同じインターフェースで操作
- ユーザーは「AI を選ぶ」だけ
- 細かいオプションは隠蔽
- 自動選択機能で完全自動化

効果：
✅ 覚えやすい
✅ 使いやすい
✅ 自動化可能
✅ エラーが少ない
```

---

**これで、すべての AI CLI が「同じコマンド」で実行できます！** ✨
