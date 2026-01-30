# FAILURE RECORD 005 - 依存チェーンの不整合

## 概要
fastapi/uvicorn/pydantic/pytest の組み合わせが不整合で、依存解決が失敗。

## 発生状況
- fastapi 0.100.0 と pydantic 2.0.0 の組み合わせで conflict
- requirements のピンが一致しない

## 根本原因
- 依存バージョンの整合表がない
- requirements の見直し不足

## 影響
- pip install が ResolutionImpossible
- 起動/テストが進まない

## 対応
- fastapi/uvicorn/pydantic/pytest の互換セットを選定
- lockfile 管理へ移行

## 再発防止
- バージョン固定のレビュー手順を追加
- CI で依存解決テストを実行
