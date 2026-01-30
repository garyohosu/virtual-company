# NOTE ARTICLE IDEAS - Failure Records

## タイトル案
- 「Sakura FreeBSD でハマった5つの罠」
- 「AIエージェント運用でやらかした話と対策」
- 「Python環境構築で死んだ話」

## 構成案
1. イントロ: なぜ失敗記録が必要か
2. 失敗1: Linux手順をFreeBSDに適用
3. 失敗2: Rust依存の pydantic-core
4. 失敗3: Python 3.8 の罠
5. 失敗4: Git 競合
6. 失敗5: 依存チェーン崩壊
7. まとめ: 事前検証チェックリスト

## まとめ用箇条書き
- 「OS確認 → 依存互換 → 実行」
- 「wheel が無いなら詰む」
- 「並列作業は pull/rebase で守る」

## 追記ネタ
- 実際のエラーログの抜粋
- CI/CD による再発防止策
