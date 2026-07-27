import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const emptyForm = { doctor_name: "", specialization: "", phone: "", email: "", experience: "", availability: "" };

export default function Doctors() {
  const { role } = useAuth();
  const canEdit = role === "admin";
  const [doctors, setDoctors] = useState([]);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  async function load() {
    try {
      setDoctors(await api.listDoctors(search));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => { load(); }, [search]);

  function startEdit(doc) {
    setEditingId(doc.doctor_id);
    setForm({ ...doc, experience: doc.experience ?? "" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    const payload = { ...form, experience: form.experience === "" ? null : Number(form.experience) };
    try {
      if (editingId) {
        await api.updateDoctor(editingId, payload);
      } else {
        await api.createDoctor(payload);
      }
      resetForm();
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this doctor?")) return;
    try {
      await api.deleteDoctor(id);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h1>Doctors</h1>
      {error && <div className="alert-error">{error}</div>}

      <input
        className="search-box"
        placeholder="Search doctors by name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {canEdit && (
        <form className="inline-form" onSubmit={handleSubmit}>
          <input placeholder="Name" required value={form.doctor_name}
                 onChange={(e) => setForm({ ...form, doctor_name: e.target.value })} />
          <input placeholder="Specialization" required value={form.specialization}
                 onChange={(e) => setForm({ ...form, specialization: e.target.value })} />
          <input placeholder="Phone" value={form.phone || ""}
                 onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <input placeholder="Email" value={form.email || ""}
                 onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input placeholder="Experience (yrs)" type="number" value={form.experience}
                 onChange={(e) => setForm({ ...form, experience: e.target.value })} />
          <input placeholder="Availability" value={form.availability || ""}
                 onChange={(e) => setForm({ ...form, availability: e.target.value })} />
          <button type="submit">{editingId ? "Update Doctor" : "Add Doctor"}</button>
          {editingId && <button type="button" onClick={resetForm}>Cancel</button>}
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Name</th><th>Specialization</th><th>Phone</th><th>Email</th>
            <th>Experience</th><th>Availability</th>{canEdit && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {doctors.map((d) => (
            <tr key={d.doctor_id}>
              <td>{d.doctor_name}</td>
              <td>{d.specialization}</td>
              <td>{d.phone}</td>
              <td>{d.email}</td>
              <td>{d.experience}</td>
              <td>{d.availability}</td>
              {canEdit && (
                <td>
                  <button onClick={() => startEdit(d)}>Edit</button>
                  <button onClick={() => handleDelete(d.doctor_id)}>Delete</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
