import React, { useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout.jsx";
import PasswordField from "../components/PasswordField.jsx";
import { login } from "../services/authService.js";
import { validateEmail } from "../utils/validation.js";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const emailError =
    (touched.email || submitted) &&
    (!email.trim()
      ? "Enter your email address."
      : !validateEmail(email)
        ? "Enter a valid email address."
        : "");
  const passwordError =
    (touched.password || submitted) && !password
      ? "Enter your password."
      : "";

  function updateField(setter) {
    return (event) => {
      setter(event.target.value);
      setFeedback(null);
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitted(true);
    setFeedback(null);
    if (!email.trim() || !validateEmail(email) || !password) return;

    setLoading(true);
    try {
      const succeeded = await login({ email: email.trim(), password });
      setFeedback(
        succeeded
          ? { type: "success", message: "You're signed in." }
          : {
              type: "error",
              message: "We couldn't sign you in. Please try again.",
            },
      );
    } catch {
      setFeedback({
        type: "error",
        message: "We couldn't sign you in. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to pick up where you left off."
    >
      <form className="flex flex-col gap-[19px] max-sm:gap-[17px]" onSubmit={handleSubmit} noValidate>
        <div className="min-w-0">
          <label className="mb-2 block text-[13px] font-semibold text-[#34414e]" htmlFor="email">
            Email address
          </label>
          <input
            className={`block h-[46px] w-full rounded-lg border bg-white px-[13px] text-sm text-[#202a35] outline-none transition-colors hover:border-slate-400 focus:border-[#315e83] focus:ring-[3px] focus:ring-[#315e83]/15 ${
              emailError ? "border-[#bf6666]" : "border-[#cfd6de]"
            }`}
            id="email"
            name="email"
            type="email"
            value={email}
            onChange={updateField(setEmail)}
            onBlur={() => setTouched((current) => ({ ...current, email: true }))}
            autoComplete="email"
            aria-invalid={Boolean(emailError)}
            aria-describedby={emailError ? "email-error" : undefined}
            required
          />
          {emailError && (
            <p className="mt-[7px] text-xs leading-[1.4] text-[#a23c3c]" id="email-error">
              {emailError}
            </p>
          )}
        </div>

        <PasswordField
          label="Password"
          value={password}
          onChange={updateField(setPassword)}
          onBlur={() => setTouched((current) => ({ ...current, password: true }))}
          error={passwordError}
        />

        {feedback && (
          <p
            className={`-mt-0.5 rounded-md border px-3 py-[11px] text-[13px] leading-relaxed ${
              feedback.type === "error"
                ? "border-[#efd4d4] bg-[#fff8f8] text-[#8c3434]"
                : "border-[#d2e5d8] bg-[#f5fbf6] text-[#2d6a50]"
            }`}
            role={feedback.type === "error" ? "alert" : "status"}
            aria-live={feedback.type === "error" ? "assertive" : "polite"}
          >
            {feedback.message}
          </p>
        )}

        <button
          className="mt-0.5 flex min-h-[46px] items-center justify-center gap-2 rounded-lg border border-[#315e83] bg-[#315e83] px-4 text-sm font-semibold text-white transition-colors hover:border-[#274c6c] hover:bg-[#274c6c] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#315e83] active:translate-y-px disabled:cursor-wait disabled:opacity-75 motion-reduce:transition-none"
          type="submit"
          disabled={loading}
        >
          {loading ? (
            <>
              <span
                className="size-[14px] animate-spin rounded-full border-2 border-white/45 border-t-white motion-reduce:animate-none"
                aria-hidden="true"
              />
              Signing in…
            </>
          ) : (
            "Sign in"
          )}
        </button>
      </form>

      <p className="mt-[23px] text-center text-[13px] text-[#687582]">
        New to L2E CyberGuard?{" "}
        <Link className="font-semibold text-[#315e83] hover:text-[#274c6c] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#315e83]" to="/register">
          Create an account
        </Link>
      </p>
    </AuthLayout>
  );
}
