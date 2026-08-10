// Role : Message uniforme (success / error / warning / info) avec icone.

import { AlertTriangle, CheckCircle2, Info, XCircle } from "lucide-react";

const CONFIG = {
  success: { icon: CheckCircle2, className: "alert-success" },
  error: { icon: XCircle, className: "alert-error" },
  warning: { icon: AlertTriangle, className: "alert-warning" },
  info: { icon: Info, className: "alert-info" },
};

export default function Alert({ type = "info", children }) {
  if (!children) {
    return null;
  }

  const { icon: Icon, className } = CONFIG[type] || CONFIG.info;

  return (
    <div className={`alert ${className}`} role="alert">
      <Icon size={18} />
      <span>{children}</span>
    </div>
  );
}
