// Role : Grille des dernieres images analysees ; cliquer ouvre la modal de detail.

import { API_ORIGIN } from "../../api/axiosClient";

export default function GalleryGrid({ inspections, onSelect }) {
  if (inspections.length === 0) {
    return <p className="chart-empty">No inspection yet.</p>;
  }

  return (
    <div className="gallery-grid">
      {inspections.map((inspection) => (
        <button
          key={inspection.id}
          type="button"
          className={`gallery-item gallery-${inspection.predicted_class}`}
          onClick={() => onSelect(inspection)}
          aria-label={`View inspection ${inspection.id} details`}
        >
          <img src={`${API_ORIGIN}/${inspection.image_path}`} alt={`Inspection ${inspection.id}`} />
        </button>
      ))}
    </div>
  );
}
