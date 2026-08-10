// Role : Barre de progression indeterminee (affichee pendant l'analyse d'image).

export default function ProgressBar() {
  return (
    <div className="progress-bar" role="progressbar" aria-label="Analyzing image">
      <div className="progress-bar-fill" />
    </div>
  );
}
