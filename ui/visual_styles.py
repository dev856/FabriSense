"""Styles for the shared icon vocabulary and illustrated material references."""

VISUAL_CSS = """
<style>
[data-testid="stMainBlockContainer"] { padding-top: 4.8rem !important; }
.fs-icon { display: inline-block; flex: 0 0 auto; vertical-align: middle; }
.stApp .fs-icon * { color: inherit !important; }
.icon-badge {
    display: inline-flex !important; align-items: center; justify-content: center;
    flex: 0 0 auto; width: 42px; height: 42px; border-radius: 13px;
    border: 1px solid rgba(126, 97, 48, .14); background: #eadcc3;
}
.stApp .icon-badge, .stApp .icon-badge svg { color: #795b29 !important; }
.stApp .icon-badge.tone-sage { background: #dce8df; border-color: #b9cdc0; }
.stApp .icon-badge.tone-sage svg { color: #3d6655 !important; }
.stApp .icon-badge.tone-blue { background: #dde7ef; border-color: #becfdd; }
.stApp .icon-badge.tone-blue svg { color: #476880 !important; }
.stApp .icon-badge.tone-rose { background: #efdfd8; border-color: #d9bbb0; }
.stApp .icon-badge.tone-rose svg { color: #8b5c4c !important; }

/* Inline Markdown icons and SVG headings have different Streamlit wrappers. */
.stTabs [role="tablist"] {
    gap: .5rem !important;
    padding: .4rem 1rem !important;
    max-width: 100%;
    scroll-padding-inline: 1.5rem;
    scrollbar-width: thin;
    scrollbar-color: #8d7752 transparent;
}
.stTabs [role="tab"] {
    flex: 0 0 auto;
    height: auto !important;
    min-height: 46px !important;
    padding: .65rem 1rem !important;
    white-space: nowrap;
    color: #d2c9bc !important;
    -webkit-text-fill-color: #d2c9bc !important;
}
.stTabs [role="tab"] [data-testid="stMarkdownContainer"] p {
    display: flex;
    align-items: center;
    column-gap: .625rem;
    margin: 0 !important;
    line-height: 1.5 !important;
    font-size: .85rem !important;
}
.stTabs [role="tab"] [data-testid="stMarkdownContainer"],
.stTabs [role="tab"] p,
.stTabs [role="tab"] p > span {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}
.stTabs [role="tab"] span[role="img"],
.stTabs [role="tab"] [data-testid="stIconMaterial"] {
    display: inline-flex !important;
    flex: 0 0 20px;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    font-size: 20px !important;
    line-height: 1 !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    color: #242017 !important;
    -webkit-text-fill-color: #242017 !important;
    background: #f7f3ec !important;
}
.stTabs [role="tab"]:hover:not([aria-selected="true"]) {
    color: #f7f3ec !important;
    -webkit-text-fill-color: #f7f3ec !important;
    background: rgba(201, 168, 107, .12) !important;
}
.stTabs [role="tab"]:focus-visible {
    outline: 2px solid #e1c58f !important;
    outline-offset: -3px;
}
.stTabs [role="tabpanel"] { padding-top: 1.25rem !important; }
.stTabs, .metric-band, .page-intro { scroll-margin-top: 5rem; }
.heading-content {
    display: inline-flex;
    align-items: center;
    column-gap: .7rem;
    max-width: 100%;
    min-width: 0;
    vertical-align: middle;
}
.heading-text { min-width: 0; overflow-wrap: anywhere; line-height: 1.35; }
.stButton > button, .stDownloadButton > button { column-gap: .6rem; }
.stButton button [data-has-shortcut], .stDownloadButton button [data-has-shortcut] {
    column-gap: .6rem !important;
    align-items: center;
}
.stButton [data-testid="stIconMaterial"], .stDownloadButton [data-testid="stIconMaterial"] {
    flex-shrink: 0;
}

/* Result values stay readable as text grows or the viewport gets narrower. */
.metric-band { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
/* Streamlit trims a paragraph margin even when this block contains only cards. */
[data-testid="stMarkdownContainer"]:has(> .metric-band) { margin-bottom: 0 !important; }
.metric-band .fs-metric-card { height: 100%; min-height: 140px !important; box-sizing: border-box; }
.metric-band .fs-metric-value { line-height: 1.3 !important; }
.fs-metric-value, .fs-passport-value, .kv-value, .result-card li { overflow-wrap: anywhere; }
.stApp .sample-card-title {
    color: #e8dfd1 !important;
    -webkit-text-fill-color: #e8dfd1 !important;
    margin: .55rem 0 .4rem !important;
}
.stApp [data-testid="stFileUploaderDropzoneInstructions"] span,
.stApp [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #62594c !important;
    -webkit-text-fill-color: #62594c !important;
}
.confidence-bar-container {
    display: grid;
    grid-template-columns: minmax(6rem, 1fr) minmax(4rem, 2fr) 3.5rem;
    gap: .65rem;
    align-items: center;
    margin-bottom: .85rem;
}
.stApp .confidence-name, .stApp .confidence-bar-label {
    color: #d8cfc1 !important;
    -webkit-text-fill-color: #d8cfc1 !important;
    font-size: .82rem;
    font-weight: 600;
    overflow-wrap: anywhere;
}
.confidence-bar-label { text-align: right; }
.ivory-card .confidence-name, .ivory-card .confidence-bar-label {
    color: #494238 !important;
    -webkit-text-fill-color: #494238 !important;
}

/* Native radios retain their keyboard behavior and accessible page names. */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top: .5rem; }
.sidebar-brand-card {
    padding: .7rem .45rem 1.2rem !important; border: 0 !important;
    border-bottom: 1px solid var(--atelier-line) !important; border-radius: 0 !important;
    background: transparent !important; box-shadow: none !important;
}
.sidebar-brand-card::after { display: none; }
.sidebar-logo {
    display: grid; place-items: center; width: 48px; height: 48px; flex-shrink: 0;
    border: 1px solid #9c8153; border-radius: 15px; background: #292a25;
}
.sidebar-logo svg { color: #e1c58f; }
.stApp .nav-section-label {
    margin: 0 .5rem .15rem; color: #a69e92 !important; -webkit-text-fill-color: #a69e92 !important;
    font-size: .65rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: .42rem !important; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    display: flex !important; align-items: center; box-sizing: border-box;
    min-height: 49px !important; padding: .7rem .85rem !important;
}
/* BaseWeb puts the radio indicator first; React Aria wraps indicator + text. */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child:not(:has([data-testid="stMarkdownContainer"])) {
    display: block !important; position: absolute !important;
    width: 1px !important; height: 1px !important; overflow: hidden;
    clip-path: inset(50%); white-space: nowrap;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:has([data-testid="stMarkdownContainer"]) {
    display: flex !important; align-items: center; min-width: 0;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div > div:not([data-testid="stMarkdownContainer"]):not(:has(input)) {
    display: none !important;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label::before {
    content: "" !important; display: inline-block; flex: 0 0 22px;
    width: 22px !important; min-width: 22px !important; height: 22px !important;
    margin-right: .85rem !important; border: 0 !important; border-radius: 0 !important;
    background: #b6ad9e !important;
    -webkit-mask-size: contain; mask-size: contain;
    -webkit-mask-position: center; mask-position: center;
    -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
}
section[data-testid="stSidebar"] .stRadio label:has(input:checked)::before {
    background: #e5c487 !important;
}
section[data-testid="stSidebar"] .stRadio label:has(input:focus-visible) {
    outline: 2px solid #e1c58f !important; outline-offset: 3px;
}
.sidebar-note {
    display: flex; gap: .7rem; margin-top: 1.8rem; padding: 1rem .7rem;
    border: 1px solid var(--atelier-line); border-radius: 16px; background: rgba(201,168,107,.045);
}
.sidebar-note .icon-badge { width: 32px; height: 32px; border-radius: 10px; }
.sidebar-note .fs-icon { width: 18px; height: 18px; }
.stApp .sidebar-note strong { display: block; color: #e1d7c7 !important; font-size: .73rem; line-height: 1.55; }
.stApp .sidebar-note p { margin: .35rem 0 0; color: #afa99e !important; font-size: .7rem; line-height: 1.65; }
.sidebar-status { margin: 1rem .2rem 0 !important; font-size: .62rem !important; }

/* Real textile imagery stays bundled with the app. */
.hero-shell.atelier-home-card {
    min-height: 365px !important; padding: clamp(1.7rem, 3vw, 3rem) !important;
    grid-template-columns: minmax(0, 1.1fr) minmax(260px, .9fr) !important;
    gap: 2rem !important;
}
.hero-shell.atelier-home-card h1 { max-width: 14ch !important; font-size: clamp(2.8rem, 4.5vw, 4.6rem) !important; line-height: 1.04 !important; }
.hero-shell .hero-text { font-size: .92rem !important; max-width: 31rem !important; margin-top: 1rem !important; }
.hero-shell .hero-tags > span { display: inline-flex; align-items: center; gap: .4rem; }
.hero-visual { min-height: 300px; }
.swatch-stack { position: absolute; width: 78%; height: 240px; padding: 7px; background: #f6f0e5; border-radius: 18px; box-shadow: 0 15px 30px #33291835; }
.swatch-stack img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
.swatch-back { top: 1%; right: 0; transform: rotate(9deg); }
.swatch-front { top: 7%; left: 0; transform: rotate(-8deg); }
.scan-corners { position: absolute; inset: 20% 23%; border: 1px solid #f0dfbca1; border-radius: 12px; box-shadow: 0 0 0 14px #fff1; }
.scan-corners::after { content: ""; position: absolute; top: 50%; left: -12%; width: 124%; height: 1px; background: #f8ecd4c9; box-shadow: 0 0 14px 2px #e5d4a650; }
.stApp .swatch-label {
    position: absolute; inset: auto 15px 15px; display: flex; align-items: center; gap: .4rem;
    padding: .55rem; background: #142d24de; color: #fff8e9 !important; -webkit-text-fill-color: #fff8e9 !important;
    border-radius: 8px; font-size: .6rem; letter-spacing: .03em;
}
.swatch-label svg { color: #fff8e9 !important; }
.material-ticket { width: 76%; bottom: -4px; right: -4px; z-index: 2; transform: rotate(3deg); }
.ticket-head > span { display: inline-flex; align-items: center; gap: .35rem; }
.feature-card-grid { gap: .75rem !important; }
.info-card.ivory-card { min-height: 166px !important; padding: 1.1rem !important; gap: .6rem; }
.info-card .icon-badge { margin-bottom: .2rem; }
.info-card.ivory-card p { margin-top: .45rem !important; }
.workflow-step { position: relative; }
.workflow-step.ivory-card > .icon-badge { width: 36px !important; height: 36px !important; padding: 6px !important; border-radius: 11px !important; }
.workflow-step .step-number { position: absolute; right: .85rem; top: 1rem; color: #807460; font-size: .65rem; letter-spacing: .1em; }
.scenario-card > .icon-badge { margin-bottom: .8rem; }

/* Topic-specific illustrations give every page a recognizable identity. */
.page-intro.ivory-card {
    grid-template-columns: minmax(0, 1fr) 210px !important; gap: 1.4rem !important;
    min-height: 218px; padding: 1.8rem 2rem !important;
}
.page-heading-label { display: flex; align-items: center; gap: .65rem; margin-bottom: .75rem; }
.page-heading-label > .icon-badge { width: 32px; height: 32px; border-radius: 10px; }
.page-heading-label > .icon-badge svg { width: 19px; height: 19px; }
.stApp .page-heading-label > span:last-child { color: #75603c !important; -webkit-text-fill-color: #75603c !important; font-size: .66rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; }
.page-intro.ivory-card h2 { font-size: clamp(2rem, 3vw, 3rem) !important; max-width: 25ch; margin: 0 !important; }
.page-intro.ivory-card .page-intro-text { font-size: .87rem !important; max-width: 48rem !important; }
.page-art { width: 100%; }
.page-illustration { display: block; width: 100%; height: auto; }
.section-heading, .icon-heading, .input-section-head h3 { display: flex; align-items: center; gap: .65rem; }
.stApp h3.section-heading { font-family: var(--font-sans) !important; font-size: 1.05rem !important; margin: .9rem 0 .6rem !important; }
.section-heading .icon-badge { width: 34px; height: 34px; border-radius: 10px; }
.section-heading .icon-badge svg { width: 20px; height: 20px; }
.input-section-head h3 > svg { color: #947543 !important; }
.metric-heading { display: flex; align-items: center; gap: .6rem; margin-bottom: .65rem; }
.metric-heading .icon-badge { width: 30px; height: 30px; border-radius: 9px; }
.metric-heading svg { width: 18px; height: 18px; }
.stApp .metric-card .metric-label, .stApp .metric-card .fs-metric-sub { color: #635e55 !important; -webkit-text-fill-color: #635e55 !important; }
.highlight-banner { display: flex; align-items: flex-start; gap: .8rem; }
.highlight-banner > .icon-badge { width: 36px; height: 36px; background: #e6d2ad; }
.highlight-banner > .icon-badge svg { width: 21px; height: 21px; }
.empty-state-card { padding: 2rem 1.3rem !important; background: linear-gradient(120deg, #f7f3ec, #ede7dc) !important; }
.empty-state-art { position: relative; display: grid; place-items: center; width: 78px; height: 78px; margin: 0 auto 1.15rem; border: 1px solid #cbb895; border-radius: 24px; background: #eadfc9; transform: rotate(-5deg); }
.empty-state-art > svg { color: #80643a !important; transform: rotate(5deg); }
.empty-state-art .art-dot { position: absolute; width: 12px; height: 12px; border: 1px solid #9caf9f; border-radius: 4px; background: #c8d7ca; top: -7px; right: -12px; }
.empty-state-art .art-dot:last-child { width: 8px; height: 8px; top: auto; right: auto; bottom: 4px; left: -19px; background: #dcc298; border-color: #c1a378; }
.about-illustration { width: 160px; margin: .75rem auto; }
.about-proof-list svg { color: #d5bd91; }

/* Fabric and care references: visual, readable, and responsive. */
.fabric-reference { overflow: hidden; border: 1px solid #d8c8b1; border-radius: 20px; background: #f7f3ec; margin-bottom: 1rem; }
.fabric-reference-image { position: relative; height: 150px; overflow: hidden; background: #9eab9d; }
.fabric-reference-image img { width: 100%; height: 100%; object-fit: cover; }
.stApp .fabric-reference-image > span {
    position: absolute; bottom: 12px; left: 16px; display: inline-flex; align-items: center; gap: .4rem;
    background: #f7f3ecee; color: #34362e !important; -webkit-text-fill-color: #34362e !important;
    padding: .35rem .6rem; border-radius: 7px; font-size: .65rem;
}
.fabric-reference-body { padding: 1.1rem 1.25rem; }
.fabric-reference h3 { font-size: 1.7rem !important; margin: 0 0 .85rem !important; }
.reference-detail { display: flex; gap: .65rem; margin-top: .75rem; }
.reference-detail > svg { margin-top: 3px; color: #7b6a4f !important; }
.stApp .reference-detail strong { font-size: .72rem; }
.stApp .reference-detail p { font-size: .8rem; line-height: 1.6; margin: .15rem 0 0; color: #5b574f !important; -webkit-text-fill-color: #5b574f !important; }
.care-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-bottom: 1.2rem; }
.care-reference { border: 1px solid #d8c8b1; border-radius: 20px; padding: 1.2rem; background: #f7f3ec; }
.care-reference h3 { display: flex; align-items: center; gap: .5rem; margin: 0 0 .8rem !important; font-size: 1.4rem !important; }
.care-instruction { display: flex; align-items: flex-start; gap: .7rem; padding: .85rem 0; border-top: 1px solid #ded6c9; }
.care-instruction .icon-badge { width: 35px; height: 35px; border-radius: 10px; }
.care-instruction .icon-badge svg { width: 21px; height: 21px; }
.care-instruction strong { font-size: .74rem; }
.stApp .care-instruction p { margin: .2rem 0 0; font-size: .78rem; line-height: 1.55; color: #5b574f !important; -webkit-text-fill-color: #5b574f !important; }

@media (max-width: 1100px) {
    .hero-shell.atelier-home-card { grid-template-columns: minmax(0, 1fr) minmax(225px, .8fr) !important; gap: 1.25rem !important; }
    .hero-shell.atelier-home-card h1 { font-size: 3.2rem !important; }
    .page-intro.ivory-card { grid-template-columns: minmax(0, 1fr) 155px !important; }
    .care-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
    .metric-band { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem; }
    .metric-band .fs-metric-card { min-height: 125px !important; }
    .stTabs [role="tab"] { padding: .6rem .85rem !important; }
    .confidence-bar-container { grid-template-columns: minmax(0, 1fr) 3.5rem !important; }
    .confidence-name { grid-column: 1 / -1; }
    .hero-shell.atelier-home-card { grid-template-columns: 1fr !important; padding: 1.5rem !important; }
    .hero-shell.atelier-home-card h1 { font-size: clamp(2.7rem, 8vw, 3.5rem) !important; }
    .hero-visual { width: min(100%, 360px); min-height: 285px; margin: .4rem auto; }
    .feature-card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
    .workflow-step-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
    .page-intro.ivory-card { grid-template-columns: minmax(0, 1fr) 100px !important; padding: 1.3rem !important; }
    .page-intro.ivory-card h2 { font-size: 2rem !important; }
    .page-intro.ivory-card .page-intro-text { font-size: .8rem !important; }
    .highlight-banner { gap: .6rem; }
}
@media (max-width: 480px) {
    .care-grid { grid-template-columns: 1fr; }
    .page-intro.ivory-card { grid-template-columns: 1fr !important; }
    .page-art { display: none; }
    .hero-kicker { font-size: .6rem !important; letter-spacing: .1em !important; }
    .info-card.ivory-card { padding: .85rem !important; }
    .info-card.ivory-card h3 { font-size: 1rem !important; }
}
</style>
"""
