// Role : Barre de navigation principale (pages privees), fixe en haut de l'ecran.

import { NavLink, useNavigate } from "react-router-dom";
import { Eye, LayoutDashboard, LogOut, ScanLine, History, UserCircle } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";
import { logout as logoutApi } from "../../api/authApi";
import Button from "./Button";
import ThemeToggle from "./ThemeToggle";
import NotificationBell from "./NotificationBell";

export default function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    try {
      await logoutApi();
    } catch {
      // Le logout cote backend ne fait que verifier le JWT ; meme si
      // l'appel echoue (token deja expire, par exemple), on deconnecte
      // quand meme l'utilisateur localement.
    }
    logout();
    navigate("/login", { replace: true });
  }

  const linkClass = ({ isActive }) => `nav-link${isActive ? " active" : ""}`;

  return (
    <nav className="navbar">
      <NavLink to="/dashboard" className="navbar-brand">
        <span className="brand-icon">
          <Eye size={18} />
        </span>
        VisionInspect AI
      </NavLink>

      <div className="navbar-links">
        <NavLink to="/dashboard" className={linkClass}>
          <LayoutDashboard size={16} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/upload" className={linkClass}>
          <ScanLine size={16} />
          <span>Prediction</span>
        </NavLink>
        <NavLink to="/history" className={linkClass}>
          <History size={16} />
          <span>History</span>
        </NavLink>
        <NavLink to="/profile" className={linkClass}>
          <UserCircle size={16} />
          <span>Profile</span>
        </NavLink>
        <NotificationBell />
        <ThemeToggle />
        <Button variant="danger" size="sm" onClick={handleLogout}>
          <LogOut size={14} />
          Logout
        </Button>
      </div>
    </nav>
  );
}
