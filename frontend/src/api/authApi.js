// Role : Appels API lies a l'authentification.

import axiosClient from "./axiosClient";

export function login(email, password) {
  return axiosClient.post("/auth/login", { email, password }).then((res) => res.data);
}

export function register(firstName, lastName, email, password) {
  return axiosClient
    .post("/auth/register", {
      first_name: firstName,
      last_name: lastName,
      email,
      password,
    })
    .then((res) => res.data);
}

export function logout() {
  return axiosClient.post("/auth/logout").then((res) => res.data);
}

export function getMe() {
  return axiosClient.get("/auth/me").then((res) => res.data);
}
