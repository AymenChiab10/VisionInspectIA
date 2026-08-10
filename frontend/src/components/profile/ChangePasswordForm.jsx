// Role : Formulaire de changement de mot de passe.

import { useState } from "react";
import { Lock } from "lucide-react";
import Button from "../common/Button";
import Alert from "../common/Alert";

export default function ChangePasswordForm({ onSubmit, submitting }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [mismatchError, setMismatchError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (newPassword !== confirmPassword) {
      setMismatchError("New passwords do not match.");
      return;
    }

    setMismatchError("");
    onSubmit(currentPassword, newPassword);
    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <Alert type="error">{mismatchError}</Alert>

      <div className="form-group">
        <label htmlFor="currentPassword">Current password</label>
        <div className="input-wrap">
          <Lock size={16} />
          <input
            id="currentPassword"
            type="password"
            placeholder="••••••••"
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="newPassword">New password</label>
        <div className="input-wrap">
          <Lock size={16} />
          <input
            id="newPassword"
            type="password"
            placeholder="••••••••"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            required
            minLength={6}
            maxLength={72}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="confirmNewPassword">Confirm new password</label>
        <div className="input-wrap">
          <Lock size={16} />
          <input
            id="confirmNewPassword"
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            required
            minLength={6}
            maxLength={72}
          />
        </div>
      </div>

      <Button type="submit" variant="secondary" loading={submitting}>
        {submitting ? "Updating..." : "Update password"}
      </Button>
    </form>
  );
}
