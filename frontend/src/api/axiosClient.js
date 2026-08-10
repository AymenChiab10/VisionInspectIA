// Role : Instance Axios centralisee (base URL, injection du token JWT).

import axios from "axios";

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

// Origine du backend (sans le prefixe /api/v1), utilisee pour construire
// les URLs des images servies statiquement (voir components/history).
export const API_ORIGIN = API_URL.replace(/\/api\/v1\/?$/, "");

const axiosClient = axios.create({
  baseURL: API_URL,
});

// Attache automatiquement le JWT (s'il existe) a chaque requete.
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Si le token n'est plus valide (expire, invalide), on nettoie la session
// et on renvoie l'utilisateur vers la page de connexion. On ignore le cas
// du login lui-meme, qui renvoie normalement 401 pour un mauvais mot de passe.
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginRequest = error.config?.url?.includes("/auth/login");
    if (error.response?.status === 401 && !isLoginRequest) {
      localStorage.removeItem("token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Transforme une erreur Axios en message affichable a l'utilisateur.
// Les messages du backend (app/services/*.py) sont deja rediges pour un
// utilisateur final ; on ne montre jamais une erreur technique brute.
export function getErrorMessage(error) {
  const detail = error?.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (!error?.response) {
    return "Impossible de contacter le serveur. Verifiez votre connexion.";
  }

  return "Une erreur est survenue. Veuillez reessayer.";
}

export default axiosClient;
