// Role : Page profil — informations, edition, mot de passe, suppression de compte.

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BarChart3, Calendar, Mail, ShieldCheck, User } from "lucide-react";
import { useAuth } from "../hooks/useAuth";
import { useToast } from "../hooks/useToast";
import Avatar from "../components/common/Avatar";
import StatCard from "../components/dashboard/StatCard";
import EditProfileForm from "../components/profile/EditProfileForm";
import ChangePasswordForm from "../components/profile/ChangePasswordForm";
import DeleteAccountSection from "../components/profile/DeleteAccountSection";
import { updateProfile, updatePassword, deleteAccount } from "../api/usersApi";
import { getStatistics } from "../api/dashboardApi";
import { getHistory } from "../api/historyApi";
import { getErrorMessage } from "../api/axiosClient";
import { CLASS_LABELS, getFirstLastInspection, getMostDetectedClass } from "../utils/inspectionStats";

export default function ProfilePage() {
  const { user, updateUser, logout } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [savingProfile, setSavingProfile] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [stats, setStats] = useState(null);
  const [inspections, setInspections] = useState([]);

  useEffect(() => {
    Promise.all([getStatistics(), getHistory()])
      .then(([statsData, historyData]) => {
        setStats(statsData);
        setInspections(historyData);
      })
      .catch(() => {
        // Les statistiques utilisateur restent optionnelles sur cette page :
        // une erreur ici ne doit pas empecher l'edition du profil.
      });
  }, []);

  if (!user) {
    return null;
  }

  const mostDetected = getMostDetectedClass(stats);
  const { first, last } = getFirstLastInspection(inspections);

  async function handleProfileSubmit(firstName, lastName, email) {
    setSavingProfile(true);
    try {
      const updated = await updateProfile(firstName, lastName, email);
      updateUser(updated);
      showToast("success", "Profile updated successfully.");
    } catch (err) {
      showToast("error", getErrorMessage(err));
    } finally {
      setSavingProfile(false);
    }
  }

  async function handlePasswordSubmit(currentPassword, newPassword) {
    setSavingPassword(true);
    try {
      await updatePassword(currentPassword, newPassword);
      showToast("success", "Password updated successfully.");
    } catch (err) {
      showToast("error", getErrorMessage(err));
    } finally {
      setSavingPassword(false);
    }
  }

  async function handleDeleteAccount() {
    setDeleting(true);
    try {
      await deleteAccount();
      showToast("success", "Account deleted. Goodbye!");
      logout();
      navigate("/login", { replace: true });
    } catch (err) {
      showToast("error", getErrorMessage(err));
      setDeleting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Profile</h1>
          <p className="page-subtitle">Manage your account information and security.</p>
        </div>
      </div>

      <div className="card fade-in" style={{ maxWidth: 520 }}>
        <div className="profile-header">
          <Avatar firstName={user.first_name} lastName={user.last_name} size="lg" />
          <div>
            <p style={{ margin: 0, fontWeight: 700, fontSize: 17 }}>
              {user.first_name} {user.last_name}
            </p>
            <p style={{ margin: 0, color: "var(--color-text-secondary)", fontSize: 13.5 }}>{user.email}</p>
          </div>
        </div>

        <ul className="profile-list">
          <li>
            <span className="field-label">
              <User size={15} /> First name
            </span>
            <span className="field-value">{user.first_name}</span>
          </li>
          <li>
            <span className="field-label">
              <User size={15} /> Last name
            </span>
            <span className="field-value">{user.last_name}</span>
          </li>
          <li>
            <span className="field-label">
              <Mail size={15} /> Email
            </span>
            <span className="field-value">{user.email}</span>
          </li>
          <li>
            <span className="field-label">
              <ShieldCheck size={15} /> Role
            </span>
            <span className="field-value">{user.role}</span>
          </li>
          <li>
            <span className="field-label">
              <Calendar size={15} /> Created at
            </span>
            <span className="field-value">{new Date(user.created_at).toLocaleDateString("en-US")}</span>
          </li>
        </ul>
      </div>

      {stats && (
        <div className="settings-section" style={{ maxWidth: 520 }}>
          <h2 style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <BarChart3 size={16} />
            Your activity
          </h2>
          <div className="stat-grid" style={{ gridTemplateColumns: "repeat(2, 1fr)" }}>
            <StatCard label="Total Inspections" value={stats.total_inspections} icon={BarChart3} tone="primary" />
            <StatCard
              label="Most Detected"
              value={mostDetected ? CLASS_LABELS[mostDetected.key] : "—"}
              icon={BarChart3}
              tone="violet"
            />
            <StatCard label="Average Confidence" value={`${stats.average_confidence} %`} icon={BarChart3} tone="secondary" />
            <StatCard
              label="First Inspection"
              value={first ? new Date(first.created_at).toLocaleDateString("en-US") : "—"}
              icon={Calendar}
              tone="warning"
            />
            <StatCard
              label="Last Inspection"
              value={last ? new Date(last.created_at).toLocaleDateString("en-US") : "—"}
              icon={Calendar}
              tone="primary"
            />
          </div>
        </div>
      )}

      <div className="settings-section card" style={{ maxWidth: 520 }}>
        <h2>Edit profile</h2>
        <p className="settings-hint">Update your name and email address.</p>
        <EditProfileForm user={user} onSubmit={handleProfileSubmit} submitting={savingProfile} />
      </div>

      <div className="settings-section card" style={{ maxWidth: 520 }}>
        <h2>Change password</h2>
        <p className="settings-hint">Choose a new password for your account.</p>
        <ChangePasswordForm onSubmit={handlePasswordSubmit} submitting={savingPassword} />
      </div>

      <div className="settings-section" style={{ maxWidth: 520 }}>
        <DeleteAccountSection onConfirm={handleDeleteAccount} submitting={deleting} />
      </div>
    </div>
  );
}
