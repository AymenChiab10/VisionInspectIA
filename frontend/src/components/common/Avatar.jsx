// Role : Avatar genere automatiquement a partir des initiales de l'utilisateur.

const COLORS = ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"];

function getInitials(firstName, lastName) {
  const first = firstName?.[0] || "";
  const last = lastName?.[0] || "";
  return (first + last).toUpperCase() || "?";
}

function getColor(seed) {
  let hash = 0;
  for (const char of seed) {
    hash = char.charCodeAt(0) + ((hash << 5) - hash);
  }
  return COLORS[Math.abs(hash) % COLORS.length];
}

export default function Avatar({ firstName = "", lastName = "", size = "lg" }) {
  const initials = getInitials(firstName, lastName);
  const color = getColor(`${firstName}${lastName}`);

  return (
    <div className={`avatar avatar-${size}`} style={{ background: color }} aria-hidden="true">
      {initials}
    </div>
  );
}
