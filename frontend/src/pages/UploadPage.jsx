// Role : Page d'upload d'image et affichage du resultat de prediction.

import { useState } from "react";
import { ScanLine } from "lucide-react";
import ImageUploader from "../components/upload/ImageUploader";
import PredictionResult from "../components/upload/PredictionResult";
import Alert from "../components/common/Alert";
import Button from "../components/common/Button";
import Spinner from "../components/common/Spinner";
import ProgressBar from "../components/common/ProgressBar";
import { predictImage } from "../api/predictionApi";
import { getErrorMessage } from "../api/axiosClient";
import { useToast } from "../hooks/useToast";

export default function UploadPage() {
  const { showToast } = useToast();
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [totalTimeMs, setTotalTimeMs] = useState(null);

  function handleFileSelected(selectedFile) {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
    setTotalTimeMs(null);
    setError("");
  }

  async function handlePredict() {
    if (!file) {
      return;
    }

    setError("");
    setSubmitting(true);
    const startedAt = performance.now();
    try {
      const prediction = await predictImage(file);
      setResult(prediction);
      setTotalTimeMs(performance.now() - startedAt);
      showToast("success", "Image analyzed successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Analyze an Image</h1>
          <p className="page-subtitle">Upload a bottle photo to detect a potential defect.</p>
        </div>
      </div>

      <Alert type="error">{error}</Alert>

      <ImageUploader onFileSelected={handleFileSelected} />

      <Button onClick={handlePredict} disabled={!file} loading={submitting} style={{ marginBottom: 28 }}>
        <ScanLine size={16} />
        {submitting ? "Analyzing..." : "Analyze Image"}
      </Button>

      {submitting && (
        <div className="spinner-wrap fade-in">
          <Spinner />
          <span>Analyzing image...</span>
          <ProgressBar />
        </div>
      )}

      <PredictionResult result={result} previewUrl={previewUrl} totalTimeMs={totalTimeMs} />
    </div>
  );
}
