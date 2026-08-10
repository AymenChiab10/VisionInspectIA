// Role : Etat d'authentification global (utilisateur connecte, token).

import { createContext, useEffect, useState } from "react";
import { getMe } from "../api/authApi";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  // Tant que "loading" est vrai, on ne sait pas encore si l'utilisateur
  // est authentifie (verification du token en cours) : ProtectedRoute
  // attend cette valeur avant de decider d'une redirection.
  const [loading, setLoading] = useState(true);

  // Au chargement de l'application (montage initial / rafraichissement de
  // page), si un token existe deja (session precedente), on recupere
  // automatiquement l'utilisateur via /me. Ne s'execute qu'une seule fois :
  // apres un login interactif, loginUser() recoit deja les infos utilisateur
  // (LoginPage appelle /me elle-meme) donc un second appel serait redondant.
  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    getMe()
      .then((data) => setUser(data))
      .catch(() => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function loginUser(newToken, userData) {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(userData);
  }

  function logoutUser() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  // Met a jour l'utilisateur en memoire apres une modification de profil
  // (PUT /users/me), sans re-appeler /me ni toucher au token.
  function updateUser(userData) {
    setUser(userData);
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(token && user),
    login: loginUser,
    logout: logoutUser,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
