// Role : Page de connexion.

import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Eye } from "lucide-react";
import LoginForm from "../components/auth/LoginForm";
import Alert from "../components/common/Alert";
import { login as loginApi, getMe } from "../api/authApi";
import { getErrorMessage } from "../api/axiosClient";
import { useAuth } from "../hooks/useAuth";
import { useToast } from "../hooks/useToast";

export default function LoginPage() {
  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(email, password) {
    setError("");
    setSubmitting(true);
    try {
      const { access_token: accessToken } = await loginApi(email, password);
      localStorage.setItem("token", accessToken);
      const user = await getMe();
      login(accessToken, user);
      showToast("success", "Login successful.");
      navigate("/dashboard", { replace: true });
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
          <Eye size={24} />
        </div>
        <h1>Welcome back</h1>
        <p className="auth-subtitle">Sign in to VisionInspect AI</p>

        {location.state?.registered && (
          <Alert type="success">Account created successfully. You can now sign in.</Alert>
        )}
        <Alert type="error">{error}</Alert>

        <LoginForm onSubmit={handleSubmit} submitting={submitting} />

        <p className="auth-switch">
          Don&apos;t have an account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
}
