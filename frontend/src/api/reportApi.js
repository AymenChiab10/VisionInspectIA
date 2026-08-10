// Role : Appel API de telechargement du rapport PDF d'une inspection.

import axiosClient from "./axiosClient";

// Telecharge le PDF et declenche le telechargement dans le navigateur.
export function downloadReport(inspectionId) {
  return axiosClient
    .get(`/reports/${inspectionId}`, { responseType: "blob" })
    .then((response) => {
      const url = window.URL.createObjectURL(
        new Blob([response.data], { type: "application/pdf" })
      );
      const link = document.createElement("a");
      link.href = url;
      link.download = `inspection_${inspectionId}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    });
}
