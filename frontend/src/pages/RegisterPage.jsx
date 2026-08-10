// Role : Page de creation de compte.

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ScanLine } from "lucide-react";
import RegisterForm from "../components/auth/RegisterForm";
import Alert from "../components/common/Alert";
import { register as registerApi } from "../api/authApi";
import { getErrorMessage } from "../api/axiosClient";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(firstName, lastName, email, password) {
    setError("");
    setSubmitting(true);
    try {
      await registerApi(firstName, lastName, email, password);
      // Conformement a la consigne : apres l'inscription, on redirige
      // vers la page de connexion (pas de connexion automatique).
      navigate("/login", { replace: true, state: { registered: true } });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">
          <ScanLine size={24} />
        </div>
        <h1>Create your account</h1>
        <p className="auth-subtitle">Start detecting defects with VisionInspect AI</p>

        <Alert type="error">{error}</Alert>

        <RegisterForm onSubmit={handleSubmit} submitting={submitting} />

        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
