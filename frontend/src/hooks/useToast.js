// Role : Hook d'acces au systeme de notifications toast.

import { useContext } from "react";
import { ToastContext } from "../context/ToastContext";

export function useToast() {
  const context = useContext(ToastContext);

  if (!context) {
    throw new Error("useToast doit etre utilise a l'interieur d'un ToastProvider.");
  }

  return context;
}
