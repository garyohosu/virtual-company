# skills/ai-execution-options/SKILL.md

**対象**: Virtual Company の全 AI エージェント
**目的**: 各 AI の実行オプションを統一・比較
**更新日**: 2026-01-31

---

## 🎯 AI 別：実行オプション比較表

| AI | タイプ | `--yolo` | 自動承認 | 非対話 | 用途 |
|-----|--------|---------|---------|--------|------|
| **Codex CLI** | CLI | ✅ `--yolo` | ✅ | ✅ `-p` | SSH 直結・短時間 |
| **Gemini CLI** | CLI | ✅ `--yolo` | ✅ `--approval-mode yolo` | ✅ | 中時間・バックアップ |
| **Genspark** | CLI | ❓ 確認中 | ？ | ✅ | 長時間・無制限 |
| **Claude Code** | VS Code 拡張 | ❌ なし | 手動承認 | UI のみ | 短時間・IDE 統合 |
| **ChatGPT** | Web / CLI | 部分的 | API key で自動 | ✅ | バックアップ・並行 |

---

## 💡 正確な実行コマンド

### Codex CLI（最速・最安定）

```bash
# 自動承認モード
codex --yolo order_file.md

# または
cyx order_file.md  # エイリアス
```

**出力**: 結果を即座に表示

---

### Gemini CLI（制限なし）

```bash
# YOLO モード（完全自動）
gemini --yolo order_file.md

# または
gem --yolo order_file.md  # エイリアス
gem -y order_file.md      # 短縮形

# より詳細な制御
gemini --approval-mode yolo order_file.md
```

**出力**: 結果をストリーミング表示

---

### Genspark（要確認）

```bash
# 予想：自動実行オプト
genspark --execute order_file.md
genspark --auto order_file.md
genspark -y order_file.md

# 確認コマンド
genspark --help
```

**確認状況**: ユーザーが検証中

---

### Claude Code（VS Code 拡張）

```
❌ CLI オプションなし
❌ 常に手動対話（UI で承認必要）

代わりに使用可能:
- Codex CLI で自動実行
- Gemini CLI で自動実行
- Genspark で自動実行
```

**用途**: IDE 統合が必要な短時間タスク只用

---

## 🔄 推奨：実行フロー図

```
Order を受け取った
  ↓
推定時間を判定
  ↓
  ├─ 30 分以内 → codex --yolo order.md
  │
  ├─ 30 分～2h → gemini --yolo order.md
  │  （Codex の残り時間が 50% 未満の場合）
  │
  ├─ 2h 以上 → genspark --execute order.md
  │  （確認: genspark -y order.md かも）
  │
  └─ IDE 統合が必要 → Claude Code（UI で手動）
```

---

## 📊 実装状況

| AI | --yolo 実装 | 動作確認 | 備考 |
|----|-----------|---------|------|
| Codex CLI | ✅ | ✅ 確認済み | 本番運用中 |
| Gemini CLI | ✅ | ✅ 確認済み | 次から使用開始 |
| Genspark | ❓ | ⏳ 検証待ち | ユーザー確認中 |
| Claude Code | ❌ | N/A | UI のみ・自動化不可 |
| ChatGPT CLI | ？ | ❓ | 確認予定 |

---

## 🎯 Windows PowerShell 設定（確定版）

```powershell
# $PROFILE に追加

# ========================================
# 確認済み：CLI オプション統一
# ========================================

# Codex CLI
Set-Alias -Name cyx -Value 'codex --yolo'

# Gemini CLI
Set-Alias -Name gym -Value 'gemini --yolo'

# 将来：Genspark
# Set-Alias -Name gspark -Value 'genspark --yolo'  # 確認後追加

# 自動選択関数（改良版）
function Run-Order {
    param(
        [string]$File,
        [string]$AI = "auto"
    )
    
    if (-not (Test-Path $File)) {
        Write-Host "❌ ファイルが見つかりません: $File"
        return
    }
    
    if ($AI -eq "auto") {
        $size = (Get-Item $File).Length
        
        if ($size -gt 100KB) {
            Write-Host "📄 大ファイル（$([math]::Round($size/1KB))KB） → Gemini"
            gemini --yolo $File
        } else {
            Write-Host "📄 小ファイル（$([math]::Round($size/1KB))KB） → Codex"
            codex --yolo $File
        }
    } else {
        & "$AI-yolo" $File
    }
}

Set-Alias -Name run-order -Value Run-Order
```

**使い方**:
```powershell
cyx order_file.md                          # codex --yolo
gym order_file.md                          # gemini --yolo
run-order order_file.md                    # 自動選択
run-order order_file.md -AI gym            # Gemini 指定
```

---

## ✅ 確定事項

```
✅ Codex CLI と Gemini CLI は `--yolo` で統一
✅ 両方とも非対話・完全自動実行可能
✅ Windows PowerShell でエイリアス設定完了
✅ 本番運用可能

❓ Genspark の確認待ち
❌ Claude Code は自動化不可（VS Code 拡張だから）
```

---

## 🚀 次のステップ

1. **Genspark の確認**
   ```bash
   genspark --help | grep -E "yolo|auto|execute"
   ```

2. **Gemini CLI で診断実行**
   ```powershell
   gym order_magicboxai_diagnostic.md
   ```

3. **結果を読んで修正**

---

**Virtual Company の自動化がほぼ完成しました！** ✨
