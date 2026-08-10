// Role : Contenu de la modal de detail d'une inspection (image, classe,
// confiance, date, fichier, utilisateur, telechargement PDF).
// Reutilisee depuis History et depuis la Galerie du Dashboard.

import Modal from "../common/Modal";
import Badge from "../common/Badge";
import DownloadReportButton from "../report/DownloadReportButton";
import { API_ORIGIN } from "../../api/axiosClient";

export default function InspectionDetailsModal({ inspection, userName, onClose }) {
  return (
    <Modal open={Boolean(inspection)} onClose={onClose} title="Inspection details">
      {inspection && (
        <div className="inspection-details">
          <img
            src={`${API_ORIGIN}/${inspection.image_path}`}
            alt={`Inspection ${inspection.id}`}
            className="inspection-details-image"
          />

          <div className="inspection-details-info">
            <Badge predictedClass={inspection.predicted_class} />

            <ul className="profile-list">
              <li>
                <span className="field-label">Confidence</span>
                <span className="field-value">{(inspection.confidence * 100).toFixed(2)} %</span>
              </li>
              <li>
                <span className="field-label">Date</span>
                <span className="field-value">{new Date(inspection.created_at).toLocaleString("en-US")}</span>
              </li>
              <li>
                <span className="field-label">File name</span>
                <span className="field-value">{inspection.image_path.split("/").pop()}</span>
              </li>
              <li>
                <span className="field-label">User</span>
                <span className="field-value">{userName}</span>
              </li>
            </ul>

            <DownloadReportButton inspectionId={inspection.id} />
          </div>
        </div>
      )}
    </Modal>
  );
}
