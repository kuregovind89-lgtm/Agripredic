import React, { useState } from "react";
import { FiAlertTriangle } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import api from "../api/api";
import { useAuth } from "../context/AuthContext";

const RISK_LABELS = [
  { key: "disease_risk", label: "Disease Risk", icon: "🦠" },
  { key: "pest_risk", label: "Pest Risk", icon: "🐛" },
  { key: "flood_risk", label: "Flood Risk", icon: "🌊" },
  { key: "drought_risk", label: "Drought Risk", icon: "☀️" },
  { key: "heatwave_risk", label: "Heatwave Risk", icon: "🌡️" },
  { key: "crop_failure_risk", label: "Crop Failure Risk", icon: "🌾" },
];

function levelFromScore(score) {
  if (score >= 65) return "High";
  if (score >= 35) return "Medium";
  return "Low";
}

export default function RiskPrediction() {
  const { user } = useAuth();
  const [location, setLocation] = useState(user?.location || "");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!location) return;
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/api/risk/assess", { params: { location } });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not fetch risk data for that location.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar title="Risk Prediction" subtitle="Disease, pest, flood, drought, heatwave & crop-failure risk in one place" />

        <div className="glass-card animate-in weather-search">
          <form onSubmit={handleSubmit} className="weather-form">
            <input placeholder="Enter city/village name (e.g. Pune)" value={location} onChange={(e) => setLocation(e.target.value)} />
            <button className="btn-primary" type="submit" disabled={loading}>
              {loading ? "Assessing..." : "Assess Risk"}
            </button>
          </form>
          {error && <div className="alert-error">{error}</div>}
        </div>

        {loading && <Loader text="Analyzing weather & risk factors..." />}

        {result && (
          <>
            <div className={`glass-card risk-banner risk-${result.overall_level.toLowerCase()} animate-in`}>
              <FiAlertTriangle size={30} />
              <div>
                <h2>Overall Risk: {result.overall_level}</h2>
                <p>{location} — Temp {result.weather.temperature}°C, Humidity {result.weather.humidity}%, Rain {result.weather.rainfall}mm, Wind {result.weather.wind_speed} km/h</p>
              </div>
            </div>

            <div className="risk-grid">
              {RISK_LABELS.map(({ key, label, icon }) => {
                const score = result[key];
                const level = levelFromScore(score);
                return (
                  <div key={key} className="glass-card risk-card animate-in">
                    <div className="risk-card-head">
                      <span className="risk-icon">{icon}</span>
                      <span className="risk-label">{label}</span>
                      <span className={`badge badge-${level.toLowerCase()}`}>{level}</span>
                    </div>
                    <div className="risk-bar-track">
                      <div className={`risk-bar-fill risk-fill-${level.toLowerCase()}`} style={{ width: `${score}%` }} />
                    </div>
                    <div className="risk-score">{score}%</div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
