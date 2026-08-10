// Role : Affiche les notifications toast actives, en superposition flottante.

import { AlertTriangle, CheckCircle2, Info, X, XCircle } from "lucide-react";
import { useToast } from "../../hooks/useToast";

const CONFIG = {
  success: { icon: CheckCircle2, className: "alert-success" },
  error: { icon: XCircle, className: "alert-error" },
  warning: { icon: AlertTriangle, className: "alert-warning" },
  info: { icon: Info, className: "alert-info" },
};

export default function ToastContainer() {
  const { toasts, removeToast } = useToast();

  if (toasts.length === 0) {
    return null;
  }

  return (
    <div className="toast-container">
      {toasts.map((toast) => {
        const { icon: Icon, className } = CONFIG[toast.type] || CONFIG.info;
        return (
          <div key={toast.id} className={`toast ${className}`} role="status">
            <Icon size={18} />
            <span>{toast.message}</span>
            <button type="button" className="toast-close" onClick={() => removeToast(toast.id)} aria-label="Dismiss">
              <X size={14} />
            </button>
          </div>
        );
      })}
    </div>
  );
}
