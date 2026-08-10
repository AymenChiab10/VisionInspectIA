// Role : Hook d'acces au contexte d'authentification (AuthContext).

import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth doit etre utilise a l'interieur d'un AuthProvider.");
  }

  return context;
}
