/**
 * LandingPage.jsx — FocusCore v2.0
 * Landing page with hero, features, how-it-works, live demo widget
 */

import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

// ─── Demo data cycling in the live widget ─────────────────────────
const DEMO_TASKS = [
  {
    description: "Implémenter le module d'authentification JWT",
    category: "Deep Work",
    score: 88,
    cls: "Haut",
    color: "#E8A020",
    conf: 91,
  },
  {
    description: "Préparer les slides de soutenance IA-Indus",
    category: "Communication",
    score: 71,
    cls: "Haut",
    color: "#E8A020",
    conf: 82,
  },
  {
    description: "Répondre aux emails non urgents",
    category: "Admin",
    score: 8,
    cls: "Faible",
    color: "#9E5050",
    conf: 89,
  },
  {
    description: "Étudier les transformers Hugging Face",
    category: "Apprentissage",
    score: 54,
    cls: "Moyen",
    color: "#5B8FD4",
    conf: 77,
  },
  {
    description: "Concevoir le dashboard principal React",
    category: "Créativité",
    score: 67,
    cls: "Haut",
    color: "#E8A020",
    conf: 85,
  },
];

function ScoreRingSmall({ score, color, size = 64, stroke = 5 }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - score / 100);
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#2A2A2C" strokeWidth={stroke} />
      <circle
        cx={size/2} cy={size/2} r={r}
        fill="none" stroke={color} strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circ}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size/2} ${size/2})`}
        style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.34,1.56,0.64,1), stroke 0.4s" }}
      />
      <text
        x={size/2} y={size/2 + 4}
        textAnchor="middle"
        fill={color}
        fontSize={size * 0.25}
        fontFamily="'DM Mono', monospace"
        fontWeight="500"
      >
        {score}
      </text>
    </svg>
  );
}

function LiveDemoWidget() {
  const [idx, setIdx] = useState(0);
  const [analyzing, setAnalyzing] = useState(false);
  const [displayed, setDisplayed] = useState(DEMO_TASKS[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnalyzing(true);
      setTimeout(() => {
        const next = (idx + 1) % DEMO_TASKS.length;
        setIdx(next);
        setDisplayed(DEMO_TASKS[next]);
        setAnalyzing(false);
      }, 900);
    }, 3500);
    return () => clearInterval(interval);
  }, [idx]);

  return (
    <div style={{
      background: "#141416",
      border: "1px solid #2A2A2C",
      borderRadius: 8,
      padding: 20,
      maxWidth: 380,
      margin: "0 auto",
    }}>
      <div style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, marginBottom: 14 }}>
        ◎ DÉMO EN DIRECT
      </div>

      {/* Fake task input */}
      <div style={{
        background: "#0C0C0E",
        border: "1px solid #2A2A2C",
        borderRadius: 4,
        padding: "10px 14px",
        fontSize: 12,
        color: "#888",
        marginBottom: 14,
        fontStyle: "italic",
        minHeight: 40,
        display: "flex",
        alignItems: "center",
        transition: "opacity 0.3s",
        opacity: analyzing ? 0.4 : 1,
      }}>
        {displayed.description}
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
        <div style={{
          fontSize: 10, padding: "4px 10px",
          background: "rgba(232,160,32,0.1)",
          border: "1px solid rgba(232,160,32,0.3)",
          color: "#E8A020", borderRadius: 3,
          fontFamily: "'DM Mono'",
        }}>
          {displayed.category}
        </div>
        {analyzing && (
          <div style={{
            fontSize: 10, padding: "4px 10px",
            background: "rgba(91,143,212,0.1)",
            border: "1px solid rgba(91,143,212,0.3)",
            color: "#5B8FD4", borderRadius: 3,
            fontFamily: "'DM Mono'",
            animation: "pulse 0.8s ease-in-out infinite",
          }}>
            Analyse IA...
          </div>
        )}
      </div>

      {/* Result */}
      <div style={{
        display: "flex", alignItems: "center", gap: 16,
        padding: "12px 14px",
        background: `rgba(${displayed.color === "#E8A020" ? "232,160,32" : displayed.color === "#9E5050" ? "158,80,80" : "91,143,212"},0.05)`,
        border: `1px solid ${displayed.color}33`,
        borderRadius: 4,
        opacity: analyzing ? 0.3 : 1,
        transition: "opacity 0.4s",
      }}>
        <ScoreRingSmall score={displayed.score} color={displayed.color} />
        <div>
          <div style={{ fontSize: 13, fontWeight: 700, color: displayed.color, letterSpacing: 1, fontFamily: "'DM Mono'" }}>
            IMPACT {displayed.cls.toUpperCase()}
          </div>
          <div style={{ fontSize: 11, color: "#666", marginTop: 4, fontFamily: "'DM Mono'" }}>
            Confiance : {displayed.conf}%
          </div>
        </div>
      </div>

      <div style={{ display: "flex", gap: 4, marginTop: 12, justifyContent: "center" }}>
        {DEMO_TASKS.map((_, i) => (
          <div key={i} style={{
            width: i === idx ? 16 : 4, height: 4,
            borderRadius: 2,
            background: i === idx ? "#E8A020" : "#2A2A2C",
            transition: "all 0.4s",
          }} />
        ))}
      </div>
    </div>
  );
}

export default function LandingPage() {
  const navigate = useNavigate();
  const featuresRef = useRef(null);
  const howRef = useRef(null);

  function scrollTo(ref) {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  }

  const features = [
    {
      icon: "⬡",
      title: "Analyse ML en temps réel",
      desc: "Random Forest entraîné sur 1500 tâches réelles. Chaque prédiction inclut un score de confiance et une explication lisible.",
    },
    {
      icon: "◎",
      title: "Score d'impact psychologique",
      desc: "L'IA pondère l'alignement sur tes objectifs, l'effort, l'urgence et la catégorie pour calculer un impact 0–100 ancré dans la réalité.",
    },
    {
      icon: "◈",
      title: "Blocage du bruit de fond",
      desc: "Quand une tâche à faible impact veut s'imposer, FocusCore t'interpelle : ta priorité #1 attend encore.",
    },
  ];

  const steps = [
    { n: "01", title: "Décris ta tâche", desc: "Nom, catégorie, urgence, effort estimé et alignement objectif — 10 secondes." },
    { n: "02", title: "L'IA analyse l'impact", desc: "Le modèle Random Forest calcule la classe d'impact et la probabilité de chaque prédiction." },
    { n: "03", title: "Focus sur ce qui compte", desc: "Tes tâches se trient automatiquement par impact réel. Le bruit de fond reste en bas." },
  ];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0C0C0E",
      fontFamily: "'Syne', sans-serif",
      color: "#E8E4D9",
      scrollBehavior: "smooth",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
        @keyframes fadeUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
        @keyframes glow { 0%,100% { opacity:0.3; } 50% { opacity:0.6; } }
        .nav-link {
          font-size: 12px;
          color: #666;
          cursor: pointer;
          font-family: 'DM Mono', monospace;
          letter-spacing: 1px;
          transition: color 0.2s;
          background: none;
          border: none;
          padding: 0;
        }
        .nav-link:hover { color: #E8E4D9; }
        .cta-btn {
          background: #E8A020;
          border: none;
          color: #0C0C0E;
          font-family: 'Syne', sans-serif;
          font-weight: 800;
          font-size: 14px;
          padding: 14px 32px;
          border-radius: 4px;
          cursor: pointer;
          letter-spacing: 0.5px;
          transition: background 0.2s, transform 0.1s;
        }
        .cta-btn:hover { background: #F0B040; transform: translateY(-1px); }
        .cta-btn:active { transform: scale(0.98); }
        .feature-card {
          background: #141416;
          border: 1px solid #2A2A2C;
          border-radius: 6px;
          padding: 28px 24px;
          transition: border-color 0.2s, transform 0.2s;
          animation: fadeUp 0.6s ease both;
        }
        .feature-card:hover {
          border-color: rgba(232,160,32,0.4);
          transform: translateY(-2px);
        }
        .step-card {
          display: flex;
          gap: 20px;
          align-items: flex-start;
          padding: 24px;
          background: #141416;
          border: 1px solid #1E1E20;
          border-radius: 6px;
          animation: fadeUp 0.6s ease both;
        }
      `}</style>

      {/* ── Sticky Nav ─────────────────────────────────────────── */}
      <nav style={{
        position: "sticky", top: 0, zIndex: 50,
        background: "rgba(12,12,14,0.92)",
        backdropFilter: "blur(12px)",
        borderBottom: "1px solid #1E1E20",
        padding: "14px 0",
      }}>
        <div style={{
          maxWidth: 1000, margin: "0 auto",
          padding: "0 32px",
          display: "flex", justifyContent: "space-between", alignItems: "center",
        }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
            <span style={{ fontSize: 18, fontWeight: 800, letterSpacing: -0.5 }}>
              FOCUS<span style={{ color: "#E8A020" }}>CORE</span>
            </span>
            <span style={{ fontSize: 9, fontFamily: "'DM Mono'", color: "#444", letterSpacing: 2 }}>v2.0</span>
          </div>
          <div style={{ display: "flex", gap: 28, alignItems: "center" }}>
            <button className="nav-link" onClick={() => scrollTo(featuresRef)}>Fonctionnalités</button>
            <button className="nav-link" onClick={() => scrollTo(howRef)}>Comment ça marche</button>
            <button
              onClick={() => navigate("/app")}
              style={{
                fontSize: 11, fontFamily: "'DM Mono'", letterSpacing: 1,
                padding: "7px 16px",
                background: "transparent",
                border: "1px solid #E8A020",
                color: "#E8A020",
                borderRadius: 3, cursor: "pointer",
                transition: "background 0.2s",
              }}
              onMouseEnter={e => e.currentTarget.style.background = "rgba(232,160,32,0.1)"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}
            >
              Démarrer →
            </button>
          </div>
        </div>
      </nav>

      {/* ── Hero ───────────────────────────────────────────────── */}
      <section style={{
        maxWidth: 1000, margin: "0 auto",
        padding: "80px 32px 60px",
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 48,
        alignItems: "center",
      }}>
        <div style={{ animation: "fadeUp 0.7s ease both" }}>
          {/* Badge */}
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            fontSize: 10, fontFamily: "'DM Mono'", color: "#3E8A50",
            border: "1px solid rgba(62,138,80,0.3)",
            padding: "5px 12px", borderRadius: 3, marginBottom: 28,
            letterSpacing: 1,
          }}>
            <div style={{ width: 5, height: 5, borderRadius: "50%", background: "#3E8A50" }} />
            IA-INDUS-4.0 · MINI-PROJET ACADÉMIQUE
          </div>

          <h1 style={{
            fontSize: 52,
            fontWeight: 800,
            lineHeight: 1.05,
            letterSpacing: -2,
            color: "#E8E4D9",
            marginBottom: 20,
          }}>
            Ton gestionnaire<br />
            de tâches piloté<br />
            <span style={{ color: "#E8A020" }}>par l'IA.</span>
          </h1>

          <p style={{
            fontSize: 15,
            color: "#666",
            lineHeight: 1.7,
            maxWidth: 400,
            marginBottom: 36,
          }}>
            FocusCore analyse l'impact réel de chaque tâche grâce à un modèle Random Forest entraîné,
            et t'aide à te concentrer sur ce qui compte vraiment.
          </p>

          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <button className="cta-btn" onClick={() => navigate("/app")}>
              Commencer →
            </button>
            <button
              className="nav-link"
              onClick={() => scrollTo(howRef)}
              style={{ fontSize: 12, padding: "14px 0" }}
            >
              Comment ça marche ↓
            </button>
          </div>

          {/* Stats row */}
          <div style={{
            display: "flex", gap: 24, marginTop: 40,
            paddingTop: 28, borderTop: "1px solid #1E1E20",
          }}>
            {[
              { val: "1 500", label: "tâches d'entraînement" },
              { val: "5", label: "catégories d'impact" },
              { val: "RF", label: "Random Forest" },
            ].map(s => (
              <div key={s.label}>
                <div style={{ fontSize: 20, fontWeight: 800, color: "#E8A020", fontFamily: "'DM Mono'" }}>
                  {s.val}
                </div>
                <div style={{ fontSize: 10, color: "#555", fontFamily: "'DM Mono'", letterSpacing: 1, marginTop: 3 }}>
                  {s.label.toUpperCase()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Demo */}
        <div style={{ animation: "fadeUp 0.7s ease 0.15s both" }}>
          <LiveDemoWidget />
        </div>
      </section>

      {/* ── Features ───────────────────────────────────────────── */}
      <section ref={featuresRef} style={{
        maxWidth: 1000, margin: "0 auto",
        padding: "60px 32px",
        borderTop: "1px solid #1E1E20",
      }}>
        <div style={{ marginBottom: 36 }}>
          <div style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, marginBottom: 10 }}>
            FONCTIONNALITÉS
          </div>
          <h2 style={{ fontSize: 30, fontWeight: 800, letterSpacing: -1 }}>
            Ce que FocusCore fait pour toi
          </h2>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
          {features.map((f, i) => (
            <div className="feature-card" key={f.title} style={{ animationDelay: `${i * 0.1}s` }}>
              <div style={{
                fontSize: 22, color: "#E8A020",
                marginBottom: 14,
                width: 40, height: 40,
                display: "flex", alignItems: "center", justifyContent: "center",
                background: "rgba(232,160,32,0.08)",
                border: "1px solid rgba(232,160,32,0.2)",
                borderRadius: 6,
              }}>
                {f.icon}
              </div>
              <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 10, lineHeight: 1.3 }}>
                {f.title}
              </h3>
              <p style={{ fontSize: 12, color: "#666", lineHeight: 1.7 }}>
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── How it works ───────────────────────────────────────── */}
      <section ref={howRef} style={{
        maxWidth: 1000, margin: "0 auto",
        padding: "60px 32px",
        borderTop: "1px solid #1E1E20",
      }}>
        <div style={{ marginBottom: 36 }}>
          <div style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#555", letterSpacing: 2, marginBottom: 10 }}>
            COMMENT ÇA MARCHE
          </div>
          <h2 style={{ fontSize: 30, fontWeight: 800, letterSpacing: -1 }}>
            3 étapes, zéro friction
          </h2>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {steps.map((s, i) => (
            <div className="step-card" key={s.n} style={{ animationDelay: `${i * 0.12}s` }}>
              <div style={{
                fontSize: 28, fontWeight: 800, fontFamily: "'DM Mono'",
                color: "rgba(232,160,32,0.25)",
                minWidth: 48, lineHeight: 1,
                paddingTop: 2,
              }}>
                {s.n}
              </div>
              <div>
                <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 8 }}>{s.title}</h3>
                <p style={{ fontSize: 13, color: "#666", lineHeight: 1.6 }}>{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA Section ────────────────────────────────────────── */}
      <section style={{
        maxWidth: 1000, margin: "0 auto",
        padding: "60px 32px 80px",
        borderTop: "1px solid #1E1E20",
        textAlign: "center",
      }}>
        <div style={{
          background: "#141416",
          border: "1px solid #2A2A2C",
          borderRadius: 8,
          padding: "48px 32px",
          position: "relative",
          overflow: "hidden",
        }}>
          {/* Glow bg */}
          <div style={{
            position: "absolute", top: -40, right: -40,
            width: 200, height: 200,
            background: "radial-gradient(circle, rgba(232,160,32,0.08) 0%, transparent 70%)",
            animation: "glow 3s ease-in-out infinite",
          }} />
          <h2 style={{ fontSize: 32, fontWeight: 800, letterSpacing: -1, marginBottom: 14, position: "relative" }}>
            Prêt à prioriser<br />
            <span style={{ color: "#E8A020" }}>ce qui compte vraiment ?</span>
          </h2>
          <p style={{ fontSize: 13, color: "#666", marginBottom: 28, position: "relative" }}>
            Lance l'application et analyse ta première tâche en 10 secondes.
          </p>
          <button className="cta-btn" onClick={() => navigate("/app")} style={{ position: "relative" }}>
            Ouvrir FocusCore →
          </button>
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────────────── */}
      <footer style={{
        borderTop: "1px solid #1E1E20",
        padding: "24px 32px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        maxWidth: 1000,
        margin: "0 auto",
      }}>
        <span style={{ fontSize: 14, fontWeight: 800 }}>
          FOCUS<span style={{ color: "#E8A020" }}>CORE</span>
        </span>
        <div style={{
          display: "flex", gap: 8, alignItems: "center",
          fontSize: 10, fontFamily: "'DM Mono'", color: "#444", letterSpacing: 1,
        }}>
          {["FastAPI", "scikit-learn", "React", "Random Forest"].map((tech, i, arr) => (
            <span key={tech}>
              {tech}
              {i < arr.length - 1 && <span style={{ margin: "0 4px", opacity: 0.4 }}>·</span>}
            </span>
          ))}
        </div>
        <span style={{ fontSize: 10, fontFamily: "'DM Mono'", color: "#333", letterSpacing: 1 }}>
          IA-INDUS-4.0
        </span>
      </footer>
    </div>
  );
}
