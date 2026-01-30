# Scale-free Network Implementation - 各層のテンプレート

## 🎯 4層でそれぞれ何をするか

### Layer 1: 係（Employee） - 日次作業実行

```
Employee/
├─ Skills.md              # 「このエラー見たことある」パターン
├─ Memory.md              # 今日何やったか
├─ order_employee_yoro.md # 今日のタスク
└─ Reports/
   └─ daily_report.md     # 課長への日報
```

#### order_employee_yoro.md の例

```markdown
# Employee_001 - Daily Task

## 今日の指示（2025-01-30）

### タスク1: ユーザー認証テスト
- [ ] ログイン機能をテスト
- [ ] エラーメッセージを確認
- [ ] ドキュメント更新
- 予定: 3時間
- Status: ⏳ 開始前

### タスク2: バグ修正
- [ ] GitHub Issue #123 を確認
- [ ] コードを修正
- [ ] テストを実行
- 予定: 2時間
- Status: ⏳ 開始前

### 注意事項
- もし同じエラーに遭遇したら Skills.md を確認
- 新しいエラーなら daily_report.md に記録
- 1時間ごとに進捗を記録

---

## もし判断が必要なら

課長に相談。自分で判断するな。
```

#### Memory.md（日記） の例

```markdown
# Employee_001 Memory - Daily Log

## 2025-01-30

### Morning (09:00-12:00)
**Task 1: ユーザー認証テスト**
- Status: ✅ 完了
- Time: 2.5h (予定: 3h)
- Result: 3個のエラー発見

**Error 1: パスワード空文字チェック**
- Pattern: これ見たことある（2025-01-28 にも出た）
- Solution: Skills.md の Pattern #5 参照
- Time to fix: 10分
- Status: ✅ 解決

**Error 2: ログイン画面タイムアウト**
- Pattern: 新しいエラー
- Investigation: Session timeout が短すぎる？
- Status: 課長に報告予定

### Afternoon (13:00-17:00)
**Task 2: バグ修正**
- Status: ⏳ 進行中
- Time: 1.5h (予定: 2h)
- Current: コード修正完了、テスト中

### 本日の成果
- ✅ Error 1 を自力で解決（Skills 活用）
- ✅ Task 1 を完了
- ⏳ Task 2 を 75% 完了
- ⏳ Error 2 を課長に報告

### 困ったこと
- DB接続がタイムアウト（Error 2）
- 課長に聞く必要がありそう

### 明日の予定
- Task 2 の続き
- Code review
```

#### daily_report.md（課長への報告） の例

```markdown
# Employee_001 Daily Report - 2025-01-30

**Status**: ✅ Good Progress

## 完了タスク
- ✅ ユーザー認証テスト（3個エラー発見・修正）
- 🟡 バグ修正（75% 完了）

## 自力で解決したエラー
- ✅ パスワード空文字チェック（Skills #5 参照）

## エスカレートが必要
- ⏳ ログイン画面タイムアウト（調査中）

## 成長
- 今日は過去パターンから 1 回自力解決できました
- Skills.md の活用が習慣化してきました

## 困ったこと
- DB接続タイムアウト（原因不明）
- Advice needed
```

---

### Layer 2: 課長（Manager） - 週次チーム管理

```
Manager/
├─ Skills.md              # 「このチーム管理パターン見たことある」
├─ Memory.md              # 週の進捗
├─ order_manager_yoro.md  # 週間目標
└─ Reports/
   ├─ employee_001_report.md  # 係1からの報告（集約）
   └─ weekly_report.md        # 部長への週報
```

#### Memory.md（週間進捗） の例

```markdown
# Manager_A1 Memory - Weekly Progress

## Week 1 (Jan 27-31)

### チーム構成
- Employee_001: ✅ Good
- Employee_002: 🟡 Need check-in
- Employee_003: ✅ Good
- Employee_004: 🔴 Blocked

### 週間目標
- 5つのタスク完了予定
- 現在: 3つ完了, 1つ 75% 完了

### Employee_001 Status
- Daily report: ✅ Good
- 自力解決: 1回（Skills活用）
- Escalation: DB timeout 1件
- Evaluation: ⬆️ 成長中

### Employee_002 Status
- Daily report: 🟡 遅延
- Issues: Code review 待ち
- Support needed: YES
- Action: 明日フォローアップ

### Employee_003 Status
- Daily report: ✅ Good
- Issues: None
- Evaluation: 安定中

### Employee_004 Status
- Daily report: 🔴 Blocked
- Issue: DB migration script 待ち
- Escalation to Director: YES (リソース不足)

### パターン分析
- Code review の遅延（複数人報告）
  → Manager-Skills.md に記録：「Code review が週の遅延要因」
  → 来週: Reviewer 追加割当が必要

- DB timeout issue（Employee_001 報告）
  → 新しいエラーか、既知か確認中
  → 来週: 再発チェック

### 課長の判断
1. Employee_002 への支援体制
2. Code review process の改善
3. Employee_004 のリソース確保（部長に報告）

### 部長への報告予定
- ✅ 3/5 タスク完了予定で good
- 🟡 Code review が瓶首
- 🔴 リソース不足（1名）
```

#### Manager-Skills.md（失敗パターン） の例

```markdown
# Manager_A1 Skills - Failure Patterns

## Pattern #1: Code Review Bottleneck 🔴

**What**: Code review が週の完了を 2-3日遅延させる

**When**: 毎週金曜日

**Why**: 
- Reviewer が他業務で忙しい
- 並列化されていない

**Prevention**:
- Backup reviewer を指定
- 金曜日は Code review 専念の時間を作る
- Pair programming で事前チェック

**Last Occurrence**: 2025-01-29

---

## Pattern #2: New Hire Estimation Drift 🟡

**What**: 新人が作業時間を過小評価する

**When**: 新人の最初の 3-4週

**Why**:
- 業務フローが把握できていない
- 共有知識がない

**Prevention**:
- 新人の予定には +30% buffer を加える
- Senior engineer を buddy に

**Last Occurrence**: 2025-01-28

---

## Pattern #3: Resource Contention

**What**: 複数チームが同じリソース（DB admin など）を必要とする

**When**: 月中旬

**Why**:
- スケジュール調整がない
- キャパシティ計画がない

**Prevention**:
- 月初に各チームのリソース需要を把握
- 部長に事前報告

**Last Occurrence**: 2025-01-30 (今日！)

---

## 課長が避けるべき判断ミス

1. 係の報告を聞かずに判断
2. 問題を部長に報告しない（隠蔽）
3. 係のサポートを後回しにする
4. Escalation を躊躇する

これらをやると、部長に「判断不足」と評価される。
```

#### weekly_report.md（部長への報告） の例

```markdown
# Manager_A1 Weekly Report - Week 1 (Jan 27-31)

**Overall Status**: 🟡 Good but resource issue

## チーム完了度
- 予定: 5タスク
- 完了: 3タスク (60%)
- 進行中: 1タスク (75% complete)
- Blocked: 1タスク

## 成功事例
- ✅ Employee_001: 過去パターンから自力解決（成長中）
- ✅ Employee_003: 安定して進捗

## 課題と対応
- 🟡 Code review が瓶首
  → 来週: Backup reviewer 指定
  → Manager-Skills.md に Pattern #1 として記録
  
- 🔴 Employee_004 がリソース待ちで blocked
  → Issue: DB migration script 不足
  → 部長への Escalation: YES

## パターン検出
- Code review bottleneck（Pattern #1）が再発
- これは組織レベルの問題か？

## 部長への質問
1. DB admin の余裕はありますか？ (Employee_004 for DB migration)
2. Code review を改善するため、reviewer を増やせますか？

## 来週の予定
- 残り 2タスク の完了
- Code review process 改善
- Employee_004 のサポート
```

---

### Layer 3: 部長（Director） - 月次部門管理

```
Director/
├─ Skills.md              # 「この部門管理パターン見たことある」
├─ Memory.md              # 月間進捗
├─ order_director_yoro.md # 月間目標
└─ Reports/
   ├─ manager_a1_report.md   # 課長1からの報告（集約）
   ├─ manager_a2_report.md   # 課長2からの報告
   └─ monthly_report.md      # CEO への月報
```

#### Memory.md（月間進捗） の例

```markdown
# Director_A Memory - Monthly Progress

## Month: January 2025

### 部門構成
- Manager_A1: 4 employees
- Manager_A2: 4 employees
- Manager_A3: 3 employees
Total: 11 employees

### 月間目標
- 計画: 20タスク完了
- 現在: 12タスク完了 (60%)

### Manager の状況

**Manager_A1**: 🟡 Good with resource issue
- Weekly status: Code review 瓶首、Employee_004 blocked
- Escalation: DB migration が必要
- Pattern detected: Code review bottleneck（新しいパターン）

**Manager_A2**: ✅ Good
- Weekly status: 安定進捗
- No escalation
- All employees happy

**Manager_A3**: ✅ Good
- Weekly status: 順調
- No escalation
- 1名の新人が成長中（Pattern #1 を回避）

### パターン分析（月間集約）
- Code review bottleneck（Manager_A1 報告）
  → 他の Manager にも聞いて確認
  → もし全部門なら CEO に報告
  → Director-Skills.md に記録

- Resource contention（Manager_A1 報告）
  → DB admin が忙しい
  → Engineering director とリソース調整が必要

### 部長の判断
1. Code review が全部門的な問題か確認
2. DB admin のキャパシティ計画
3. CEO への escalation レベルの決定

### CEO への報告予定
- ✅ 順調に進捗中（60%）
- 🟡 Code review 瓶首（全部門か確認中）
- 🔴 DB admin リソース不足（対応案 3 つ準備）
```

#### Director-Skills.md（判断ミスパターン） の例

```markdown
# Director_A Skills - Management Failure Patterns

## Pattern #1: Ignoring Manager Escalation 🔴

**What**: Manager からの escalation を軽視して問題を大きくした

**When**: 月の中旬以降

**Why**:
- CEO が忙しくて報告できていない
- 重要度の判断を間違えた
- 対応を後回しにした

**Prevention**:
- Manager からの escalation は翌日中に対応
- 問題の大きさを 3段階分類（LOW/MEDIUM/HIGH）
- CEO への報告判断を明確化

**Last Occurrence**: 2024-12月（大きなトラブルになった）

---

## Pattern #2: Micro-management 🟡

**What**: CEO に細かい報告をしすぎて CEO を疲れさせた

**When**: 月初

**Why**:
- 部門の全詳細を CEO に報告しようとした
- CEO は大局を見たいだけ

**Prevention**:
- 月報では「重要なパターン」3-5個だけ
- Manager の細かい日報は自分で管理
- CEO には「意思決定が必要な案件」だけ報告

---

## 部長が避けるべき判断ミス

1. Manager の escalation を無視
2. 問題を CEO に隠蔽
3. CEO に細かすぎる報告
4. 部門内リソース配分を CEO に丸投げ
```

#### monthly_report.md（CEO への報告） の例

```markdown
# Director_A Monthly Report - January 2025

**Overall Status**: ✅ Good Progress

## 部門完了度
- 計画: 20タスク
- 完了: 12タスク (60%)
- On track

## 重要パターン 3つ

### Pattern #1: Code Review Bottleneck 🟡
**Impact**: Week 1 で発見、1-2日遅延
**Cause**: Reviewer キャパシティ不足
**Action**: Manager に backup reviewer 指定させた
**Outcome**: 来週から改善予定
**CEO Decision Needed**: NO (tactical fix)

### Pattern #2: DB Admin Resource 🟡
**Impact**: 1 employee blocked
**Cause**: DB migration script が必要
**Action**: 3つの対応案を用意
  - Option A: Contract DB specialist ($5k)
  - Option B: Pull from Director_B ($0)
  - Option C: Defer migration to Feb ($delay)
**CEO Decision Needed**: YES (budget or delay)

### Pattern #3: New Hire Success ✅
**Impact**: Positive
**Cause**: Buddy system + Pattern recognition
**Action**: Manager_A3 の新人が Pattern #1 を回避
**Outcome**: Company-wide best practice に
**CEO Note**: Buddy system を他の部門にも

## パターン集計（3つ）
CEO は何を覚えるか？
- Code review が瓶首（全社的か？）
- DB admin がネック（CEO level resource planning）
- Buddy system が有効（拡大推奨）

CEO は何を覚えない？
- 各 Manager の細かい weekly 進捗
- 各 Employee の daily タスク
- Manager_A1 の特定の employee issue
```

---

### Layer 4: CEO（CEO） - 年次戦略

```
CEO/
├─ Skills.md              # CEO が陥る判断ミス
├─ Memory.md              # 年間戦略進捗
└─ Reports/
   ├─ director_a_report.md   # 部長A からの報告
   ├─ director_b_report.md   # 部長B からの報告
   └─ CEO-decision.md        # CEO の判断・決定記録
```

#### Memory.md（年間戦略） の例

```markdown
# CEO Memory - Annual Strategy

## 2025年 Strategic Progress

### Director の状況

**Director_A**: ✅ Good
- Monthly status: Code review 瓶首（解決中）
- Resource issue: DB admin（決定待ち）
- Pattern: Code review bottleneck は全社的か？

**Director_B**: ✅ Good
- Monthly status: 順調
- No major issues
- Can loan DB admin to Director_A?

**Director_C**: ✅ Good
- Monthly status: 順調
- New hire success（Buddy system 有効）

### CEO が覚えていること
1. Code review が全社的な瓶首？（来月確認）
2. DB admin が不足（予算か構成か決定必要）
3. Buddy system は有効（HR 部門に展開）

### CEO が覚えていないこと
- 各 Director の週間進捗（Director のメモリ）
- 各 Manager の日報（Manager のメモリ）
- 各 Employee の作業内容（Employee のメモリ）

### CEO の来月の判断
1. 「Code review 瓶首」が全社的なら → Reviewer hiring
2. 「DB admin」リソース → Option B (Director_B from) で OK
3. 「Buddy system」を HR に展開
```

#### CEO-decision.md（判断記録） の例

```markdown
# CEO Decisions - January 2025

## Decision #1: DB Admin Resource
**Issue**: Director_A が DB admin 不足
**Options**:
- A: Contract specialist ($5k)
- B: Pull from Director_B ($0)
- C: Defer ($delay)

**Decision**: Option B
**Reasoning**: Director_B has spare capacity
**Outcome**: Director_B に連絡、1月末から Director_A 支援予定

**CEO Memory**: 
「Director_B は柔軟に対応できる人材」← 来年の人事参考

---

## Decision #2: Buddy System Expansion
**Issue**: Director_A の新人が成長（Pattern #3 detected）
**Proposal**: 全社に展開
**Decision**: YES, hire HR coordinator for buddy matching

**CEO Memory**: 
「Small system changes can have big impact」← CEO Skill #1
```

---

## 🎯 まとめ：相似構造

```
CEO:
- Memory: 3 パターン（戦略レベル）
- Skill: CEO が陥る判断ミス 3 つ
- Reports: 部長からの月報のみ

部長:
- Memory: 5 パターン（月間レベル）
- Skill: 部長が陥る判断ミス 5 つ
- Reports: 課長からの週報のみ

課長:
- Memory: 5 パターン（週間レベル）
- Skill: 課長が陥る判断ミス 5 つ
- Reports: 係からの日報のみ

係:
- Memory: 100 エラー（日々のレベル）
- Skill: これまでのエラーパターン 20 個
- Reports: 日報のみ

各層が「相似的に」
同じアーキテクチャで
上位層は下位層の詳細を知らない
```

---

**Scale-free Network 完成！** 🎉

CEO は 3 つのパターンを覚える。
でも組織全体として 100+ のエラーから学ぶ。

これが **フラクタル組織** です。
