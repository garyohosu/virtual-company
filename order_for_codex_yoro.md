# Order for Codex CLI - Yoro Mode

## 🎯 このファイルについて

このファイルは **Codex CLI の自動実行指示書** です。

```
ユーザー: codex --yoro
   ↓
Codex: このファイルを GitHub から自動読込
   ↓
Codex: 以下の指示に従って実行
   ↓
完了後: Claude AI が次の指示をここに記述
```

---

## 📋 現在の指示

### Status: Ready for first task

**待機中**: ユーザーの最初の指示待ち

---

## 🚀 実行パターン（Codex への指示）

Codex CLI が起動されたら、以下を実行してください：

### Step 1: このファイルを読む

```bash
# GitHub raw URL から読み込む
curl -s https://raw.githubusercontent.com/garyohosu/virtual-company/main/order_for_codex_yoro.md
```

### Step 2: 「現在の指示」セクションを実行

このファイルの「現在の指示」に書かれたタスクを実行してください。

### Step 3: 完了後

```bash
git push origin main
# （Claude AI が次の指示をここに書く）
```

---

## ⚙️ Codex への起動指示

次回 Codex を起動するとき、以下の指示文を使ってください：

```
"order_for_codex_yoro.mdをGitHubから読んで、
その中の『現在の指示』セクションに書かれたタスクを
完全に実行してください。
完了したら git push してください。"
```

---

## 📝 このファイルの管理

- **ユーザー**: `codex --yoro` と言うだけ
- **Codex**: このファイルを読んで実行
- **Claude AI**: GitHub MCP でこのファイルを更新
  - 次のタスク
  - 進捗記録
  - 結果確認

---

## 🔄 サイクル

```
1️⃣ ユーザー: codex --yoro
   ↓
2️⃣ Codex: GitHub から order_for_codex_yoro.md を読む
   ↓
3️⃣ Codex: 「現在の指示」を実行
   ↓
4️⃣ Codex: 完了 → git push
   ↓
5️⃣ Claude AI: GitHub で order_for_codex_yoro.md を更新
   （次のタスクをここに記述）
   ↓
6️⃣ （繰り返し）
```

---

**Last Updated**: 2025-01-30  
**Status**: Ready for Yoro mode  
**Version**: 1.0
