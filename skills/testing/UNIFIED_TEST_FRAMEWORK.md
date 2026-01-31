# skills/testing/UNIFIED_TEST_FRAMEWORK.md

**対象**: Virtual Company の全 AI エージェント
**目的**: ローカル・リモート環境で統一されたテスト実行
**更新日**: 2026-01-31

---

## 🎯 特徴

✅ **同じテストコードで 2 つの環境をテスト**
- ローカル（Python/FastAPI）
- リモート（PHP/Sakura）

✅ **環境変数で自動切り替え**
- 開発者は同じコマンド実行

✅ **バグが本番環境に行かない**
- ローカル + リモート二重チェック

---

## 🚀 テスト実行方法

### ローカルテスト（FastAPI）

```bash
python -m pytest tests/test_magicboxai_api.py -v
```

**実行内容**:
- FastAPI サーバーをメモリ上で起動
- テストケース実行
- 約 5 秒で完了

**使用場面**:
- 開発中の迅速な検証
- git commit 前のチェック

---

### リモートテスト（PHP/Sakura）

```powershell
$env:MAGICBOXAI_BASE_URL="https://garyo.sakura.ne.jp/magicboxai"
python -m pytest tests/test_magicboxai_api.py -v
```

**実行内容**:
- 実際の Sakura サーバーへ HTTP リクエスト送信
- 本番環境での動作確認
- レート制限テストはスキップ（本番保護）

**使用場面**:
- 本番前の最終確認
- CI/CD パイプラインでの自動実行

---

## 📊 テストマトリックス

| 環境 | 実行場所 | 速度 | テスト対象 | 用途 |
|------|--------|------|---------|------|
| ローカル | PC (FastAPI) | 高速（5秒） | Python/FastAPI | 開発中 |
| リモート | Sakura (PHP) | 遅い（30秒） | 本番環境 | 本番前確認 |

---

## ✅ テストケース

```python
# 1. 正常系
✅ save() で HTML を保存 → token 取得
✅ view() で token から HTML を取得
✅ health check が "ok" を返す

# 2. バリデーション
✅ 空の HTML は拒否
✅ whitespace のみの HTML は拒否（修正済み）

# 3. レート制限（ローカルのみ）
✅ 1日5回の制限を検証
✅ 日が変わると リセット
```

---

## 🔧 GitHub Actions での使用

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      # ローカルテスト
      - name: Local Test (FastAPI)
        run: python -m pytest tests/test_magicboxai_api.py
      
      # リモートテスト
      - name: Remote Test (Sakura PHP)
        env:
          MAGICBOXAI_BASE_URL: https://garyo.sakura.ne.jp/magicboxai
        run: python -m pytest tests/test_magicboxai_api.py
```

---

## 🎓 バグ修正の例

### 発見されたバグ

```
PHP 版: whitespace のみの HTML を受け入れていた
Python 版: whitespace のみを拒否

→ 不一致！
```

### Gemini の対応

```
1️⃣ バグを自動検出
2️⃣ PHP コード修正
3️⃣ Sakura に自動デプロイ
4️⃣ リモートテスト再実行
5️⃣ 修正確認
```

**結果**: 両環境で同じ動作に統一

---

## 📝 テスト実行結果

```
ローカルテスト:
4 passed in 0.32s ✅

リモートテスト (Sakura):
3 passed (1 skipped - rate limit test) ✅
```

---

## 🚀 推奨ワークフロー

```
開発中:
git add .
git commit -m "Feature: ..."
python -m pytest                    # ローカルテスト

本番デプロイ前:
$env:MAGICBOXAI_BASE_URL="https://..."
python -m pytest                    # リモートテスト

git push                            # GitHub Actions 自動実行
```

---

**テストあり = 安心できる開発環境** ✨
