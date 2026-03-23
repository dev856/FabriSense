"""Custom CSS for FabriSense."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

:root {
    --bg: #f3eadb;
    --paper: rgba(255, 250, 243, 0.78);
    --paper-strong: rgba(255, 248, 238, 0.92);
    --panel: rgba(255, 255, 255, 0.44);
    --ink: #191512;
    --muted: #63574d;
    --accent: #b5532a;
    --accent-deep: #8b3f1e;
    --accent-soft: #efc5a7;
    --green-soft: #7f9b7f;
    --line: rgba(53, 35, 22, 0.12);
    --shadow: 0 24px 60px rgba(61, 43, 28, 0.09);
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(181, 83, 42, 0.20), transparent 26%),
        radial-gradient(circle at bottom left, rgba(127, 155, 127, 0.18), transparent 24%),
        linear-gradient(180deg, #f5ede1 0%, #ecd9c1 100%);
    color: var(--ink);
}

body, p, div, label, span, button, input, textarea {
    font-family: 'Manrope', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Instrument Serif', serif;
    letter-spacing: -0.02em;
    color: var(--ink);
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1240px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,248,239,0.96), rgba(242,229,211,0.96));
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

.sidebar-brand-card,
.page-intro,
.hero-shell,
.stat-card,
.info-card,
.metric-card,
.result-card,
.loading-card,
.color-card,
.highlight-banner,
.upload-shell {
    border-radius: 24px;
    border: 1px solid var(--line);
    background: var(--paper);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow);
}

.sidebar-brand-card {
    padding: 1rem 1rem 0.95rem;
    margin-bottom: 1rem;
    background: linear-gradient(180deg, rgba(255,251,247,0.92), rgba(248,238,225,0.88));
}

.sidebar-brand-card h3 {
    font-size: 1.45rem;
    line-height: 1.04;
    margin: 0.35rem 0 0.45rem;
}

.sidebar-brand-card p {
    margin: 0;
    color: var(--muted);
    font-size: 0.92rem;
}

.sidebar-kicker,
.eyebrow {
    margin: 0 0 0.55rem 0;
    color: var(--accent);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.22em;
    text-transform: uppercase;
}

.page-intro {
    padding: 1.1rem 1.2rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, rgba(255,255,255,0.64), rgba(252,242,232,0.72));
}

.page-intro h2 {
    margin: 0;
    font-size: 2.2rem;
}

.page-intro-text {
    margin: 0.5rem 0 0;
    color: var(--muted);
    max-width: 52rem;
}

.hero-shell {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1.55fr 0.95fr;
    gap: 1.25rem;
    margin-bottom: 1.25rem;
    padding: 1.55rem;
    background: linear-gradient(135deg, rgba(255,255,255,0.72), rgba(253,241,229,0.62));
}

.hero-shell::before,
.hero-shell::after {
    content: "";
    position: absolute;
    border-radius: 999px;
    filter: blur(4px);
    opacity: 0.7;
    animation: drift 8s ease-in-out infinite;
}

.hero-shell::before {
    width: 180px;
    height: 180px;
    right: -30px;
    top: -24px;
    background: radial-gradient(circle, rgba(181,83,42,0.18), transparent 65%);
}

.hero-shell::after {
    width: 130px;
    height: 130px;
    left: 44%;
    bottom: -38px;
    background: radial-gradient(circle, rgba(127,155,127,0.18), transparent 65%);
    animation-delay: 1.6s;
}

.hero-shell h1 {
    font-size: 3.55rem;
    line-height: 0.98;
    margin: 0 0 0.8rem;
}

.hero-text {
    font-size: 1.05rem;
    max-width: 42rem;
    color: var(--muted);
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 1rem;
}

.hero-tags span {
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(181, 83, 42, 0.10);
    border: 1px solid rgba(181, 83, 42, 0.16);
    color: var(--accent-deep);
    font-size: 0.85rem;
    font-weight: 700;
}

.hero-stats {
    display: grid;
    gap: 0.8rem;
}

.stat-card,
.info-card,
.metric-card,
.color-card,
.result-card {
    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.stat-card:hover,
.info-card:hover,
.metric-card:hover,
.color-card:hover,
.result-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 28px 62px rgba(61, 43, 28, 0.12);
    border-color: rgba(181, 83, 42, 0.22);
}

.stat-card {
    padding: 1.1rem 1.15rem;
    background: linear-gradient(180deg, rgba(255,250,245,0.90), rgba(247,235,220,0.90));
}

.stat-card h4 {
    font-size: 1.15rem;
    margin: 0 0 0.4rem;
}

.stat-card p,
.info-card p,
.metric-card p,
.color-card p,
.loading-card,
.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.stat-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    margin-bottom: 0.85rem;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(181,83,42,0.18), rgba(139,63,30,0.12));
    color: var(--accent-deep);
    font-size: 1.3rem;
    font-weight: 800;
}

.info-card,
.metric-card,
.result-card {
    padding: 1rem 1rem 0.95rem 1rem;
    height: 100%;
    background: var(--paper-strong);
}

.info-card h3,
.metric-card h3,
.color-card h4 {
    margin-bottom: 0.35rem;
}

.metric-card {
    min-height: 132px;
}

.metric-card h3 {
    font-size: 1.85rem;
}

.upload-shell {
    padding: 0.35rem 0.55rem 0.55rem;
    margin-bottom: 0.4rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.44), rgba(255,244,232,0.68));
}

.loading-card,
.highlight-banner {
    padding: 0.95rem 1rem;
    margin-bottom: 1rem;
}

.highlight-banner strong {
    display: block;
    margin-bottom: 0.3rem;
    color: var(--accent-deep);
}

.highlight-banner p {
    margin: 0;
    color: var(--muted);
}

.color-card {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.9rem;
    margin-bottom: 0.8rem;
    background: rgba(255,250,245,0.88);
}

.compare-summary-card {
    padding: 1rem;
    margin: 0.3rem 0 0.85rem;
    border-radius: 24px;
    border: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,251,246,0.92), rgba(246,235,221,0.90));
    box-shadow: var(--shadow);
}

.compare-summary-label {
    margin: 0 0 0.8rem;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent);
}

.compare-summary-flow {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
}

.compare-summary-flow div {
    padding: 0.85rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.58);
    border: 1px solid rgba(53, 35, 22, 0.08);
}

.compare-summary-flow span {
    display: block;
    margin-bottom: 0.3rem;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.compare-summary-flow strong {
    display: block;
    line-height: 1.35;
    color: var(--ink);
}

.compare-card {
    padding: 1rem;
    margin-top: 0.75rem;
    border-radius: 24px;
    border: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,252,247,0.90), rgba(248,237,225,0.90));
    box-shadow: var(--shadow);
}

.compare-card h3 {
    margin: 0 0 0.85rem;
    font-size: 1.5rem;
}

.compare-card-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
}

.compare-card-grid div {
    padding: 0.8rem 0.85rem;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.56);
    border: 1px solid rgba(53, 35, 22, 0.08);
}

.compare-card-grid span {
    display: block;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}

.compare-card-grid strong {
    display: block;
    color: var(--ink);
    line-height: 1.35;
}

.mini-swatch-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin: 0.8rem 0 1.2rem;
}

.mini-swatch {
    width: 18px;
    height: 18px;
    border-radius: 999px;
    display: inline-block;
    border: 1px solid rgba(0, 0, 0, 0.12);
    box-shadow: 0 6px 12px rgba(61, 43, 28, 0.10);
}

.swatch {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    flex-shrink: 0;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, var(--accent), var(--accent-deep));
    color: white;
    font-weight: 800;
    padding: 0.82rem 1.18rem;
    box-shadow: 0 16px 32px rgba(181, 83, 42, 0.20);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #c75f31, #964623);
}

.stFileUploader,
[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput > div > div {
    border-radius: 18px !important;
}

.stRadio [role="radiogroup"] {
    gap: 0.5rem;
}

.stRadio label {
    border-radius: 999px;
}

hr {
    border-color: var(--line);
}

@keyframes drift {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(10px) translateX(-6px); }
}

@media (max-width: 900px) {
    .hero-shell {
        grid-template-columns: 1fr;
    }

    .hero-shell h1 {
        font-size: 2.75rem;
    }

    .page-intro h2 {
        font-size: 1.9rem;
    }
}
</style>
"""