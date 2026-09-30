import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GiPlantSeed } from "react-icons/gi";
import api from "../api/api";
import { PlantGrowthIllustration } from "../components/Illustrations";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "", phone: "", location: "", role: "farmer" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.post("/api/auth/register", form);
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-split">
        <div className="auth-illustration-panel tilt-3d">
          <PlantGrowthIllustration style={{ width: "100%", maxWidth: 320 }} />
          <h2>Join Thousands of Farmers</h2>
          <p>Track crop health, get instant diagnoses, and grow with confidence.</p>
        </div>
        <div className="glass-card auth-card animate-in">
        <div className="auth-brand">
          <GiPlantSeed size={40} color="var(--brand-leaf)" />
          <h1>AgriPredic</h1>
        </div>
        <p className="auth-subtitle">Create your farmer account</p>

        {error && <div className="alert-error">{error}</div>}
        {success && <div className="alert-success">Account created! Redirecting to login...</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <label>Full Name</label>
          <input name="name" required placeholder="Your Name" value={form.name} onChange={handleChange} />
          <label>Email</label>
          <input name="email" type="email" required placeholder="Your Email" value={form.email} onChange={handleChange} />
          <label>Phone</label>
          <input name="phone" placeholder="+91" value={form.phone} onChange={handleChange} />
          <label>Farm Location</label>
          <input name="location" placeholder="Your Location" value={form.location} onChange={handleChange} />
          <label>I am registering as</label>
          <select name="role" value={form.role} onChange={handleChange}>
            <option value="farmer">Farmer</option>
            <option value="expert">Agriculture Expert</option>
          </select>
          <label>Password</label>
          <input name="password" type="password" required placeholder="*******" value={form.password} onChange={handleChange} />
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
        </div>
      </div>
    </div>
  );
}
