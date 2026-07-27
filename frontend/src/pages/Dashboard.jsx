import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [today, setToday] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [s, t] = await Promise.all([api.dashboard(), api.todaysSchedule()]);
        setSummary(s);
        setToday(t);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
  }, []);

  if (error) return <div className="alert-error">{error}</div>;
  if (!summary) return <p>Loading dashboard...</p>;

  const cards = [
    { label: "Total Doctors", value: summary.total_doctors },
    { label: "Total Patients", value: summary.total_patients },
    { label: "Total Appointments", value: summary.total_appointments },
    { label: "Today's Appointments", value: summary.todays_appointments },
    { label: "Scheduled", value: summary.scheduled_count },
    { label: "Completed", value: summary.completed_count },
    { label: "Cancelled", value: summary.cancelled_count },
  ];

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="card-grid">
        {cards.map((c) => (
          <div className="summary-card" key={c.label}>
            <div className="summary-value">{c.value}</div>
            <div className="summary-label">{c.label}</div>
          </div>
        ))}
      </div>

      <h2>Today's Schedule</h2>
      {today.length === 0 ? (
        <p>No appointments scheduled for today.</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Time</th><th>Patient</th><th>Doctor</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {today.map((a) => (
              <tr key={a.appointment_id}>
                <td>{a.appointment_time}</td>
                <td>{a.patient_name}</td>
                <td>{a.doctor_name}</td>
                <td><span className={`status status-${a.status.toLowerCase()}`}>{a.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
