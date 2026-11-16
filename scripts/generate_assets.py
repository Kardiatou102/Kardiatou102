"""Génère les visuels SVG animés du profil GitHub (bannière, compétences, cartes projets).

Usage : python scripts/generate_assets.py   (depuis la racine du dépôt)
GitHub n'autorise pas le JavaScript dans un README : les animations sont donc
faites en CSS/SMIL à l'intérieur des SVG, qui eux sont affichés comme images.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Ubuntu, 'Helvetica Neue', Arial, sans-serif"
BG1, BG2 = "#ffffff", "#f6f8fa"
BORDER = "#d8dee4"
TEXT, MUTED = "#24292f", "#57606a"


def text_w(s, size, bold=False):
    """Largeur approximative d'un texte (pas de mesure réelle possible en SVG statique)."""
    k = 0.60 if bold else 0.56
    return len(s) * size * k


# Icônes vectorielles au trait (grille 24x24), dessinées dans la couleur de l'élément.
ICONS = {
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "trend": '<polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/>',
    "pulse": '<polyline points="3 12 7 12 10 5 14 19 17 12 21 12"/>',
    "bars": '<line x1="4" y1="20" x2="20" y2="20"/><rect x="6" y="11" width="3" height="9"/><rect x="11" y="6" width="3" height="14"/><rect x="16" y="14" width="3" height="6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "grid": '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/>',
    "pie": '<path d="M21 12A9 9 0 1 1 12 3v9z"/><path d="M15 3.5A9 9 0 0 1 20.5 9H15z"/>',
    "sigma": '<path d="M18 6V4H6l6 8-6 8h12v-2"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "code": '<polyline points="8 7 3 12 8 17"/><polyline points="16 7 21 12 16 17"/><line x1="14" y1="4" x2="10" y2="20"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}


def icon(name, x, y, size, color):
    """Place l'icône `name` (coin haut-gauche en x, y) à la taille `size`."""
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({size / 24:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("écrit", path.relative_to(ROOT))


# --------------------------------------------------------------------------- bannière
def header():
    W, H = 900, 220
    nodes = [(560, 60), (640, 120), (720, 50), (790, 140), (850, 70), (690, 185), (610, 30), (820, 200)]
    edges = [(0, 1), (1, 2), (2, 4), (1, 3), (3, 4), (1, 5), (3, 5), (0, 6), (6, 2), (3, 7)]
    graph = []
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        graph.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#5a5fb0" stroke-opacity=".25" stroke-width="1.2"/>')
    for i, (x, y) in enumerate(nodes):
        dur = 3 + (i % 3)
        graph.append(
            f'<circle cx="{x}" cy="{y}" r="{4 + i % 3}" fill="{["#5a5fb0", "#2f7f7a", "#a8577e"][i % 3]}">'
            f'<animate attributeName="r" values="{4 + i % 3};{7 + i % 3};{4 + i % 3}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".55;1;.55" dur="{dur}s" repeatCount="indefinite"/></circle>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Kardiatou BA — Data Science">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="#eef1f7"/></linearGradient>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#5a5fb0"/><stop offset=".5" stop-color="#2f7f7a"/><stop offset="1" stop-color="#a8577e"/></linearGradient>
  <clipPath id="type"><rect x="40" y="40" height="80" width="460"><animate attributeName="width" values="0;0;460" keyTimes="0;.15;1" begin="0s" dur="1.9s"/></rect></clipPath>
  <style>
    .t {{ font-family: {FONT}; }}
    .fr {{ animation: fr 10s infinite; }} .en {{ animation: en 10s infinite; opacity: 0; }}
    @keyframes fr {{ 0%,45% {{opacity:1}} 50%,95% {{opacity:0}} 100% {{opacity:1}} }}
    @keyframes en {{ 0%,45% {{opacity:0}} 50%,95% {{opacity:1}} 100% {{opacity:0}} }}
    .tags {{ animation: in .8s 2s backwards; }}
    @keyframes in {{ from {{ opacity: 0; }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
{"".join(graph)}
<text x="44" y="62" class="t" font-size="18" fill="{MUTED}">Bonjour, je suis · Hi, I'm</text>
<g clip-path="url(#type)"><text x="42" y="112" class="t" font-size="50" font-weight="700" fill="url(#name)">Kardiatou BA</text></g>
<text x="44" y="150" class="t fr" font-size="19" fill="{TEXT}">Étudiante en Master 1 MIASHS · Data Science</text>
<text x="44" y="150" class="t en" font-size="19" fill="{TEXT}">Master's student in Applied Maths &amp; CS · Data Science</text>
<text x="44" y="186" class="t tags" font-size="15" fill="#2f7f7a">Data · Machine Learning · Deep Learning</text>
</svg>'''
    write(ASSETS / "header.svg", svg)


# --------------------------------------------------------------------------- compétences
SKILLS = {
    "fr": [
        ("pie", "Data Science", "#2f7f7a", ["Collecte & nettoyage des données", "Analyse exploratoire (EDA)", "Data visualisation", "Feature engineering", "Modélisation prédictive", "Évaluation de modèles", "Communication des résultats"]),
        ("sigma", "Mathématiques &amp; statistique", "#5a5fb0", ["Statistique descriptive", "Statistique inférentielle", "Modélisation statistique", "Analyse de données (ACP)", "Algèbre linéaire & bilinéaire", "Optimisation", "Calcul différentiel"]),
        ("cpu", "Machine Learning &amp; IA", "#a8577e", ["Apprentissage supervisé", "Apprentissage non supervisé", "Deep Learning", "NLP", "LLM", "RAG"]),
        ("code", "Langages &amp; bibliothèques", "#3f6f9f", ["Python (Pandas, NumPy, Matplotlib, Scikit-learn)", "R", "SQL", "Jupyter"]),
        ("database", "Bases de données &amp; outils", "#6b7a8f", ["Modélisation de données (MCD / MLD)", "Bases relationnelles (MySQL)", "Bases de données NoSQL", "Git & GitHub", "Docker", "Algorithmique", "Graphes & réseaux"]),
        ("globe", "Développement web", "#a8762a", ["JavaScript (POO)", "PHP", "HTML / CSS", "jQuery & AJAX", "API (Flask, FastAPI)"]),
    ],
    "en": [
        ("pie", "Data Science", "#2f7f7a", ["Data collection & cleaning", "Exploratory data analysis (EDA)", "Data visualization", "Feature engineering", "Predictive modeling", "Model evaluation", "Communicating results"]),
        ("sigma", "Mathematics &amp; statistics", "#5a5fb0", ["Descriptive statistics", "Inferential statistics", "Statistical modeling", "Multivariate analysis (PCA)", "Linear & bilinear algebra", "Optimization", "Differential calculus"]),
        ("cpu", "Machine Learning &amp; AI", "#a8577e", ["Supervised learning", "Unsupervised learning", "Deep Learning", "NLP", "LLM", "RAG"]),
        ("code", "Languages &amp; libraries", "#3f6f9f", ["Python (Pandas, NumPy, Matplotlib, Scikit-learn)", "R", "SQL", "Jupyter"]),
        ("database", "Databases &amp; tools", "#6b7a8f", ["Data modeling", "Relational databases (MySQL)", "NoSQL databases", "Git & GitHub", "Docker", "Algorithms", "Graphs & networks"]),
        ("globe", "Web development", "#a8762a", ["JavaScript (OOP)", "PHP", "HTML / CSS", "jQuery & AJAX", "APIs (Flask, FastAPI)"]),
    ],
}


def skills(lang):
    W, PAD, FS, PH, GAP = 900, 32, 13.5, 30, 10
    body, y, n = [], PAD, 0
    for ci, (icon_name, title, color, items) in enumerate(SKILLS[lang]):
        d = ci * 0.35
        body.append(f'<g class="cat" style="animation-delay:{d:.2f}s">{icon(icon_name, PAD, y + 2, 19, color)}<text x="{PAD + 28}" y="{y + 18}" class="t" font-size="16" font-weight="700" fill="{color}">{title}</text></g>')
        y += 32
        x = PAD
        for item in items:
            w = text_w(item, FS) + 28
            if x + w > W - PAD:
                x, y = PAD, y + PH + GAP
            delay = d + 0.15 + n * 0.035
            body.append(
                f'<g transform="translate({x:.0f},{y})"><g class="pill" style="animation-delay:{delay:.2f}s">'
                f'<rect width="{w:.0f}" height="{PH}" rx="15" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".55"/>'
                f'<text x="{w / 2:.0f}" y="20" text-anchor="middle" class="t" font-size="{FS}" fill="{TEXT}">{escape(item)}</text></g></g>'
            )
            x += w + GAP
            n += 1
        y += PH + 26
    H = y + PAD - 26 + 6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Compétences / Skills">
<defs><style>
  .t {{ font-family: {FONT}; }}
  .cat {{ animation: fade .55s ease-out backwards; }}
  .pill {{ animation: pop .55s ease-out backwards; }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  @keyframes pop {{ from {{ opacity: 0; transform: translateY(10px); }} }}
</style></defs>
<rect width="{W}" height="{H}" rx="18" fill="{BG1}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
{"".join(body)}
</svg>'''
    write(ASSETS / f"skills-{lang}.svg", svg)


# --------------------------------------------------------------------------- cartes projets
PROJECTS = [
    dict(slug="pairia", icon="chat", color="#a8577e", title="PairIA",
         sub={"fr": "Chatbot IA pour l'e-commerce", "en": "AI chatbot for e-commerce"},
         desc={"fr": "Boutique de chaussures avec un assistant IA 100 % local : recherche en langage naturel, par image (CLIP) ou à la voix (Whisper), 75 langues, chatbot admin à 25 outils.",
               "en": "Shoe e-commerce site with a fully local AI assistant: natural-language, image (CLIP) and voice (Whisper) search, 75 languages, admin chatbot with 25 tools."},
         tags=["Deep Learning", "NLP", "RAG", "CamemBERT", "LLaMA 3.1", "Docker"]),
    dict(slug="salary", icon="trend", color="#2f7f7a", title="Salary Predict",
         sub={"fr": "Prédiction de salaires par machine learning", "en": "Salary prediction with machine learning"},
         desc={"fr": "Application web qui estime le salaire d'une offre d'emploi. 5 modèles comparés : régression, Random Forest, KNN, MLP et Gradient Boosting (retenu).",
               "en": "Web app estimating the salary of a job offer. 5 models compared: regression, Random Forest, KNN, MLP and Gradient Boosting (best)."},
         tags=["Scikit-learn", "Pandas", "Flask", "MySQL", "PHP"]),
    # Masqué pour l'instant (hidden=True) : à réactiver quand le bon lien du dépôt sera prêt.
    dict(slug="lirmm", hidden=True, icon="pulse", color="#5a5fb0", title="Stage LIRMM",
         title_en="LIRMM Internship",
         sub={"fr": "Concepts cliniques extraits par un LLM", "en": "Clinical concepts extracted with an LLM"},
         desc={"fr": "Extraction de concepts cliniques depuis des questionnaires de santé mentale (PHQ-9, GAD-7, Epworth) avec Qwen2.5 en local, alignés sur SNOMED CT.",
               "en": "Extracting clinical concepts from mental-health questionnaires (PHQ-9, GAD-7, Epworth) with a local Qwen2.5 model, mapped to SNOMED CT."},
         tags=["NLP", "LLM", "Qwen2.5", "Ollama", "Python"]),
    dict(slug="gbsc", icon="bars", color="#a8762a", title="Disparités territoriales",
         title_en="Territorial disparities",
         sub={"fr": "Analyse statistique des départements", "en": "Statistical analysis of French departments"},
         desc={"fr": "Les départements où l'on vit le mieux sont-ils les plus riches ? Revenus, chômage, pauvreté et offre culturelle analysés (corrélations, ANOVA).",
               "en": "Are the best places to live also the richest? Income, unemployment, poverty and cultural facilities analyzed (correlations, ANOVA)."},
         tags=["R", "ggplot2", "ANOVA", "MySQL"]),
    dict(slug="departement", icon="pin", color="#3f6f9f", title="Départ(ement)",
         sub={"fr": "Carte interactive pour choisir où vivre", "en": "Interactive map to choose where to live"},
         desc={"fr": "Plateforme web pour comparer les départements selon ses priorités : coût de la vie, revenus, culture et enseignement supérieur.",
               "en": "Web platform to compare French departments by personal priorities: cost of living, income, culture and higher education."},
         tags=["JavaScript", "AJAX", "PHP", "Leaflet", "MySQL"]),
    dict(slug="more", icon="grid", color="#6e7781", title="Plus de projets", title_en="More projects",
         sub={"fr": "Tous mes dépôts GitHub", "en": "All my GitHub repositories"},
         desc={"fr": "Retrouvez l'ensemble de mes travaux, projets universitaires et expérimentations sur mon profil GitHub.",
               "en": "Browse all my work, university projects and experiments on my GitHub profile."},
         tags=["GitHub"]),
]


def card(p, lang, index):
    W, H, P = 460, 236, 26
    title = p.get("title_en", p["title"]) if lang == "en" else p["title"]
    c = p["color"]
    desc_txt = p["desc"][lang]
    for punct in ":?!;":  # espace insécable devant la ponctuation double (typographie française)
        desc_txt = desc_txt.replace(" " + punct, " " + punct)
    lines = wrap(desc_txt, 62)[:3]
    desc = "".join(f'<text x="{P}" y="{116 + i * 21}" class="t" font-size="13.5" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(lines))
    pills, x = [], P
    for t in p["tags"]:
        w = text_w(t, 12) + 22
        if x + w > W - P:
            break
        pills.append(f'<rect x="{x:.0f}" y="190" width="{w:.0f}" height="24" rx="12" fill="{c}" fill-opacity=".14"/>'
                     f'<text x="{x + w / 2:.0f}" y="206" text-anchor="middle" class="t" font-size="12" fill="{c}">{escape(t)}</text>')
        x += w + 7
    link = "Voir le dépôt ↗" if lang == "fr" else "View repo ↗"
    if p["slug"] == "more":
        link = "Voir tout ↗" if lang == "fr" else "See all ↗"
    d = index * 0.12
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
  <linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="bar"><rect x="0" y="0" width="{W}" height="4" rx="2"/></clipPath>
  <style>
    .t {{ font-family: {FONT}; }}
    .card {{ animation: up .7s {d:.2f}s ease-out backwards; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} }}
  </style>
</defs>
<g class="card">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#bg)" stroke="{BORDER}"/>
  <g transform="translate(16,1)" clip-path="url(#bar)">
    <rect width="{W - 32}" height="4" fill="{c}"/>
    <rect x="-140" width="120" height="4" fill="url(#shine)"><animate attributeName="x" values="-140;{W};{W}" keyTimes="0;.5;1" dur="5s" begin="{1 + d:.2f}s" repeatCount="indefinite"/></rect>
  </g>
  <circle cx="{P + 24}" cy="54" r="24" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".45"/>
  {icon(p["icon"], P + 13, 43, 22, c)}
  <text x="{P + 62}" y="50" class="t" font-size="20" font-weight="700" fill="{TEXT}">{escape(title)}</text>
  <text x="{P + 62}" y="72" class="t" font-size="13" fill="{c}">{escape(p["sub"][lang])}</text>
  <text x="{W - P}" y="34" text-anchor="end" class="t" font-size="12" fill="{MUTED}">{link}</text>
  {desc}
  {"".join(pills)}
</g>
</svg>'''
    write(ASSETS / "cards" / f"{p['slug']}-{lang}.svg", svg)


if __name__ == "__main__":
    header()
    for lang in ("fr", "en"):
        skills(lang)
        visible = [p for p in PROJECTS if not p.get("hidden")]
        for i, p in enumerate(visible):
            card(p, lang, i % 2)
