import React, { useState, useEffect } from "react";
import { FiTrendingUp } from "react-icons/fi";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import api from "../api/api";
import { INDIAN_STATES, getDistricts } from "../data/indiaLocations";

const SOIL_TYPES = ["Loamy", "Clay", "Sandy", "Sandy Loam", "Black", "Alluvial", "Laterite"];
const SEASONS = ["Kharif", "Rabi", "Zaid", "Annual"];

const DEFAULTS = {
  soil_type: "Loamy", soil_ph: 6.5, nitrogen: 80, phosphorus: 45, potassium: 45,
  temperature: 26, humidity: 65, rainfall: 100, season: "Kharif", district: "", state: "",
};

export default function CropRecommendation() {
  const [form, setForm] = useState(DEFAULTS);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [noSoilTest, setNoSoilTest] = useState(false);
  const [soilDefaults, setSoilDefaults] = useState({});

  useEffect(() => {
    api.get("/api/crop/soil-defaults").then((res) => setSoilDefaults(res.data)).catch(() => {});
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "state") {
      setForm((prev) => ({ ...prev, state: value, district: "" }));
      return;
    }
    setForm((prev) => {
      const next = { ...prev, [name]: value };
      if (noSoilTest && name === "soil_type" && soilDefaults[value]) {
        const d = soilDefaults[value];
        next.nitrogen = d.N; next.phosphorus = d.P; next.potassium = d.K; next.soil_ph = d.ph;
      }
      return next;
    });
  };

  const toggleNoSoilTest = () => {
    const turningOn = !noSoilTest;
    setNoSoilTest(turningOn);
    if (turningOn && soilDefaults[form.soil_type]) {
      const d = soilDefaults[form.soil_type];
      setForm((prev) => ({ ...prev, nitrogen: d.N, phosphorus: d.P, potassium: d.K, soil_ph: d.ph }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = {
        ...form,
        soil_ph: parseFloat(form.soil_ph), nitrogen: parseFloat(form.nitrogen),
        phosphorus: parseFloat(form.phosphorus), potassium: parseFloat(form.potassium),
        temperature: parseFloat(form.temperature), humidity: parseFloat(form.humidity),
        rainfall: parseFloat(form.rainfall),
      };
      const res = await api.post("/api/crop/recommend", payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate recommendation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar title="Crop Recommendation" subtitle="Enter soil & climate data to find the best-suited crops" />

        <div className="crop-rec-grid">
          <div className="glass-card animate-in crop-form-card">
            <form onSubmit={handleSubmit} className="farm-form-grid">
              <div>
                <label>Soil Type</label>
                <select name="soil_type" value={form.soil_type} onChange={handleChange}>
                  {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>Season</label>
                <select name="season" value={form.season} onChange={handleChange}>
                  {SEASONS.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>Soil pH</label>
                <input name="soil_ph" type="number" step="0.1" min="0" max="14" value={form.soil_ph} onChange={handleChange} disabled={noSoilTest} />
              </div>

              <div className="soil-toggle-row">
                <label className="toggle-switch">
                  <input type="checkbox" checked={noSoilTest} onChange={toggleNoSoilTest} />
                  <span className="toggle-slider" />
                </label>
                <span>I don't have a Soil Test Report (auto-fill typical values for {form.soil_type})</span>
              </div>

              {!noSoilTest && (
                <>
                  <div>
                    <label>Nitrogen (N, kg/ha)</label>
                    <input name="nitrogen" type="number" value={form.nitrogen} onChange={handleChange} />
                  </div>
                  <div>
                    <label>Phosphorus (P, kg/ha)</label>
                    <input name="phosphorus" type="number" value={form.phosphorus} onChange={handleChange} />
                  </div>
                  <div>
                    <label>Potassium (K, kg/ha)</label>
                    <input name="potassium" type="number" value={form.potassium} onChange={handleChange} />
                  </div>
                </>
              )}
              <div>
                <label>Temperature (°C)</label>
                <input name="temperature" type="number" value={form.temperature} onChange={handleChange} />
              </div>
              <div>
                <label>Humidity (%)</label>
                <input name="humidity" type="number" value={form.humidity} onChange={handleChange} />
              </div>
              <div>
                <label>Rainfall (mm)</label>
                <input name="rainfall" type="number" value={form.rainfall} onChange={handleChange} />
              </div>
              <div>
                <label>State (optional)</label>
                <select name="state" value={form.state} onChange={handleChange}>
                  <option value="">Select state</option>
                  {INDIAN_STATES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>District (optional)</label>
                <select name="district" value={form.district} onChange={handleChange} disabled={!form.state}>
                  <option value="">{form.state ? "Select district" : "Select state first"}</option>
                  {getDistricts(form.state).map((d) => <option key={d} value={d}>{d}</option>)}
                </select>
              </div>

              <div className="farm-form-actions">
                <button className="btn-primary" type="submit" disabled={loading}>
                  {loading ? "Analyzing..." : "Get Recommendation"}
                </button>
              </div>
            </form>
            {error && <div className="alert-error">{error}</div>}
          </div>

          <div className="glass-card animate-in crop-result-card">
            <h3>Recommended Crops</h3>
            {loading && <Loader text="Running crop recommendation model..." />}
            {!loading && !result && <p className="empty-hint">Fill the form and submit to see top crop matches.</p>}
            {result && (
              <div className="crop-result-list">
                {result.results.map((r, i) => (
                  <div key={r.crop} className={`crop-result-item ${i === 0 ? "top-pick" : ""}`}>
                    <div className="crop-result-head">
                      <span className="crop-rank"><FiTrendingUp /> #{i + 1}</span>
                      <span className="crop-name">{r.crop}</span>
                      <span className="crop-confidence">{r.confidence}%</span>
                    </div>
                    <div className="crop-confidence-bar">
                      <div className="crop-confidence-fill" style={{ width: `${r.confidence}%` }} />
                    </div>
                    <div className="crop-meta">
                      <span className={r.season_match ? "match-yes" : "match-no"}>
                        {r.season_match ? "✓" : "✗"} Season: {r.suitable_seasons.join(", ")}
                      </span>
                      <span className={r.soil_match ? "match-yes" : "match-no"}>
                        {r.soil_match ? "✓" : "✗"} Soil: {r.suitable_soils.join(", ")}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
