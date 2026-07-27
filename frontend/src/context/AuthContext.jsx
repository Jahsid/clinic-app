import { createContext, useContext, useState } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(() => ({
    token: localStorage.getItem("token"),
    role: localStorage.getItem("role"),
    fullName: localStorage.getItem("full_name"),
  }));

  async function login(username, password) {
    const data = await api.login(username, password);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    localStorage.setItem("full_name", data.full_name);
    setAuth({ token: data.access_token, role: data.role, fullName: data.full_name });
    return data;
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("full_name");
    setAuth({ token: null, role: null, fullName: null });
  }

  return (
    <AuthContext.Provider value={{ ...auth, login, logout, isAuthenticated: !!auth.token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
