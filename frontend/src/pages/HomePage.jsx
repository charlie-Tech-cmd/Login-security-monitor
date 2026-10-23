import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ApiError, getCurrentUser, logout } from "../services/authService.js";

export default function HomePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function loadUser() {
      try {
        const currentUser = await getCurrentUser();

        if (active) {
          setUser(currentUser);
        }
      } catch (err) {
        if (!active) return;

        if (err instanceof ApiError && err.status === 401) {
          logout();
          navigate("/login", { replace: true });
          return;
        }

        setError("Unable to load your account. Please try again.");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadUser();

    return () => {
      active = false;
    };
  }, [navigate]);

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <section className="w-full max-w-3xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm max-sm:p-5">
      <header className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <p className="text-sm font-semibold text-[#315e83]">L2E CyberGuard</p>
          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Account dashboard
          </h1>
        </div>
        <button
          type="button"
          onClick={handleLogout}
          className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#315e83]"
        >
          Sign out
        </button>
      </header>

      <div className="py-8">
        {loading ? (
          <p role="status" className="text-sm text-slate-600">
            Verifying your session…
          </p>
        ) : error ? (
          <p role="alert" className="text-sm text-red-700">
            {error}
          </p>
        ) : user ? (
          <>
            <h2 className="text-lg font-semibold text-slate-800">
              Welcome
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              You are signed in as{" "}
              <span className="font-medium text-slate-800">{user.email}</span>.
            </p>
            <p className="mt-4 text-sm text-slate-500">
              Your account has been verified.
            </p>
          </>
        ) : null}
      </div>
    </section>
  );
}
