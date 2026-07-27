const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, { method = "GET", body } = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("full_name");
    window.location.href = "/login";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    let detail = "Request failed";
    try {
      const errBody = await res.json();
      detail = errBody.detail || detail;
    } catch (_) {}
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  login: (username, password) =>
    request("/api/login", { method: "POST", body: { username, password } }),
  profile: () => request("/api/profile"),

  dashboard: () => request("/api/dashboard"),
  todaysSchedule: () => request("/api/dashboard/today"),

  listDoctors: (search = "") => request(`/api/doctors${search ? `?search=${encodeURIComponent(search)}` : ""}`),
  createDoctor: (data) => request("/api/doctors", { method: "POST", body: data }),
  updateDoctor: (id, data) => request(`/api/doctors/${id}`, { method: "PUT", body: data }),
  deleteDoctor: (id) => request(`/api/doctors/${id}`, { method: "DELETE" }),

  listPatients: (search = "") => request(`/api/patients${search ? `?search=${encodeURIComponent(search)}` : ""}`),
  createPatient: (data) => request("/api/patients", { method: "POST", body: data }),
  updatePatient: (id, data) => request(`/api/patients/${id}`, { method: "PUT", body: data }),
  deletePatient: (id) => request(`/api/patients/${id}`, { method: "DELETE" }),

  listAppointments: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/appointments${qs ? `?${qs}` : ""}`);
  },
  createAppointment: (data) => request("/api/appointments", { method: "POST", body: data }),
  updateAppointment: (id, data) => request(`/api/appointments/${id}`, { method: "PUT", body: data }),
  cancelAppointment: (id) => request(`/api/appointments/${id}`, { method: "DELETE" }),
};
