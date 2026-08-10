// Role : Affichage du resultat d'une prediction (image, classe, confiance,
// date, modele, temps d'inference et temps total).

import Badge from "../common/Badge";

export default function PredictionResult({ result, previewUrl, totalTimeMs }) {
  if (!result) {
    return null;
  }

  return (
    <div className={`card result-card result-${result.predicted_class} slide-up`}>
      {previewUrl && <img src={previewUrl} alt="Inspected bottle" className="result-image" />}

      <div>
        <p className="result-label">Prediction result</p>
        <Badge predictedClass={result.predicted_class} />

        <p className="result-confidence">
          Confidence : <strong>{(result.confidence * 100).toFixed(2)} %</strong>
        </p>

        <ul className="profile-list" style={{ marginTop: 14 }}>
          <li>
            <span className="field-label">Model</span>
            <span className="field-value">MobileNetV2</span>
          </li>
          {typeof result.inference_time_ms === "number" && (
            <li>
              <span className="field-label">Inference time</span>
              <span className="field-value">{result.inference_time_ms.toFixed(2)} ms</span>
            </li>
          )}
          {typeof totalTimeMs === "number" && (
            <li>
              <span className="field-label">Total time</span>
              <span className="field-value">{totalTimeMs.toFixed(0)} ms</span>
            </li>
          )}
          <li>
            <span className="field-label">Date</span>
            <span className="field-value">{new Date(result.created_at).toLocaleString("en-US")}</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
