// Role : Page tableau de bord / statistiques / graphiques / galerie.

import { useEffect, useState } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Gauge,
  ShieldAlert,
  Sparkles,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import StatCard from "../components/dashboard/StatCard";
import ClassPieChart from "../components/dashboard/ClassPieChart";
import InspectionsBarChart from "../components/dashboard/InspectionsBarChart";
import EvolutionChart from "../components/dashboard/EvolutionChart";
import GalleryGrid from "../components/dashboard/GalleryGrid";
import InspectionDetailsModal from "../components/inspection/InspectionDetailsModal";
import Loader from "../components/common/Loader";
import Alert from "../components/common/Alert";
import { getStatistics } from "../api/dashboardApi";
import { getHistory } from "../api/historyApi";
import { getErrorMessage } from "../api/axiosClient";
import { useAuth } from "../hooks/useAuth";
import {
  getClassBreakdown,
  getConfidenceExtremes,
  getDailyCounts,
  getFirstLastInspection,
} from "../utils/inspectionStats";

const GALLERY_SIZE = 8;

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [inspections, setInspections] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedInspection, setSelectedInspection] = useState(null);

  useEffect(() => {
    Promise.all([getStatistics(), getHistory()])
      .then(([statsData, historyData]) => {
        setStats(statsData);
        setInspections(historyData);
      })
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  const classBreakdown = getClassBreakdown(stats);
  const dailyCounts = getDailyCounts(inspections);
  const { highest, lowest } = getConfidenceExtremes(inspections);
  const { last } = getFirstLastInspection(inspections);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Overview of your inspection activity.</p>
        </div>
      </div>

      <Alert type="error">{error}</Alert>

      {loading && <Loader label="Loading statistics..." />}

      {stats && (
        <>
          <div className="stat-grid">
            <StatCard label="Total Inspections" value={stats.total_inspections} icon={Sparkles} tone="primary" />
            <StatCard label="Good Bottles" value={stats.total_good} icon={CheckCircle2} tone="secondary" />
            <StatCard label="Broken Large" value={stats.total_broken_large} icon={AlertOctagon} tone="danger" />
            <StatCard label="Broken Small" value={stats.total_broken_small} icon={AlertTriangle} tone="warning" />
            <StatCard label="Contamination" value={stats.total_contamination} icon={ShieldAlert} tone="violet" />
            <StatCard
              label="Average Confidence"
              value={`${stats.average_confidence} %`}
              icon={Gauge}
              tone="primary"
            />
            <StatCard
              label="Highest Confidence"
              value={highest ? `${(highest.confidence * 100).toFixed(2)} %` : "—"}
              icon={TrendingUp}
              tone="secondary"
            />
            <StatCard
              label="Lowest Confidence"
              value={lowest ? `${(lowest.confidence * 100).toFixed(2)} %` : "—"}
              icon={TrendingDown}
              tone="warning"
            />
            <StatCard
              label="Last Inspection"
              value={last ? new Date(last.created_at).toLocaleDateString("en-US") : "—"}
              icon={Clock}
              tone="primary"
            />
          </div>

          <div className="chart-grid">
            <div className="card">
              <h2 className="section-title">Class Distribution</h2>
              <ClassPieChart data={classBreakdown} />
            </div>
            <div className="card">
              <h2 className="section-title">Inspections by Class</h2>
              <InspectionsBarChart data={classBreakdown} />
            </div>
          </div>

          <div className="card" style={{ marginBottom: 28 }}>
            <h2 className="section-title">Inspections Over Time</h2>
            <EvolutionChart data={dailyCounts} />
          </div>

          <div className="card">
            <h2 className="section-title">Latest Inspections</h2>
            <GalleryGrid inspections={inspections.slice(0, GALLERY_SIZE)} onSelect={setSelectedInspection} />
          </div>
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
