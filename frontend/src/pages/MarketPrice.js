import React, { useEffect, useState } from "react";
import { FiTrendingUp, FiTrendingDown, FiMinus } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import api from "../api/api";

const TREND_ICON = {
  up: <FiTrendingUp color="var(--brand-leaf)" />,
  down: <FiTrendingDown color="var(--brand-red)" />,
  stable: <FiMinus color="var(--text-muted)" />,
};

export default function MarketPrice() {
  const [data, setData] = useState({ prices: [], source: "sample", district: null });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/market/prices").then((res) => setData(res.data)).finally(() => setLoading(false));
  }, []);

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar
          title="Market Price Information"
          subtitle={data.district ? `Live-style APMC prices near ${data.district}` : "Latest mandi prices to help you decide when to sell"}
        />

        {data.source === "sample" && !loading && (
          <div className="glass-card animate-in market-source-banner">
            Showing sample prices. To see live Agmarknet/data.gov.in prices, add your free <code>DATA_GOV_API_KEY</code> to backend/.env.
          </div>
        )}

        {loading ? <Loader text="Loading market prices..." /> : (
          <div className="market-grid">
            {data.prices.map((p, idx) => (
              <div className="glass-card market-card animate-in" key={idx}>
                <div className="market-header">
                  <h4>{p.crop}</h4>
                  {TREND_ICON[p.trend]}
                </div>
                <p className="market-market">{p.market}</p>
                <div className="market-price">₹{p.price_per_quintal.toLocaleString()} <span>/quintal</span></div>
                {typeof p.change_pct === "number" && (
                  <div className={`market-change ${p.trend}`}>
                    {p.trend === "up" ? "▲" : p.trend === "down" ? "▼" : "—"} {Math.abs(p.change_pct)}% (7-day)
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
