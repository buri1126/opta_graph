"use client";

import { useState } from "react";

interface PlayerStats {
  name: string;
  apps: number;
  mins: number;
  goals: number;
  xg: number;
  goals_vs_xg: number;
  shots: number;
  sot: number;
  conv_percent: string;
  xg_per_shot: number;
}

interface TottenhamStatsResponse {
  success: boolean;
  team: string;
  total_players: number;
  players: PlayerStats[];
  headers: string[];
  error?: string;
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState<TottenhamStatsResponse | null>(null);

  const fetchTottenhamData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        "http://localhost:8000/api/scraping/theanalyst-tottenham",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const rawResult = await response.json();
      console.log("Raw API response:", rawResult);
      console.log("Has formatted_data:", !!rawResult.formatted_data);
      
      const result = rawResult.formatted_data || rawResult;
      console.log("Final result:", result);
      console.log("Total players:", result.total_players);
      
      setData(result);
      // コンソールにデータを表示
      // console.log("=== Tottenham Player Stats ===");
      // console.log(`Team: ${result.team}`);
      // console.log(`Total Players: ${result.total_players}`);
      // console.log("Headers:", result.headers);
      // console.log("Players:");
      // result.players.forEach((player, index) => {
      //   console.log(`${index + 1}. Player data:`, player);
      //   console.log("---");
      // });
    } catch (error) {
      console.error("Error fetching data:", error);
      setData({
        success: false,
        team: "tottenham",
        total_players: 0,
        players: [],
        headers: [],
        error: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center max-w-md mx-auto p-6">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Tottenham Stats
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Next.js + FastAPI スクレイピングアプリ
        </p>

        <button
          onClick={fetchTottenhamData}
          disabled={isLoading}
          className={`px-6 py-3 rounded-lg font-semibold text-white transition-colors ${
            isLoading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {isLoading ? "データ取得中..." : "Tottenhamデータを取得"}
        </button>

        {data && (
          <div className="mt-8 p-4 bg-white rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">結果</h2>
            {data.success ? (
              <div className="text-left">
                <p className="text-green-600">
                  ✅ 成功: {data.total_players}人の選手データを取得
                </p>
                <p className="text-sm text-gray-600 mt-2">
                  詳細はブラウザのコンソール（F12 → Console）で確認してください
                </p>
              </div>
            ) : (
              <p className="text-red-600">❌ エラー: {data.error}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
