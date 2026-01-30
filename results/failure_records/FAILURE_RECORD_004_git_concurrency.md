# FAILURE RECORD 004 - SSH 並列作業で git 競合

## 概要
複数の作業で git add/push の順序が崩れ、非fast-forwardが発生。

## 発生状況
- 複数の実行が並行
- 先に push された変更をローカルが取り込みできず reject

## 根本原因
- 作業前の `git pull --rebase` が徹底されていない
- 変更の順序管理が不足

## 影響
- push 失敗
- 作業が中断

## 対応
- `git pull --rebase` を先に実行
- 衝突時は再解決して push

## 再発防止
- すべての order に「pull -> work -> push」明記
- 並行作業時はブランチ運用を検討
