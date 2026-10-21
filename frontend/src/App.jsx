import React from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <main className="grid min-h-screen place-items-center bg-slate-50 px-5 py-12 text-slate-800 max-sm:px-3.5 max-sm:py-7">
        <Routes>
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/register" replace />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
