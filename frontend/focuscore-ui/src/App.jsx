/**
 * FocusCore v2.0 — App.jsx
 * Routing principal : / → LandingPage, /app → Dashboard avec Sidebar
 */

import { Routes, Route, Navigate } from "react-router-dom";
import LandingPage from "./LandingPage.jsx";
import Dashboard from "./Dashboard.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/app" element={<Dashboard />} />
      <Route path="/app/*" element={<Dashboard />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
