// Role : Page d'historique des inspections (recherche, filtres, tri, detail, export CSV).

import { useEffect, useMemo, useState } from "react";
import { Download } from "lucide-react";
import HistoryTable from "../components/history/HistoryTable";
import HistoryFilters from "../components/history/HistoryFilters";
import InspectionDetailsModal from "../components/inspection/InspectionDetailsModal";
import Loader from "../components/common/Loader";
import Alert from "../components/common/Alert";
import Button from "../components/common/Button";
import { getHistory, deleteInspection } from "../api/historyApi";
import { getErrorMessage } from "../api/axiosClient";
import { useToast } from "../hooks/useToast";
import { useAuth } from "../hooks/useAuth";
import { exportInspectionsToCsv } from "../utils/csvExport";

const DAY_MS = 24 * 60 * 60 * 1000;

function isWithinRange(dateStr, range) {
  if (range === "all") {
    return true;
  }
  const date = new Date(dateStr).getTime();
  const now = Date.now();
  if (range === "today") {
    return now - date < DAY_MS;
  }
  if (range === "7days") {
    return now - date < 7 * DAY_MS;
  }
  if (range === "month") {
    return now - date < 30 * DAY_MS;
  }
  return true;
}

function applyFilters(inspections, filters) {
  let result = inspections.filter((inspection) => {
    const matchesSearch =
      !filters.search ||
      inspection.predicted_class.toLowerCase().includes(filters.search.toLowerCase());
    const matchesClass =
      filters.predictedClass === "all" || inspection.predicted_class === filters.predictedClass;
    const matchesDate = isWithinRange(inspection.created_at, filters.dateRange);

    return matchesSearch && matchesClass && matchesDate;
  });

  result = [...result].sort((a, b) => {
    if (filters.sort === "newest") return new Date(b.created_at) - new Date(a.created_at);
    if (filters.sort === "oldest") return new Date(a.created_at) - new Date(b.created_at);
    if (filters.sort === "highest") return b.confidence - a.confidence;
    if (filters.sort === "lowest") return a.confidence - b.confidence;
    return 0;
  });

  return result;
}

export default function HistoryPage() {
  const { showToast } = useToast();
  const { user } = useAuth();
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);
  const [selectedInspection, setSelectedInspection] = useState(null);
  const [filters, setFilters] = useState({
    search: "",
    predictedClass: "all",
    dateRange: "all",
    sort: "newest",
  });

  useEffect(() => {
    loadHistory();
  }, []);

  function loadHistory() {
    setLoading(true);
    getHistory()
      .then(setInspections)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }

  async function handleDelete(id) {
    const confirmed = window.confirm("Delete this inspection permanently?");
    if (!confirmed) {
      return;
    }

    setError("");
    setDeletingId(id);
    try {
      await deleteInspection(id);
      setInspections((current) => current.filter((inspection) => inspection.id !== id));
      showToast("success", "Inspection deleted successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setDeletingId(null);
    }
  }

  function handleExportCsv() {
    const userName = `${user.first_name} ${user.last_name}`;
    exportInspectionsToCsv(filteredInspections, userName);
  }

  const filteredInspections = useMemo(
    () => applyFilters(inspections, filters),
    [inspections, filters]
  );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">History</h1>
          <p className="page-subtitle">All your past inspections.</p>
        </div>
        <Button variant="secondary" onClick={handleExportCsv} disabled={filteredInspections.length === 0}>
          <Download size={16} />
          Export CSV
        </Button>
      </div>

      <Alert type="error">{error}</Alert>

      {loading ? (
        <Loader label="Loading history..." />
      ) : (
        <>
          <HistoryFilters filters={filters} onChange={setFilters} />
          <HistoryTable
            inspections={filteredInspections}
            onDelete={handleDelete}
            deletingId={deletingId}
            onRowClick={setSelectedInspection}
          />
        </>
      )}

      <InspectionDetailsModal
        inspection={selectedInspection}
        userName={user ? `${user.first_name} ${user.last_name}` : ""}
        onClose={() => setSelectedInspection(null)}
      />
    </div>
  );
}
