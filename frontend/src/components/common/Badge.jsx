// Role : Badge colore representant une classe de prediction.

const LABELS = {
  good: "Good",
  broken_large: "Broken Large",
  broken_small: "Broken Small",
  contamination: "Contamination",
};

export default function Badge({ predictedClass }) {
  const label = LABELS[predictedClass] || predictedClass;

  return <span className={`badge badge-${predictedClass}`}>{label}</span>;
}
