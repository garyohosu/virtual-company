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

### Task 001: Yoro Mode 動作確認テスト

**目的**: Yoro Mode が正しく動作しているか確認

**実行内容**:

1. このファイル（order_for_codex_yoro.md）が GitHub から正しく読み込まれたか確認
2. テストディレクトリを作成
   ```bash
   mkdir -p yoro_test
   ```
3. テストファイルを作成（yoro_test/test_001.md）
   ```markdown
   # Yoro Mode Test - Task 001

   **Status**: ✅ SUCCESS

   Codex successfully read instructions from GitHub:
   - File: order_for_codex_yoro.md
   - Source: https://raw.githubusercontent.com/garyohosu/virtual-company/main/order_for_codex_yoro.md
   - Date: $(date)

   **Next**: Claude AI will update order_for_codex_yoro.md with Task 002
   ```

4. Git に追加・コミット・プッシュ
   ```bash
   git add yoro_test/test_001.md
   git commit -m "test: Yoro Mode Task 001 - GitHub read test completed"
   git push origin main
   ```

5. 完了報告（ターミナルで表示）
   ```
   ✅ Task 001 Complete
   - File created: yoro_test/test_001.md
   - Pushed to GitHub: ✅
   - Ready for Task 002
   ```

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
order_for_codex_yoro.md をGitHub
https://raw.githubusercontent.com/garyohosu/virtual-company/main/order_for_codex_yoro.md
から読んでください。

そして「現在の指示」セクションに書かれたタスクを
完全に実行してください。

完了したら git push してください。

すべて bash で実行してください。
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
3️⃣ Codex: 「現在の指示」セクション（Task 001）を実行
   ↓
4️⃣ Codex: yoro_test/test_001.md を作成
   ↓
5️⃣ Codex: git push
   ↓
6️⃣ Claude AI: GitHub で order_for_codex_yoro.md を更新
   （Task 002 を記述）
   ↓
7️⃣ （繰り返し）
```

---

## 📊 進捗

| Task | Status | Details |
|------|--------|---------|
| 001 | ⏳ Pending | GitHub read test |
| 002 | ⏳ Pending | TBD by Claude AI |
| 003+ | ⏳ Pending | TBD by Claude AI |

---

**Last Updated**: 2025-01-30  
**Status**: Ready for Task 001  
**Version**: 1.0
