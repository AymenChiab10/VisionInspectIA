// Role : Barre de recherche, filtres (classe, date) et tri pour l'historique.
// Filtrage/tri effectues cote client sur la liste deja chargee via
// GET /history — aucun appel API supplementaire necessaire.

import { Search } from "lucide-react";

export const DATE_RANGES = [
  { value: "all", label: "All" },
  { value: "today", label: "Today" },
  { value: "7days", label: "Last 7 days" },
  { value: "month", label: "Last Month" },
];

export const SORT_OPTIONS = [
  { value: "newest", label: "Newest" },
  { value: "oldest", label: "Oldest" },
  { value: "highest", label: "Highest confidence" },
  { value: "lowest", label: "Lowest confidence" },
];

export const CLASS_OPTIONS = [
  { value: "all", label: "All classes" },
  { value: "good", label: "Good" },
  { value: "broken_large", label: "Broken Large" },
  { value: "broken_small", label: "Broken Small" },
  { value: "contamination", label: "Contamination" },
];

export default function HistoryFilters({ filters, onChange }) {
  function update(key, value) {
    onChange({ ...filters, [key]: value });
  }

  return (
    <div className="history-filters card">
      <div className="input-wrap" style={{ flex: 1, minWidth: 200 }}>
        <Search size={16} />
        <input
          type="text"
          placeholder="Search by class..."
          value={filters.search}
          onChange={(event) => update("search", event.target.value)}
          aria-label="Search inspections"
        />
      </div>

      <select value={filters.predictedClass} onChange={(event) => update("predictedClass", event.target.value)} aria-label="Filter by class">
        {CLASS_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      <select value={filters.dateRange} onChange={(event) => update("dateRange", event.target.value)} aria-label="Filter by date">
        {DATE_RANGES.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      <select value={filters.sort} onChange={(event) => update("sort", event.target.value)} aria-label="Sort">
        {SORT_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
