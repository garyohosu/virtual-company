# Yoro Mode - 最小構成自動化システム

## 🎯 何これ？

ユーザーが **一言言うだけで** 自動実行が続く仕組みです。

```
あなた: codex --yoro
   ↓
Codex: GitHub から指示を読む
   ↓
Codex: 実行
   ↓
私: GitHub で次の指示を書く
   ↓
（繰り返し）
```

**あなたの役割**: 「codex --yoro」と言うだけ

---

## 📖 使い方（3ステップ）

### Step 1: Codex CLI を起動（これだけ）

```bash
codex --yoro
```

### Step 2: Codex への指示文（コピペしてください）

Codex CLI のプロンプトで以下をコピペ：

```
order_for_codex_yoro.md という指示書を
GitHub https://raw.githubusercontent.com/garyohosu/virtual-company/main/order_for_codex_yoro.md
から読んでください。

そして「現在の指示」セクションに書かれたタスクを
完全に実行してください。

完了したら git push してください。
```

### Step 3: 完了

Codex が自動的に：
1. GitHub から指示を読む
2. 実行
3. git push

その後、私が `order_for_codex_yoro.md` を更新して、次のタスクを記述します。

---

## 🔄 サイクル例

### 初回

```
あなた: codex --yoro
Codex: order_for_codex_yoro.md を読む
Codex: 「Status: Ready for first task」を確認
Codex: 「ユーザーからの指示待ち」と報告
Codex: git push
```

### 次のサイクル（私が指示を書いた後）

```
あなた: codex --yoro
Codex: order_for_codex_yoro.md を読む
Codex: 「現在の指示: テストして」を実行
Codex: 完了報告
Codex: git push

（私が GitHub で次の指示を記述）
```

---

## 📂 ファイル構成

```
GitHub
├── order_for_codex_yoro.md ← Codex がこれを読む
│   ├─ 現在の指示（Codex がこれを実行）
│   └─ 進捗記録（完了後、私が更新）
```

---

## 🎯 フロー図

```
┌─────────────────────────────────────┐
│      あなたのマシン                  │
│                                     │
│  $ codex --yoro                     │
│         ↓                           │
│  Codex CLI 起動                     │
│         ↓                           │
│  「order_for_codex_yoro.mdを       │
│    GitHub から読め」                │
└────────────┬────────────────────────┘
             │ 読み込み
             ↓
    ┌────────────────────┐
    │     GitHub         │
    │                    │
    │ order_for_codex    │
    │ _yoro.md           │
    │                    │
    │ 【現在の指示】      │
    │ テストして         │
    └────────────────────┘
             ↑ 更新
             │
    ┌────────────────────┐
    │  Claude AI (私)    │
    │                    │
    │  GitHub MCP で    │
    │  ファイル更新      │
    │  次の指示を記述    │
    └────────────────────┘
```

---

## 💾 実装の流れ

### 今（v1.0）

- ✅ GitHub に `order_for_codex_yoro.md` がある
- ✅ Codex が読める仕様になっている
- ⏳ 私が GitHub で指示を更新する機能（実装予定）

### 次（v1.1）

- 自動で `order_for_codex_yoro.md` に指示を書き込む
- Codex の完了報告を自動解析
- 次のタスクを自動生成

---

## 🚀 最初の指示（テスト用）

`order_for_codex_yoro.md` の現在の指示：

```markdown
## 📋 現在の指示

### Status: Ready for first task

**待機中**: ユーザーの最初の指示待ち
```

つまり、まだ「待機中」なので：

```
あなた: codex --yoro
Codex: order_for_codex_yoro.md を読む
Codex: 「待機中」と確認
Codex: 「まだ指示がないので待機中です」と報告
Codex: git push
```

これで正常です。

---

## 📝 次のステップ

私が以下のタスクを `order_for_codex_yoro.md` に書き込みます：

```markdown
## 📋 現在の指示

### Task: テストファイル作成

以下のファイルを作成してください：
- test_hello.md
- test_goodbye.md

内容は適当でいいです。

完了したら報告してください。
```

そうしたら、あなたが：

```bash
codex --yoro
```

と言うだけで、Codex が自動的にテストファイルを作成します。

---

## 🎯 ポイント

| 項目 | 従来 | Yoro Mode |
|------|------|-----------|
| あなたの指示 | 長い説明 | 「codex --yoro」 |
| 指示書 | チャットで説明 | GitHub で管理 |
| 次の指示 | 毎回チャットで | GitHub で自動更新 |
| ナレッジ | 消える | GitHub に永続 |

---

## ✅ Ready to go!

```
あなた: codex --yoro

を実行したら、以下をコピペしてください：

---

order_for_codex_yoro.md という指示書を
GitHub https://raw.githubusercontent.com/garyohosu/virtual-company/main/order_for_codex_yoro.md
から読んでください。

そして「現在の指示」セクションに書かれたタスクを
完全に実行してください。

完了したら git push してください。

---
```

**準備完了です！** 🚀
