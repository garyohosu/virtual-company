# 📂 instructions フォルダについて

**場所**: https://github.com/garyohosu/virtual-company/tree/main/instructions

**目的**: **すべての自動実行スクリプト・指示書の保存場所**

---

## 🎯 このフォルダは何？

```
instructions/
└─ Claude, Gemini, Codex などの AI エージェント
   が自動実行するファイルが保存されているフォルダ

git pull するだけで
ここのファイルが自動的に実行される！
```

---

## 📋 このフォルダの中身

### 設定ファイル（エージェントが読むルール）

```
instructions/
├── Agents.md      ← すべてのエージェントが従うルール
├── Claude.md      ← Claude の役割と責務
├── Gemini.md      ← Gemini の役割と責務
└── CLAUDE_MEMORY.md ← Claude の永続記憶
```

### 指示書・スクリプト（実際に実行されるファイル）

```
instructions/
├── SETUP_*.md              ← セットアップ（最初に実行）
├── order_*.sh              ← 標準指示スクリプト
├── order_*.md              ← 指示書（Markdown形式）
├── TEST_*.sh               ← テストスクリプト
├── VERIFY_*.sh             ← 検証スクリプト
├── cleanup_organize_files.sh ← ファイル整理
└── ... その他
```

---

## 🚀 実行フロー

### ステップバイステップ

```
1️⃣ ユーザーが git pull を実行
   └─ cd ~/garyohosu/virtual-company && git pull origin main

2️⃣ CLI ツール（Gemini など）が自動起動
   └─ ~/.bashrc or ~/.zshrc で設定

3️⃣ CLI が instructions/ をスキャン
   └─ 新しい .sh / .md ファイルを検出

4️⃣ CLI が Agents.md のルールを読む
   └─ 何を実行するかを判断

5️⃣ CLI が指示書を実行（上から順に）
   ├─ 1️⃣ order_magicboxai_ui.sh
   ├─ 2️⃣ order_sakura_deploy.sh
   └─ 3️⃣ TEST_magicboxai.md

6️⃣ 完了を記録
   └─ .last_agent_run をアップデート
   └─ Git にコミット & プッシュ
```

---

## 📝 ファイルの種類と実行方法

### タイプ 1: Bash スクリプト（.sh）

**ファイル例**: `instructions/order_magicboxai_ui.sh`

**実行方法**:
```bash
bash instructions/order_magicboxai_ui.sh
```

**内容**:
```bash
#!/bin/bash
# MagicBoxAI の UI を更新する

echo "🎯 何をするのか明確に記述"

# Step 1
echo "Step 1️⃣: xxx"
cd ~/garyohosu/magic-box-ai
# ... 処理 ...

# Step 2
echo "Step 2️⃣: yyy"
# ... 処理 ...

echo "✅ 完了"
```

### タイプ 2: Markdown（.md）

**ファイル例**: `instructions/SETUP_phase3.md`

**実行方法**:
```bash
cat instructions/SETUP_phase3.md
# または
gemini --yolo instructions/SETUP_phase3.md
```

**内容**:
```markdown
# セットアップ Phase 3

## 概要
このドキュメントはセットアップの手順を記述しています。

## ステップ
1. xxx を実行
2. yyy を実行
3. zzz を確認
```

---

## 🔄 完全な実行例

### シナリオ: Claude が新しい指示書を作成

```
① Claude が GitHub に新しいファイルを作成
   └─ github:create_or_update_file で
   └─ path: "instructions/order_new_feature.sh"
   └─ owner: "garyohosu"
   └─ repo: "virtual-company"

② 新しいファイル:
   └─ https://github.com/garyohosu/virtual-company/blob/main/instructions/order_new_feature.sh

③ ユーザーが実行
   └─ cd ~/garyohosu/virtual-company
   └─ git pull origin main
   └─ ✨ Gemini が自動実行 ✨

④ Gemini が実行
   └─ bash instructions/order_new_feature.sh
   └─ stdout に出力
   └─ 完了を記録

⑤ 自動コミット & プッシュ
   └─ git commit -m "chore: Update agent timestamp"
   └─ git push origin main
```

---

## 📂 フォルダの階層

```
garyohosu/virtual-company/（GitHub リポジトリ）
│
├── instructions/               ← 👈 この フォルダ
│   ├── 🔴 設定ファイル
│   │   ├── Agents.md           ← ルール定義
│   │   ├── Claude.md           ← Claude の役割
│   │   ├── Gemini.md           ← Gemini の役割
│   │   └── CLAUDE_MEMORY.md    ← 永続記憶
│   │
│   ├── 🟢 実行ファイル（最優先）
│   │   ├── SETUP_phase1.sh
│   │   ├── SETUP_phase2.sh
│   │   └── MAGICBOXAI_FINAL_SETUP.md
│   │
│   ├── 🟡 実行ファイル（次）
│   │   ├── order_magicboxai_ui.sh
│   │   ├── order_sakura_deploy.sh
│   │   ├── order_github_secrets.md
│   │   └── ... その他 order_*.* ファイル
│   │
│   ├── 🔵 テストファイル
│   │   ├── TEST_magicboxai_local.sh
│   │   ├── VERIFY_magicboxai_chrome.sh
│   │   └── TEST_ci_cd.sh
│   │
│   └── 🟣 その他ユーティリティ
│       ├── cleanup_organize_files.sh
│       └── ... その他
│
├── Employees/
├── results/
├── scripts/
└── ... その他ディレクトリ
```

---

## ✅ instructions フォルダが何かを理解するチェックリスト

```
□ このフォルダにはすべての自動実行ファイルが入っている
□ git pull で新ファイルが追加される
□ CLI ツール（Gemini など）がここをスキャンする
□ .sh ファイルは bash で自動実行される
□ .md ファイルは読まれる or 解析される
□ Agents.md / Claude.md / Gemini.md が規則を定める
□ CLAUDE_MEMORY.md は参照用（実行しない）
□ _*.md / _*.sh は下書き（実行しない）
□ ファイルが実行される順序は Agents.md に記載
```

---

## 🎯 重要なポイント

### ❌ よくある誤解

```
❌ 「instructions フォルダは何か」わからない
❌ 「どのファイルが実行されるのか」わからない
❌ 「このファイルが何をするのか」わからない
```

### ✅ 正しい理解

```
✅ instructions/ = 自動実行ファイルが保存されるフォルダ
✅ git pull するだけで自動実行される
✅ Agents.md に実行順序が記載されている
✅ 各ファイルの先頭に「何をするのか」が書いてある
```

---

## 📝 指示書を作成する時のルール

### ✅ 必ず従うこと

```
1️⃣ ファイルを作成する場所
   └─ garyohosu/virtual-company/instructions/
   └─ 他の場所には作成しない

2️⃣ ファイル名の命名
   ├─ SETUP_xxx.sh        (セットアップ)
   ├─ order_xxx.sh        (標準指示)
   ├─ order_xxx.md        (指示書)
   ├─ TEST_xxx.sh         (テスト)
   └─ VERIFY_xxx.sh       (検証)

3️⃣ ファイルの先頭に説明を書く
   ├─ 何をするのか明確に
   ├─ なぜやるのか
   └─ 期待される結果

4️⃣ ステップごとに分割
   └─ 各ステップで echo で進捗を表示

5️⃣ 完了を明示
   └─ 最後に ✅ 完了 と表示
```

---

## 🔗 参照すべきファイル

| ファイル | 目的 | リンク |
|---------|------|--------|
| **Agents.md** | すべてのエージェントの統一ルール | [→](https://github.com/garyohosu/virtual-company/blob/main/instructions/Agents.md) |
| **Claude.md** | Claude の役割と責務 | [→](https://github.com/garyohosu/virtual-company/blob/main/instructions/Claude.md) |
| **Gemini.md** | Gemini の役割と責務 | [→](https://github.com/garyohosu/virtual-company/blob/main/instructions/Gemini.md) |
| **CLAUDE_MEMORY.md** | Claude の永続記憶 | [→](https://github.com/garyohosu/virtual-company/blob/main/instructions/CLAUDE_MEMORY.md) |

---

## 🚀 次のステップ

### 1️⃣ このファイルの役割を理解する
```
このファイル（README_instructions.md）
= instructions フォルダの説明書
= 何が実行されるのかを理解するためのドキュメント
```

### 2️⃣ Agents.md を読む
```
git pull 時に何が実行されるのかのルール
```

### 3️⃣ 各エージェントのファイルを読む
```
Claude.md / Gemini.md で、
自分が何をするべきかを確認
```

### 4️⃣ 実際に git pull で試す
```
cd ~/garyohosu/virtual-company
git pull origin main
# 自動実行が始まる！
```

---

**このフォルダ（instructions/）が Virtual Company の心臓です！** 🫀✨

```
ここに指示書が保存される
  ↓
git pull で取得される
  ↓
AI エージェントが自動実行
  ↓
すべてが自動化される！
```
