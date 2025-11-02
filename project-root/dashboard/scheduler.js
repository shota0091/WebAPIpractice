// dashboard/scheduler.js
const axios = require("axios");

const API_URL = "http://127.0.0.1:5000/status";
let latestData = [];

// FlaskのAPIを1分ごとに叩く
function startScheduler() {
  console.log("⏱️ Flask監視APIを1分ごとに呼び出します");

  async function callApi() {
    try {
      const res = await axios.post(API_URL, {
        targetList: ["notepad.exe", "git-bash.exe"],
      });
      latestData = res.data;
      console.log(`[${new Date().toLocaleString()}] ✅ データ更新`);
    } catch (err) {
      console.error(`[${new Date().toLocaleString()}] ❌ API呼び出し失敗: ${err.message}`);
    }
  }

  callApi(); // 起動時に1回実行
  setInterval(callApi, 60 * 1000);
}

function getLatestData() {
  return latestData;
}

module.exports = { startScheduler, getLatestData };
