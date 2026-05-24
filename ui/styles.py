"""Custom CSS for the FabriSense Atelier Noir redesign."""

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
    background: var(--bg-top) !important;
    color: #E8E3DB;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: var(--bg-top) !important;
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
.stApp span,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p {
    font-family: var(--font-sans) !important;
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
    transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
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

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover,
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
    background: rgba(var(--brass-rgb), 0.10) !important;
    border-color: var(--line) !important;
    color: var(--surface) !important;
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
    padding: clamp(2rem, 4.5vw, 4rem) clamp(1.8rem, 4vw, 4.5rem) !important;
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
    min-height: 116px !important;
}

.info-card h3,
.workflow-strip h3 {
    font-size: 1.05rem !important;
    line-height: 1.25 !important;
}

.info-card p,
.workflow-step p,
.scenario-card p,
.stat-card p {
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
.scenario-card,
.floating-action-bar {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: rgba(var(--surface-rgb), 0.04) !important;
    padding: 1rem !important;
}

.workflow-strip {
    background: #121820 !important;
}

.workflow-strip h3 {
    color: var(--surface-0) !important;
}

.workflow-step-grid,
.scenario-grid,
.bento-grid {
    display: grid !important;
    gap: 1rem !important;
}

.workflow-step-grid,
.scenario-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}

.workflow-step-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
}

.workflow-step {
    padding: 0.9rem !important;
    min-height: 112px !important;
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
.color-card:hover {
    border-color: var(--line-strong) !important;
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
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(1.05) !important;
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
</style>
"""


DARK_MODE_CSS = """
<style>
:root {
    --bg: #0B0F14;
    --bg-elev: #121820;
    --surface: #FAF7F2;
    --brass: #C9A86B;
    --text-1: #E8E3D8;
    --text-2: #B8B2A9;
}
section[data-testid="stSidebar"] { background: var(--bg-elev) !important; }
.stat-card,
.info-card { background: var(--surface) !important; }
.stTextArea textarea { background: rgba(var(--surface-rgb), 0.06) !important; }
.stTabs [aria-selected="true"] { color: var(--brass) !important; }
</style>
"""


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


def get_dynamic_theme_css(hex_color: str, is_dark_mode: bool = False) -> str:
    """Expose the detected fabric color without overriding Atelier Noir tokens."""
    accent_soft = hex_to_rgba_str(hex_color, 0.18)
    return f"""
<style>
:root {{
    --fabric-accent: {hex_color};
    --fabric-accent-soft: {accent_soft};
}}
</style>
"""
