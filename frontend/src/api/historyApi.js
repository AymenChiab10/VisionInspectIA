// Role : Appels API de l'historique des inspections.

import axiosClient from "./axiosClient";

export function getHistory() {
  return axiosClient.get("/history").then((res) => res.data);
}

export function getInspection(id) {
  return axiosClient.get(`/history/${id}`).then((res) => res.data);
}

export function deleteInspection(id) {
  return axiosClient.delete(`/history/${id}`).then((res) => res.data);
}
