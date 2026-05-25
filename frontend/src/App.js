import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import axios from "axios";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [stats, setStats] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/stats`),
      axios.get(`${API}/anomalies?limit=100`)
    ]).then(([s, a]) => {
      setStats(s.data);
      setAnomalies(a.data);
      setLoading(false);
    });
  }, []);

  const filtered = anomalies.filter(a =>
    a.provider_id?.toString().includes(search) ||
    a.billing_code?.includes(search) ||
    a.explanation?.toLowerCase().includes(search.toLowerCase())
  );

  const chartData = stats ? Object.entries(stats.top_billing_codes).map(([code, count]) => ({
    code, count
  })) : [];

  if (loading) return <div style={styles.loading}>Loading anomaly data...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Medicaid Billing Anomaly Detection Platform</h1>
        <p style={styles.subtitle}>AI-powered analysis of 238M+ public Medicaid claims</p>
      </div>
      <div style={styles.statsRow}>
        <StatCard title="Anomalies Flagged" value={stats.total_anomalies.toLocaleString()} color="#ef4444" />
        <StatCard title="Unknown Providers" value={stats.unknown_providers.toLocaleString()} color="#f97316" />
        <StatCard title="Avg Patients Flagged" value={Math.round(stats.avg_patients_flagged).toLocaleString()} color="#eab308" />
        <StatCard title="Total Paid (Flagged)" value={`$${(stats.total_paid_flagged / 1e12).toFixed(1)}T`} color="#8b5cf6" />
      </div>
      <div style={styles.chartBox}>
        <h2 style={styles.sectionTitle}>Top Anomalous Billing Codes</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <XAxis dataKey="code" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6">
              {chartData.map((_, i) => <Cell key={i} fill={["#3b82f6","#ef4444","#f97316","#eab308","#8b5cf6"][i]} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div style={styles.tableBox}>
        <h2 style={styles.sectionTitle}>Flagged Providers</h2>
        <input
          style={styles.search}
          placeholder="Search by provider ID, billing code, or reason..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <table style={styles.table}>
          <thead>
            <tr>
              {["Provider ID","Billing Code","Total Patients","Total Paid","Anomaly Score","Explanation"].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, 50).map((a, i) => (
              <tr key={i} style={i % 2 === 0 ? styles.trEven : styles.trOdd}>
                <td style={styles.td}>{a.provider_id === "Unknown" ? "Unknown" : a.provider_id}</td>
                <td style={styles.td}>{a.billing_code}</td>
                <td style={styles.td}>{Number(a.total_patients).toLocaleString()}</td>
                <td style={styles.td}>${Number(a.total_paid).toLocaleString()}</td>
                <td style={styles.td}>{Number(a.anomaly_probability).toFixed(3)}</td>
                <td style={{...styles.td, fontSize: "11px", color: "#6b7280"}}>{a.explanation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div style={{...styles.card, borderTop: `4px solid ${color}`}}>
      <div style={{...styles.cardValue, color}}>{value}</div>
      <div style={styles.cardTitle}>{title}</div>
    </div>
  );
}

const styles = {
  container: { fontFamily: "sans-serif", backgroundColor: "#f9fafb", minHeight: "100vh", padding: "24px" },
  header: { textAlign: "center", marginBottom: "32px" },
  title: { fontSize: "24px", fontWeight: "bold", color: "#111827", margin: 0 },
  subtitle: { color: "#6b7280", marginTop: "8px" },
  statsRow: { display: "flex", gap: "16px", marginBottom: "24px", flexWrap: "wrap" },
  card: { flex: 1, minWidth: "180px", backgroundColor: "white", borderRadius: "8px", padding: "20px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" },
  cardValue: { fontSize: "28px", fontWeight: "bold" },
  cardTitle: { color: "#6b7280", fontSize: "14px", marginTop: "4px" },
  chartBox: { backgroundColor: "white", borderRadius: "8px", padding: "24px", marginBottom: "24px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" },
  tableBox: { backgroundColor: "white", borderRadius: "8px", padding: "24px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" },
  sectionTitle: { fontSize: "18px", fontWeight: "600", marginBottom: "16px", color: "#111827" },
  search: { width: "100%", padding: "10px", borderRadius: "6px", border: "1px solid #d1d5db", marginBottom: "16px", fontSize: "14px", boxSizing: "border-box" },
  table: { width: "100%", borderCollapse: "collapse", fontSize: "13px" },
  th: { backgroundColor: "#f3f4f6", padding: "10px 12px", textAlign: "left", fontWeight: "600", color: "#374151", borderBottom: "1px solid #e5e7eb" },
  td: { padding: "10px 12px", borderBottom: "1px solid #f3f4f6", color: "#374151" },
  trEven: { backgroundColor: "white" },
  trOdd: { backgroundColor: "#f9fafb" },
  loading: { display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", fontSize: "18px", color: "#6b7280" }
};
