"""Small, local SVG vocabulary shared by navigation and content.

Icons are decorative; the adjacent text supplies the accessible label. No icon
font, CDN, or JavaScript is needed, including for the native radio navigation.
"""

from urllib.parse import quote


ICON_PATHS = {
    "scan": '<path d="M8 3H5a2 2 0 0 0-2 2v3m13-5h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3m8 0h3a2 2 0 0 0 2-2v-3M3 12h18"/><path d="M8 8h8v8H8z"/>',
    "layers": '<path d="m12 3 10 5-10 5L2 8zM2 12l10 5 10-5M2 16l10 5 10-5"/>',
    "compare": '<rect x="3" y="4" width="7" height="16" rx="2"/><rect x="14" y="4" width="7" height="16" rx="2"/><path d="M7 9h10m-2-2 2 2-2 2M17 15H7m2-2-2 2 2 2"/>',
    "history": '<path d="M3 11a9 9 0 1 1 2.7 7.4M3 4v7h7m2-4v5l3 2"/>',
    "book": '<path d="M12 5v16M3 3c4 0 6 0 9 2 3-2 5-2 9-2v16c-4 0-6 0-9 2-3-2-5-2-9-2z"/>',
    "care": '<path d="M12 3C9 7 5 10 5 14a7 7 0 0 0 14 0c0-4-4-7-7-11Z"/><path d="m9 14 2 2 4-4"/>',
    "chip": '<rect x="5" y="5" width="14" height="14" rx="3"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v3m6-3v3M9 19v3m6-3v3M2 9h3m-3 6h3m14-6h3m-3 6h3"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.01"/>',
    "weave": '<path d="M7 3v18M12 3v18M17 3v18M3 7h18M3 12h18M3 17h18"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 1-3.7 1.5 1.5 0 0 1 .8-2.8H18A3 3 0 0 0 21 12a9 9 0 0 0-9-9Z"/><circle cx="7.5" cy="10" r=".8"/><circle cx="11" cy="6.8" r=".8"/><circle cx="16" cy="8" r=".8"/><circle cx="7.5" cy="15" r=".8"/>',
    "texture": '<path d="M3 6c3-4 6 4 9 0s6 4 9 0M3 12c3-4 6 4 9 0s6 4 9 0M3 18c3-4 6 4 9 0s6 4 9 0"/>',
    "report": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6M8 13h8M8 17h5"/>',
    "upload": '<path d="M12 16V3m-5 5 5-5 5 5M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.5"/><path d="m21 15-5-5L5 21"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "shield": '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6z"/><path d="m8 12 3 3 5-6"/>',
    "spark": '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z"/>',
    "leaf": '<path d="M20 3C9 3 3 6 4 13c1 6 8 9 12 4 3-4 4-9 4-14ZM4 21l11-11"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z"/>',
    "chart": '<path d="M4 3v17h17M8 16v-4m5 4V7m5 9v-6"/>',
    "tag": '<path d="M3 3h8l10 10-8 8L3 11z"/><circle cx="7.5" cy="7.5" r="1"/>',
    "wash": '<path d="m3 6 2 14h14l2-14M4 10c3-3 5 3 8 0s5 3 8 0"/>',
    "dry": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="6"/><path d="M12 10v4"/>',
    "iron": '<path d="M5 8h10l5 11H3v-4a7 7 0 0 1 7-7M3 15h15M7 4h8l2 4"/>',
    "arrow": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
}


def icon_svg(name: str, size: int = 24) -> str:
    """Return one of our trusted decorative SVGs, never user-provided markup."""
    paths = ICON_PATHS.get(name, ICON_PATHS["spark"])
    return (
        f'<svg class="fs-icon" xmlns="http://www.w3.org/2000/svg" '
        f'width="{int(size)}" height="{int(size)}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.65" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        f'focusable="false">{paths}</svg>'
    )


def icon_badge(name: str, tone: str = "gold") -> str:
    tone = tone if tone in {"gold", "sage", "blue", "rose"} else "gold"
    return f'<span class="icon-badge tone-{tone}">{icon_svg(name)}</span>'


def navigation_icon_css(names: list[str]) -> str:
    """Keep masks in exactly the same order as the native navigation options."""
    rules = []
    for index, name in enumerate(names, 1):
        uri = "data:image/svg+xml," + quote(icon_svg(name), safe="")
        rules.append(
            'section[data-testid="stSidebar"] .stRadio '
            f'[role="radiogroup"] label:nth-child({index})::before '
            f'{{ -webkit-mask-image: url("{uri}"); mask-image: url("{uri}"); }}'
        )
    return "<style>" + "".join(rules) + "</style>"


def section_icon(title: str) -> str:
    """Select a consistent visual cue for existing shared content blocks."""
    keywords = {
        "palette": "palette", "color": "palette", "pattern": "weave",
        "fabric": "layers", "material": "layers", "texture": "texture",
        "care": "care", "wash": "wash", "quality": "star", "rating": "star",
        "eco": "leaf", "sustainab": "leaf", "season": "sun", "price": "tag",
        "model": "chip", "checkpoint": "chip", "label": "tag",
        "confidence": "chart", "metric": "chart", "benchmark": "chart",
        "report": "report", "review": "check", "history": "history",
        "warning": "info", "habit": "care", "story": "book",
    }
    return next((icon for word, icon in keywords.items() if word in title.lower()), "spark")


def page_illustration(kind: str) -> str:
    """Compact, topic-specific vector drawings for the page headers."""
    drawings = {
        "layers": '<rect x="80" y="35" width="108" height="120" rx="12" transform="rotate(14 134 95)" fill="#d4b78a"/><rect x="54" y="42" width="108" height="120" rx="12" transform="rotate(-8 108 102)" fill="#8ba79b"/><rect x="86" y="64" width="78" height="64" rx="5" fill="#eee5d5"/><path d="M96 80h58m-58 10h58m-58 10h58m-58 10h58M107 74v48m16-48v48m16-48v48"/>',
        "compare": '<rect x="28" y="43" width="87" height="112" rx="12" fill="#92aaa0"/><rect x="145" y="43" width="87" height="112" rx="12" fill="#d5b483"/><path d="m43 66 56 56m-56-36 36 36m-16-56 36 36M161 67h54m-54 15h54m-54 15h54m-54 15h54M104 168h52m-8-7 8 7-8 7"/>',
        "history": '<rect x="45" y="42" width="110" height="126" rx="12" fill="#e4d5ba"/><path d="M63 68h64m-64 22h45m-45 22h34"/><circle cx="163" cy="118" r="43" fill="#92aaa0"/><path d="M163 91v29l19 11"/>',
        "book": '<path d="M36 45q48-12 94 10 46-22 94-10v116q-48-12-94 10-46-22-94-10z" fill="#e4d5ba"/><path d="M130 55v116M54 75h53m-53 19h53m-53 19h40"/><rect x="150" y="72" width="54" height="58" rx="5" fill="#8ba79b"/><path d="M158 84h38m-38 12h38m-38 12h38m-27-30v44m14-44v44"/>',
        "care": '<path d="M130 27c-14 22-52 57-52 88a52 52 0 0 0 104 0c0-31-38-66-52-88Z" fill="#92aaa0"/><path d="m108 115 16 16 30-33M52 50v24m-12-12h24m141 71v20m-10-10h20"/>',
        "chip": '<path d="M72 53 130 101 195 53M61 148l69-47 68 47"/><circle cx="72" cy="53" r="16" fill="#e4d5ba"/><circle cx="195" cy="53" r="16" fill="#92aaa0"/><circle cx="61" cy="148" r="16" fill="#92aaa0"/><circle cx="198" cy="148" r="16" fill="#e4d5ba"/><rect x="96" y="67" width="68" height="68" rx="14" fill="#d4b78a"/><rect x="114" y="85" width="32" height="32" rx="5"/><path d="M117 56v11m26-11v11m-26 68v11m26-11v11M85 88h11m-11 26h11m68-26h11m-11 26h11"/>',
    }
    drawing = drawings.get(kind, '<path d="M65 38v127m43-127v127m44-127v127m43-127v127M43 60h174M43 103h174M43 146h174" stroke-width="16" stroke="#bca06e"/><path d="M65 52v16m43 27v16m44 27v16m43-92v16" stroke-width="16" stroke="#87a397"/>')
    return (
        '<svg class="page-illustration" xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 260 200" fill="none" aria-hidden="true" focusable="false">'
        '<circle cx="130" cy="100" r="86" fill="#eae2d5"/>'
        '<circle cx="130" cy="100" r="96" stroke="#c2aa83" stroke-dasharray="2 7"/>'
        f'<g stroke="#5d6258" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{drawing}</g></svg>'
    )
