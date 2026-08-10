// Role : Bouton uniforme reutilise sur toute l'application
// (variantes, taille, etat loading/disabled).

import Spinner from "./Spinner";

export default function Button({
  children,
  variant = "primary",
  size,
  block = false,
  loading = false,
  disabled = false,
  className = "",
  type = "button",
  ...props
}) {
  const classes = [
    "btn",
    `btn-${variant}`,
    size === "sm" ? "btn-sm" : "",
    block ? "btn-block" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button type={type} className={classes} disabled={disabled || loading} {...props}>
      {loading && <Spinner small />}
      {children}
    </button>
  );
}
