// Role : Indicateur de chargement plein bloc (spinner + texte), reutilisable.

import Spinner from "./Spinner";

export default function Loader({ label = "Loading..." }) {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <Spinner />
      <span>{label}</span>
    </div>
  );
}
