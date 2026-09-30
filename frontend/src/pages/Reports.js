import React, { useState } from "react";
import { FiDownload, FiFileText } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import api from "../api/api";

const REPORTS = [
  { key: "disease", title: "Disease Detection Report", desc: "All your crop disease scans with confidence & severity." },
  { key: "risk", title: "Risk Assessment Report", desc: "History of disease, flood, drought & heatwave risk checks." },
  { key: "farm", title: "Farm Summary Report", desc: "Farm profile details plus scan and alert totals." },
];

export default function Reports() {
  const [downloading, setDownloading] = useState(null);

  const download = async (reportKey, format) => {
    setDownloading(`${reportKey}-${format}`);
    try {
      const res = await api.get(`/api/reports/${reportKey}`, { params: { format }, responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${reportKey}_report.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar title="Reports" subtitle="Export your farm data as PDF or CSV" />

        <div className="reports-grid">
          {REPORTS.map((r) => (
            <div key={r.key} className="glass-card animate-in report-card">
              <div className="report-card-icon"><FiFileText size={22} /></div>
              <h3>{r.title}</h3>
              <p>{r.desc}</p>
              <div className="report-card-actions">
                <button className="btn-primary" onClick={() => download(r.key, "pdf")} disabled={downloading === `${r.key}-pdf`}>
                  <FiDownload /> {downloading === `${r.key}-pdf` ? "Preparing..." : "PDF"}
                </button>
                <button className="btn-secondary" onClick={() => download(r.key, "csv")} disabled={downloading === `${r.key}-csv`}>
                  <FiDownload /> {downloading === `${r.key}-csv` ? "Preparing..." : "CSV"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
