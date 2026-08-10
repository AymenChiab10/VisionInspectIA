// Role : Zone de suppression de compte, avec confirmation forte
// (saisie du mot "DELETE" avant que le bouton final ne soit actif).

import { useState } from "react";
import { AlertTriangle, Trash2 } from "lucide-react";
import Button from "../common/Button";

export default function DeleteAccountSection({ onConfirm, submitting }) {
  const [expanded, setExpanded] = useState(false);
  const [confirmText, setConfirmText] = useState("");

  const canConfirm = confirmText.trim().toUpperCase() === "DELETE";

  return (
    <div className="card danger-zone">
      <h2>
        <AlertTriangle size={16} style={{ verticalAlign: "-3px", marginRight: 6 }} />
        Danger zone
      </h2>
      <p className="settings-hint">
        Permanently delete your account and all associated inspections. This action cannot be undone.
      </p>

      {!expanded ? (
        <Button variant="danger" onClick={() => setExpanded(true)}>
          <Trash2 size={15} />
          Delete account
        </Button>
      ) : (
        <div className="confirm-delete-box">
          <p style={{ margin: 0, fontSize: 13.5 }}>
            Type <strong>DELETE</strong> to confirm.
          </p>
          <input
            type="text"
            value={confirmText}
            onChange={(event) => setConfirmText(event.target.value)}
            placeholder="DELETE"
          />
          <div style={{ display: "flex", gap: 10 }}>
            <Button variant="danger" disabled={!canConfirm} loading={submitting} onClick={onConfirm}>
              Confirm deletion
            </Button>
            <Button
              variant="secondary"
              onClick={() => {
                setExpanded(false);
                setConfirmText("");
              }}
            >
              Cancel
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
