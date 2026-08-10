// Role : Tableau de l'historique des inspections (image, classe, confiance, date, PDF, suppression).
// Pagination geree cote client : GET /history renvoie deja la liste complete,
// aucun changement d'API necessaire. Le clic sur une ligne ouvre la modal de
// detail (les boutons PDF/Delete stoppent la propagation pour ne pas l'ouvrir).

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import { API_ORIGIN } from "../../api/axiosClient";
import Badge from "../common/Badge";
import Button from "../common/Button";
import DownloadReportButton from "../report/DownloadReportButton";

const PAGE_SIZE = 8;

export default function HistoryTable({ inspections, onDelete, deletingId, onRowClick }) {
  const [page, setPage] = useState(1);

  // Revenir a la premiere page quand la liste filtree/triee change
  // (nouveau filtre, recherche, ou suppression).
  useEffect(() => {
    setPage(1);
  }, [inspections.length]);

  if (inspections.length === 0) {
    return <p className="spinner-wrap">No inspection matches your filters.</p>;
  }

  const pageCount = Math.max(1, Math.ceil(inspections.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount);
  const start = (currentPage - 1) * PAGE_SIZE;
  const visible = inspections.slice(start, start + PAGE_SIZE);

  return (
    <div className="table-wrap fade-in">
      <table>
        <thead>
          <tr>
            <th>Image</th>
            <th>Class</th>
            <th>Confidence</th>
            <th>Date</th>
            <th>Report</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {visible.map((inspection) => (
            <tr key={inspection.id} className="clickable-row" onClick={() => onRowClick(inspection)}>
              <td>
                <img
                  src={`${API_ORIGIN}/${inspection.image_path}`}
                  alt={`Inspection ${inspection.id}`}
                  className="history-thumb"
                />
              </td>
              <td>
                <Badge predictedClass={inspection.predicted_class} />
              </td>
              <td>{(inspection.confidence * 100).toFixed(2)} %</td>
              <td>{new Date(inspection.created_at).toLocaleString("en-US")}</td>
              <td onClick={(event) => event.stopPropagation()}>
                <DownloadReportButton inspectionId={inspection.id} />
              </td>
              <td onClick={(event) => event.stopPropagation()}>
                <div className="row-actions">
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => onDelete(inspection.id)}
                    loading={deletingId === inspection.id}
                  >
                    <Trash2 size={14} />
                    Delete
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {pageCount > 1 && (
        <div className="pagination">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
          >
            {"<"}
          </button>
          {Array.from({ length: pageCount }, (_, i) => i + 1).map((pageNumber) => (
            <button
              key={pageNumber}
              type="button"
              className={pageNumber === currentPage ? "active" : ""}
              onClick={() => setPage(pageNumber)}
            >
              {pageNumber}
            </button>
          ))}
          <button
            type="button"
            onClick={() => setPage((p) => Math.min(pageCount, p + 1))}
            disabled={currentPage === pageCount}
          >
            {">"}
          </button>
        </div>
      )}
    </div>
  );
}
