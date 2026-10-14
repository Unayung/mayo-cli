---
name: mayo
description: 用 CLI 操作 MayoHR Apollo XE：網頁打卡（上班/下班/休息）、查剩餘假別、請假紀錄、送請假單。使用者提到「打卡」「上班卡」「下班卡」「MayoHR」「Apollo」「剩幾天特休」「請假」時使用。打卡和請假都是真實出勤紀錄，送出前確認。
---

# mayo

`mayo` drives MayoHR Apollo XE. Always pass `--json` when parsing.

## Before anything

`mayo status --json` — `data.next` lists what can be punched now (`in`, `out`, `break`, `break-end`).
Exit 3 = not logged in: ask the user to run `! mayo login --user <account>` (password is prompted, never pass it in argv).

## Punch

`mayo punch in|out|break|break-end`. This writes a real attendance record — only when the user asked for it.
- Exit 2 "cannot punch X now": the web would not offer it either; tell the user what `status` says.
- Exit 2 "outside the PostponeWork window": ask the user for a reason, then `--reason "..."`.
- `--dry-run` prints the body without punching.

## Leave

- `mayo leave balance --json` — `AvailableTime - UsedMinutes` is minutes left; `Detail[].ExpiryDate` per batch.
- `mayo leave list --json` — this year's forms, `StatusName` is the approval state.
- `mayo leave apply <特休|事假|有薪病假|code> --date YYYY-MM-DD [--to ...] [--start HH:MM --end HH:MM] --reason ...`
  previews by default. Show the preview line to the user, and add `--yes` only after they confirm —
  it notifies the 代理人 and the approver.
- Withdraw (unverified): `mayo raw PUT pt/api/LeaveRequestForms/Delete/<LeaveRequestFormId>`.
