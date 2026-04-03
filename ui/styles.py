"""Custom CSS for FabriSense."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Fraunces:opsz,wght,SOFT@9..144,500..700,50&display=swap');

:root {
    --bg-top: #f7f3ec;
    --bg-bottom: #e4ddd1;
    --surface-0: rgba(255, 252, 247, 0.72);
    --surface-1: rgba(255, 252, 248, 0.88);
    --surface-2: rgba(247, 242, 235, 0.96);
    --surface-3: rgba(238, 232, 223, 0.95);
    --ink-strong: #14212b;
    --ink: #243240;
    --muted: #5e6b77;
    --muted-soft: #8090a0;
    --line: rgba(20, 33, 43, 0.10);
    --line-strong: rgba(20, 33, 43, 0.18);
    --accent: #bb6c3f;
    --accent-strong: #9d5630;
    --accent-soft: rgba(187, 108, 63, 0.12);
    --accent-cool: #2f7487;
    --success: #2f7d63;
    --warning: #9f6a24;
    --danger: #9a4b49;
    --shadow-sm: 0 10px 30px rgba(18, 28, 36, 0.07);
    --shadow-md: 0 22px 60px rgba(18, 28, 36, 0.12);
    --shadow-lg: 0 36px 80px rgba(18, 28, 36, 0.16);
    --radius-sm: 16px;
    --radius-md: 22px;
    --radius-lg: 30px;
    --radius-pill: 999px;
}

.stApp {
    background:
        radial-gradient(circle at 12% 12%, rgba(47, 116, 135, 0.10), transparent 24%),
        radial-gradient(circle at 90% 8%, rgba(187, 108, 63, 0.14), transparent 20%),
        radial-gradient(circle at 84% 84%, rgba(47, 125, 99, 0.10), transparent 18%),
        linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
    color: var(--ink);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(20, 33, 43, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(20, 33, 43, 0.035) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(circle at center, rgba(0,0,0,0.22), transparent 78%);
    pointer-events: none;
    z-index: 0;
}

html, body, p, div, label, span, button, input, textarea {
    font-family: 'Manrope', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Fraunces', serif;
    letter-spacing: -0.03em;
    color: var(--ink-strong);
}

p, li, label, .stMarkdown, .stCaption {
    color: var(--ink);
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1.55rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(248,245,239,0.95), rgba(233,226,216,0.98));
    border-right: 1px solid var(--line);
    backdrop-filter: blur(18px);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.1rem;
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
.upload-shell,
.compare-summary-card,
.compare-card {
    border-radius: var(--radius-lg);
    border: 1px solid var(--line);
    background: var(--surface-0);
    backdrop-filter: blur(18px);
    box-shadow: var(--shadow-md);
}

.sidebar-brand-card {
    position: relative;
    overflow: hidden;
    padding: 1.2rem 1.1rem 1.1rem;
    margin-bottom: 1rem;
    background:
        radial-gradient(circle at top right, rgba(187,108,63,0.15), transparent 36%),
        linear-gradient(180deg, rgba(255,255,255,0.92), rgba(242,237,230,0.88));
}

.sidebar-brand-card::after {
    content: "";
    position: absolute;
    inset: auto -28px -44px auto;
    width: 120px;
    height: 120px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(47,116,135,0.18), transparent 68%);
}

.sidebar-brand-card h3 {
    font-size: 1.55rem;
    line-height: 1.02;
    margin: 0.35rem 0 0.5rem;
}

.sidebar-brand-card p {
    margin: 0;
    color: var(--muted);
    font-size: 0.93rem;
    line-height: 1.55;
}

.sidebar-kicker,
.eyebrow {
    margin: 0 0 0.6rem;
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.24em;
    text-transform: uppercase;
}

.page-intro {
    position: relative;
    overflow: hidden;
    padding: 1.15rem 1.3rem 1.2rem;
    margin-bottom: 1rem;
    background:
        radial-gradient(circle at top left, rgba(47,116,135,0.08), transparent 26%),
        linear-gradient(135deg, rgba(255,255,255,0.92), rgba(243,238,232,0.84));
}

.page-intro::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent-cool));
    opacity: 0.75;
}

.page-intro h2 {
    margin: 0;
    font-size: 2.35rem;
    line-height: 0.98;
}

.page-intro-text {
    margin: 0.55rem 0 0;
    color: var(--muted);
    max-width: 56rem;
    font-size: 1rem;
    line-height: 1.65;
}

.input-section-head {
    margin-bottom: 0.75rem;
}

.input-section-head h3 {
    margin: 0;
    font-size: 1.45rem;
}

.input-section-head p:last-child {
    margin: 0.35rem 0 0;
    color: var(--muted);
}

.hero-shell {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.95fr);
    gap: 1.2rem;
    margin-bottom: 1.35rem;
    padding: 1.75rem;
    background:
        radial-gradient(circle at top right, rgba(187,108,63,0.16), transparent 28%),
        radial-gradient(circle at bottom left, rgba(47,116,135,0.14), transparent 24%),
        linear-gradient(135deg, rgba(255,255,255,0.94), rgba(244,238,231,0.86));
}

.hero-shell::before,
.hero-shell::after {
    content: "";
    position: absolute;
    border-radius: 999px;
    filter: blur(2px);
    opacity: 0.75;
    animation: drift 10s ease-in-out infinite;
}

.hero-shell::before {
    width: 210px;
    height: 210px;
    right: -38px;
    top: -48px;
    background: radial-gradient(circle, rgba(187,108,63,0.20), transparent 68%);
}

.hero-shell::after {
    width: 160px;
    height: 160px;
    left: 48%;
    bottom: -58px;
    background: radial-gradient(circle, rgba(47,116,135,0.18), transparent 68%);
    animation-delay: 1.8s;
}

.hero-shell h1 {
    max-width: 10.5ch;
    margin: 0 0 0.9rem;
    font-size: 4rem;
    line-height: 0.9;
}

.hero-copy {
    position: relative;
    z-index: 1;
}

.hero-text {
    max-width: 44rem;
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.75;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 1rem;
}

.hero-tags span {
    padding: 0.5rem 0.85rem;
    border-radius: var(--radius-pill);
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(20, 33, 43, 0.09);
    color: var(--ink-strong);
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    box-shadow: var(--shadow-sm);
}

.hero-stats {
    position: relative;
    z-index: 1;
    display: grid;
    gap: 0.85rem;
}

.stat-card,
.info-card,
.metric-card,
.color-card,
.result-card,
.compare-summary-card,
.compare-card {
    transition:
        transform 180ms ease,
        box-shadow 180ms ease,
        border-color 180ms ease,
        background 180ms ease;
}

.stat-card:hover,
.info-card:hover,
.metric-card:hover,
.color-card:hover,
.result-card:hover,
.compare-summary-card:hover,
.compare-card:hover {
    transform: translateY(-4px);
    border-color: rgba(187, 108, 63, 0.22);
    box-shadow: var(--shadow-lg);
}

.stat-card {
    padding: 1.15rem 1.2rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(241,235,228,0.88));
}

.stat-card h4 {
    margin: 0 0 0.4rem;
    font-size: 1.18rem;
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
    width: 48px;
    height: 48px;
    margin-bottom: 0.85rem;
    border-radius: 15px;
    background: linear-gradient(135deg, rgba(187,108,63,0.18), rgba(47,116,135,0.16));
    color: var(--ink-strong);
    font-size: 1.25rem;
    font-weight: 800;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}

.info-card,
.metric-card,
.result-card {
    padding: 1.05rem 1.05rem 1rem;
    height: 100%;
    background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
}

.info-card h3,
.metric-card h3,
.color-card h4 {
    margin: 0 0 0.35rem;
}

.info-card {
    min-height: 144px;
}

.metric-card {
    min-height: 138px;
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: "";
    position: absolute;
    right: -20px;
    top: -24px;
    width: 72px;
    height: 72px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(187,108,63,0.18), transparent 70%);
}

.metric-card h3 {
    font-size: 2rem;
    line-height: 0.96;
}

.upload-shell {
    padding: 0.85rem 0.9rem 0.95rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.66), rgba(244,238,231,0.88));
}

.sample-card-title {
    margin: 0.5rem 0 0.6rem;
    font-size: 0.93rem;
    font-weight: 800;
    color: var(--ink-strong);
    text-align: center;
    letter-spacing: 0.03em;
}

.loading-card,
.highlight-banner {
    position: relative;
    overflow: hidden;
    padding: 1rem 1.05rem;
    margin-bottom: 1rem;
}

.highlight-banner {
    background:
        radial-gradient(circle at top right, rgba(47,116,135,0.08), transparent 28%),
        linear-gradient(135deg, rgba(255,255,255,0.88), rgba(239,233,226,0.92));
}

.highlight-banner strong {
    display: block;
    margin-bottom: 0.3rem;
    color: var(--ink-strong);
    font-size: 1rem;
    letter-spacing: -0.01em;
}

.highlight-banner p {
    margin: 0;
    color: var(--muted);
    line-height: 1.6;
}

.color-card {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.9rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(243,237,231,0.86));
}

.compare-summary-card {
    padding: 1rem;
    margin: 0.3rem 0 0.85rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(239,233,226,0.90));
}

.compare-summary-label {
    margin: 0 0 0.8rem;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
}

.compare-summary-flow {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
}

.compare-summary-flow div,
.compare-card-grid div {
    padding: 0.86rem;
    border-radius: var(--radius-sm);
    background: rgba(255,255,255,0.66);
    border: 1px solid rgba(20, 33, 43, 0.08);
}

.compare-summary-flow span,
.compare-card-grid span {
    display: block;
    margin-bottom: 0.34rem;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted-soft);
}

.compare-summary-flow strong,
.compare-card-grid strong {
    display: block;
    color: var(--ink-strong);
    line-height: 1.35;
}

.compare-card {
    padding: 1rem;
    margin-top: 0.75rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(240,234,227,0.92));
}

.compare-card h3 {
    margin: 0 0 0.85rem;
    font-size: 1.45rem;
}

.compare-card-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
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
    border: 1px solid rgba(20, 33, 43, 0.12);
    box-shadow: 0 6px 18px rgba(18, 28, 36, 0.12);
}

.swatch {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    border: 1px solid rgba(20, 33, 43, 0.08);
    flex-shrink: 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}

.stButton > button,
.stDownloadButton > button {
    border-radius: var(--radius-pill);
    border: 1px solid rgba(20, 33, 43, 0.06);
    background: linear-gradient(135deg, var(--accent), var(--accent-strong));
    color: white;
    font-weight: 800;
    letter-spacing: 0.01em;
    padding: 0.82rem 1.2rem;
    box-shadow: 0 18px 34px rgba(187, 108, 63, 0.18);
    transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 24px 40px rgba(187, 108, 63, 0.22);
    filter: brightness(1.02);
}

.stButton > button:focus,
.stDownloadButton > button:focus {
    box-shadow: 0 0 0 4px rgba(187,108,63,0.18);
}

.stFileUploader,
[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput > div > div,
.stTextArea textarea {
    border-radius: var(--radius-sm) !important;
}

.stTextArea textarea,
.stTextInput input {
    background: rgba(255,255,255,0.72) !important;
}

.stRadio [role="radiogroup"] {
    gap: 0.55rem;
}

.stRadio [role="radiogroup"] label {
    border-radius: var(--radius-pill);
    padding: 0.24rem 0.78rem 0.24rem 0.36rem;
    background: rgba(255,255,255,0.58);
    border: 1px solid rgba(20, 33, 43, 0.08);
    box-shadow: var(--shadow-sm);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background: rgba(255,255,255,0.68);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.55rem;
    margin-bottom: 0.95rem;
}

.stTabs [data-baseweb="tab"] {
    height: auto;
    padding: 0.72rem 1rem;
    border-radius: var(--radius-pill);
    background: rgba(255,255,255,0.62);
    border: 1px solid rgba(20, 33, 43, 0.08);
    color: var(--muted);
    font-weight: 800;
    box-shadow: var(--shadow-sm);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(187,108,63,0.16), rgba(47,116,135,0.16));
    color: var(--ink-strong);
    border-color: rgba(187,108,63,0.18);
}

[data-testid="stMetric"] {
    padding: 1rem 1rem 0.9rem;
    border-radius: var(--radius-md);
    background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(240,234,227,0.90));
    border: 1px solid var(--line);
    box-shadow: var(--shadow-sm);
}

[data-testid="stDataFrame"] {
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--line);
    box-shadow: var(--shadow-md);
    background: rgba(255,255,255,0.78);
}

[data-testid="stDataFrame"] [role="table"] {
    background: rgba(255,255,255,0.72);
}

.streamlit-expanderHeader {
    border-radius: var(--radius-md);
    background: rgba(255,255,255,0.56);
    border: 1px solid rgba(20,33,43,0.08);
}

hr {
    border-color: var(--line);
}

@keyframes drift {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(10px) translateX(-6px); }
}

@media (max-width: 980px) {
    .hero-shell {
        grid-template-columns: 1fr;
    }

    .hero-shell h1 {
        max-width: none;
        font-size: 3.1rem;
    }

    .page-intro h2 {
        font-size: 2rem;
    }
}

@media (max-width: 720px) {
    .block-container {
        padding-top: 1.2rem;
    }

    .hero-shell {
        padding: 1.3rem;
    }

    .hero-shell h1 {
        font-size: 2.55rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: wrap;
    }
}
</style>
"""
