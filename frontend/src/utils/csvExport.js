// Role : Export CSV de l'historique, genere entierement cote client
// (meme approche que le telechargement PDF : Blob + lien temporaire).

function escapeCsvField(value) {
  const stringValue = String(value ?? "");
  if (/[",\n]/.test(stringValue)) {
    return `"${stringValue.replace(/"/g, '""')}"`;
  }
  return stringValue;
}

export function exportInspectionsToCsv(inspections, userName) {
  const header = ["Date", "Prediction", "Confidence", "Image", "User"];

  const rows = inspections.map((inspection) => [
    new Date(inspection.created_at).toLocaleString("en-US"),
    inspection.predicted_class,
    `${(inspection.confidence * 100).toFixed(2)}%`,
    inspection.image_path.split("/").pop(),
    userName,
  ]);

  const csvContent = [header, ...rows]
    .map((row) => row.map(escapeCsvField).join(","))
    .join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `inspections_history_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
