"""Custom CSS for FabriSense."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

:root {
    --bg: #f4ebdd;
    --paper: rgba(255, 248, 239, 0.76);
    --panel: rgba(255, 255, 255, 0.42);
    --ink: #1f1a16;
    --muted: #68594d;
    --accent: #c35b2c;
    --accent-soft: #efb387;
    --line: rgba(62, 40, 24, 0.12);
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(195, 91, 44, 0.18), transparent 28%),
        radial-gradient(circle at bottom left, rgba(103, 135, 96, 0.16), transparent 22%),
        linear-gradient(180deg, #f6efe5 0%, #efe0ca 100%);
    color: var(--ink);
}

body, p, div, label, span {
    font-family: 'Space Grotesk', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Fraunces', serif;
    letter-spacing: -0.02em;
    color: var(--ink);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero-shell {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 1.2rem;
    margin-bottom: 1.5rem;
    padding: 1.5rem;
    border: 1px solid var(--line);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.7), rgba(255,244,233,0.55));
    box-shadow: 0 18px 48px rgba(68, 46, 28, 0.08);
}

.eyebrow {
    margin: 0 0 0.6rem 0;
    color: var(--accent);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.24em;
}

.hero-shell h1 {
    font-size: 3.3rem;
    line-height: 1.02;
    margin-bottom: 0.7rem;
}

.hero-text {
    font-size: 1.04rem;
    max-width: 44rem;
    color: var(--muted);
}

.hero-stats {
    display: grid;
    gap: 0.8rem;
}

.stat-card, .info-card, .metric-card, .result-card, .loading-card, .color-card {
    border-radius: 22px;
    border: 1px solid var(--line);
    background: var(--paper);
    backdrop-filter: blur(10px);
}

.stat-card {
    padding: 1.2rem;
}

.stat-card span {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}

.stat-card small {
    color: var(--muted);
}

.info-card, .metric-card, .result-card {
    padding: 1rem 1rem 0.95rem 1rem;
    height: 100%;
}

.info-card h3, .metric-card h3, .color-card h4 {
    margin-bottom: 0.35rem;
}

.info-card p, .metric-card p, .color-card p {
    color: var(--muted);
    margin-bottom: 0;
}

.metric-card h3 {
    font-size: 1.7rem;
}

.loading-card {
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    color: var(--muted);
}

.color-card {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.9rem;
    margin-bottom: 0.8rem;
}

.swatch {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    flex-shrink: 0;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #c35b2c, #ad4218);
    color: white;
    font-weight: 700;
    padding: 0.8rem 1.1rem;
}

.stFileUploader {
    padding: 0.4rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.35);
}

@media (max-width: 900px) {
    .hero-shell {
        grid-template-columns: 1fr;
    }

    .hero-shell h1 {
        font-size: 2.5rem;
    }
}
</style>
"""
