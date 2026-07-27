import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { fullName, role, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const linkClass = ({ isActive }) => "nav-link" + (isActive ? " nav-link-active" : "");

  return (
    <nav className="navbar">
      <div className="navbar-brand">Clinic Desk</div>
      <div className="navbar-links">
        <NavLink to="/" end className={linkClass}>Dashboard</NavLink>
        <NavLink to="/doctors" className={linkClass}>Doctors</NavLink>
        <NavLink to="/patients" className={linkClass}>Patients</NavLink>
        <NavLink to="/appointments" className={linkClass}>Appointments</NavLink>
      </div>
      <div className="navbar-user">
        <span>{fullName} ({role})</span>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}
