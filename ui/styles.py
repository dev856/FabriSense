"""Custom CSS for the FabriSense interface."""

from __future__ import annotations

import colorsys


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@300;400;500;600;700&display=swap');

:root {
    --bg-top: #0B0F14;
    --bg-bottom: #0B0F14;
    --surface-0: #FAF7F2;
    --surface-1: #FAF7F2;
    --surface-2: #F2EDE6;
    --surface-3: #E8E3DB;
    --ink-strong: #1A1A1A;
    --ink: #2C2A27;
    --muted: #5C5A57;
    --muted-soft: #8A867F;
    --line: rgba(201,168,107,0.20);
    --line-strong: rgba(201,168,107,0.35);
    --accent: #C9A86B;
    --accent-strong: #A8834A;
    --accent-soft: rgba(201,168,107,0.12);
    --accent-cool: #D0B87E;
    --success: #C9A86B;
    --warning: #B08968;
    --danger: #8B5E3C;
    --shadow-sm: 0 10px 30px rgba(0,0,0,0.25);
    --shadow-md: 0 22px 60px rgba(0,0,0,0.35);
    --shadow-lg: 0 36px 80px rgba(0,0,0,0.45);
    --radius-sm: 12px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --radius-pill: 999px;
}

:root {
    --bg: var(--bg-top);
    --bg-rgb: 11, 15, 20;
    --bg-elev: #121820;
    --surface: var(--surface-0);
    --surface-rgb: 250, 247, 242;
    --surface-muted: var(--surface-3);
    --brass: var(--accent);
    --brass-rgb: 201, 168, 107;
    --brass-2: var(--accent-cool);
    --text-1: var(--surface-3);
    --text-2: #C9C0B6;
    --ink-soft: var(--muted);
    --stone: var(--muted-soft);
    --danger-rgb: 139, 94, 60;
    --success-rgb: 201, 168, 107;
    --warning-rgb: 176, 137, 104;
    --radius: var(--radius-md);
    --shadow: var(--shadow-md);
    --shadow-soft: var(--shadow-sm);
    --font-serif: 'Fraunces', Georgia, serif;
    --font-sans: 'Manrope', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

html, body {
    background: var(--bg-top) !important;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 8%, rgba(201,168,107,0.06), transparent 40%),
        radial-gradient(ellipse at 85% 92%, rgba(201,168,107,0.04), transparent 35%),
        radial-gradient(ellipse at 50% 50%, rgba(208,184,126,0.025), transparent 60%),
        var(--bg-top) !important;
    color: #E8E3DB;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"],
header[data-testid="stHeader"] {
    background: var(--bg-top) !important;
    border-bottom: 1px solid rgba(201,168,107,0.10) !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    background: transparent !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] [role="button"] {
    color: var(--muted-soft) !important;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
    z-index: 0;
}

html,
body,
.stApp,
.stApp p,
.stApp div,
.stApp label,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p {
    font-family: var(--font-sans) !important;
}

/* Keep Streamlit/Material ligature icons from rendering as literal text. */
.stApp [class*="material-icons"],
.stApp [class*="material-symbols"],
.stApp [data-testid*="IconMaterial"],
.stApp [data-testid*="IconMaterial"] span {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    line-height: 1 !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    font-feature-settings: "liga" !important;
    -webkit-font-feature-settings: "liga" !important;
    -webkit-font-smoothing: antialiased !important;
}

.stApp [data-testid="stMarkdownContainer"] a.anchor-link {
    display: none !important;
}

h1,
h2,
h3,
h4,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3,
.stApp [data-testid="stMarkdownContainer"] h4 {
    color: var(--text-1);
    font-family: var(--font-serif) !important;
    font-weight: 600;
    letter-spacing: -0.01em;
}

p, li, label, .stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-2);
}

a {
    color: var(--brass);
}

hr {
    border-color: var(--line) !important;
}

.block-container {
    position: relative;
    z-index: 1;
    width: min(100%, 1280px);
    max-width: 1280px;
    padding: 1.35rem clamp(1rem, 2.4vw, 2.75rem) 5rem;
}

section[data-testid="stSidebar"] {
    background: #121820 !important;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.1rem 0.65rem 2rem;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    display: none;
}

.sidebar-brand-card {
    padding: 1rem 0.95rem 1.1rem;
    margin-bottom: 1rem;
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    background: rgba(var(--surface-rgb), 0.04);
    box-shadow: var(--shadow-soft);
}

.sidebar-brand-card h3 {
    margin: 0.35rem 0 0.5rem;
    color: var(--surface);
    font-size: 1.35rem;
    line-height: 1.08;
}

.sidebar-brand-card p {
    margin: 0;
    color: var(--text-2);
    font-size: 0.86rem;
    line-height: 1.5;
}

.sidebar-kicker,
.eyebrow {
    margin: 0 0 0.6rem;
    color: var(--brass);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

/* CONTRAST FIX: any ivory surface must use dark ink, never light page text. */
.ivory-card,
.ivory-card h1,
.ivory-card h2,
.ivory-card h3,
.ivory-card h4,
.ivory-card h5,
.ivory-card h6,
.ivory-card p,
.ivory-card li,
.ivory-card label,
.ivory-card span,
.ivory-card div,
.ivory-card strong,
.ivory-card em,
.ivory-card small,
.ivory-card [data-testid="stMarkdownContainer"] p {
    color: #1A1A1A !important;
    opacity: 1 !important;
}

.ivory-card .eyebrow,
.ivory-card .metric-label,
.ivory-card .fs-label,
.ivory-card .fs-passport-label,
.ivory-card .compare-summary-label,
.ivory-card .compare-summary-flow span,
.ivory-card .compare-card-grid span {
    color: #1A1A1A !important;
}

.ivory-card a,
.ivory-card code,
.ivory-card .fs-metric-value,
.ivory-card .metric-counter {
    color: #1A1A1A !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 0.35rem;
    flex-direction: column;
    align-items: stretch !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    width: 100% !important;
    min-height: 44px;
    margin: 0 !important;
    padding: 0.62rem 0.8rem;
    border: 1px solid transparent;
    border-radius: 12px;
    background: transparent;
    color: var(--text-2);
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child {
    display: none;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label::before {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    min-width: 24px;
    height: 24px;
    margin-right: 0.55rem;
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--brass);
    font-size: 0.88rem;
    line-height: 1;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(1)::before { content: "\\2315"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(2)::before { content: "\\25A6"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(3)::before { content: "\\21C4"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(4)::before { content: "\\25F7"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(5)::before { content: "\\25A4"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(6)::before { content: "\\2726"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(7)::before { content: "\\25C6"; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(8)::before { content: "\\25C7"; }

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(var(--brass-rgb), 0.08) !important;
    border-color: var(--line) !important;
    color: var(--surface) !important;
    transform: translateX(3px);
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
    background: rgba(var(--brass-rgb), 0.14) !important;
    border-color: rgba(var(--brass-rgb), 0.30) !important;
    color: var(--surface) !important;
    box-shadow: 0 4px 16px rgba(var(--brass-rgb), 0.08) !important;
}

section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p {
    color: var(--text-2) !important;
    font-size: 0.9rem;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover div[data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
    color: var(--surface-0) !important;
}

.fs-card,
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
.bento-cell,
.chat-fabric-bubble {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--surface) !important;
    color: var(--ink) !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.35s ease !important;
    animation: cardReveal 0.5s cubic-bezier(0.16, 1, 0.3, 1) backwards !important;
}

.fs-card {
    padding: 28px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow) !important;
    padding: 1.35rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: var(--ink) !important;
    font-family: var(--font-serif) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] label,
[data-testid="stVerticalBlockBorderWrapper"] span {
    color: var(--ink-soft) !important;
}

.fs-card h1,
.fs-card h2,
.fs-card h3,
.fs-card h4,
.page-intro h2,
.hero-shell h1,
.stat-card h4,
.info-card h3,
.metric-card h3,
.result-card h3,
.color-card h4,
.compare-card h3,
.empty-state-card h3,
.bento-cell h4 {
    color: var(--ink) !important;
}

.fs-card p,
.page-intro p,
.hero-shell p,
.stat-card p,
.info-card p,
.metric-card p,
.result-card p,
.color-card p,
.compare-card p,
.empty-state-card p,
.bento-cell p {
    color: var(--ink-soft) !important;
}

.page-intro {
    padding: 1.3rem 1.5rem !important;
    margin-bottom: 1.2rem !important;
}

.page-intro h2 {
    margin: 0 !important;
    font-size: clamp(2rem, 3vw, 3.2rem) !important;
    line-height: 1.05 !important;
}

.page-intro-text {
    max-width: 62rem !important;
    margin: 0.6rem 0 0 !important;
    font-size: 1rem !important;
    line-height: 1.65 !important;
}

.hero-shell {
    display: grid !important;
    gap: 1.4rem !important;
    width: 100% !important;
    min-height: 340px !important;
    margin: 0 0 0.9rem !important;
    padding: clamp(2rem, 4.5vw, 4rem) clamp(1.8rem, 4vw, 4.5rem) !important;
    align-items: center !important;
}

.atelier-home-card {
    text-align: center !important;
}

.hero-shell h1 {
    max-width: 18ch !important;
    margin: 0 auto 1rem !important;
    color: var(--ink-strong) !important;
    font-size: clamp(2.6rem, 4.2vw, 4.6rem) !important;
    line-height: 1.02 !important;
}

.hero-text {
    max-width: 42rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
    color: var(--muted) !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}

.hero-tags,
.mini-swatch-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.5rem !important;
}

.hero-tags span,
.badge {
    display: inline-flex !important;
    align-items: center !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-pill) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
}

.hero-tags span {
    padding: 0.44rem 0.72rem !important;
    color: var(--ink) !important;
    background: rgba(var(--brass-rgb), 0.10) !important;
}

.atelier-home-card .hero-tags {
    justify-content: center !important;
}

.hero-stats {
    display: grid !important;
    gap: 0.85rem !important;
}

.stat-card,
.info-card,
.metric-card,
.result-card,
.compare-summary-card,
.compare-card,
.empty-state-card,
.confusion-card,
.color-wheel-card,
.bento-cell {
    padding: 1rem !important;
}

.info-card {
    display: flex !important;
    min-height: 128px !important;
    height: 100% !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
}

.info-card h3,
.workflow-strip h3 {
    margin: 0 0 0.55rem !important;
    font-size: 1.05rem !important;
    line-height: 1.25 !important;
}

.info-card p,
.workflow-step p,
.scenario-card p,
.stat-card p {
    margin: 0 !important;
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    line-height: 1.55 !important;
    opacity: 1 !important;
}

.stat-icon,
.empty-state-icon {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 44px !important;
    height: 44px !important;
    border-radius: 12px !important;
    background: var(--bg) !important;
    color: var(--brass) !important;
}

.metric-card {
    background: var(--surface-0) !important;
    color: #1A1A1A !important;
    min-height: 128px !important;
}

.fs-metric-card {
    padding: 20px !important;
    min-height: 120px !important;
}

.metric-card .metric-label,
.fs-label,
.compare-summary-label,
.compare-summary-flow span,
.compare-card-grid span {
    color: var(--stone) !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

.metric-card h3,
.fs-metric-value,
.metric-counter {
    margin: 0.35rem 0 0.15rem !important;
    color: var(--brass) !important;
    font-family: var(--font-serif) !important;
    font-size: 2rem !important;
    font-variant-numeric: tabular-nums !important;
    line-height: 1.05 !important;
}

.fs-metric-sub {
    color: var(--ink-soft) !important;
    font-size: 0.82rem !important;
    line-height: 1.45 !important;
}

.upload-shell {
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(201,168,107,0.04) !important;
    border: 2px dashed var(--accent) !important;
    border-radius: 16px !important;
    min-height: 220px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(var(--brass-rgb), 0.06) !important;
}

[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {
    color: var(--text-2) !important;
}

.fs-sticky-image {
    position: sticky !important;
    top: 1rem !important;
}

.result-sticky {
    position: sticky;
    top: 1.5rem;
}

.fs-sticky-image img,
.compare-card img,
[data-testid="stImage"] img {
    border-radius: var(--radius) !important;
}

.fs-passport {
    display: grid !important;
    gap: 1rem !important;
}

.fs-passport-grid,
.compare-card-grid,
.compare-summary-flow {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 0.8rem !important;
}

.fs-passport-item,
.compare-card-grid div,
.compare-summary-flow div {
    padding: 0.9rem !important;
    border: 1px solid rgba(var(--bg-rgb), 0.08) !important;
    border-radius: 12px !important;
    background: rgba(var(--bg-rgb), 0.03) !important;
}

.fs-passport-label {
    color: var(--stone) !important;
    font-size: 0.68rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

.fs-passport-value,
.compare-card-grid strong,
.compare-summary-flow strong {
    display: block !important;
    margin-top: 0.3rem !important;
    color: var(--ink) !important;
    font-weight: 700 !important;
    line-height: 1.35 !important;
}

.fs-palette-bar {
    display: flex !important;
    gap: 6px !important;
    margin: 0.75rem 0 0.25rem !important;
}

.fs-gradient-bar {
    height: 16px !important;
    margin-bottom: 0.6rem !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 20px rgba(var(--bg-rgb), 0.10) !important;
}

.fs-palette-chip {
    flex: 1 !important;
    min-width: 28px !important;
    height: 16px !important;
    border-radius: 6px !important;
    border: 1px solid var(--line) !important;
}

.color-card {
    display: flex !important;
    align-items: center !important;
    gap: 0.9rem !important;
    margin-bottom: 0.8rem !important;
}

.swatch {
    width: 62px !important;
    height: 62px !important;
    flex-shrink: 0 !important;
    border: 1px solid rgba(var(--bg-rgb), 0.10) !important;
    border-radius: 16px !important;
}

.mini-swatch {
    display: inline-block !important;
    width: 18px !important;
    height: 18px !important;
    border: 1px solid rgba(var(--bg-rgb), 0.12) !important;
    border-radius: var(--radius-pill) !important;
}

.highlight-banner {
    padding: 1rem 1.1rem !important;
    margin-bottom: 1rem !important;
    background: var(--bg-elev) !important;
    color: var(--text-1) !important;
}

.highlight-banner strong {
    display: block !important;
    margin-bottom: 0.3rem !important;
    color: var(--brass) !important;
}

.highlight-banner p {
    margin: 0 !important;
    color: var(--text-2) !important;
}

.empty-state-card {
    display: grid !important;
    grid-template-columns: auto minmax(0, 1fr) !important;
    gap: 0.2rem 1rem !important;
    align-items: center !important;
}

.empty-state-icon {
    grid-row: 1 / span 2 !important;
}

.workflow-strip,
.feature-strip,
.scenario-card,
.floating-action-bar {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: rgba(var(--surface-rgb), 0.04) !important;
    padding: 1rem !important;
}

.workflow-strip {
    background: #121820 !important;
    margin: 0 0 1rem !important;
    padding: 1rem !important;
}

.workflow-strip h3 {
    color: var(--surface-0) !important;
}

.workflow-step-grid,
.feature-card-grid,
.scenario-grid,
.bento-grid {
    display: grid !important;
    gap: 1rem !important;
}

.workflow-step-grid,
.feature-card-grid,
.scenario-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}

.workflow-step-grid,
.feature-card-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
}

.feature-strip {
    margin: 0 0 0.95rem !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

.workflow-step {
    display: flex !important;
    height: 100% !important;
    flex-direction: column !important;
    padding: 0.9rem !important;
    min-height: 124px !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    color: var(--ink) !important;
}

.workflow-step span {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 26px !important;
    height: 26px !important;
    margin-bottom: 0.55rem !important;
    border-radius: 8px !important;
    background: var(--bg) !important;
    color: var(--brass) !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}

.workflow-step strong,
.scenario-card h4 {
    display: block !important;
    color: var(--ink) !important;
}

.scenario-card {
    background: var(--surface) !important;
    color: var(--ink) !important;
}

.bento-grid.cols-4 {
    grid-template-columns: repeat(4, 1fr) !important;
}

.bento-grid.cols-3 {
    grid-template-columns: repeat(3, 1fr) !important;
}

.bento-grid .span-2 {
    grid-column: span 2 !important;
}

.bento-grid .span-row {
    grid-row: span 2 !important;
}

.bento-cell:hover,
.stat-card:hover,
.info-card:hover,
.metric-card:hover,
.result-card:hover,
.compare-card:hover,
.color-card:hover,
.fs-card:hover,
.compare-summary-card:hover,
.confusion-card:hover,
.color-wheel-card:hover,
.empty-state-card:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(201,168,107,0.35) !important;
    box-shadow: var(--shadow-lg), 0 0 40px rgba(201,168,107,0.06) !important;
}

.stButton > button,
.stDownloadButton > button {
    height: 44px !important;
    border: 0 !important;
    border-radius: 12px !important;
    background: linear-gradient(180deg, var(--brass-2), var(--brass)) !important;
    color: var(--bg) !important;
    font-weight: 700 !important;
    box-shadow: 0 14px 28px -18px rgba(var(--brass-rgb), 0.75) !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.2s ease,
                filter 0.2s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    filter: brightness(1.08) !important;
    box-shadow: 0 18px 36px -14px rgba(var(--brass-rgb), 0.85) !important;
}

.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
    filter: brightness(0.98) !important;
}

.stTextArea textarea,
.stTextInput input,
[data-baseweb="select"] > div {
    border-color: var(--line) !important;
    border-radius: 12px !important;
    background: rgba(var(--surface-rgb), 0.06) !important;
    color: var(--text-1) !important;
}

.stRadio [role="radiogroup"] label,
.stCheckbox label,
.stToggle label {
    color: var(--text-2) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem !important;
    border-bottom: 1px solid var(--line) !important;
}

.stTabs [data-baseweb="tab"] {
    border: 1px solid transparent !important;
    border-radius: 12px 12px 0 0 !important;
    color: var(--text-2) !important;
}

.stTabs [aria-selected="true"] {
    border-color: var(--line) !important;
    background: rgba(var(--brass-rgb), 0.10) !important;
    color: var(--brass) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--brass) !important;
}

[data-testid="stMetric"],
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    color: var(--ink) !important;
    box-shadow: var(--shadow-soft) !important;
}

[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
    color: var(--ink) !important;
}

[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: var(--stone) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--brass) !important;
    font-family: var(--font-serif) !important;
}

.badge {
    padding: 0.22rem 0.55rem !important;
}

.badge-success {
    background: rgba(var(--success-rgb), 0.12) !important;
    color: var(--success) !important;
}

.badge-warning {
    background: rgba(var(--warning-rgb), 0.12) !important;
    color: var(--warning) !important;
}

.badge-danger {
    background: rgba(var(--danger-rgb), 0.12) !important;
    color: var(--danger) !important;
}

.badge-accent,
.badge-cool {
    background: rgba(var(--brass-rgb), 0.14) !important;
    color: var(--brass) !important;
}

.status-dot {
    display: inline-block !important;
    width: 0.65rem !important;
    height: 0.65rem !important;
    margin-right: 0.4rem !important;
    border-radius: var(--radius-pill) !important;
    background: var(--danger) !important;
}

.status-dot.online {
    background: var(--success) !important;
}

.pulse-dot {
    box-shadow: 0 0 0 0 rgba(var(--success-rgb), 0.50) !important;
    animation: pulse 1.8s ease-out infinite !important;
}

.confidence-bar-container {
    display: grid !important;
    grid-template-columns: minmax(8ch, auto) 1fr 4.5rem !important;
    gap: 0.65rem !important;
    align-items: center !important;
    margin-bottom: 0.55rem !important;
}

.confidence-bar {
    height: 8px !important;
    overflow: hidden !important;
    border-radius: var(--radius-pill) !important;
    background: rgba(var(--bg-rgb), 0.10) !important;
}

.confidence-bar-fill {
    height: 100% !important;
    border-radius: inherit !important;
    background: var(--brass) !important;
}

.confidence-bar-fill.low {
    background: var(--danger) !important;
}

.confidence-bar-fill.medium {
    background: var(--warning) !important;
}

.confidence-bar-fill.high {
    background: var(--success) !important;
}

.confidence-bar-label {
    color: var(--ink) !important;
    font-weight: 700 !important;
    text-align: right !important;
}

.skeleton {
    border-radius: 10px !important;
    background: linear-gradient(90deg, rgba(var(--brass-rgb),0.10), rgba(var(--surface-rgb),0.18), rgba(var(--brass-rgb),0.10)) !important;
    background-size: 220% 100% !important;
    animation: shimmer 1.5s infinite !important;
}

.skeleton-title {
    width: 45% !important;
    height: 18px !important;
    margin-bottom: 0.8rem !important;
}

.skeleton-text {
    height: 12px !important;
    margin-bottom: 0.5rem !important;
}

.skeleton-card {
    height: 116px !important;
}

.skeleton-swatch {
    width: 64px !important;
    height: 64px !important;
}

.ag-theme-balham,
.ag-header,
.ag-row {
    border-color: var(--line) !important;
}

.ag-header {
    background: var(--bg-elev) !important;
    color: var(--text-1) !important;
}

.ag-row:hover,
.ag-row-selected {
    background: rgba(var(--brass-rgb), 0.08) !important;
}

.image-comparison-container {
    border-color: var(--line) !important;
}

.floating-action-bar {
    position: sticky !important;
    bottom: 1rem !important;
    z-index: 10 !important;
    display: flex !important;
    gap: 0.75rem !important;
    align-items: center !important;
    color: var(--text-1) !important;
    background: var(--bg-elev) !important;
}

.fab-label {
    color: var(--brass) !important;
    font-weight: 700 !important;
}

details[data-testid="stExpander"],
[data-testid="stExpander"] {
    overflow: hidden !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: rgba(var(--surface-rgb), 0.04) !important;
    box-shadow: var(--shadow-sm) !important;
}

details[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary,
.streamlit-expanderHeader {
    min-height: 48px !important;
    border-bottom: 1px solid var(--line) !important;
    background: var(--surface-2) !important;
    color: var(--ink-strong) !important;
    font-weight: 800 !important;
}

details[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary p,
.streamlit-expanderHeader p {
    color: var(--ink-strong) !important;
    font-weight: 800 !important;
}

[data-testid="stExpanderDetails"] {
    background: rgba(var(--bg-rgb), 0.25) !important;
    border-top: 0 !important;
}

[data-testid="stExpanderDetails"] p,
[data-testid="stExpanderDetails"] li,
[data-testid="stExpanderDetails"] span {
    color: var(--text-1) !important;
}

/* Perfect light/dark theme text overrides */
.stApp p, .stApp li, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp code {
    color: var(--text-1);
}

.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stCaptionContainer"] p,
.stApp div[role="radiogroup"] p {
    color: var(--text-1) !important;
}

.stApp code {
    background: rgba(250, 247, 242, 0.08) !important;
    color: var(--accent) !important;
    border: 1px solid var(--line) !important;
    border-radius: 6px !important;
}

.page-intro,
.page-intro div,
.page-intro span {
    color: var(--ink) !important;
}

.page-intro h1,
.page-intro h2,
.page-intro h3,
.page-intro h4 {
    color: var(--ink-strong) !important;
}

.page-intro p,
.page-intro .page-intro-text {
    color: var(--muted) !important;
}

.page-intro .eyebrow {
    color: var(--accent) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stWidgetLabel"] p,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p,
[data-testid="stVerticalBlockBorderWrapper"] label,
[data-testid="stVerticalBlockBorderWrapper"] span {
    color: var(--ink-soft) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: var(--ink-strong) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] > div,
[data-testid="stVerticalBlockBorderWrapper"] .stTextInput input,
[data-testid="stVerticalBlockBorderWrapper"] .stTextArea textarea {
    background: rgba(var(--bg-rgb), 0.03) !important;
    color: var(--ink) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] *,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stFileUploaderDropzone"] span,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stFileUploaderDropzone"] small {
    color: var(--ink) !important;
}

details[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary p,
.streamlit-expanderHeader p,
.streamlit-expanderHeader [data-testid="stMarkdownContainer"] p {
    color: var(--ink-strong) !important;
    font-weight: 800 !important;
}

/* Force dark text for readability on ivory cards */
.fs-card p, .fs-card li, .fs-card label, .fs-card span, .fs-card h1, .fs-card h2, .fs-card h3, .fs-card h4, .fs-card [data-testid="stMarkdownContainer"] p, .fs-card div,
.compare-card p, .compare-card li, .compare-card label, .compare-card span, .compare-card h1, .compare-card h2, .compare-card h3, .compare-card h4, .compare-card [data-testid="stMarkdownContainer"] p, .compare-card div,
.metric-card p, .metric-card li, .metric-card label, .metric-card span, .metric-card h1, .metric-card h2, .metric-card h3, .metric-card h4, .metric-card [data-testid="stMarkdownContainer"] p, .metric-card div,
.stat-card p, .stat-card li, .stat-card label, .stat-card span, .stat-card h1, .stat-card h2, .stat-card h3, .stat-card h4, .stat-card [data-testid="stMarkdownContainer"] p, .stat-card div,
.info-card p, .info-card li, .info-card label, .info-card span, .info-card h1, .info-card h2, .info-card h3, .info-card h4, .info-card [data-testid="stMarkdownContainer"] p, .info-card div,
.result-card p, .result-card li, .result-card label, .result-card span, .result-card h1, .result-card h2, .result-card h3, .result-card h4, .result-card [data-testid="stMarkdownContainer"] p, .result-card div,
.compare-summary-card p, .compare-summary-card li, .compare-summary-card label, .compare-summary-card span, .compare-summary-card h1, .compare-summary-card h2, .compare-summary-card h3, .compare-summary-card h4, .compare-summary-card [data-testid="stMarkdownContainer"] p, .compare-summary-card div,
.hero-shell p, .hero-shell li, .hero-shell label, .hero-shell span, .hero-shell h1, .hero-shell h2, .hero-shell h3, .hero-shell h4, .hero-shell [data-testid="stMarkdownContainer"] p, .hero-shell div {
    color: var(--ink-soft) !important;
}

.fs-card h1, .fs-card h2, .fs-card h3, .fs-card h4,
.compare-card h1, .compare-card h2, .compare-card h3, .compare-card h4,
.metric-card h1, .metric-card h2, .metric-card h3, .metric-card h4,
.stat-card h1, .stat-card h2, .stat-card h3, .stat-card h4,
.info-card h1, .info-card h2, .info-card h3, .info-card h4,
.result-card h1, .result-card h2, .result-card h3, .result-card h4,
.compare-summary-card h1, .compare-summary-card h2, .compare-summary-card h3, .compare-summary-card h4,
.hero-shell h1, .hero-shell h2, .hero-shell h3, .hero-shell h4 {
    color: var(--brass) !important; /* Headings inside cards stand out beautifully in brass */
}

/* Ensure strong spec values inside cards are pure dark ink */
.fs-card strong, .compare-card strong, .metric-card strong, .stat-card strong, .info-card strong, .result-card strong, .compare-summary-card strong, .hero-shell strong {
    color: var(--ink) !important;
}

.result-card .kv-row {
    padding: 0.75rem 0 !important;
    border-bottom: 1px solid rgba(var(--bg-rgb), 0.08) !important;
}

.result-card .kv-row:last-child {
    border-bottom: 0 !important;
}

.result-card .kv-label {
    display: block !important;
    color: var(--muted-soft) !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

.result-card .kv-value {
    display: block !important;
    margin-top: 0.25rem !important;
    color: var(--ink-strong) !important;
    font-weight: 700 !important;
    line-height: 1.45 !important;
}

.result-card ul {
    margin: 0 !important;
    padding-left: 1.1rem !important;
}

.result-card li {
    margin-bottom: 0.45rem !important;
    color: var(--ink-soft) !important;
}

/* Ivory cards always use dark ink for readability. */
.page-intro h1, .page-intro h2, .page-intro h3, .page-intro h4,
.page-intro p, .page-intro li, .page-intro label, .page-intro span, .page-intro div,
.hero-shell h1, .hero-shell h2, .hero-shell h3, .hero-shell h4,
.hero-shell p, .hero-shell li, .hero-shell label, .hero-shell span, .hero-shell div,
.fs-card h1, .fs-card h2, .fs-card h3, .fs-card h4,
.fs-card p, .fs-card li, .fs-card label, .fs-card span, .fs-card div,
.stat-card h1, .stat-card h2, .stat-card h3, .stat-card h4,
.stat-card p, .stat-card li, .stat-card label, .stat-card span, .stat-card div,
.info-card h1, .info-card h2, .info-card h3, .info-card h4,
.info-card p, .info-card li, .info-card label, .info-card span, .info-card div,
.metric-card h1, .metric-card h2, .metric-card h3, .metric-card h4,
.metric-card p, .metric-card li, .metric-card label, .metric-card span, .metric-card div,
.result-card h1, .result-card h2, .result-card h3, .result-card h4,
.result-card p, .result-card li, .result-card label, .result-card span, .result-card div,
.color-card h1, .color-card h2, .color-card h3, .color-card h4,
.color-card p, .color-card li, .color-card label, .color-card span, .color-card div,
.compare-card h1, .compare-card h2, .compare-card h3, .compare-card h4,
.compare-card p, .compare-card li, .compare-card label, .compare-card span, .compare-card div,
.compare-summary-card h1, .compare-summary-card h2, .compare-summary-card h3, .compare-summary-card h4,
.compare-summary-card p, .compare-summary-card li, .compare-summary-card label, .compare-summary-card span, .compare-summary-card div,
.empty-state-card h1, .empty-state-card h2, .empty-state-card h3, .empty-state-card h4,
.empty-state-card p, .empty-state-card li, .empty-state-card label, .empty-state-card span, .empty-state-card div,
.workflow-step h1, .workflow-step h2, .workflow-step h3, .workflow-step h4,
.workflow-step p, .workflow-step li, .workflow-step label, .workflow-step span, .workflow-step div,
.scenario-card h1, .scenario-card h2, .scenario-card h3, .scenario-card h4,
.scenario-card p, .scenario-card li, .scenario-card label, .scenario-card span, .scenario-card div,
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4,
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li,
[data-testid="stVerticalBlockBorderWrapper"] label,
[data-testid="stVerticalBlockBorderWrapper"] span,
[data-testid="stVerticalBlockBorderWrapper"] div {
    color: #1A1A1A !important;
    opacity: 1 !important;
}

.page-intro .eyebrow,
.hero-shell .eyebrow,
.fs-card .eyebrow,
.stat-card .eyebrow,
.info-card .eyebrow,
.metric-card .eyebrow,
.result-card .eyebrow,
.workflow-step .eyebrow,
.scenario-card .eyebrow {
    color: #1A1A1A !important;
}

.atelier-home-card h1,
.atelier-home-card h2,
.atelier-home-card h3,
.atelier-home-card h4 {
    color: var(--ink) !important;
    font-family: var(--font-serif) !important;
}

.atelier-home-card .eyebrow,
.atelier-home-card .hero-tags span {
    color: #1A1A1A !important;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(201, 168, 107, 0.50); }
    70% { box-shadow: 0 0 0 8px rgba(201, 168, 107, 0); }
    100% { box-shadow: 0 0 0 0 rgba(201, 168, 107, 0); }
}

@keyframes cardReveal {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes cardSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes gradientShift {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.04); }
}

@keyframes skeletonShimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

@keyframes brassGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(201,168,107,0.04); }
    50% { box-shadow: 0 0 30px rgba(201,168,107,0.08); }
}

@media (max-width: 980px) {
    .hero-shell {
        padding: 1.5rem !important;
    }
}

@media (max-width: 720px) {
    .fs-card,
    .page-intro,
    .hero-shell {
        border-radius: var(--radius) !important;
    }
}

@media (max-width: 900px) {
    .workflow-step-grid,
    .feature-card-grid,
    .scenario-grid,
    .bento-grid.cols-4,
    .bento-grid.cols-3,
    .fs-passport-grid,
    .compare-card-grid,
    .compare-summary-flow {
        grid-template-columns: 1fr !important;
    }

    .block-container {
        padding-inline: 1rem !important;
    }
}

/* FINAL CONTRAST GUARD: this must stay after all card typography rules. */
.ivory-card,
.ivory-card *,
.ivory-card [data-testid="stMarkdownContainer"],
.ivory-card [data-testid="stMarkdownContainer"] *,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] *,
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] *,
[data-testid="stTable"],
[data-testid="stTable"] * {
    color: #1A1A1A !important;
    -webkit-text-fill-color: #1A1A1A !important;
    opacity: 1 !important;
}

.ivory-card svg text,
[data-testid="stVerticalBlockBorderWrapper"] svg text {
    fill: #1A1A1A !important;
}

.ivory-card input,
.ivory-card textarea,
.ivory-card select,
[data-testid="stVerticalBlockBorderWrapper"] input,
[data-testid="stVerticalBlockBorderWrapper"] textarea,
[data-testid="stVerticalBlockBorderWrapper"] select {
    color: #1A1A1A !important;
    -webkit-text-fill-color: #1A1A1A !important;
}

.ivory-card .stat-icon,
.ivory-card .empty-state-icon,
.ivory-card.workflow-step span,
.ivory-card .workflow-step span {
    color: var(--accent) !important;
    -webkit-text-fill-color: var(--accent) !important;
}

/* Expander headers sit on ivory even when the body is dark. */
details[data-testid="stExpander"] summary,
details[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
.streamlit-expanderHeader,
.streamlit-expanderHeader * {
    color: #1A1A1A !important;
    -webkit-text-fill-color: #1A1A1A !important;
    opacity: 1 !important;
}
</style>
"""


# Final, version-stable polish layer. Keeping this separate makes the broad
# Streamlit compatibility rules above easier to reason about and preserves the
# original component contract used throughout the app.
PREMIUM_CSS = """
<style>
:root {
    --atelier-bg: #090d12;
    --atelier-panel: #111820;
    --atelier-panel-2: #171f28;
    --atelier-ivory: #f7f3ec;
    --atelier-ivory-2: #efe8dd;
    --atelier-ink: #181713;
    --atelier-copy: #5f5a52;
    --atelier-brass: #c9a86b;
    --atelier-brass-bright: #e1c58f;
    --atelier-line: rgba(201, 168, 107, 0.20);
    --atelier-line-strong: rgba(201, 168, 107, 0.42);
    --atelier-shadow: 0 22px 60px rgba(0, 0, 0, 0.28);
    --atelier-shadow-soft: 0 12px 34px rgba(0, 0, 0, 0.20);
    --atelier-ease: cubic-bezier(0.16, 1, 0.3, 1);
}

html {
    scroll-behavior: smooth;
}

html,
body,
.stApp {
    background: var(--atelier-bg) !important;
}

.stApp {
    background:
        radial-gradient(circle at 18% 6%, rgba(201, 168, 107, 0.075), transparent 31rem),
        radial-gradient(circle at 88% 88%, rgba(110, 127, 138, 0.075), transparent 34rem),
        linear-gradient(135deg, #090d12 0%, #0c1117 52%, #090d12 100%) !important;
}

.stApp::before {
    opacity: 0.38;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}

.block-container {
    width: min(100%, 1360px) !important;
    max-width: 1360px !important;
    padding: 1.6rem clamp(1rem, 2.5vw, 2.75rem) 6rem !important;
}

header[data-testid="stHeader"] {
    height: 3.25rem !important;
    background: rgba(9, 13, 18, 0.82) !important;
    border-bottom: 1px solid rgba(201, 168, 107, 0.08) !important;
    backdrop-filter: blur(18px);
}

[data-testid="stDeployButton"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    visibility: visible !important;
    pointer-events: auto !important;
}

[data-testid="stHeaderActionElements"],
.stApp a.anchor-link,
.stApp a[data-testid="stHeaderActionElements"] {
    display: none !important;
}

/* Sidebar and product identity */
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 15% 0%, rgba(201, 168, 107, 0.09), transparent 18rem),
        linear-gradient(180deg, #111820 0%, #0e151c 100%) !important;
    border-right: 1px solid var(--atelier-line) !important;
    box-shadow: 18px 0 50px rgba(0, 0, 0, 0.16) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.15rem 0.9rem 2rem !important;
}

.sidebar-brand-card {
    position: relative;
    overflow: hidden;
    margin: 0 0 1.1rem !important;
    padding: 1rem !important;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 20px !important;
    background: linear-gradient(145deg, rgba(247, 243, 236, 0.07), rgba(247, 243, 236, 0.025)) !important;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.20) !important;
}

.sidebar-brand-card::after {
    content: "";
    position: absolute;
    right: -2.5rem;
    bottom: -2.5rem;
    width: 7rem;
    height: 7rem;
    border: 1px solid rgba(201, 168, 107, 0.14);
    border-radius: 50%;
}

.sidebar-wordmark {
    display: flex;
    gap: 0.7rem;
    align-items: center;
}

.sidebar-mark {
    position: relative;
    display: inline-flex;
    width: 38px;
    min-width: 38px;
    height: 38px;
    border: 1px solid rgba(225, 197, 143, 0.45);
    border-radius: 12px;
    background: linear-gradient(145deg, rgba(201, 168, 107, 0.23), rgba(201, 168, 107, 0.06));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10);
}

.sidebar-mark::before,
.sidebar-mark::after,
.sidebar-mark span::before,
.sidebar-mark span::after {
    content: "";
    position: absolute;
    border-radius: 99px;
    background: var(--atelier-brass-bright);
}

.sidebar-mark::before,
.sidebar-mark::after {
    top: 8px;
    bottom: 8px;
    width: 3px;
}

.sidebar-mark::before { left: 12px; }
.sidebar-mark::after { right: 12px; }
.sidebar-mark span::before,
.sidebar-mark span::after {
    left: 8px;
    right: 8px;
    height: 3px;
}
.sidebar-mark span::before { top: 12px; }
.sidebar-mark span::after { bottom: 12px; }

.sidebar-product,
.sidebar-product-meta {
    margin: 0 !important;
}

.sidebar-product {
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
    font-family: var(--font-serif) !important;
    font-size: 1.15rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.01em;
}

.sidebar-product-meta {
    margin-top: 0.05rem !important;
    color: #a9a39a !important;
    -webkit-text-fill-color: #a9a39a !important;
    font-size: 0.68rem !important;
    font-weight: 650 !important;
    letter-spacing: 0.11em;
    text-transform: uppercase;
}

.sidebar-rule {
    height: 1px;
    margin: 0.9rem 0 0.85rem;
    background: linear-gradient(90deg, var(--atelier-line-strong), transparent);
}

.sidebar-brand-card h3 {
    position: relative;
    z-index: 1;
    margin: 0 !important;
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
    font-size: 1.34rem !important;
    line-height: 1.07 !important;
    letter-spacing: -0.02em !important;
}

.sidebar-brand-card .sidebar-brand-copy {
    position: relative;
    z-index: 1;
    margin: 0.65rem 0 0 !important;
    color: #b8b1a8 !important;
    -webkit-text-fill-color: #b8b1a8 !important;
    font-size: 0.78rem !important;
    line-height: 1.55 !important;
}

.sidebar-status {
    position: relative;
    z-index: 1;
    display: inline-flex;
    gap: 0.42rem;
    align-items: center;
    margin-top: 0.85rem;
    padding: 0.34rem 0.52rem;
    border: 1px solid rgba(201, 168, 107, 0.20);
    border-radius: 999px;
    color: var(--atelier-brass-bright) !important;
    -webkit-text-fill-color: var(--atelier-brass-bright) !important;
    background: rgba(201, 168, 107, 0.07);
    font-size: 0.65rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.sidebar-status > span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--atelier-brass-bright);
    box-shadow: 0 0 0 4px rgba(201, 168, 107, 0.10);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 0.25rem !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    position: relative;
    min-height: 46px !important;
    padding: 0.62rem 0.72rem !important;
    border-radius: 13px !important;
    transition: transform 180ms var(--atelier-ease), background 180ms ease, border-color 180ms ease !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label::before {
    width: 26px !important;
    min-width: 26px !important;
    height: 26px !important;
    margin-right: 0.58rem !important;
    border-color: rgba(201, 168, 107, 0.20) !important;
    border-radius: 9px !important;
    background: rgba(201, 168, 107, 0.035);
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    transform: translateX(2px) !important;
    background: rgba(247, 243, 236, 0.055) !important;
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"],
section[data-testid="stSidebar"] .stRadio label:has(input:checked),
section[data-testid="stSidebar"] .stRadio label:has([aria-checked="true"]) {
    background: linear-gradient(90deg, rgba(201, 168, 107, 0.17), rgba(201, 168, 107, 0.07)) !important;
    border-color: rgba(201, 168, 107, 0.28) !important;
    box-shadow: inset 3px 0 0 var(--atelier-brass), 0 9px 24px rgba(0, 0, 0, 0.14) !important;
}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"]::after,
section[data-testid="stSidebar"] .stRadio label:has(input:checked)::after,
section[data-testid="stSidebar"] .stRadio label:has([aria-checked="true"])::after {
    content: "";
    position: absolute;
    right: 0.8rem;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--atelier-brass-bright);
}

section[data-testid="stSidebar"] .stRadio label:has(input:checked) p,
section[data-testid="stSidebar"] .stRadio label:has([aria-checked="true"]) p {
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
}

[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"] {
    border: 1px solid var(--atelier-line) !important;
    border-radius: 12px !important;
    color: var(--atelier-brass-bright) !important;
    background: rgba(17, 24, 32, 0.94) !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.20) !important;
}

[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
    color: var(--atelier-brass-bright) !important;
    -webkit-text-fill-color: var(--atelier-brass-bright) !important;
}

/* Editorial hero */
.hero-shell.atelier-home-card {
    position: relative !important;
    isolation: isolate;
    display: grid !important;
    grid-template-columns: minmax(0, 1.18fr) minmax(300px, 0.82fr) !important;
    gap: clamp(2rem, 4vw, 4.5rem) !important;
    min-height: 430px !important;
    overflow: hidden !important;
    padding: clamp(2.2rem, 4.5vw, 4.5rem) !important;
    border-color: rgba(201, 168, 107, 0.30) !important;
    border-radius: 30px !important;
    background:
        radial-gradient(circle at 95% 5%, rgba(201, 168, 107, 0.16), transparent 18rem),
        linear-gradient(135deg, #fbf8f2 0%, #f4eee5 100%) !important;
    box-shadow: 0 34px 90px rgba(0, 0, 0, 0.32), inset 0 1px 0 #ffffff !important;
    text-align: left !important;
}

.hero-shell.atelier-home-card::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: 0;
    opacity: 0.18;
    background-image:
        linear-gradient(rgba(24, 23, 19, 0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(24, 23, 19, 0.06) 1px, transparent 1px);
    background-size: 26px 26px;
    mask-image: linear-gradient(90deg, transparent 25%, #000 100%);
}

.hero-copy {
    align-self: center;
}

.stApp .hero-kicker {
    display: inline-flex;
    gap: 0.5rem;
    align-items: center;
    margin: 0 0 1.1rem !important;
    color: #7f6a43 !important;
    -webkit-text-fill-color: #7f6a43 !important;
    font-size: 0.7rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.hero-kicker > span {
    display: inline-block;
    width: 1.7rem;
    height: 1px;
    background: var(--atelier-brass);
}

.hero-shell.atelier-home-card h1 {
    max-width: 12ch !important;
    margin: 0 !important;
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: clamp(3rem, 5.2vw, 5.25rem) !important;
    font-weight: 600 !important;
    line-height: 0.95 !important;
    letter-spacing: -0.045em !important;
}

.hero-shell .hero-text {
    max-width: 39rem !important;
    margin: 1.35rem 0 0 !important;
    color: var(--atelier-copy) !important;
    -webkit-text-fill-color: var(--atelier-copy) !important;
    font-size: 0.98rem !important;
    line-height: 1.7 !important;
}

.hero-shell .hero-tags {
    justify-content: flex-start !important;
    margin-top: 1.2rem;
}

.hero-shell .hero-tags span {
    padding: 0.43rem 0.68rem !important;
    border-color: rgba(127, 106, 67, 0.22) !important;
    color: #574a35 !important;
    -webkit-text-fill-color: #574a35 !important;
    background: rgba(255, 255, 255, 0.50) !important;
    box-shadow: 0 5px 14px rgba(60, 47, 27, 0.04);
}

.hero-proof-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.65rem;
    padding-top: 1.1rem;
    border-top: 1px solid rgba(24, 23, 19, 0.11);
}

.hero-proof-row > div {
    display: grid;
    gap: 0.15rem;
}

.stApp .hero-proof-row strong {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: 0.77rem;
    letter-spacing: 0.03em;
}

.stApp .hero-proof-row span {
    color: #79736a !important;
    -webkit-text-fill-color: #79736a !important;
    font-size: 0.66rem;
    line-height: 1.35;
}

.hero-visual {
    position: relative;
    min-height: 330px;
    align-self: center;
}

.hero-weave-window {
    position: absolute;
    inset: 0.25rem 1rem 2.4rem 0;
    overflow: hidden;
    border: 1px solid rgba(201, 168, 107, 0.34);
    border-radius: 28px;
    background:
        repeating-linear-gradient(28deg, rgba(255, 255, 255, 0.028) 0 2px, transparent 2px 7px),
        repeating-linear-gradient(118deg, rgba(201, 168, 107, 0.035) 0 1px, transparent 1px 8px),
        linear-gradient(145deg, #171f27, #0c1117);
    box-shadow: 0 24px 55px rgba(22, 18, 12, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.hero-weave-window::before,
.hero-weave-window::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(1px);
}

.hero-weave-window::before {
    top: -22%;
    right: -10%;
    width: 75%;
    aspect-ratio: 1;
    background: radial-gradient(circle, rgba(201, 168, 107, 0.32), transparent 67%);
}

.hero-weave-window::after {
    bottom: -28%;
    left: -18%;
    width: 76%;
    aspect-ratio: 1;
    border: 1px solid rgba(201, 168, 107, 0.12);
}

.hero-weave-window > p {
    position: absolute;
    right: 1.15rem;
    bottom: 0.9rem;
    margin: 0 !important;
    color: #d8cab1 !important;
    -webkit-text-fill-color: #d8cab1 !important;
    font-size: 0.62rem !important;
    font-weight: 750;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.weave-thread {
    position: absolute;
    display: block;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, transparent, rgba(225, 197, 143, 0.9), transparent);
    transform: rotate(-18deg);
}

.thread-one { top: 28%; left: -8%; width: 82%; }
.thread-two { top: 43%; left: 12%; width: 94%; opacity: 0.55; }
.thread-three { top: 58%; left: -4%; width: 70%; opacity: 0.32; }

.weave-focus-ring {
    position: absolute;
    top: 50%;
    left: 52%;
    display: grid;
    width: 106px;
    height: 106px;
    border: 1px solid rgba(225, 197, 143, 0.55);
    border-radius: 50%;
    place-items: center;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 11px rgba(201, 168, 107, 0.045), 0 0 0 24px rgba(201, 168, 107, 0.025);
}

.weave-focus-ring > span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--atelier-brass-bright);
    box-shadow: 0 0 22px rgba(225, 197, 143, 0.72);
}

.material-ticket {
    position: absolute;
    right: 0;
    bottom: 0;
    width: min(86%, 280px);
    padding: 0.85rem 0.95rem;
    border: 1px solid rgba(24, 23, 19, 0.12);
    border-radius: 18px;
    background: rgba(252, 249, 244, 0.93);
    box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(14px);
}

.ticket-head,
.ticket-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
}

.ticket-head {
    padding-bottom: 0.55rem;
    border-bottom: 1px solid rgba(24, 23, 19, 0.10);
}

.ticket-row {
    padding-top: 0.48rem;
}

.stApp .ticket-head span,
.stApp .ticket-row span {
    color: #7b756c !important;
    -webkit-text-fill-color: #7b756c !important;
    font-size: 0.61rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.stApp .ticket-head strong,
.stApp .ticket-row strong {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: 0.68rem;
}

.ticket-palette {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 3px;
    height: 9px;
    margin-top: 0.7rem;
    overflow: hidden;
    border-radius: 99px;
}

.ticket-palette i:nth-child(1) { background: #d9c9ae; }
.ticket-palette i:nth-child(2) { background: #9c7950; }
.ticket-palette i:nth-child(3) { background: #4a4037; }
.ticket-palette i:nth-child(4) { background: #c9a86b; }

/* Section hierarchy and cards */
.workflow-strip {
    position: relative;
    margin: 1rem 0 !important;
    padding: 1.3rem !important;
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 24px !important;
    background: linear-gradient(145deg, rgba(23, 31, 40, 0.96), rgba(13, 19, 25, 0.96)) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

.workflow-strip::after {
    content: "";
    position: absolute;
    top: -5rem;
    right: -3rem;
    width: 15rem;
    height: 15rem;
    border: 1px solid rgba(201, 168, 107, 0.09);
    border-radius: 50%;
}

.workflow-strip-head {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    align-items: end;
    margin-bottom: 1rem;
}

.workflow-strip-head h3 {
    max-width: 30rem;
    margin: 0 !important;
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
    font-size: 1.28rem !important;
}

.workflow-strip-head p {
    max-width: 25rem;
    margin: 0 !important;
    color: #aaa39a !important;
    -webkit-text-fill-color: #aaa39a !important;
    font-size: 0.78rem !important;
    line-height: 1.5 !important;
    text-align: right;
}

.workflow-step-grid {
    position: relative;
    z-index: 1;
    gap: 0.7rem !important;
}

.workflow-step.ivory-card {
    min-height: 132px !important;
    padding: 0.95rem !important;
    border-color: rgba(24, 23, 19, 0.09) !important;
    border-radius: 17px !important;
    background: linear-gradient(145deg, #fbf8f3, #f0e9de) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.14) !important;
}

.workflow-step.ivory-card > span {
    display: inline-grid !important;
    width: 28px !important;
    height: 28px !important;
    margin-bottom: 0.7rem !important;
    border: 1px solid rgba(201, 168, 107, 0.45);
    border-radius: 9px !important;
    color: var(--atelier-brass-bright) !important;
    -webkit-text-fill-color: var(--atelier-brass-bright) !important;
    background: var(--atelier-panel) !important;
    place-items: center;
    font-size: 0.72rem !important;
}

.workflow-step.ivory-card strong {
    display: block;
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: 0.88rem;
}

.workflow-step.ivory-card p {
    margin: 0.28rem 0 0 !important;
    color: var(--atelier-copy) !important;
    -webkit-text-fill-color: var(--atelier-copy) !important;
    font-size: 0.75rem !important;
    line-height: 1.46 !important;
}

.feature-strip {
    margin: 0 0 1.2rem !important;
}

.feature-card-grid {
    gap: 0.8rem !important;
}

.info-card.ivory-card {
    position: relative;
    min-height: 154px !important;
    overflow: hidden;
    padding: 1.2rem !important;
    border-color: rgba(201, 168, 107, 0.22) !important;
    border-radius: 22px !important;
    background: linear-gradient(145deg, #f8f4ed, #eee6da) !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.20) !important;
}

.info-card.ivory-card::after {
    content: "";
    position: absolute;
    right: -2rem;
    bottom: -2.4rem;
    width: 6rem;
    height: 6rem;
    border: 1px solid rgba(201, 168, 107, 0.15);
    border-radius: 50%;
}

.feature-index {
    display: block;
    margin-bottom: 1.1rem;
    color: #9d8152 !important;
    -webkit-text-fill-color: #9d8152 !important;
    font-size: 0.65rem;
    font-weight: 850;
    letter-spacing: 0.14em;
}

.info-card.ivory-card h3 {
    margin: 0 !important;
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: 1.12rem !important;
}

.info-card.ivory-card p {
    margin: auto 0 0 !important;
    color: var(--atelier-copy) !important;
    -webkit-text-fill-color: var(--atelier-copy) !important;
    font-size: 0.77rem !important;
    line-height: 1.55 !important;
}

.page-intro.ivory-card {
    position: relative;
    display: grid !important;
    grid-template-columns: 6px minmax(0, 1fr) !important;
    gap: 1.25rem !important;
    align-items: center;
    margin-bottom: 1.25rem !important;
    padding: clamp(1.35rem, 2.6vw, 2.1rem) !important;
    overflow: hidden;
    border-color: rgba(201, 168, 107, 0.26) !important;
    border-radius: 24px !important;
    background: linear-gradient(135deg, #faf7f1, #f0e8dc) !important;
    box-shadow: var(--atelier-shadow) !important;
}

.page-intro-rule {
    width: 6px;
    height: 100%;
    min-height: 68px;
    border-radius: 99px;
    background: linear-gradient(180deg, var(--atelier-brass-bright), #8d7041);
}

.page-intro.ivory-card h2 {
    max-width: 24ch;
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: clamp(2rem, 3.4vw, 3.45rem) !important;
    line-height: 1.02 !important;
    letter-spacing: -0.03em !important;
}

.page-intro.ivory-card .page-intro-text {
    max-width: 58rem !important;
    margin-top: 0.62rem !important;
    color: var(--atelier-copy) !important;
    -webkit-text-fill-color: var(--atelier-copy) !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
}

.fs-card,
.stat-card,
.metric-card,
.result-card,
.color-card,
.compare-summary-card,
.compare-card,
.empty-state-card,
.confusion-card,
.color-wheel-card,
.bento-cell,
.scenario-card {
    border-radius: 20px !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

.metric-card:hover,
.result-card:hover,
.compare-card:hover,
.color-card:hover,
.fs-card:hover,
.bento-cell:hover,
.info-card:hover,
.scenario-card:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(201, 168, 107, 0.38) !important;
    box-shadow: 0 24px 58px rgba(0, 0, 0, 0.28) !important;
}

.metric-card.fs-metric-card {
    min-height: 116px !important;
    padding: 1.05rem !important;
    border-top: 3px solid rgba(201, 168, 107, 0.70) !important;
    background: linear-gradient(145deg, #faf7f1, #eee7dc) !important;
}

.stApp .metric-card .metric-label,
.stApp .metric-card .fs-metric-sub {
    color: #7b756c !important;
    -webkit-text-fill-color: #7b756c !important;
}

.stApp .metric-card .fs-metric-value {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-family: var(--font-serif) !important;
    font-size: clamp(1.55rem, 2.4vw, 2.1rem) !important;
}

.result-card,
.compare-card,
.color-card,
.fs-card,
.empty-state-card,
.scenario-card {
    border-color: rgba(201, 168, 107, 0.22) !important;
    background: linear-gradient(145deg, #faf7f1, #eee7dc) !important;
}

.highlight-banner {
    position: relative;
    padding: 1.05rem 1.15rem 1.05rem 1.35rem !important;
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 20px !important;
    color: var(--atelier-ivory) !important;
    background: linear-gradient(135deg, rgba(24, 33, 43, 0.98), rgba(15, 21, 28, 0.98)) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

.highlight-banner::before {
    content: "";
    position: absolute;
    top: 0.8rem;
    bottom: 0.8rem;
    left: 0;
    width: 3px;
    border-radius: 99px;
    background: var(--atelier-brass);
}

.stApp .highlight-banner strong {
    color: var(--atelier-brass-bright) !important;
    -webkit-text-fill-color: var(--atelier-brass-bright) !important;
}

.stApp .highlight-banner p {
    margin: 0.35rem 0 0 !important;
    color: #d0c9bf !important;
    -webkit-text-fill-color: #d0c9bf !important;
    font-size: 0.86rem !important;
    line-height: 1.58 !important;
}

.scenario-grid {
    gap: 0.85rem !important;
}

.scenario-card.ivory-card {
    padding: 1.25rem !important;
    border-top: 3px solid rgba(201, 168, 107, 0.64) !important;
}

.about-proof-card {
    position: relative;
    min-height: 418px;
    height: 100%;
    overflow: hidden;
    padding: 1.45rem;
    border: 1px solid var(--atelier-line);
    border-radius: 22px;
    background:
        repeating-linear-gradient(28deg, rgba(255, 255, 255, 0.018) 0 2px, transparent 2px 8px),
        linear-gradient(145deg, #18212a, #0f151c);
    box-shadow: var(--atelier-shadow-soft);
}

.about-proof-card::after {
    content: "";
    position: absolute;
    right: -5rem;
    bottom: -5rem;
    width: 15rem;
    height: 15rem;
    border: 1px solid rgba(201, 168, 107, 0.12);
    border-radius: 50%;
    box-shadow: 0 0 0 2.8rem rgba(201, 168, 107, 0.025);
}

.about-proof-head {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--atelier-line);
}

.stApp .about-proof-head span,
.stApp .about-proof-head strong {
    color: var(--atelier-brass-bright) !important;
    -webkit-text-fill-color: var(--atelier-brass-bright) !important;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}

.about-proof-mark {
    position: relative;
    z-index: 1;
    display: grid;
    width: 64px;
    height: 64px;
    margin: 1.35rem 0 1.15rem;
    border: 1px solid rgba(225, 197, 143, 0.45);
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(201, 168, 107, 0.22), rgba(201, 168, 107, 0.05));
    place-items: center;
}

.about-proof-mark::before,
.about-proof-mark::after,
.about-proof-mark span::before,
.about-proof-mark span::after {
    content: "";
    position: absolute;
    border-radius: 99px;
    background: var(--atelier-brass-bright);
}

.about-proof-mark::before,
.about-proof-mark::after {
    top: 14px;
    bottom: 14px;
    width: 4px;
}

.about-proof-mark::before { left: 21px; }
.about-proof-mark::after { right: 21px; }
.about-proof-mark span::before,
.about-proof-mark span::after {
    left: 14px;
    right: 14px;
    height: 4px;
}
.about-proof-mark span::before { top: 21px; }
.about-proof-mark span::after { bottom: 21px; }

.about-proof-card h3 {
    position: relative;
    z-index: 1;
    max-width: 17ch;
    margin: 0 !important;
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
    font-size: clamp(1.55rem, 2.6vw, 2.2rem) !important;
    line-height: 1.04 !important;
}

.about-proof-card > p {
    position: relative;
    z-index: 1;
    max-width: 32rem;
    margin: 0.75rem 0 1.1rem !important;
    color: #bdb6ac !important;
    -webkit-text-fill-color: #bdb6ac !important;
    font-size: 0.8rem !important;
    line-height: 1.58 !important;
}

.about-proof-list {
    position: relative;
    z-index: 1;
    display: grid;
    gap: 0.45rem;
}

.about-proof-list > div {
    display: grid;
    grid-template-columns: 2rem minmax(0, 1fr);
    gap: 0.55rem;
    align-items: center;
    padding-top: 0.45rem;
    border-top: 1px solid rgba(201, 168, 107, 0.12);
}

.stApp .about-proof-list span {
    color: #8f7953 !important;
    -webkit-text-fill-color: #8f7953 !important;
    font-size: 0.62rem;
    font-weight: 800;
}

.stApp .about-proof-list strong {
    color: #e7e0d6 !important;
    -webkit-text-fill-color: #e7e0d6 !important;
    font-size: 0.73rem;
}

/* Streamlit surfaces and controls */
[data-testid="stVerticalBlockBorderWrapper"] {
    padding: clamp(1rem, 2vw, 1.4rem) !important;
    border: 1px solid rgba(201, 168, 107, 0.24) !important;
    border-radius: 22px !important;
    background: linear-gradient(145deg, #f9f5ef, #eee7dc) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] > div {
    gap: 0.8rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] label,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p {
    color: var(--atelier-copy) !important;
    -webkit-text-fill-color: var(--atelier-copy) !important;
}

.input-section-head {
    margin-bottom: 0.25rem;
}

.input-section-head h3 {
    margin: 0 !important;
    font-size: clamp(1.35rem, 2.3vw, 1.85rem) !important;
}

.input-section-head p {
    margin: 0.35rem 0 0 !important;
    font-size: 0.8rem !important;
    line-height: 1.5 !important;
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 132px;
    padding: 1rem !important;
    border: 1px dashed rgba(141, 112, 65, 0.48) !important;
    border-radius: 17px !important;
    background:
        linear-gradient(rgba(201, 168, 107, 0.035), rgba(201, 168, 107, 0.035)),
        #fcfaf6 !important;
    transition: border-color 180ms ease, background 180ms ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #9d7c49 !important;
    background: #fffdf9 !important;
}

[data-testid="stFileUploaderDropzone"] svg {
    color: #8b7045 !important;
    fill: #8b7045 !important;
}

[data-testid="stImage"] img {
    border: 1px solid rgba(201, 168, 107, 0.18);
    border-radius: 18px !important;
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.16);
}

.sample-card-title {
    margin: 0.45rem 0 0.25rem !important;
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    font-size: 0.78rem !important;
    font-weight: 750 !important;
    text-align: center;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] {
    display: inline-flex !important;
    gap: 0.25rem !important;
    max-width: 100%;
    padding: 0.28rem !important;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 14px !important;
    background: rgba(247, 243, 236, 0.045) !important;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label {
    min-height: 38px !important;
    margin: 0 !important;
    padding: 0.48rem 0.78rem !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    transition: background 180ms ease, border-color 180ms ease, transform 180ms ease !important;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label > div:first-child {
    display: none !important;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label p {
    color: #c9c2b8 !important;
    -webkit-text-fill-color: #c9c2b8 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label[aria-checked="true"],
[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked),
[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has([aria-checked="true"]) {
    border-color: rgba(201, 168, 107, 0.22) !important;
    background: var(--atelier-ivory) !important;
    box-shadow: 0 7px 18px rgba(0, 0, 0, 0.18) !important;
}

[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label[aria-checked="true"] p,
[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p,
[data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label:has([aria-checked="true"]) p {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid^="stBaseButton-"] {
    min-height: 44px !important;
    border-radius: 13px !important;
    font-size: 0.82rem !important;
    font-weight: 750 !important;
    letter-spacing: 0.01em;
    transition: transform 180ms var(--atelier-ease), box-shadow 180ms ease, border-color 180ms ease, background 180ms ease !important;
}

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    border: 1px solid #d8ba80 !important;
    color: #11161c !important;
    -webkit-text-fill-color: #11161c !important;
    background: linear-gradient(135deg, #e2c991 0%, #b99255 100%) !important;
    box-shadow: 0 14px 28px rgba(126, 91, 39, 0.28) !important;
}

.stButton > button[kind="secondary"],
[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    border: 1px solid rgba(201, 168, 107, 0.28) !important;
    color: #efe9df !important;
    -webkit-text-fill-color: #efe9df !important;
    background: linear-gradient(145deg, #19212a, #111820) !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16) !important;
}

.stButton > button[kind="primary"] *,
[data-testid="stBaseButton-primary"] *,
.stButton > button[kind="secondary"] *,
[data-testid="stBaseButton-secondary"] *,
.stDownloadButton > button * {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid^="stBaseButton-"]:hover {
    transform: translateY(-1px) !important;
    border-color: rgba(225, 197, 143, 0.68) !important;
    filter: none !important;
}

.stButton > button:active,
.stDownloadButton > button:active,
[data-testid^="stBaseButton-"]:active {
    transform: translateY(0) scale(0.985) !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible,
input:focus-visible,
textarea:focus-visible,
[data-baseweb="select"] > div:focus-within {
    outline: 3px solid rgba(225, 197, 143, 0.30) !important;
    outline-offset: 2px !important;
}

.stButton > button:disabled,
.stDownloadButton > button:disabled {
    opacity: 0.46 !important;
    transform: none !important;
    box-shadow: none !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-baseweb="select"] > div {
    min-height: 44px;
    border-color: rgba(201, 168, 107, 0.24) !important;
    border-radius: 12px !important;
    color: var(--atelier-ivory) !important;
    -webkit-text-fill-color: var(--atelier-ivory) !important;
    background: #151d25 !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] .stTextInput input,
[data-testid="stVerticalBlockBorderWrapper"] .stTextArea textarea,
[data-testid="stVerticalBlockBorderWrapper"] .stNumberInput input,
[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] > div {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
    background: #fffdf9 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-baseweb="select"] *,
[data-testid="stVerticalBlockBorderWrapper"] input::placeholder,
[data-testid="stVerticalBlockBorderWrapper"] textarea::placeholder {
    color: #716b62 !important;
    -webkit-text-fill-color: #716b62 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem !important;
    padding: 0.35rem !important;
    overflow-x: auto;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 15px !important;
    background: rgba(247, 243, 236, 0.04) !important;
}

.stTabs [data-baseweb="tab"] {
    min-height: 42px !important;
    padding: 0.45rem 0.85rem !important;
    border: 0 !important;
    border-radius: 11px !important;
    color: #bbb4aa !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}

.stTabs [aria-selected="true"] {
    color: var(--atelier-ink) !important;
    background: var(--atelier-ivory) !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

details[data-testid="stExpander"],
[data-testid="stExpander"] {
    border-color: var(--atelier-line) !important;
    border-radius: 18px !important;
    background: rgba(17, 24, 32, 0.80) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

details[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary,
.streamlit-expanderHeader {
    min-height: 52px !important;
    padding-inline: 1rem !important;
    border: 0 !important;
    border-radius: 17px !important;
    background: linear-gradient(145deg, #faf7f1, #eee7dc) !important;
}

details[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary *,
.streamlit-expanderHeader * {
    color: #1A1A1A !important;
    -webkit-text-fill-color: #1A1A1A !important;
    opacity: 1 !important;
}

[data-testid="stExpanderDetails"] {
    padding: 0.9rem 1rem 1rem !important;
    border-top: 1px solid var(--atelier-line) !important;
    background: rgba(17, 24, 32, 0.94) !important;
}

[data-testid="stExpanderDetails"] p,
[data-testid="stExpanderDetails"] li,
[data-testid="stExpanderDetails"] span {
    color: #d6cfc5 !important;
    -webkit-text-fill-color: #d6cfc5 !important;
}

[data-testid="stAlert"] {
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 16px !important;
    background: rgba(17, 24, 32, 0.94) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: #e5ded4 !important;
    -webkit-text-fill-color: #e5ded4 !important;
}

[data-testid="stMetric"],
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    overflow: hidden;
    border-color: rgba(201, 168, 107, 0.24) !important;
    border-radius: 18px !important;
    background: #f8f4ed !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
}

.color-card {
    display: grid !important;
    grid-template-columns: 62px minmax(0, 1fr) !important;
    gap: 0.85rem !important;
    align-items: center !important;
}

.color-card .swatch {
    width: 62px !important;
    height: 62px !important;
    border: 4px solid rgba(255, 255, 255, 0.82) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15) !important;
}

.fs-gradient-bar,
.fs-palette-bar {
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 999px !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15) !important;
}

.result-card .kv-row {
    padding: 0.82rem 0 !important;
}

.result-card .kv-label {
    color: #827b71 !important;
    -webkit-text-fill-color: #827b71 !important;
}

.result-card .kv-value {
    color: var(--atelier-ink) !important;
    -webkit-text-fill-color: var(--atelier-ink) !important;
}

.empty-state-card {
    padding: clamp(1.7rem, 4vw, 3rem) !important;
    text-align: center !important;
}

.empty-state-icon {
    display: inline-grid !important;
    width: 58px !important;
    height: 58px !important;
    margin-bottom: 0.7rem;
    border: 1px solid rgba(201, 168, 107, 0.34);
    border-radius: 18px;
    color: #8d7041 !important;
    -webkit-text-fill-color: #8d7041 !important;
    background: rgba(201, 168, 107, 0.10);
    place-items: center;
}

.chat-fabric-bubble,
[data-testid="stChatMessage"] {
    border: 1px solid var(--atelier-line) !important;
    border-radius: 20px !important;
    background: linear-gradient(145deg, #171f28, #111820) !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

.ag-theme-balham {
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 18px !important;
}

.ag-header {
    background: #171f28 !important;
}

.image-comparison-container {
    overflow: hidden;
    border: 1px solid var(--atelier-line) !important;
    border-radius: 20px !important;
    box-shadow: var(--atelier-shadow-soft) !important;
}

/* Global type rhythm on the dark canvas */
[data-testid="stMain"] > div > div > div > [data-testid="stVerticalBlock"] > div > div > [data-testid="stMarkdownContainer"] > h2,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] > h2 {
    margin-top: 1.4rem;
}

.stApp [data-testid="stCaptionContainer"] p {
    color: #9f988f !important;
    -webkit-text-fill-color: #9f988f !important;
    font-size: 0.74rem !important;
}

.stApp hr {
    margin-block: 1.8rem !important;
    border-color: rgba(201, 168, 107, 0.15) !important;
}

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0b1016;
}

::-webkit-scrollbar-thumb {
    border: 3px solid #0b1016;
    border-radius: 999px;
    background: #4b4338;
}

::-webkit-scrollbar-thumb:hover {
    background: #6f5c3f;
}

@media (max-width: 1100px) {
    .hero-shell.atelier-home-card {
        grid-template-columns: minmax(0, 1fr) minmax(270px, 0.72fr) !important;
        gap: 2rem !important;
    }

    .hero-proof-row {
        grid-template-columns: 1fr !important;
        gap: 0.45rem;
    }

    .hero-proof-row > div {
        grid-template-columns: 5rem 1fr;
        align-items: baseline;
    }
}

@media (max-width: 980px) {
    .hero-shell.atelier-home-card {
        grid-template-columns: 1fr !important;
        min-height: 340px !important;
    }

    .hero-visual {
        min-height: 285px;
    }

    .feature-card-grid,
    .workflow-step-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }

    .workflow-strip-head {
        display: block;
    }

    .workflow-strip-head p {
        margin-top: 0.4rem !important;
        text-align: left;
    }
}

@media (max-width: 720px) {
    .block-container {
        padding: 1rem 0.8rem 4rem !important;
    }

    .hero-shell.atelier-home-card {
        gap: 1.5rem !important;
        padding: 1.5rem !important;
        border-radius: 22px !important;
    }

    .hero-shell.atelier-home-card h1 {
        font-size: clamp(2.55rem, 13vw, 4rem) !important;
    }

    .hero-proof-row {
        grid-template-columns: 1fr !important;
    }

    .hero-visual {
        min-height: 250px;
    }

    .hero-weave-window {
        inset: 0 0.5rem 2rem 0;
    }

    .material-ticket {
        width: 82%;
    }

    .feature-card-grid,
    .workflow-step-grid,
    .scenario-grid,
    .bento-grid.cols-4,
    .bento-grid.cols-3,
    .fs-passport-grid,
    .compare-card-grid,
    .compare-summary-flow {
        grid-template-columns: 1fr !important;
    }

    .info-card.ivory-card {
        min-height: 138px !important;
    }

    .about-proof-card {
        min-height: 360px;
        padding: 1.2rem;
        border-radius: 19px;
    }

    .page-intro.ivory-card {
        grid-template-columns: 4px minmax(0, 1fr) !important;
        gap: 0.9rem !important;
        padding: 1.2rem !important;
        border-radius: 19px !important;
    }

    .page-intro-rule {
        width: 4px;
    }

    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        width: 100%;
        flex-direction: column !important;
    }

    [data-testid="stMain"] [data-testid="stRadio"] [role="radiogroup"] > label {
        width: 100%;
    }

    .confidence-bar-container {
        grid-template-columns: 1fr 3.6rem !important;
    }

    .confidence-bar-container > span:first-child {
        grid-column: 1 / -1;
    }

    .stTabs [data-baseweb="tab"] {
        padding-inline: 0.65rem !important;
    }
}

@media (max-width: 480px) {
    .hero-visual {
        min-height: 220px;
    }

    .hero-weave-window {
        right: 0;
    }

    .material-ticket {
        right: 0.35rem;
        width: 90%;
    }

    .hero-proof-row > div {
        grid-template-columns: 4.5rem 1fr;
    }

    .workflow-strip {
        padding: 0.85rem !important;
        border-radius: 19px !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    html {
        scroll-behavior: auto;
    }

    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
"""

APP_CSS += PREMIUM_CSS


def hex_to_hsl(hex_str: str) -> tuple[float, float, float]:
    """Convert #RRGGBB to (H, S, L) with H in [0, 360], S, L in [0, 100]."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    try:
        r = int(hex_str[0:2], 16) / 255.0
        r_linear = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
        g = int(hex_str[2:4], 16) / 255.0
        g_linear = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
        b = int(hex_str[4:6], 16) / 255.0
        b_linear = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
    except ValueError:
        r, g, b = 0.5, 0.5, 0.5

    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360.0, s * 100.0, l * 100.0


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert (H, S, L) to #RRGGBB."""
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return f"#{int(round(r * 255)):02x}{int(round(g * 255)):02x}{int(round(b * 255)):02x}"


def hex_to_rgba_str(hex_str: str, alpha: float) -> str:
    """Convert a HEX string to a transparent rgba() CSS string."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    except ValueError:
        r, g, b = 201, 168, 107
    return f"rgba({r}, {g}, {b}, {alpha})"


def get_dynamic_theme_css(hex_color: str) -> str:
    """Expose the detected fabric color without overriding core theme tokens."""
    accent_soft = hex_to_rgba_str(hex_color, 0.18)
    return f"""
<style>
:root {{
    --fabric-accent: {hex_color};
    --fabric-accent-soft: {accent_soft};
}}
</style>
"""
