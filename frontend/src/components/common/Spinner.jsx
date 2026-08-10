// Role : Spinner circulaire (brique de base reutilisee par Loader et Button).

export default function Spinner({ small = false }) {
  return <span className={`spinner${small ? " spinner-sm" : ""}`} aria-hidden="true" />;
}
