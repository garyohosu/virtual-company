# 🧠 Claude の永続記憶

**作成日**: 2026-01-31  
**対象**: Claude.ai（Claude Haiku）  
**目的**: 重要な設定情報と制約条件を記録

---

## 🎯 重要な制約・ルール

### ❌ ローカルPC が見えない

```
Claude からは見える：
✅ GitHub リポジトリ（GitHub MCP 経由）
✅ リモートの GitHub ファイル

Claude からは見えない：
❌ ローカルPC のファイル
❌ ローカルPC のディレクトリ構造
❌ Windows エクスプローラー
❌ ユーザーのマシンの状態
```

**覚えておくこと**: 何かローカルPCの情報が必要な場合は、**ユーザーからの報告を待つ**

---

## 📂 リポジトリ構造

### ユーザーのローカル PC

```
~/garyohosu/virtual-company/     ← ユーザーのメインリポジトリ（見えない）
├── instructions/                  ← すべての指示書がここ
│   ├── order_*.md                 （44個以上）
│   ├── CLEANUP_ORDER_FILES.md
│   ├── MAGICBOXAI_FINAL_SETUP.md
│   ├── cleanup_organize_files.sh
│   └── CLAUDE_MEMORY.md           ← この ファイル
├── magicboxai/
├── results/
├── scripts/
└── ... その他
```

### GitHub リポジトリ

```
garyohosu/virtual-company (GitHub)
└── instructions/
    ├── すべての指示書
    └── CLAUDE_MEMORY.md ← これを常に参照

garyohosu/magic-box-ai (GitHub)
├── src/                 (PHP ソース)
├── tests/               (テスト)
├── .github/workflows/   (CI/CD)
└── ... その他
```

---

## 📝 指示書作成ルール

### ✅ 必ず従うこと

```
1. すべての新しい指示書は以下に作成：
   https://github.com/garyohosu/virtual-company/tree/main/instructions

2. GitHub MCP を使用して作成：
   github:create_or_update_file で
   path: "instructions/FILENAME.md"
   owner: "garyohosu"
   repo: "virtual-company"

3. 指示書の形式：
   - Bash スクリプト実行形式が望ましい
   - または Markdown ドキュメント形式
   - Gemini CLI で実行できるようにする

4. 指示書の先頭に以下を含める：
   - 実行方法: gemini --yolo instructions/FILENAME.md
   - 対象: (どのリポジトリか、どのディレクトリか)
   - 内容: (何をするのか)
```

---

## 🚀 現在のワークフロー

```
① Claude が GitHub に指示書を作成
   ↓
② ユーザーが git pull でローカルに取得
   ↓
③ ユーザーが gemini --yolo instructions/FILENAME.md で実行
   ↓
④ Gemini CLI が指示書を読んで実行
   ↓
⑤ ユーザーが結果をメッセージで報告
   ↓
⑥ Claude が次の指示書を作成
```

---

## 📋 完了済みタスク

```
✅ Step 1: Python コード削除（virtual-company）
✅ Step 2-2: PHP コード同期（magic-box-ai に配置）
✅ Step 3: テスト戦略実装（PHPUnit + pytest）
✅ Step 4: CI/CD ワークフロー設定（GitHub Actions）
✅ Step X: order*.md ファイル整理（instructions/ に集約）
✅ ✅ ✅ すべての指示書は instructions/ に配置完了
```

---

## 🔄 次のステップ

```
① GitHub Secrets 設定（手動）
   - SAKURA_HOST
   - SAKURA_USER
   - SAKURA_KEY

② ローカルテスト（オプション）
   - composer install
   - phpunit
   - pytest

③ 次の開発フェーズ開始
```

---

## 🛠️ トラブルシューティング

### Q: 「どこに指示書を作成するのか忘れた」

**A**: このファイル（CLAUDE_MEMORY.md）を読む

```bash
curl https://raw.githubusercontent.com/garyohosu/virtual-company/main/instructions/CLAUDE_MEMORY.md
```

---

### Q: 「ローカルPCの状態がわからない」

**A**: ユーザーに確認する

```
「ローカルPC の ~/garyohosu/virtual-company の current status を教えてください」
```

---

### Q: 「指示書をどこに作成するのか」

**A**: 常にここ

```
https://github.com/garyohosu/virtual-company/tree/main/instructions/
```

---

## 📞 重要な連絡先

```
GitHub MCP 接続先：
- Owner: garyohosu
- Repos: virtual-company, magic-box-ai
- Main branch: main

Gemini 実行方法：
- gemini --yolo instructions/FILENAME.md
```

---

## ⚠️ 注意事項

```
❌ やってはいけないこと：
   - ローカルPC のファイルを直接操作しようとする
   - GitHub 外の場所に指示書を作成する
   - 指示書を garyohosu/magic-box-ai に作成する

✅ やるべきこと：
   - すべての指示書を garyohosu/virtual-company/instructions/ に作成
   - GitHub MCP で GitHub リポジトリだけを操作
   - ユーザーからの報告を待つ
   - 不明な場合はこのファイルを参照
```

---

## 🔄 更新履歴

| 日付 | 更新内容 |
|-----|--------|
| 2026-01-31 | Claude の永続記憶ファイル作成 |

---

**このファイルを常に参照してください！** 🧠✨
