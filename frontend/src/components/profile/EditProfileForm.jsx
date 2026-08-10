// Role : Formulaire d'edition du profil (prenom, nom, email).

import { useState } from "react";
import { Mail, User } from "lucide-react";
import Button from "../common/Button";

export default function EditProfileForm({ user, onSubmit, submitting }) {
  const [firstName, setFirstName] = useState(user.first_name);
  const [lastName, setLastName] = useState(user.last_name);
  const [email, setEmail] = useState(user.email);

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(firstName, lastName, email);
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="edit-firstName">First name</label>
        <div className="input-wrap">
          <User size={16} />
          <input
            id="edit-firstName"
            type="text"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="edit-lastName">Last name</label>
        <div className="input-wrap">
          <User size={16} />
          <input
            id="edit-lastName"
            type="text"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="edit-email">Email</label>
        <div className="input-wrap">
          <Mail size={16} />
          <input
            id="edit-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>
      </div>

      <Button type="submit" loading={submitting}>
        {submitting ? "Saving..." : "Save changes"}
      </Button>
    </form>
  );
}
