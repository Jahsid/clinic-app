import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const emptyForm = { patient_id: "", doctor_id: "", appointment_date: "", appointment_time: "", reason: "" };

export default function Appointments() {
  const { role } = useAuth();
  const canBook = role === "admin" || role === "receptionist";
  const canUpdateStatus = role === "admin" || role === "receptionist" || role === "doctor";

  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [filters, setFilters] = useState({ appointment_date: "", status_filter: "" });
  const [error, setError] = useState("");

  async function loadAppointments() {
    try {
      const params = {};
      if (filters.appointment_date) params.appointment_date = filters.appointment_date;
      if (filters.status_filter) params.status_filter = filters.status_filter;
      setAppointments(await api.listAppointments(params));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    api.listDoctors().then(setDoctors).catch((e) => setError(e.message));
    api.listPatients().then(setPatients).catch((e) => setError(e.message));
  }, []);

  useEffect(() => { loadAppointments(); }, [filters]);

  async function handleBook(e) {
    e.preventDefault();
    setError("");
    try {
      await api.createAppointment({
        ...form,
        patient_id: Number(form.patient_id),
        doctor_id: Number(form.doctor_id),
      });
      setForm(emptyForm);
      loadAppointments();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleStatusChange(id, status) {
    try {
      await api.updateAppointment(id, { status });
      loadAppointments();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCancel(id) {
    if (!confirm("Cancel this appointment?")) return;
    try {
      await api.cancelAppointment(id);
      loadAppointments();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h1>Appointments</h1>
      {error && <div className="alert-error">{error}</div>}

      {canBook && (
        <form className="inline-form" onSubmit={handleBook}>
          <select required value={form.patient_id} onChange={(e) => setForm({ ...form, patient_id: e.target.value })}>
            <option value="">Select Patient</option>
            {patients.map((p) => <option key={p.patient_id} value={p.patient_id}>{p.patient_name}</option>)}
          </select>
          <select required value={form.doctor_id} onChange={(e) => setForm({ ...form, doctor_id: e.target.value })}>
            <option value="">Select Doctor</option>
            {doctors.map((d) => <option key={d.doctor_id} value={d.doctor_id}>{d.doctor_name}</option>)}
          </select>
          <input type="date" required value={form.appointment_date}
                 onChange={(e) => setForm({ ...form, appointment_date: e.target.value })} />
          <input type="time" required value={form.appointment_time}
                 onChange={(e) => setForm({ ...form, appointment_time: e.target.value })} />
          <input placeholder="Reason" value={form.reason}
                 onChange={(e) => setForm({ ...form, reason: e.target.value })} />
          <button type="submit">Book Appointment</button>
        </form>
      )}

      <div className="filters">
        <input type="date" value={filters.appointment_date}
               onChange={(e) => setFilters({ ...filters, appointment_date: e.target.value })} />
        <select value={filters.status_filter}
                onChange={(e) => setFilters({ ...filters, status_filter: e.target.value })}>
          <option value="">All Statuses</option>
          <option value="Scheduled">Scheduled</option>
          <option value="Completed">Completed</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>Date</th><th>Time</th><th>Patient</th><th>Doctor</th>
            <th>Reason</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map((a) => (
            <tr key={a.appointment_id}>
              <td>{a.appointment_date}</td>
              <td>{a.appointment_time}</td>
              <td>{a.patient_name}</td>
              <td>{a.doctor_name}</td>
              <td>{a.reason}</td>
              <td><span className={`status status-${a.status.toLowerCase()}`}>{a.status}</span></td>
              <td>
                {canUpdateStatus && a.status === "Scheduled" && (
                  <button onClick={() => handleStatusChange(a.appointment_id, "Completed")}>Mark Completed</button>
                )}
                {canBook && a.status !== "Cancelled" && (
                  <button onClick={() => handleCancel(a.appointment_id)}>Cancel</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
