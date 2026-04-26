"""Custom CSS for FabriSense."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Fraunces:opsz,wght,SOFT@9..144,500..700,50&display=swap');

:root {
    --bg-top: #f5f8f7;
    --bg-bottom: #dfe9e6;
    --surface-0: rgba(255, 255, 252, 0.76);
    --surface-1: rgba(255, 255, 252, 0.9);
    --surface-2: rgba(239, 246, 244, 0.96);
    --surface-3: rgba(224, 236, 232, 0.95);
    --ink-strong: #132528;
    --ink: #25383b;
    --muted: #5b6d70;
    --muted-soft: #7d9294;
    --line: rgba(19, 37, 40, 0.10);
    --line-strong: rgba(19, 37, 40, 0.18);
    --accent: #0f7c78;
    --accent-strong: #0a5f5b;
    --accent-soft: rgba(15, 124, 120, 0.12);
    --accent-cool: #5467b0;
    --success: #277a62;
    --warning: #a66f2a;
    --danger: #9a4b55;
    --shadow-sm: 0 10px 30px rgba(18, 28, 36, 0.07);
    --shadow-md: 0 22px 60px rgba(18, 28, 36, 0.12);
    --shadow-lg: 0 36px 80px rgba(18, 28, 36, 0.16);
    --radius-sm: 16px;
    --radius-md: 22px;
    --radius-lg: 30px;
    --radius-pill: 999px;
    --skeleton-base: rgba(20, 33, 43, 0.06);
    --skeleton-shine: rgba(255, 255, 255, 0.5);
    --tooltip-bg: #1e2d3a;
    --tooltip-fg: #f0f4f8;
}

.stApp {
    background:
        radial-gradient(circle at 12% 12%, rgba(15, 124, 120, 0.10), transparent 24%),
        radial-gradient(circle at 90% 8%, rgba(84, 103, 176, 0.12), transparent 20%),
        radial-gradient(circle at 84% 84%, rgba(39, 122, 98, 0.10), transparent 18%),
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
    padding-left: clamp(1.1rem, 2.4vw, 2.6rem);
    padding-right: clamp(1.1rem, 2.4vw, 2.6rem);
    padding-bottom: 5.5rem;
    max-width: 1560px;
    margin-left: 0;
    margin-right: auto;
    box-sizing: border-box;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(250,253,251,0.92), rgba(227,238,235,0.90));
    border-right: 1px solid var(--line);
    backdrop-filter: blur(18px);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.1rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    max-width: 100%;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    display: none;
}

section[data-testid="stSidebar"] div[class*="option-menu"],
section[data-testid="stSidebar"] ul.nav,
section[data-testid="stSidebar"] .nav,
section[data-testid="stSidebar"] .nav-pills,
section[data-testid="stSidebar"] .nav-item {
    background: transparent !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] ul.nav {
    padding: 0 !important;
    border-radius: 0 !important;
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
.compare-card,
.empty-state-card,
.confusion-card,
.color-wheel-card,
.floating-action-bar {
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
        radial-gradient(circle at top right, rgba(15,124,120,0.15), transparent 36%),
        linear-gradient(180deg, rgba(255,255,255,0.94), rgba(237,246,243,0.9));
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

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 0.35rem;
    flex-direction: column;
    align-items: stretch !important;
    width: 100%;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    border-radius: 16px;
    padding: 0.68rem 0.92rem;
    width: 100% !important;
    max-width: 100% !important;
    min-height: 46px;
    margin: 0 !important;
    background: rgba(255,255,255,0.38);
    border: 1px solid rgba(19,37,40,0.05);
    box-shadow: var(--shadow-sm);
    font-weight: 700;
    font-size: 0.92rem;
    color: var(--ink);
    transition: all 200ms ease;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    justify-content: flex-start;
    box-sizing: border-box;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child {
    display: none;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label::before {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    min-width: 22px;
    height: 22px;
    border-radius: 8px;
    color: var(--accent);
    font-size: 0.85rem;
    font-weight: 800;
    line-height: 1;
    background: rgba(15, 124, 120, 0.08);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(1)::before {
    content: "A";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(2)::before {
    content: "B";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(3)::before {
    content: "C";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(4)::before {
    content: "H";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(5)::before {
    content: "G";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(6)::before {
    content: "C";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(7)::before {
    content: "M";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(8)::before {
    content: "i";
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] div[data-testid="stMarkdownContainer"] {
    flex: 1;
    min-width: 0;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(15, 124, 120, 0.08);
    border-color: var(--line);
    transform: translateX(4px);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-baseweb="radio"]:hover {
    transform: translateX(4px);
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
    background: rgba(15, 124, 120, 0.14) !important;
    border-color: rgba(15, 124, 120, 0.35) !important;
    color: var(--accent-strong) !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 22px rgba(15, 124, 120, 0.12);
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"]::before {
    background: rgba(15, 124, 120, 0.13);
    color: var(--accent-strong);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] [class*="st"] {
    gap: 0.35rem;
}

section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p {
    font-size: 0.92rem;
    font-weight: 600;
    text-align: left;
    overflow-wrap: anywhere;
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
    font-weight: 800;
    color: var(--accent-strong);
}

.page-intro {
    position: relative;
    overflow: hidden;
    padding: 1.15rem 1.3rem 1.2rem;
    margin-bottom: 1rem;
    background:
        radial-gradient(circle at top left, rgba(47,116,135,0.08), transparent 26%),
        linear-gradient(135deg, rgba(255,255,255,0.92), rgba(243,238,232,0.84));
    animation: cardSlideUp 0.5s ease-out;
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
        radial-gradient(circle at top right, rgba(15,124,120,0.15), transparent 28%),
        radial-gradient(circle at bottom left, rgba(84,103,176,0.12), transparent 24%),
        linear-gradient(135deg, rgba(255,255,255,0.96), rgba(235,245,242,0.88));
    animation: cardSlideUp 0.6s ease-out;
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
    background: radial-gradient(circle, rgba(15,124,120,0.18), transparent 68%);
}

.hero-shell::after {
    width: 160px;
    height: 160px;
    left: 48%;
    bottom: -58px;
    background: radial-gradient(circle, rgba(84,103,176,0.16), transparent 68%);
    animation-delay: 1.8s;
}

.hero-shell h1 {
    max-width: 10.5ch;
    margin: 0 0 0.9rem;
    font-size: 4rem;
    line-height: 0.9;
    background: linear-gradient(135deg, var(--ink-strong) 0%, var(--accent) 50%, var(--accent-cool) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 6s ease-in-out infinite;
    background-size: 200% 200%;
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
    transition: all 200ms ease;
}

.hero-tags span:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--accent-soft);
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
.compare-card,
.empty-state-card,
.confusion-card,
.color-wheel-card {
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
.compare-card:hover,
.empty-state-card:hover,
.confusion-card:hover,
.color-wheel-card:hover {
    transform: translateY(-4px);
    border-color: rgba(187, 108, 63, 0.22);
    box-shadow: var(--shadow-lg);
}

.stat-card {
    padding: 1.15rem 1.2rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(241,235,228,0.88));
    animation: cardSlideUp 0.5s ease-out both;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }

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
    background: linear-gradient(135deg, rgba(15,124,120,0.16), rgba(84,103,176,0.14));
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
    animation: cardSlideUp 0.5s ease-out both;
}

.info-card:nth-child(1) { animation-delay: 0.05s; }
.info-card:nth-child(2) { animation-delay: 0.1s; }
.info-card:nth-child(3) { animation-delay: 0.15s; }
.info-card:nth-child(4) { animation-delay: 0.2s; }

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
    background: radial-gradient(circle, rgba(15,124,120,0.16), transparent 70%);
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
    animation: cardSlideUp 0.5s ease-out;
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
    animation: cardSlideUp 0.4s ease-out both;
}

.color-card:nth-child(1) { animation-delay: 0.05s; }
.color-card:nth-child(2) { animation-delay: 0.1s; }
.color-card:nth-child(3) { animation-delay: 0.15s; }

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
    transition: transform 200ms ease;
}

.mini-swatch:hover {
    transform: scale(1.3);
}

.swatch {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    border: 1px solid rgba(20, 33, 43, 0.08);
    flex-shrink: 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
    transition: transform 200ms ease, box-shadow 200ms ease;
}

.swatch:hover {
    transform: scale(1.08);
    box-shadow: var(--shadow-md);
}

.empty-state-card {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    align-items: center;
    column-gap: 1rem;
    min-height: 132px;
    padding: 1.2rem 1.35rem;
    background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
    animation: cardSlideUp 0.5s ease-out;
}

.empty-state-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    grid-row: 1 / span 2;
    width: 64px;
    height: 64px;
    margin: 0;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(187,108,63,0.12), rgba(47,116,135,0.10));
    font-size: 1.75rem;
}

.bento-grid {
    display: grid;
    gap: 1rem;
    margin-bottom: 1rem;
}

.bento-grid.cols-4 {
    grid-template-columns: repeat(4, 1fr);
}

.bento-grid.cols-3 {
    grid-template-columns: repeat(3, 1fr);
}

.bento-grid .span-2 {
    grid-column: span 2;
}

.bento-grid .span-row {
    grid-row: span 2;
}

.bento-cell {
    border-radius: var(--radius-lg);
    border: 1px solid var(--line);
    background: var(--surface-0);
    backdrop-filter: blur(18px);
    box-shadow: var(--shadow-md);
    padding: 1.1rem;
    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.bento-cell:hover {
    transform: translateY(-3px);
    border-color: rgba(187, 108, 63, 0.22);
    box-shadow: var(--shadow-lg);
}

.workflow-strip {
    border-radius: var(--radius-lg);
    border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(235,245,242,0.84));
    box-shadow: var(--shadow-md);
    padding: 1.15rem;
    margin: 0 0 1rem;
    animation: cardSlideUp 0.45s ease-out;
}

.workflow-strip-head {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.9rem;
}

.workflow-strip-head h3 {
    max-width: 42rem;
    margin: 0;
    font-size: 1.45rem;
}

.workflow-step-grid,
.scenario-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
}

.workflow-step,
.scenario-card {
    border-radius: var(--radius-md);
    border: 1px solid rgba(19, 37, 40, 0.08);
    background: rgba(255,255,255,0.72);
    padding: 0.95rem;
    min-height: 132px;
    box-shadow: var(--shadow-sm);
}

.workflow-step span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    margin-bottom: 0.72rem;
    border-radius: 12px;
    background: var(--accent);
    color: white;
    font-weight: 800;
}

.workflow-step strong,
.scenario-card h4 {
    display: block;
    margin: 0 0 0.34rem;
    color: var(--ink-strong);
    font-size: 1rem;
}

.workflow-step p,
.scenario-card p {
    margin: 0;
    color: var(--muted);
    font-size: 0.88rem;
    line-height: 1.5;
}

.scenario-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    margin-bottom: 1rem;
}

.scenario-card {
    min-height: 116px;
}

.bento-cell h4 {
    margin: 0 0 0.4rem;
    font-size: 1.1rem;
}

.bento-cell p {
    margin: 0;
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.5;
}

@property --metric-target {
    syntax: '<integer>';
    inherits: false;
    initial-value: 0;
}

.metric-counter {
    font-family: 'Fraunces', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--ink-strong);
    letter-spacing: -0.03em;
    animation: metricCountIn 0.8s ease-out;
}

@keyframes metricCountIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-fabric-bubble {
    border-radius: var(--radius-lg);
    border: 1px solid var(--line);
    background: var(--surface-0);
    backdrop-filter: blur(18px);
    box-shadow: var(--shadow-sm);
    padding: 1.2rem 1.4rem;
    animation: cardSlideUp 0.4s ease-out;
}

section[data-testid="stSidebar"] .nav-link {
    border-radius: 16px;
    min-height: 44px;
    backdrop-filter: blur(14px);
}

section[data-testid="stSidebar"] .nav-link:hover {
    transform: translateX(4px);
    border-color: var(--line);
    background: rgba(255, 255, 255, 0.62) !important;
}

.image-comparison-container {
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--line);
    box-shadow: var(--shadow-md);
    margin-bottom: 1rem;
}

.ag-theme-balham {
    border-radius: var(--radius-md) !important;
    overflow: hidden;
    border: 1px solid var(--line) !important;
    box-shadow: var(--shadow-md);
}

.ag-header {
    background: rgba(244, 238, 231, 0.95) !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    border-bottom: 1px solid var(--line) !important;
}

.ag-row {
    font-family: 'Manrope', sans-serif !important;
    border-bottom: 1px solid var(--line) !important;
    transition: background 150ms ease !important;
}

.ag-row:hover {
    background: rgba(187, 108, 63, 0.06) !important;
}

.ag-row-selected {
    background: rgba(187, 108, 63, 0.12) !important;
}

.empty-state-card h3 {
    margin: 0 0 0.25rem;
    min-width: 0;
    font-size: 1.3rem;
    line-height: 1.2;
    letter-spacing: -0.015em;
    overflow-wrap: anywhere;
}

.empty-state-card p {
    max-width: 42rem;
    margin: 0;
    color: var(--muted);
    line-height: 1.6;
}

.confusion-card {
    padding: 1rem;
    background: var(--surface-1);
}

.confusion-card h4 {
    margin: 0 0 0.75rem;
}

.color-wheel-card {
    padding: 1rem;
    background: var(--surface-1);
}

.color-wheel-card h4 {
    margin: 0 0 0.5rem;
}

.skeleton {
    background: var(--skeleton-base);
    border-radius: var(--radius-sm);
    position: relative;
    overflow: hidden;
}

.skeleton::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        transparent,
        var(--skeleton-shine),
        transparent
    );
    animation: skeletonShimmer 1.8s ease-in-out infinite;
}

.skeleton-text {
    height: 14px;
    margin-bottom: 8px;
    border-radius: 6px;
}

.skeleton-text:last-child {
    width: 60%;
}

.skeleton-title {
    height: 24px;
    width: 45%;
    margin-bottom: 12px;
    border-radius: 8px;
}

.skeleton-card {
    height: 138px;
    border-radius: var(--radius-md);
}

.skeleton-swatch {
    width: 64px;
    height: 64px;
    border-radius: 18px;
}

.floating-action-bar {
    position: fixed;
    bottom: 1.2rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 999;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.65rem 1rem;
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(20px);
    border: 1px solid var(--line);
    box-shadow: 0 18px 52px rgba(18, 28, 36, 0.18);
    animation: floatBarIn 0.4s ease-out;
}

.floating-action-bar .fab-label {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ink);
    padding-right: 0.5rem;
    border-right: 1px solid var(--line);
    white-space: nowrap;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.65rem;
    border-radius: var(--radius-pill);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.badge-success {
    background: rgba(47, 125, 99, 0.12);
    color: var(--success);
    border: 1px solid rgba(47, 125, 99, 0.18);
}

.badge-warning {
    background: rgba(159, 106, 36, 0.12);
    color: var(--warning);
    border: 1px solid rgba(159, 106, 36, 0.18);
}

.badge-danger {
    background: rgba(154, 75, 73, 0.12);
    color: var(--danger);
    border: 1px solid rgba(154, 75, 73, 0.18);
}

.badge-accent {
    background: var(--accent-soft);
    color: var(--accent-strong);
    border: 1px solid rgba(187, 108, 63, 0.18);
}

.badge-cool {
    background: rgba(47, 116, 135, 0.12);
    color: var(--accent-cool);
    border: 1px solid rgba(47, 116, 135, 0.18);
}

.tooltip-trigger {
    position: relative;
    cursor: help;
    border-bottom: 1px dashed var(--muted-soft);
}

.tooltip-trigger:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    padding: 0.45rem 0.75rem;
    background: var(--tooltip-bg);
    color: var(--tooltip-fg);
    font-size: 0.78rem;
    font-weight: 600;
    line-height: 1.4;
    border-radius: 8px;
    white-space: nowrap;
    z-index: 100;
    box-shadow: 0 8px 24px rgba(0,0,0,0.14);
    animation: tooltipIn 150ms ease-out;
}

.tooltip-trigger:hover::before {
    content: "";
    position: absolute;
    bottom: calc(100% + 2px);
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: var(--tooltip-bg);
    z-index: 100;
}

.confidence-bar-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.4rem;
}

.confidence-bar {
    flex: 1;
    height: 8px;
    border-radius: 999px;
    background: var(--skeleton-base);
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 600ms ease-out;
}

.confidence-bar-fill.high {
    background: linear-gradient(90deg, var(--success), #3da87a);
}

.confidence-bar-fill.medium {
    background: linear-gradient(90deg, var(--warning), #c4862e);
}

.confidence-bar-fill.low {
    background: linear-gradient(90deg, var(--danger), #c4605e);
}

.confidence-bar-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink);
    min-width: 3.5ch;
    text-align: right;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 999px;
    margin-right: 0.3rem;
}

.status-dot.online {
    background: var(--success);
    box-shadow: 0 0 0 3px rgba(47, 125, 99, 0.2);
}

.status-dot.offline {
    background: var(--muted-soft);
}

.pulse-dot {
    animation: pulse 2s ease-in-out infinite;
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

.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0px) scale(0.98);
}

.stFileUploader,
[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput > div > div,
.stTextArea textarea {
    border-radius: var(--radius-sm) !important;
}

[data-testid="stFileUploader"] {
    width: 100%;
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 96px;
    padding: 1rem 1.2rem !important;
    border: 1px dashed rgba(15, 124, 120, 0.36) !important;
    border-radius: var(--radius-md) !important;
    background: linear-gradient(180deg, rgba(255,255,255,0.68), rgba(221,239,235,0.64)) !important;
}

[data-testid="stFileUploaderDropzone"] > div {
    min-width: 0;
}

[data-testid="stFileUploaderDropzone"] button {
    border-radius: var(--radius-sm) !important;
    white-space: nowrap;
}

.stTextArea textarea,
.stTextInput input {
    background: rgba(255,255,255,0.72) !important;
}

.stRadio [role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.55rem;
}

.stRadio [role="radiogroup"] label {
    display: inline-flex;
    align-items: center;
    min-height: 40px;
    border-radius: var(--radius-pill);
    padding: 0.24rem 0.78rem 0.24rem 0.36rem;
    background: rgba(255,255,255,0.58);
    border: 1px solid rgba(20, 33, 43, 0.08);
    box-shadow: var(--shadow-sm);
    white-space: nowrap;
}

.stRadio [role="radiogroup"] div[data-testid="stMarkdownContainer"] p {
    margin: 0;
    line-height: 1.2;
    white-space: nowrap;
}

section[data-testid="stSidebar"] .stToggle {
    margin-top: 0.5rem;
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
    transition: all 200ms ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.78);
    transform: translateY(-1px);
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
    transition: transform 180ms ease, box-shadow 180ms ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
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
    transition: all 200ms ease;
}

.streamlit-expanderHeader:hover {
    background: rgba(255,255,255,0.72);
}

hr {
    border-color: var(--line);
}

[data-testid="stStatusWidget"] {
    border-radius: var(--radius-md);
    overflow: hidden;
}

[data-testid="stToast"] {
    border-radius: var(--radius-md);
    backdrop-filter: blur(18px);
    border: 1px solid var(--line);
    box-shadow: var(--shadow-lg);
}

@keyframes drift {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(10px) translateX(-6px); }
}

@keyframes cardSlideUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

@keyframes skeletonShimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes floatBarIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

@keyframes tooltipIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(4px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
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

    .floating-action-bar {
        left: 1rem;
        right: 1rem;
        transform: none;
    }

    .workflow-step-grid,
    .scenario-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 720px) {
    .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
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

    .empty-state-card {
        grid-template-columns: 1fr;
        align-items: start;
    }

    .empty-state-icon {
        grid-row: auto;
        margin-bottom: 0.85rem;
    }

    .floating-action-bar {
        bottom: 0.8rem;
        padding: 0.5rem 0.75rem;
    }

    .workflow-strip-head {
        display: block;
    }

    .workflow-step-grid,
    .scenario-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

DARK_MODE_CSS = """
<style>
:root {
    --bg-top: #111820;
    --bg-bottom: #0d1219;
    --surface-0: rgba(28, 38, 50, 0.78);
    --surface-1: rgba(32, 44, 58, 0.88);
    --surface-2: rgba(26, 36, 48, 0.96);
    --surface-3: rgba(22, 30, 40, 0.95);
    --ink-strong: #e8edf2;
    --ink: #c5cdd6;
    --muted: #8a95a3;
    --muted-soft: #6b7a8a;
    --line: rgba(200, 215, 230, 0.08);
    --line-strong: rgba(200, 215, 230, 0.14);
    --accent: #77d4ca;
    --accent-strong: #9ff0e7;
    --accent-soft: rgba(119, 212, 202, 0.15);
    --accent-cool: #9fabff;
    --shadow-sm: 0 10px 30px rgba(0, 0, 0, 0.22);
    --shadow-md: 0 22px 60px rgba(0, 0, 0, 0.32);
    --shadow-lg: 0 36px 80px rgba(0, 0, 0, 0.40);
    --skeleton-base: rgba(255, 255, 255, 0.06);
    --skeleton-shine: rgba(255, 255, 255, 0.12);
    --tooltip-bg: #f0f4f8;
    --tooltip-fg: #1e2d3a;
}

.stApp {
    background:
        radial-gradient(circle at 12% 12%, rgba(119, 212, 202, 0.10), transparent 24%),
        radial-gradient(circle at 90% 8%, rgba(159, 171, 255, 0.12), transparent 20%),
        radial-gradient(circle at 84% 84%, rgba(47, 125, 99, 0.10), transparent 18%),
        linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
    color: var(--ink);
}

.stApp::before {
    background-image:
        linear-gradient(rgba(200, 215, 230, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(200, 215, 230, 0.025) 1px, transparent 1px);
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(24, 32, 42, 0.90), rgba(18, 24, 32, 0.88));
    border-right: 1px solid var(--line);
}

.sidebar-brand-card {
    background:
        radial-gradient(circle at top right, rgba(119,212,202,0.18), transparent 36%),
        linear-gradient(180deg, rgba(32, 44, 58, 0.92), rgba(26, 36, 48, 0.88));
}

.sidebar-brand-card h3 {
    color: var(--ink-strong);
}

.sidebar-brand-card p {
    color: var(--muted);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    color: var(--ink);
    background: rgba(32, 44, 58, 0.48);
    border-color: var(--line);
}

section[data-testid="stSidebar"] .nav-link:hover {
    background: rgba(32, 44, 58, 0.72) !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(119, 212, 202, 0.10);
    border-color: var(--line);
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
    background: rgba(119, 212, 202, 0.18) !important;
    border-color: rgba(119, 212, 202, 0.5) !important;
    color: var(--accent-strong) !important;
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
    color: var(--accent-strong) !important;
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
.compare-card,
.empty-state-card,
.confusion-card,
.color-wheel-card,
.floating-action-bar {
    background: var(--surface-0);
    border-color: var(--line);
}

.sidebar-brand-card {
    background:
        radial-gradient(circle at top right, rgba(119,212,202,0.18), transparent 36%),
        linear-gradient(180deg, rgba(32, 44, 58, 0.92), rgba(26, 36, 48, 0.88));
}

.stat-card {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.88), rgba(26, 36, 48, 0.88));
}

.info-card,
.metric-card,
.result-card {
    background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
}

.page-intro {
    background:
        radial-gradient(circle at top left, rgba(47,116,135,0.10), transparent 26%),
        linear-gradient(135deg, rgba(32, 44, 58, 0.92), rgba(26, 36, 48, 0.84));
}

.page-intro::before {
    background: linear-gradient(90deg, var(--accent), var(--accent-cool));
}

.hero-shell {
    background:
        radial-gradient(circle at top right, rgba(119,212,202,0.15), transparent 28%),
        radial-gradient(circle at bottom left, rgba(159,171,255,0.12), transparent 24%),
        linear-gradient(135deg, rgba(32, 44, 58, 0.94), rgba(26, 36, 48, 0.86));
}

.hero-shell h1 {
    background: linear-gradient(135deg, var(--ink-strong) 0%, var(--accent) 50%, var(--accent-cool) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-tags span {
    background: rgba(32, 44, 58, 0.72);
    border-color: var(--line);
    color: var(--ink-strong);
}

.highlight-banner {
    background:
        radial-gradient(circle at top right, rgba(47,116,135,0.10), transparent 28%),
        linear-gradient(135deg, rgba(32, 44, 58, 0.88), rgba(26, 36, 48, 0.92));
}

.color-card {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.88), rgba(26, 36, 48, 0.86));
}

.compare-summary-card {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.90), rgba(26, 36, 48, 0.90));
}

.compare-summary-flow div,
.compare-card-grid div {
    background: rgba(32, 44, 58, 0.66);
    border-color: var(--line);
}

.compare-card {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.90), rgba(26, 36, 48, 0.92));
}

.empty-state-card {
    background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
}

.upload-shell {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.66), rgba(26, 36, 48, 0.88));
}

.workflow-strip {
    background: linear-gradient(135deg, rgba(32, 44, 58, 0.92), rgba(26, 36, 48, 0.84));
}

.workflow-step,
.scenario-card {
    background: rgba(32, 44, 58, 0.66);
    border-color: var(--line);
}

.workflow-step strong,
.scenario-card h4 {
    color: var(--ink-strong);
}

.workflow-step p,
.scenario-card p {
    color: var(--muted);
}

.floating-action-bar {
    background: rgba(24, 32, 42, 0.92);
    border-color: var(--line);
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-strong));
}

.stTextArea textarea,
.stTextInput input {
    background: rgba(32, 44, 58, 0.72) !important;
    color: var(--ink) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.72), rgba(26, 36, 48, 0.84)) !important;
    border-color: rgba(119, 212, 202, 0.42) !important;
}

.stRadio [role="radiogroup"] label {
    background: rgba(32, 44, 58, 0.58);
    border-color: var(--line);
    color: var(--ink);
}

.stTabs [data-baseweb="tab"] {
    background: rgba(32, 44, 58, 0.62);
    border-color: var(--line);
    color: var(--muted);
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(32, 44, 58, 0.78);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(212,136,92,0.16), rgba(47,116,135,0.16));
    color: var(--ink-strong);
    border-color: rgba(212,136,92,0.18);
}

[data-testid="stMetric"] {
    background: linear-gradient(180deg, rgba(32, 44, 58, 0.90), rgba(26, 36, 48, 0.90));
    border-color: var(--line);
}

[data-testid="stDataFrame"] {
    background: rgba(32, 44, 58, 0.78);
    border-color: var(--line);
}

[data-testid="stDataFrame"] [role="table"] {
    background: rgba(32, 44, 58, 0.72);
}

.streamlit-expanderHeader {
    background: rgba(32, 44, 58, 0.56);
    border-color: var(--line);
    color: var(--ink);
}

.streamlit-expanderHeader:hover {
    background: rgba(32, 44, 58, 0.72);
}

.mini-swatch {
    border-color: var(--line);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22);
}

.swatch {
    border-color: var(--line);
}

.status-dot.online {
    box-shadow: 0 0 0 3px rgba(47, 125, 99, 0.3);
}

[data-testid="stToast"] {
    background: rgba(24, 32, 42, 0.92);
    border-color: var(--line);
    color: var(--ink);
}

h1, h2, h3, h4 {
    color: var(--ink-strong);
}

p, li, label, .stMarkdown, .stCaption {
    color: var(--ink);
}
</style>
"""
