// Role : Bouton de telechargement du rapport PDF d'une inspection.

import { useState } from "react";
import { FileDown } from "lucide-react";
import { downloadReport } from "../../api/reportApi";
import { getErrorMessage } from "../../api/axiosClient";
import Button from "../common/Button";

export default function DownloadReportButton({ inspectionId }) {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");

  async function handleClick() {
    setDownloading(true);
    setError("");
    try {
      await downloadReport(inspectionId);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setDownloading(false);
    }
  }

  return (
    <div>
      <Button variant="secondary" size="sm" onClick={handleClick} loading={downloading}>
        <FileDown size={14} />
        PDF
      </Button>
      {error && <p style={{ color: "var(--color-danger)", fontSize: 12, marginTop: 6 }}>{error}</p>}
    </div>
  );
}
