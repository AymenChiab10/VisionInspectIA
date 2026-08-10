// Role : Appels API de gestion du compte (profil, mot de passe, suppression).

import axiosClient from "./axiosClient";

export function updateProfile(firstName, lastName, email) {
  return axiosClient
    .put("/users/me", { first_name: firstName, last_name: lastName, email })
    .then((res) => res.data);
}

export function updatePassword(currentPassword, newPassword) {
  return axiosClient
    .put("/users/me/password", { current_password: currentPassword, new_password: newPassword })
    .then((res) => res.data);
}

export function deleteAccount() {
  return axiosClient.delete("/users/me").then((res) => res.data);
}
