// Role : Appels API des statistiques / dashboard.

import axiosClient from "./axiosClient";

export function getStatistics() {
  return axiosClient.get("/dashboard/statistics").then((res) => res.data);
}
