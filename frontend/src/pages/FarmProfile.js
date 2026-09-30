import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import api from "../api/api";
import { INDIAN_STATES, getDistricts } from "../data/indiaLocations";

const SOIL_TYPES = ["Loamy", "Clay", "Sandy", "Sandy Loam", "Black", "Alluvial", "Laterite"];
const IRRIGATION_SOURCES = ["Borewell", "Canal", "River", "Rain-fed", "Drip Irrigation", "Sprinkler", "Well"];

export default function FarmProfile() {
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.get("/api/farm-profile/").then((res) => setForm(res.data)).finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    setSaved(false);
    const { name, value } = e.target;
    if (name === "state") {
      setForm({ ...form, state: value, district: "" }); // reset district when state changes
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        farm_name: form.farm_name || null,
        land_area_acres: form.land_area_acres ? parseFloat(form.land_area_acres) : null,
        soil_type: form.soil_type || null,
        soil_ph: form.soil_ph ? parseFloat(form.soil_ph) : null,
        irrigation_source: form.irrigation_source || null,
        district: form.district || null,
        state: form.state || null,
        primary_crop: form.primary_crop || null,
      };
      const res = await api.put("/api/farm-profile/", payload);
      setForm(res.data);
      setSaved(true);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Topbar title="Farm Profile" subtitle="Farm details help personalize crop and risk recommendations" />

        {loading || !form ? <Loader text="Loading farm profile..." /> : (
          <div className="glass-card animate-in farm-form-card">
            <form onSubmit={handleSave} className="farm-form-grid">
              <div>
                <label>Farm Name</label>
                <input name="farm_name" placeholder="e.g. Patil Family Farm" value={form.farm_name || ""} onChange={handleChange} />
              </div>
              <div>
                <label>Land Area (acres)</label>
                <input name="land_area_acres" type="number" step="0.1" placeholder="e.g. 5.5" value={form.land_area_acres || ""} onChange={handleChange} />
              </div>
              <div>
                <label>Soil Type</label>
                <select name="soil_type" value={form.soil_type || ""} onChange={handleChange}>
                  <option value="">Select soil type</option>
                  {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>Soil pH</label>
                <input name="soil_ph" type="number" step="0.1" min="0" max="14" placeholder="e.g. 6.5" value={form.soil_ph || ""} onChange={handleChange} />
              </div>
              <div>
                <label>Irrigation Source</label>
                <select name="irrigation_source" value={form.irrigation_source || ""} onChange={handleChange}>
                  <option value="">Select source</option>
                  {IRRIGATION_SOURCES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>Primary Crop</label>
                <input name="primary_crop" placeholder="e.g. Tomato" value={form.primary_crop || ""} onChange={handleChange} />
              </div>
              <div>
                <label>State</label>
                <select name="state" value={form.state || ""} onChange={handleChange}>
                  <option value="">Select state</option>
                  {INDIAN_STATES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>District</label>
                <select name="district" value={form.district || ""} onChange={handleChange} disabled={!form.state}>
                  <option value="">{form.state ? "Select district" : "Select state first"}</option>
                  {getDistricts(form.state).map((d) => <option key={d} value={d}>{d}</option>)}
                </select>
              </div>

              <div className="farm-form-actions">
                {saved && <span className="alert-success" style={{ marginRight: 12 }}>Saved!</span>}
                <button className="btn-primary" type="submit" disabled={saving}>
                  {saving ? "Saving..." : "Save Farm Profile"}
                </button>
              </div>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
