// Role : Formulaire de creation de compte.

import { useState } from "react";
import { Lock, Mail, User } from "lucide-react";
import Button from "../common/Button";
import Alert from "../common/Alert";

export default function RegisterForm({ onSubmit, submitting }) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [mismatchError, setMismatchError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    // Validation cote client uniquement : le backend ne recoit et ne
    // valide toujours que "password" (aucun changement d'API).
    if (password !== confirmPassword) {
      setMismatchError("Passwords do not match.");
      return;
    }

    setMismatchError("");
    onSubmit(firstName, lastName, email, password);
  }

  return (
    <form onSubmit={handleSubmit}>
      <Alert type="error">{mismatchError}</Alert>

      <div className="form-group">
        <label htmlFor="firstName">First name</label>
        <div className="input-wrap">
          <User size={16} />
          <input
            id="firstName"
            type="text"
            placeholder="Jean"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="lastName">Last name</label>
        <div className="input-wrap">
          <User size={16} />
          <input
            id="lastName"
            type="text"
            placeholder="Dupont"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <div className="input-wrap">
          <Mail size={16} />
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="password">Password</label>
        <div className="input-wrap">
          <Lock size={16} />
          <input
            id="password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            minLength={6}
            maxLength={72}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="confirmPassword">Confirm password</label>
        <div className="input-wrap">
          <Lock size={16} />
          <input
            id="confirmPassword"
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            required
            minLength={6}
            maxLength={72}
          />
        </div>
      </div>

      <Button type="submit" block loading={submitting}>
        {submitting ? "Creating account..." : "Create account"}
      </Button>
    </form>
  );
}
