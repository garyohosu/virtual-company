# FAILURE RECORD 003 - Python 3.8 と pydantic-core 2.x の互換問題

## 概要
Python 3.8 環境で pydantic-core 2.14.0 が対応外となり、wheel 不足でインストール失敗。

## 発生状況
- Python 3.8 で pydantic-core 2.x を要求
- wheel がなくビルド不可

## 根本原因
- pydantic 2.x は Python 3.9+ を前提
- 依存の互換性マトリクス未確認

## 影響
- FastAPI 起動/pytest が不可

## 対応
- Python 3.9+ への移行
- もしくは pydantic 1.x 系に固定

## 再発防止
- 事前に対応バージョン表を作成
- requirements に Python バージョン条件を明記
