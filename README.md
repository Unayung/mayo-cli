# mayo

在終端機操作 MayoHR Apollo XE：網頁打卡、查剩餘假別、看請假紀錄、送請假單。
做的事跟 https://apolloxe.mayohr.com/ta?id=webpunch 和請假頁一樣，只是不用開瀏覽器。

單一檔案，Python 3.8 以上，只用標準函式庫，不需要安裝任何套件。

> **非官方工具。** 與 MAYO 人力資源（MAYO Human Capital）無關，也未經授權。
> 使用的 API 沒有公開文件，是從網頁的 JS bundle 和錄下的瀏覽器請求讀出來的，
> 對方改版就可能失效。打卡和請假都會寫進正式出勤紀錄，請只用在自己的帳號上，
> 並先確認公司規定。

## 安裝

```bash
git clone https://github.com/Unayung/mayo-cli.git
cd mayo-cli
chmod +x mayo
ln -s "$PWD/mayo" ~/.local/bin/mayo   # 選用：放進 PATH
```

## 功能

### 登入

```bash
mayo login --user you@company.com     # 互動輸入密碼
mayo whoami
mayo logout
```

- 密碼不會存下來。登入後只保留 session cookie（約 10 天）和 refresh token，
  到期前 CLI 會自動換新。兩週內至少用一次，就不必再登入。
- 狀態檔在 `~/.config/mayo/state.json`，權限 0600。設 `MAYO_HOME` 可以換位置，
  設 `MAYO_COOKIE` 可以直接指定 cookie。

### 打卡

```bash
mayo status                     # 今天的班表，現在可以打哪一種卡
mayo punch in                   # 上班
mayo punch out                  # 下班
mayo punch break                # 休息開始
mayo punch break-end            # 休息結束
mayo punch in --dry-run         # 只印出要送的內容，不打卡
mayo punch out --reason "客戶會議"
```

- 打卡前會先查網頁當下會顯示哪顆按鈕，網頁不讓按的 CLI 也不送。
  例如還沒打上班就打下班，會直接回錯誤（exit code 2）。
- 公司若有設定「延後下班須填理由」，超過寬限時間才打下班卡時，CLI 會要求加
  `--reason`，以「個人因素」送出，跟網頁的流程相同。提早上班也是一樣。

### 查假、請假

```bash
mayo leave balance                       # 剩餘假別（時數與到期日）
mayo leave list --year 2026              # 請假紀錄與簽核狀態
mayo leave apply 特休 --date 2026-10-16 --reason 家事             # 預覽
mayo leave apply 特休 --date 2026-10-16 --reason 家事 --yes       # 送出
mayo leave apply 事假 --date 2026-10-16 --start 14:00 --reason 看醫生 --yes
mayo leave apply 特休 --date 2026-10-20 --to 2026-10-22 --reason 旅遊 --yes
```

- 假別可以填名稱（`特休`）或代碼（`H1001`），可用的選項以 `mayo leave balance` 為準。
- 沒給 `--start` / `--end` 時，預設用當天班表的上下班時間。
- 請假時數由伺服器依班表計算，午休會自動扣掉。要自己指定可以用 `--minutes`。
- 代理人預設用你在系統裡設定的代理人，「代理簽核」與「表單類型」也沿用網頁的預設值。
- 沒加 `--yes` 只會預覽，不會送出。送出後會通知代理人和簽核主管。

### 給腳本與 agent 用

- 每個指令都支援 `--json`，輸出格式是 `{"ok": true, "data": ...}`。
- Exit code：0 成功、1 錯誤、2 用法錯誤或現在不能做、3 未登入、4 網路錯誤。
- `mayo api-map` 列出目前已知的 endpoint。
- `mayo raw GET pt/api/<path>` 可以呼叫 CLI 還沒包裝的 API。
- `SKILL.md` 是給 Claude Code 這類 agent 讀的使用說明。

## 限制

- **只支援帳號密碼登入。** Microsoft、Google、Okta 這類單一登入的帳號不能用。
  如果登入頁要求 reCAPTCHA（例如連續輸錯密碼後），CLI 會登入失敗，請先到網頁登入一次。
- **只支援單一公司。** 一個帳號掛多家公司、登入後要選公司的情況沒有處理。
- **只有網頁打卡。** 不支援 App 定位打卡和 QR Code 打卡。公司沒開放網頁打卡，
  或限制了打卡 IP，CLI 也一樣打不了，這些都由伺服器判斷。
- **超時打卡只支援「個人因素」。** 網頁上另一個選項「因公（加班）」沒有實作。
- **請假只支援一般假別。** 不支援特殊假別（婚假、喪假、產假等需要另外申請的假）、
  附件上傳、代理他人申請。一張假單只能填一種假別。
- **抽單沒有包成指令。** 已知 endpoint 是 `PUT pt/api/LeaveRequestForms/Delete/<id>`，
  但還沒實際驗證，需要的話請用 `mayo raw`，或直接到網頁操作。
- **沒有加班單、忘打卡申請、打卡紀錄查詢。**
- **時間以本機時區計算。** 請確認電腦時區跟公司一致（例如 Asia/Taipei）。
- **測試狀態。** 查詢類指令都用真實帳號跑過。打卡和請假要送的內容，是在瀏覽器按下按鈕時
  攔截下來的請求（攔下後沒有送出），CLI 產生的內容跟它逐欄比對過，但 CLI 本身還沒有
  實際送出過打卡或假單。

## 測試

```bash
python3 test_mayo.py
```

## 授權

MIT
