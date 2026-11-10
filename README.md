# 健身紀錄

記錄每天重訓的 Android app：選肌群自動帶入常練動作，點卡片記錄每一組的重量、次數和力竭程度，並用進步曲線追蹤成績。

## 下載
到右邊的 **Releases** 下載最新的 `.apk`，在 Android 手機上開啟安裝。

## 怎麼更新版本
1. 修改 `app/src/main/assets/index.html`（整個 app 的畫面和功能）
2. 把 `version.txt` 的版本號加一（例如 1.0.0 → 1.0.1）
3. 上傳到 main 分支，GitHub 會自動打包並發布到 Releases

## 網頁版（iPhone 也能用）
打開 https://alan0417.github.io/gym_diary/ ，iPhone 用 Safari「分享 → 加入主畫面」，Android 用 Chrome「⋮ → 加到主畫面」。

網頁版放在 `docs/` 資料夾，由 `make_web.py` 從 app 的 index.html 自動產生。改完 index.html 後執行 `python3 make_web.py`，再一起上傳。
