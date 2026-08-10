// Role : Carte affichant une statistique unique du dashboard (icone + couleur + valeur).

export default function StatCard({ label, value, icon: Icon, tone = "primary" }) {
  return (
    <div className="stat-card slide-up">
      <span className={`stat-icon tone-${tone}`}>
        <Icon size={20} />
      </span>
      <div>
        <p className="stat-label">{label}</p>
        <p className="stat-value">{value}</p>
      </div>
    </div>
  );
}
