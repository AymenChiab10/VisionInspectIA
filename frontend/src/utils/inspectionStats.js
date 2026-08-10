// Role : Calculs statistiques partages, derives des donnees deja chargees
// (GET /dashboard/statistics et GET /history). Utilise par DashboardPage
// et ProfilePage pour eviter de dupliquer cette logique deux fois.

export const CLASS_COLORS = {
  good: "#10B981",
  broken_large: "#EF4444",
  broken_small: "#F59E0B",
  contamination: "#8B5CF6",
};

export const CLASS_LABELS = {
  good: "Good",
  broken_large: "Broken Large",
  broken_small: "Broken Small",
  contamination: "Contamination",
};

// Transforme les compteurs de /dashboard/statistics en tableau exploitable
// par les graphiques (Pie/Bar charts).
export function getClassBreakdown(stats) {
  if (!stats) {
    return [];
  }

  return [
    { key: "good", name: CLASS_LABELS.good, value: stats.total_good, color: CLASS_COLORS.good },
    {
      key: "broken_large",
      name: CLASS_LABELS.broken_large,
      value: stats.total_broken_large,
      color: CLASS_COLORS.broken_large,
    },
    {
      key: "broken_small",
      name: CLASS_LABELS.broken_small,
      value: stats.total_broken_small,
      color: CLASS_COLORS.broken_small,
    },
    {
      key: "contamination",
      name: CLASS_LABELS.contamination,
      value: stats.total_contamination,
      color: CLASS_COLORS.contamination,
    },
  ];
}

// Regroupe les inspections par jour (nombre d'inspections par jour),
// triees de la plus ancienne a la plus recente.
export function getDailyCounts(inspections) {
  const counts = new Map();

  for (const inspection of inspections) {
    const day = new Date(inspection.created_at).toLocaleDateString("en-CA"); // YYYY-MM-DD
    counts.set(day, (counts.get(day) || 0) + 1);
  }

  return Array.from(counts.entries())
    .map(([date, count]) => ({ date, count }))
    .sort((a, b) => (a.date > b.date ? 1 : -1));
}

// Inspection avec la confiance la plus haute / la plus basse.
export function getConfidenceExtremes(inspections) {
  if (inspections.length === 0) {
    return { highest: null, lowest: null };
  }

  let highest = inspections[0];
  let lowest = inspections[0];

  for (const inspection of inspections) {
    if (inspection.confidence > highest.confidence) highest = inspection;
    if (inspection.confidence < lowest.confidence) lowest = inspection;
  }

  return { highest, lowest };
}

// Premiere et derniere inspection (par date).
export function getFirstLastInspection(inspections) {
  if (inspections.length === 0) {
    return { first: null, last: null };
  }

  const sorted = [...inspections].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  );

  return { first: sorted[0], last: sorted[sorted.length - 1] };
}

// Classe la plus frequemment detectee, a partir des compteurs du dashboard.
export function getMostDetectedClass(stats) {
  if (!stats || stats.total_inspections === 0) {
    return null;
  }

  const breakdown = getClassBreakdown(stats);
  return breakdown.reduce((max, current) => (current.value > max.value ? current : max));
}
