// Role : Appels API d'upload d'image et de prediction.

import axiosClient from "./axiosClient";

export function predictImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient
    .post("/predictions/predict", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((res) => res.data);
}
