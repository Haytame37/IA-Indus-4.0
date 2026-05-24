/**
 * Dashboard.jsx — FocusCore v2.0
 * Dashboard principal avec Sidebar, vraie API FastAPI, catégorie Créativité
 */

import { useState, useRef } from "react";
import SideBar from "./SideBar.jsx";

// ─── Constantes ──────────────────────────────────────────────────
const API_URL = "http://localhost:8000/predict";

const CATEGORIES = ["Deep Work", "Admin", "Communication", "Apprentissage", "Perso", "Créativité"];

const CAT_ICONS = {
  "Deep Work":      "⬡",
  "Admin":          "○",
  "Communication":  "◈",
  "Apprentissage":  "◎",
  "Perso":          "◇",
  "Créativité":     "◆",
};

const CLASS_CONFIG = {
  Haut:   { label: "HAUT",   color: "#E8A020", bg: "rgba(232,160,32,0.08)",  border: "rgba(232,160,32,0.3)"  },
  Moyen:  { label: "MOYEN",  color: "#5B8FD4", bg: "rgba(91,143,212,0.08)",  border: "rgba(91,143,212,0.3)"  },
  Faible: { label: "FAIBLE", color: "#9E5050", bg: "rgba(158,80,80,0.08)",   border: "rgba(158,80,80,0.3)"   },
};

// ─── Vraie API + gestion d'erreurs ──────────────────────────────
async function callPredict(payload, notifyFn) {
  let res;
  try {
    res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new Error("NETWORK");
  }

  if (res.status === 422) throw new Error("INVALID");
  if (!res.ok) throw new Error(`HTTP_${res.status}`);

  return res.json();
}

// ─── ScoreRing ───────────────────────────────────────────────────
function ScoreRing({ score, size = 80, stroke = 6 }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - score / 100);
  const color = score >= 60 ? "#E8A020" : score >= 30 ? "#5B8FD4" : "#9E5050";

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ display: "block" }}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#2A2A2C" strokeWidth={stroke} />
      <circle
        cx={size/2} cy={size/2} r={r}
        fill="none" stroke={color} strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circ} strokeDashoffset={offset}
        transform={`rotate(-90 ${size/2} ${size/2})`}
        style={{ transition: "stroke-dashoffset 0.7s cubic-bezier(0.34,1.56,0.64,1), stroke 0.4s" }}
      />
      <text
        x={size/2} y={size/2 + 5} textAnchor="middle"
        fill={color} fontSize={size * 0.24}
        fontFamily="'DM Mono', monospace" fontWeight="500"
        style={{ transition: "fill 0.4s" }}
      >{score}</text>
    </svg>
  );
}

// ─── TaskCard ────────────────────────────────────────────────────
function TaskCard({ task, onDelete, isTop }) {
  const cfg = CLASS_CONFIG[task.impact_class] || CLASS_CONFIG.Moyen;
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 14,
      padding: "12px 16px",
      borderBottom: "1px solid #1E1E20",
      background: isTop ? "rgba(232,160,32,0.03)" : "transparent",
      borderLeft: isTop ? "2px solid #E8A020" : "2px solid transparent",
      transition: "background 0.2s",
      animation: "slideIn 0.3s ease",
    }}>
      <div style={{ fontFamily: "'DM Mono'", fontSize: 11, color: cfg.color, minWidth: 28, textAlign: "center" }}>
        {task.impact_score}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 13, color: "#E8E4D9", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {task.description}
        </div>
        <div style={{ fontSize: 11, color: "#666", marginTop: 2, display: "flex", gap: 8, alignItems: "center" }}>
          <span>{CAT_ICONS[task.category]} {task.category}</span>
          <span style={{ color: cfg.color, fontFamily: "'DM Mono'" }}>
            {(task.confidence * 100).toFixed(0)}% conf.
          </span>
          {task.explanation && (
            <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 220, opacity: 0.6 }}>
              {task.explanation.split("—")[1]?.trim()}
            </span>
          )}
        </div>
      </div>
      <div style={{
        fontSize: 10, fontFamily: "'DM Mono'", padding: "3px 8px",
        background: cfg.bg, border: `1px solid ${cfg.border}`,
        color: cfg.color, borderRadius: 3, letterSpacing: 1,
      }}>
        {cfg.label}
      </div>
      <button
        onClick={() => onDelete(task.id)}
        style={{ background: "none", border: "none", color: "#444", cursor: "pointer", fontSize: 16, padding: "0 4px" }}
        aria-label="Supprimer"
      >×</button>
    </div>
  );
}

// ─── Dashboard principal ─────────────────────────────────────────
export default function Dashboard() {
  const [tasks, setTasks] = useState([
    {
      id: 1, description: "Finaliser l'architecture backend FocusCore API",
      category: "Deep Work", urgency: 3, effort_hours: 2.5, goal_aligned: true,
      impact_class: "Haut", impact_score: 88, confidence: 0.91,
      explanation: "Impact haut — travail de concentration profonde, aligné sur l'objectif actif.",
    },
    {
      id: 2, description: "Préparer slides soutenance mini-projet IA-Indus",
      category: "Communication", urgency: 5, effort_hours: 1.5, goal_aligned: true,
      impact_class: "Haut", impact_score: 71, confidence: 0.82,
      explanation: "Impact haut — aligné sur l'objectif actif, échéance urgente.",
    },
    {
      id: 3, description: "Répondre aux emails non urgents",
      category: "Admin", urgency: 1, effort_hours: 0.3, goal_aligned: false,
      impact_class: "Faible", impact_score: 8, confidence: 0.89,
      explanation: "Impact faible — non lié à l'objectif principal.",
    },
  ]);

  const [form, setForm] = useState({
    description: "", category: "Deep Work", urgency: 3, effort_hours: 1.0, goal_aligned: true,
  });
  const [loading, setLoading] = useState(false);
  const [blocker, setBlocker] = useState(null);
  const [activeObjective] = useState("Lancer MVP FocusCore");
  const [notification, setNotification] = useState(null);
  const inputRef = useRef(null);

  const focusScore = tasks.length
    ? Math.round(tasks.reduce((a, t) => a + t.impact_score, 0) / tasks.length)
    : 0;
  const topTask = [...tasks].sort((a, b) => b.impact_score - a.impact_score)[0];

  function notify(msg, type = "info") {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3500);
  }

  async function handleAnalyze() {
    if (!form.description.trim()) {
      notify("Décris ta tâche d'abord.", "warn");
      inputRef.current?.focus();
      return;
    }
    setLoading(true);
    try {
      const result = await callPredict(form, notify);
      const hasHighPending = tasks.some(t => t.impact_class === "Haut");
      if (result.impact_class === "Faible" && hasHighPending) {
        setBlocker({ form: { ...form }, result });
        setLoading(false);
        return;
      }
      addTask(form, result);
    } catch (e) {
      if (e.message === "NETWORK") {
        notify("Backend hors ligne — vérifie que uvicorn tourne sur :8000", "error");
      } else if (e.message === "INVALID") {
        notify("Données invalides — vérifie les champs du formulaire", "warn");
      } else {
        notify(`Erreur API ${e.message.replace("HTTP_", "")}`, "error");
      }
    }
    setLoading(false);
  }

  function addTask(f, result) {
    setTasks(prev => [{ id: Date.now(), ...f, ...result }, ...prev]);
    setForm(f => ({ ...f, description: "" }));
    notify(
      `Tâche analysée — impact ${result.impact_class.toLowerCase()} (${result.impact_score}/100)`,
      result.impact_class === "Haut" ? "success" : result.impact_class === "Moyen" ? "info" : "warn"
    );
  }

  function handleBlockerForce() {
    if (blocker) addTask(blocker.form, blocker.result);
    setBlocker(null);
  }

  return (
    <div style={{
      display: "flex", minHeight: "100vh",
      background: "#0C0C0E",
      fontFamily: "'Syne', sans-serif",
      color: "#E8E4D9",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        input, select, textarea { font-family: inherit; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0C0C0E; }
        ::-webkit-scrollbar-thumb { background: #2A2A2C; border-radius: 2px; }
        @keyframes slideIn { from { opacity:0; transform:translateY(-8px); } to { opacity:1; transform:translateY(0); } }
        @keyframes fadeIn  { from { opacity:0; } to { opacity:1; } }
        @keyframes notifIn { from { opacity:0; transform:translateX(20px); } to { opacity:1; transform:translateX(0); } }
        .fc-input {
          width: 100%; background: #141416; border: 1px solid #2A2A2C;
          color: #E8E4D9; padding: 10px 14px; border-radius: 4px;
          font-size: 13px; outline: none; transition: border-color 0.2s;
          font-family: 'Syne', sans-serif;
        }
        .fc-input:focus { border-color: #E8A020; }
        .cat-btn {
          flex: 1; padding: 6px 3px; background: #141416;
          border: 1px solid #2A2A2C; color: #888; cursor: pointer;
          font-size: 10px; border-radius: 4px; transition: all 0.15s;
          font-family: 'Syne', sans-serif; white-space: nowrap;
          overflow: hidden; text-overflow: ellipsis;
        }
        .cat-btn:hover { border-color: #444; color: #CCC; }
        .cat-btn.active { background: rgba(232,160,32,0.1); border-color: #E8A020; color: #E8A020; }
        .analyze-btn {
          width: 100%; padding: 12px; background: #E8A020;
          border: none; color: #0C0C0E; font-family: 'Syne', sans-serif;
          font-size: 14px; font-weight: 700; border-radius: 4px;
          cursor: pointer; letter-spacing: 0.5px;
          transition: background 0.2s, transform 0.1s;
        }
        .analyze-btn:hover:not(:disabled) { background: #F0B040; }
        .analyze-btn:active:not(:disabled) { transform: scale(0.99); }
        .analyze-btn:disabled { background: #2A2A2C; color: #666; cursor: not-allowed; }
      `}</style>

      {/* ── Sidebar ─────────────────────────────────────────────── */}
      <SideBar />

      {/* ── Main content ────────────────────────────────────────── */}
      <div style={{ flex: 1, overflowX: "hidden", padding: "0 0 60px" }}>

        {/* Header */}
        <div style={{
          maxWidth: 900, margin: "0 auto", padding: "28px 24px 0",
          display: "flex", justifyContent: "space-between", alignItems: "center",
        }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <span style={{ fontSize: 18, fontWeight: 800, letterSpacing: -0.5 }}>
              Dashboard
            </span>
            <span style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#444", letterSpacing: 2 }}>
              IA-INDUS-4.0
            </span>
          </div>
          <div style={{
            fontSize: 11, fontFamily: "'DM Mono'", color: "#666",
            border: "1px solid #2A2A2C", padding: "5px 12px", borderRadius: 3,
            display: "flex", alignItems: "center", gap: 6,
          }}>
            <div style={{ width: 5, height: 5, borderRadius: "50%", background: "#3E8A50" }} />
            {activeObjective}
          </div>
        </div>

        <div style={{ maxWidth: 900, margin: "0 auto", padding: "24px" }}>

          {/* Top row */}
          <div style={{ display: "grid", gridTemplateColumns: "160px 1fr", gap: 16, marginBottom: 16 }}>

            {/* Focus Score */}
            <div style={{
              background: "#141416", border: "1px solid #2A2A2C",
              borderRadius: 6, padding: 20, textAlign: "center",
            }}>
              <div style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, marginBottom: 14 }}>
                FOCUS SCORE
              </div>
              <ScoreRing score={focusScore} size={84} />
              <div style={{ fontSize: 10, color: "#555", marginTop: 12 }}>
                {focusScore >= 70 ? "Excellente journée" : focusScore >= 50 ? "Bon rythme" : focusScore >= 30 ? "À améliorer" : "Bruit de fond"}
              </div>
            </div>

            {/* Priorité #1 */}
            {topTask && (
              <div style={{
                background: "#141416", border: "1px solid #2A2A2C",
                borderLeft: "2px solid #E8A020", borderRadius: 6, padding: 20,
              }}>
                <div style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#E8A020", letterSpacing: 2, marginBottom: 12 }}>
                  ▲ PRIORITÉ #1
                </div>
                <div style={{ fontSize: 16, fontWeight: 600, color: "#E8E4D9", marginBottom: 6, lineHeight: 1.4 }}>
                  {topTask.description}
                </div>
                <div style={{ fontSize: 12, color: "#666", marginBottom: 14, fontFamily: "'DM Mono'" }}>
                  score {topTask.impact_score}/100 &nbsp;·&nbsp;
                  {topTask.category} &nbsp;·&nbsp;
                  {topTask.effort_hours}h estimée
                </div>
                <div style={{ fontSize: 12, color: "#888", fontStyle: "italic" }}>
                  {topTask.explanation}
                </div>
              </div>
            )}
          </div>

          {/* Main grid */}
          <div style={{ display: "grid", gridTemplateColumns: "340px 1fr", gap: 16 }}>

            {/* Formulaire */}
            <div style={{
              background: "#141416", border: "1px solid #2A2A2C",
              borderRadius: 6, padding: 20, alignSelf: "start",
            }}>
              <div style={{ fontSize: 11, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, marginBottom: 16 }}>
                ANALYSER UNE TÂCHE
              </div>

              {/* Description */}
              <div style={{ marginBottom: 12 }}>
                <label style={{ fontSize: 11, color: "#666", display: "block", marginBottom: 5 }}>Description</label>
                <textarea
                  ref={inputRef}
                  className="fc-input"
                  rows={3}
                  value={form.description}
                  onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                  placeholder={'ex: "Implémenter le module JWT"'}
                  style={{ resize: "none" }}
                  onKeyDown={e => { if (e.key === "Enter" && e.metaKey) handleAnalyze(); }}
                />
              </div>

              {/* Catégorie — 2 lignes de 3 */}
              <div style={{ marginBottom: 12 }}>
                <label style={{ fontSize: 11, color: "#666", display: "block", marginBottom: 5 }}>Catégorie</label>
                <div style={{ display: "flex", gap: 4, marginBottom: 4 }}>
                  {CATEGORIES.slice(0, 3).map(cat => (
                    <button
                      key={cat}
                      className={`cat-btn ${form.category === cat ? "active" : ""}`}
                      onClick={() => setForm(f => ({ ...f, category: cat }))}
                    >
                      {CAT_ICONS[cat]} {cat.split(" ")[0]}
                    </button>
                  ))}
                </div>
                <div style={{ display: "flex", gap: 4 }}>
                  {CATEGORIES.slice(3).map(cat => (
                    <button
                      key={cat}
                      className={`cat-btn ${form.category === cat ? "active" : ""}`}
                      onClick={() => setForm(f => ({ ...f, category: cat }))}
                    >
                      {CAT_ICONS[cat]} {cat.split(" ")[0]}
                    </button>
                  ))}
                </div>
              </div>

              {/* Urgence */}
              <div style={{ marginBottom: 12 }}>
                <label style={{ fontSize: 11, color: "#666", display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                  <span>Urgence</span>
                  <span style={{ fontFamily: "'DM Mono'", color: "#E8A020" }}>{form.urgency}/5</span>
                </label>
                <input
                  type="range" min={1} max={5} step={1}
                  value={form.urgency}
                  onChange={e => setForm(f => ({ ...f, urgency: parseInt(e.target.value) }))}
                  style={{ width: "100%", accentColor: "#E8A020" }}
                />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#444", fontFamily: "'DM Mono'" }}>
                  <span>Basse</span><span>Haute</span>
                </div>
              </div>

              {/* Effort */}
              <div style={{ marginBottom: 12 }}>
                <label style={{ fontSize: 11, color: "#666", display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                  <span>Effort estimé</span>
                  <span style={{ fontFamily: "'DM Mono'", color: "#E8A020" }}>{form.effort_hours}h</span>
                </label>
                <input
                  type="range" min={0.1} max={8} step={0.1}
                  value={form.effort_hours}
                  onChange={e => setForm(f => ({ ...f, effort_hours: parseFloat(e.target.value) }))}
                  style={{ width: "100%", accentColor: "#E8A020" }}
                />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#444", fontFamily: "'DM Mono'" }}>
                  <span>15 min</span><span>8h</span>
                </div>
              </div>

              {/* Alignement */}
              <div style={{ marginBottom: 18 }}>
                <label style={{ fontSize: 11, color: "#666", display: "block", marginBottom: 8 }}>
                  Aligné sur l'objectif actif ?
                </label>
                <div style={{ display: "flex", gap: 8 }}>
                  {[true, false].map(val => (
                    <button
                      key={String(val)}
                      onClick={() => setForm(f => ({ ...f, goal_aligned: val }))}
                      style={{
                        flex: 1, padding: "7px 0",
                        background: form.goal_aligned === val
                          ? (val ? "rgba(62,138,80,0.15)" : "rgba(158,80,80,0.15)")
                          : "#0C0C0E",
                        border: `1px solid ${form.goal_aligned === val
                          ? (val ? "#3E8A50" : "#9E5050")
                          : "#2A2A2C"}`,
                        color: form.goal_aligned === val
                          ? (val ? "#5CBA72" : "#C06060")
                          : "#666",
                        borderRadius: 4, cursor: "pointer", fontSize: 12,
                        fontFamily: "'Syne'", transition: "all 0.15s",
                      }}
                    >
                      {val ? "✓ Oui" : "✗ Non"}
                    </button>
                  ))}
                </div>
              </div>

              <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
                {loading ? "⟳ Analyse en cours..." : "⬡ ANALYSER L'IMPACT"}
              </button>

              <div style={{ fontSize: 10, color: "#444", textAlign: "center", marginTop: 8, fontFamily: "'DM Mono'" }}>
                ⌘↵ pour analyser rapidement
              </div>

              {/* Indicateur connexion backend */}
              <div style={{
                marginTop: 14, padding: "8px 12px",
                background: "#0C0C0E",
                border: "1px solid #1E1E20",
                borderRadius: 3,
                fontSize: 10, fontFamily: "'DM Mono'", color: "#444",
                display: "flex", alignItems: "center", gap: 6,
              }}>
                <div style={{ width: 4, height: 4, borderRadius: "50%", background: "#3E8A50" }} />
                API : localhost:8000/predict
              </div>
            </div>

            {/* Liste des tâches */}
            <div style={{
              background: "#141416", border: "1px solid #2A2A2C",
              borderRadius: 6, overflow: "hidden",
            }}>
              <div style={{
                display: "flex", justifyContent: "space-between", alignItems: "center",
                padding: "14px 16px", borderBottom: "1px solid #1E1E20",
              }}>
                <span style={{ fontSize: 11, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2 }}>
                  TÂCHES ({tasks.length})
                </span>
                <div style={{ display: "flex", gap: 12, fontSize: 11, fontFamily: "'DM Mono'" }}>
                  {["Haut", "Moyen", "Faible"].map(cls => {
                    const count = tasks.filter(t => t.impact_class === cls).length;
                    return (
                      <span key={cls} style={{ color: CLASS_CONFIG[cls].color }}>
                        {CLASS_CONFIG[cls].label} {count}
                      </span>
                    );
                  })}
                </div>
              </div>

              {tasks.length === 0 ? (
                <div style={{ padding: 40, textAlign: "center", color: "#444", fontSize: 13 }}>
                  Aucune tâche pour l'instant.<br />
                  <span style={{ fontSize: 11, fontFamily: "'DM Mono'" }}>Analyse ta première tâche →</span>
                </div>
              ) : (
                [...tasks]
                  .sort((a, b) => b.impact_score - a.impact_score)
                  .map((task, i) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      isTop={i === 0}
                      onDelete={id => setTasks(prev => prev.filter(t => t.id !== id))}
                    />
                  ))
              )}
            </div>
          </div>

          {/* Probabilities panel */}
          {tasks.length > 0 && tasks[0].probabilities && (
            <div style={{
              marginTop: 16, background: "#141416", border: "1px solid #2A2A2C",
              borderRadius: 6, padding: "14px 20px",
              display: "flex", gap: 32, alignItems: "center",
            }}>
              <span style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, whiteSpace: "nowrap" }}>
                DERNIÈRE PRÉDICTION
              </span>
              {Object.entries(tasks[0].probabilities).map(([cls, prob]) => {
                const cfg = CLASS_CONFIG[cls];
                if (!cfg) return null;
                return (
                  <div key={cls} style={{ flex: 1 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                      <span style={{ fontSize: 11, color: cfg.color, fontFamily: "'DM Mono'" }}>{cls.toUpperCase()}</span>
                      <span style={{ fontSize: 11, fontFamily: "'DM Mono'", color: "#888" }}>
                        {(prob * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div style={{ height: 3, background: "#2A2A2C", borderRadius: 2, overflow: "hidden" }}>
                      <div style={{
                        width: `${prob * 100}%`, height: "100%",
                        background: cfg.color, borderRadius: 2,
                        transition: "width 0.6s cubic-bezier(0.34,1.56,0.64,1)",
                      }} />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Blocker overlay */}
      {blocker && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.8)",
          display: "flex", alignItems: "center", justifyContent: "center",
          zIndex: 100, animation: "fadeIn 0.2s ease",
        }}>
          <div style={{
            background: "#141416", border: "1px solid #9E5050",
            borderRadius: 8, padding: 28, maxWidth: 380, textAlign: "center",
          }}>
            <div style={{ fontSize: 32, marginBottom: 12 }}>⚠</div>
            <div style={{ fontSize: 13, fontFamily: "'DM Mono'", color: "#9E5050", letterSpacing: 2, marginBottom: 8 }}>
              BRUIT DE FOND DÉTECTÉ
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, color: "#E8E4D9", marginBottom: 8 }}>
              Cette tâche a un impact faible
            </div>
            <div style={{ fontSize: 12, color: "#666", marginBottom: 6, fontFamily: "'DM Mono'" }}>
              Score prédit : <span style={{ color: "#9E5050" }}>{blocker.result.impact_score}/100</span>
            </div>
            <div style={{ fontSize: 12, color: "#666", marginBottom: 20, lineHeight: 1.6 }}>
              {blocker.result.explanation}<br />
              Ta priorité #1 attend toujours.
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <button
                onClick={() => setBlocker(null)}
                style={{
                  flex: 1, padding: "10px", background: "#E8A020",
                  border: "none", color: "#0C0C0E", fontFamily: "'Syne'",
                  fontWeight: 700, fontSize: 12, borderRadius: 4, cursor: "pointer",
                }}
              >
                Revenir à ma priorité
              </button>
              <button
                onClick={handleBlockerForce}
                style={{
                  flex: 1, padding: "10px", background: "transparent",
                  border: "1px solid #2A2A2C", color: "#666", fontFamily: "'Syne'",
                  fontSize: 12, borderRadius: 4, cursor: "pointer",
                }}
              >
                Forcer quand même
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Notification */}
      {notification && (
        <div style={{
          position: "fixed", bottom: 24, right: 24,
          background: "#141416",
          border: `1px solid ${
            notification.type === "success" ? "#3E8A50" :
            notification.type === "error" ? "#9E5050" :
            notification.type === "warn" ? "#9E5050" : "#5B8FD4"
          }`,
          color: notification.type === "success" ? "#5CBA72" :
                 notification.type === "error" ? "#C06060" :
                 notification.type === "warn" ? "#C06060" : "#7BAEE0",
          padding: "10px 16px", borderRadius: 4, fontSize: 12,
          fontFamily: "'DM Mono'", maxWidth: 360, zIndex: 200,
          animation: "notifIn 0.3s ease",
        }}>
          {notification.msg}
        </div>
      )}
    </div>
  );
}
