// dashboard/server.js
const express = require("express");
const path = require("path");
const { startScheduler, getLatestData } = require("./scheduler");

const app = express();
const PORT = 3000;

// 静的ファイル（viewsフォルダのHTMLなど）を提供
app.use(express.static(path.join(__dirname, "views")));

// APIエンドポイント：最新監視データを返す
app.get("/api/status", (req, res) => {
  res.json(getLatestData());
});

// ルートページ（index.html）を返す
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "index.html"));
});

// サーバー起動
app.listen(PORT, () => {
  console.log(`🌐 Dashboard起動中 → http://localhost:${PORT}`);
});

// スケジューラ開始
startScheduler();
