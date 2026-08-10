// Role : Panneau de notifications (icone cloche + liste des evenements
// recents). Alimente par le meme ToastContext que les toasts flottants.

import { useEffect, useRef, useState } from "react";
import { Bell, CheckCheck } from "lucide-react";
import { useToast } from "../../hooks/useToast";

function timeAgo(timestamp) {
  const seconds = Math.floor((Date.now() - new Date(timestamp).getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export default function NotificationBell() {
  const { notifications, clearNotifications } = useToast();
  const [open, setOpen] = useState(false);
  const panelRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (panelRef.current && !panelRef.current.contains(event.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="notification-wrap" ref={panelRef}>
      <button
        type="button"
        className="icon-btn"
        onClick={() => setOpen((v) => !v)}
        aria-label="Notifications"
        aria-expanded={open}
      >
        <Bell size={17} />
        {notifications.length > 0 && <span className="notification-badge">{notifications.length}</span>}
      </button>

      {open && (
        <div className="notification-panel fade-in" role="menu">
          <div className="notification-panel-header">
            <span>Notifications</span>
            {notifications.length > 0 && (
              <button type="button" className="btn-ghost-link" onClick={clearNotifications}>
                <CheckCheck size={13} />
                Clear all
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <p className="notification-empty">No notifications yet.</p>
          ) : (
            <ul className="notification-list">
              {notifications.map((notification) => (
                <li key={notification.id} className={`notification-item notification-${notification.type}`}>
                  <span>{notification.message}</span>
                  <time>{timeAgo(notification.timestamp)}</time>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
