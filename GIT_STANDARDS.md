# Git Standards

## Commit Message Format
**Format**: `[type] Description`

**Types**:
- `feat` ? new feature
- `fix` ? bug fix
- `docs` ? documentation
- `refactor` ? refactoring without behavior change
- `test` ? tests only
- `chore` ? tooling, build, or maintenance

**Examples**:
- `[feat] Add rate limiting to kick system`
- `[docs] Document setup instructions`
- `[chore] Update dependency pins`

## Branch Strategy
- `main` ? stable, production-ready
- `develop` ? integration branch
- `feature/*` ? individual features
- `hotfix/*` ? production fixes

## Pull Request Conventions
- Create a PR before merging to `main`.
- Require review from at least one AI agent.
- Include: what changed, why, and how to test.

## Tag Strategy
- Tags on `main` only.
- Use semantic versioning: `v1.0.0`, `v1.1.0`, `v2.0.0`.
- Tag when a release is production-ready.

## Notes
- Never commit secrets or `.env` files.
- Keep commits scoped and atomic.
