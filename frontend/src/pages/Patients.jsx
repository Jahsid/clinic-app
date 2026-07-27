import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const emptyForm = { patient_name: "", age: "", gender: "", phone: "", email: "", address: "", blood_group: "" };

export default function Patients() {
  const { role } = useAuth();
  const canEdit = role === "admin" || role === "receptionist";
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  async function load() {
    try {
      setPatients(await api.listPatients(search));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => { load(); }, [search]);

  function startEdit(p) {
    setEditingId(p.patient_id);
    setForm({ ...p, age: p.age ?? "" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    const payload = { ...form, age: form.age === "" ? null : Number(form.age) };
    try {
      if (editingId) {
        await api.updatePatient(editingId, payload);
      } else {
        await api.createPatient(payload);
      }
      resetForm();
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this patient?")) return;
    try {
      await api.deletePatient(id);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h1>Patients</h1>
      {error && <div className="alert-error">{error}</div>}

      <input
        className="search-box"
        placeholder="Search patients by name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {canEdit && (
        <form className="inline-form" onSubmit={handleSubmit}>
          <input placeholder="Name" required value={form.patient_name}
                 onChange={(e) => setForm({ ...form, patient_name: e.target.value })} />
          <input placeholder="Age" type="number" value={form.age}
                 onChange={(e) => setForm({ ...form, age: e.target.value })} />
          <select value={form.gender || ""} onChange={(e) => setForm({ ...form, gender: e.target.value })}>
            <option value="">Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
          <input placeholder="Phone" value={form.phone || ""}
                 onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <input placeholder="Email" value={form.email || ""}
                 onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input placeholder="Address" value={form.address || ""}
                 onChange={(e) => setForm({ ...form, address: e.target.value })} />
          <input placeholder="Blood Group" value={form.blood_group || ""}
                 onChange={(e) => setForm({ ...form, blood_group: e.target.value })} />
          <button type="submit">{editingId ? "Update Patient" : "Register Patient"}</button>
          {editingId && <button type="button" onClick={resetForm}>Cancel</button>}
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Name</th><th>Age</th><th>Gender</th><th>Phone</th>
            <th>Blood Group</th>{canEdit && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {patients.map((p) => (
            <tr key={p.patient_id}>
              <td>{p.patient_name}</td>
              <td>{p.age}</td>
              <td>{p.gender}</td>
              <td>{p.phone}</td>
              <td>{p.blood_group}</td>
              {canEdit && (
                <td>
                  <button onClick={() => startEdit(p)}>Edit</button>
                  <button onClick={() => handleDelete(p.patient_id)}>Delete</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
