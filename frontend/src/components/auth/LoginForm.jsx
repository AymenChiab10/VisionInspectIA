// Role : Formulaire de connexion (email + mot de passe).

import { useState } from "react";
import { Lock, Mail } from "lucide-react";
import Button from "../common/Button";

export default function LoginForm({ onSubmit, submitting }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(email, password);
  }

  return (
    <form onSubmit={handleSubmit}>
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
          />
        </div>
      </div>

      <Button type="submit" block loading={submitting}>
        {submitting ? "Signing in..." : "Login"}
      </Button>
    </form>
  );
}
