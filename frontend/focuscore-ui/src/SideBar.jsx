/**
 * SideBar.jsx — FocusCore v2.0
 * Collapsible sidebar with icons, active state, localStorage persistence
 */

import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  {
    id: "dashboard",
    label: "Dashboard",
    path: "/app",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="1" y="1" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="1.4"/>
        <rect x="9" y="1" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="1.4"/>
        <rect x="1" y="9" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="1.4"/>
        <rect x="9" y="9" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="1.4"/>
      </svg>
    ),
  },
  {
    id: "historique",
    label: "Historique",
    path: "/app/historique",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="6.3" stroke="currentColor" strokeWidth="1.4"/>
        <path d="M8 4.5V8L10.5 10" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      </svg>
    ),
  },
  {
    id: "objectifs",
    label: "Objectifs",
    path: "/app/objectifs",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="6.3" stroke="currentColor" strokeWidth="1.4"/>
        <circle cx="8" cy="8" r="3" stroke="currentColor" strokeWidth="1.4"/>
        <circle cx="8" cy="8" r="1" fill="currentColor"/>
      </svg>
    ),
  },
  {
    id: "parametres",
    label: "Paramètres",
    path: "/app/parametres",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="2.5" stroke="currentColor" strokeWidth="1.4"/>
        <path d="M8 1.5V3M8 13v1.5M1.5 8H3M13 8h1.5M3.1 3.1l1.05 1.05M11.85 11.85l1.05 1.05M3.1 12.9l1.05-1.05M11.85 4.15l1.05-1.05" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      </svg>
    ),
  },
];

export default function SideBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [open, setOpen] = useState(() => {
    try {
      const saved = localStorage.getItem("fc_sidebar");
      return saved !== null ? JSON.parse(saved) : true;
    } catch {
      return true;
    }
  });

  useEffect(() => {
    localStorage.setItem("fc_sidebar", JSON.stringify(open));
  }, [open]);

  const width = open ? 220 : 52;

  return (
    <div style={{
      width,
      minWidth: width,
      height: "100vh",
      background: "#0F0F11",
      borderRight: "1px solid #1E1E20",
      display: "flex",
      flexDirection: "column",
      transition: "width 0.25s cubic-bezier(0.4,0,0.2,1), min-width 0.25s cubic-bezier(0.4,0,0.2,1)",
      overflow: "hidden",
      position: "sticky",
      top: 0,
    }}>
      {/* Logo + toggle */}
      <div style={{
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: open ? "0 14px 0 18px" : "0 14px",
        borderBottom: "1px solid #1E1E20",
        flexShrink: 0,
      }}>
        {open && (
          <span style={{
            fontSize: 14, fontWeight: 800,
            fontFamily: "'Syne', sans-serif",
            letterSpacing: -0.5,
            color: "#E8E4D9",
            whiteSpace: "nowrap",
            overflow: "hidden",
          }}>
            FOCUS<span style={{ color: "#E8A020" }}>CORE</span>
          </span>
        )}
        <button
          onClick={() => setOpen(o => !o)}
          style={{
            background: "none",
            border: "none",
            color: "#555",
            cursor: "pointer",
            padding: 4,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: 4,
            transition: "color 0.15s, background 0.15s",
            marginLeft: open ? 0 : "auto",
            marginRight: open ? 0 : "auto",
          }}
          onMouseEnter={e => { e.currentTarget.style.color = "#E8E4D9"; e.currentTarget.style.background = "#1E1E20"; }}
          onMouseLeave={e => { e.currentTarget.style.color = "#555"; e.currentTarget.style.background = "none"; }}
          title={open ? "Réduire" : "Ouvrir"}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            {open ? (
              <path d="M10 3L5 8l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            ) : (
              <path d="M6 3l5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            )}
          </svg>
        </button>
      </div>

      {/* Nav items */}
      <nav style={{ flex: 1, padding: "12px 0" }}>
        {NAV_ITEMS.map(item => {
          const active = location.pathname === item.path ||
            (item.path === "/app" && location.pathname === "/app");
          return (
            <button
              key={item.id}
              onClick={() => navigate(item.path)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: open ? "9px 18px" : "9px 0",
                justifyContent: open ? "flex-start" : "center",
                background: active ? "rgba(232,160,32,0.08)" : "none",
                border: "none",
                borderLeft: active ? "2px solid #E8A020" : "2px solid transparent",
                color: active ? "#E8A020" : "#555",
                cursor: "pointer",
                fontFamily: "'Syne', sans-serif",
                fontSize: 13,
                fontWeight: active ? 600 : 400,
                transition: "all 0.15s",
                whiteSpace: "nowrap",
              }}
              onMouseEnter={e => {
                if (!active) {
                  e.currentTarget.style.color = "#E8E4D9";
                  e.currentTarget.style.background = "#1A1A1C";
                }
              }}
              onMouseLeave={e => {
                if (!active) {
                  e.currentTarget.style.color = "#555";
                  e.currentTarget.style.background = "none";
                }
              }}
              title={!open ? item.label : ""}
            >
              <span style={{ flexShrink: 0, display: "flex" }}>{item.icon}</span>
              {open && (
                <span style={{
                  opacity: open ? 1 : 0,
                  transition: "opacity 0.2s",
                }}>
                  {item.label}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom: version */}
      {open && (
        <div style={{
          padding: "14px 18px",
          borderTop: "1px solid #1E1E20",
          fontSize: 10,
          fontFamily: "'DM Mono'",
          color: "#333",
          letterSpacing: 1,
        }}>
          FOCUSCORE v2.0 · IA-INDUS-4.0
        </div>
      )}
    </div>
  );
}
