import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import StatCard from "../components/StatCard";
import { FiUsers, FiActivity, FiAlertTriangle } from "react-icons/fi";
import api from "../api/api";

const TABS = ["Farmers", "Predictions", "High-Risk Farms"];

export default function Expert() {
  const [tab, setTab] = useState("Farmers");
  const [farmers, setFarmers] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [highRisk, setHighRisk] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/api/expert/farmers"),
      api.get("/api/expert/predictions"),
      api.get("/api/expert/high-risk-farms"),
    ]).then(([f, p, h]) => {
      setFarmers(f.data);
      setPredictions(p.data);
      setHighRisk(h.data);
    }).finally(() => setLoading(false));
  }, []);

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar title="Agriculture Expert Panel" subtitle="Read-only oversight of farmers, scans, and risk alerts" />

        {loading ? <Loader text="Loading expert dashboard..." /> : (
          <>
            <div className="stat-grid">
              <StatCard icon={<FiUsers color="#fff" />} label="Registered Farmers" value={farmers.length} accent="var(--brand-leaf)" />
              <StatCard icon={<FiActivity color="#fff" />} label="Total Scans" value={predictions.length} accent="var(--brand-blue)" />
              <StatCard icon={<FiAlertTriangle color="#fff" />} label="High-Risk Alerts" value={highRisk.length} accent="var(--brand-red)" />
            </div>

            <div className="tab-bar">
              {TABS.map((t) => (
                <button key={t} className={`tab-btn ${tab === t ? "active" : ""}`} onClick={() => setTab(t)}>{t}</button>
              ))}
            </div>

            {tab === "Farmers" && (
              <div className="glass-card animate-in table-card">
                <table className="admin-table">
                  <thead><tr><th>Name</th><th>Email</th><th>Location</th><th>Joined</th></tr></thead>
                  <tbody>
                    {farmers.map((f) => (
                      <tr key={f.id}>
                        <td>{f.name}</td><td>{f.email}</td><td>{f.location || "-"}</td>
                        <td>{new Date(f.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {tab === "Predictions" && (
              <div className="glass-card animate-in table-card">
                <table className="admin-table">
                  <thead><tr><th>Disease</th><th>Crop</th><th>Confidence</th><th>Severity</th><th>Date</th></tr></thead>
                  <tbody>
                    {predictions.map((p) => (
                      <tr key={p.id}>
                        <td>{p.disease_name}</td><td>{p.crop}</td><td>{p.confidence}%</td>
                        <td><span className={`badge badge-${p.severity.toLowerCase()}`}>{p.severity}</span></td>
                        <td>{new Date(p.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {tab === "High-Risk Farms" && (
              <div className="glass-card animate-in table-card">
                <table className="admin-table">
                  <thead><tr><th>Farmer</th><th>Location</th><th>Crop Failure Risk</th><th>Date</th></tr></thead>
                  <tbody>
                    {highRisk.map((h, i) => (
                      <tr key={i}>
                        <td>{h.farmer_name}</td><td>{h.location}</td>
                        <td><span className="badge badge-high">{h.crop_failure_risk}%</span></td>
                        <td>{new Date(h.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
