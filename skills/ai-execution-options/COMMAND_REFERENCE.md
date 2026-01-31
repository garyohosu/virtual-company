# skills/ai-execution-options/COMMAND_REFERENCE.md

**対象**: Virtual Company の全 AI エージェント
**目的**: 実際の実行環境に応じたコマンド指示
**更新日**: 2026-01-31

---

## 🎯 ユーザーの実装環境

### 環境構成

```
OS: Windows 11
Shell: PowerShell
AI CLI 設定: エイリアスなし（フルコマンド使用）
Claude Tool: claudeyolo.bat（カスタム Batch ファイル）
```

---

## 🚀 実行コマンド（ユーザー環境）

### Codex CLI

```powershell
codex --yolo order_file.md
```

**用途**: 短時間 Order（30 分以内）

### Gemini CLI

```powershell
gemini --yolo order_file.md
```

**用途**: 中時間 Order（1～3 時間）

### Claude（Batch ファイル経由）

```powershell
claudeyolo.bat order_file.md
```

**用途**: 高品質が必要（複雑な実装）

**内容**: 
```batch
@echo off
claude --dangerously-skip-permissions %1 %2 %3 %4 %5
```

### Genspark

```powershell
genspark --execute order_file.md
```

**用途**: 長時間 Order（3 時間以上）・無制限

---

## 📊 AI 選択フロー

```
Order を受け取った
  ↓
推定実行時間を判定
  ↓
  ├─ 30 分以内 → codex --yolo order.md
  │
  ├─ 30 分～3h → gemini --yolo order.md
  │
  ├─ 3h 以上 → genspark --execute order.md
  │
  └─ 高品質必須 → claudeyolo.bat order.md
```

---

## ✅ 環境設定の確認

### Step 1: claudeyolo.bat の存在確認

```powershell
Test-Path C:\Users\garyo\bin\claudeyolo.bat
```

### Step 2: PATH に追加されているか確認

```powershell
$env:PATH -split ';' | Select-String 'bin'
```

### Step 3: テスト実行

```powershell
claudeyolo.bat --help
```

---

## 🎓 なぜエイリアスを使わないのか

```
理由 1: 環境依存を最小化
- PowerShell のバージョン依存を避ける
- 他の環境（CMD、Git Bash）でも同じコマンドで動作

理由 2: 可読性が高い
- フルコマンドなら何をしているか明確
- Order ファイルを読む人も理解しやすい

理由 3: 保守性が高い
- Batch ファイルなら Windows でも Linux でも対応可能
- エイリアス設定不要（設定ミス防止）
```

---

## 📝 Order ファイルでの推奨記載

```markdown
# Order - [名前]

**推奨実行コマンド**: 
\`\`\`powershell
gemini --yolo order_[name].md
\`\`\`

**代替コマンド**:
- Codex 使用時: `codex --yolo order_[name].md`
- Claude 使用時: `claudeyolo.bat order_[name].md`
```

---

## 🔄 今後の改善（オプション）

```
ユーザーが PowerShell エイリアスを登録したい場合：

$PROFILE に追加：
Set-Alias -Name cyx -Value 'codex --yolo'
Set-Alias -Name gym -Value 'gemini --yolo'
Set-Alias -Name cly -Value 'claudeyolo.bat'

すると以下で実行可能：
cyx order.md
gym order.md
cly order.md
```

---

**環境に応じた柔軟な設定 = Virtual Company の特徴** ✨
