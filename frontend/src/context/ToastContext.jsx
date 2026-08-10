// Role : Etat global des notifications.
//
// Un seul point d'entree (showToast) alimente a la fois :
// - les toasts flottants (auto-fermeture apres quelques secondes) ;
// - le centre de notifications (panneau persistant, cloche dans la Navbar).
// Cela evite de dupliquer les appels "notifier l'utilisateur" a chaque
// endroit de l'application (login, prediction, suppression, profil...).

import { createContext, useCallback, useState } from "react";

export const ToastContext = createContext(null);

let nextId = 1;
const MAX_NOTIFICATIONS = 20;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const [notifications, setNotifications] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const showToast = useCallback(
    (type, message, duration = 4000) => {
      const id = nextId++;

      setToasts((current) => [...current, { id, type, message }]);
      setTimeout(() => removeToast(id), duration);

      setNotifications((current) => [
        { id, type, message, timestamp: new Date().toISOString() },
        ...current,
      ].slice(0, MAX_NOTIFICATIONS));
    },
    [removeToast]
  );

  const clearNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, showToast, removeToast, notifications, clearNotifications }}>
      {children}
    </ToastContext.Provider>
  );
}
