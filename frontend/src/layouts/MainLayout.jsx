// Role : Mise en page commune aux pages privees (Navbar + contenu).

import { Outlet } from "react-router-dom";
import Navbar from "../components/common/Navbar";

export default function MainLayout() {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
}
