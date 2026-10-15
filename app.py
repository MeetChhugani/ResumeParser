import html
import os
import re

import pandas as pd
import PyPDF2
import streamlit as st
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


st.set_page_config(page_title="Resume Matcher", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');
:root { --ink:#18233f; --muted:#63708b; --violet:#7049e8; --teal:#149b96; }
.stApp { background:radial-gradient(circle at 8% 6%,#d9f8ff 0,transparent 23%),radial-gradient(circle at 90% 0%,#f8d9ff 0,transparent 28%),linear-gradient(145deg,#f7f6ff,#fdfaff 48%,#effcff); color:var(--ink); font-family:'DM Sans',sans-serif; }
.block-container { max-width:1180px; padding-top:2.5rem; padding-bottom:3rem; } #MainMenu,footer,header { visibility:hidden; }
h1,h2,h3 { font-family:'Outfit',sans-serif; color:var(--ink); }
.hero { position:relative; overflow:hidden; padding:2.45rem 2.7rem; margin:0 0 2rem; border-radius:28px; background:linear-gradient(115deg,#4930ad,#7648e8 52%,#c052d6); color:white; box-shadow:0 20px 45px rgba(83,48,173,.27); }
.hero:after { content:''; position:absolute; width:250px; height:250px; right:-70px; top:-110px; border-radius:50%; background:rgba(255,255,255,.13); }
.eyebrow { position:relative; z-index:1; display:inline-block; padding:.35rem .7rem; border-radius:999px; background:rgba(255,255,255,.18); font-size:.78rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.hero h1 { position:relative; z-index:1; color:white; font-size:clamp(2rem,4vw,3.25rem); margin:.55rem 0 .45rem; letter-spacing:-.04em; }.hero p { position:relative; z-index:1; max-width:700px; margin:0; font-size:1.05rem; line-height:1.6; color:#f5eeff; }
.section-label { color:var(--violet); font-size:.78rem; font-weight:800; text-transform:uppercase; letter-spacing:.11em; margin:0 0 .35rem; }
.role-intro { padding:1.55rem 1.8rem; margin:.4rem 0 1.2rem; border:1px solid rgba(117,76,227,.22); border-radius:24px; background:linear-gradient(110deg,#fff,#f4efff 62%,#e4fbff); box-shadow:0 14px 34px rgba(71,49,132,.09); }.role-intro h2 { margin:.6rem 0 .35rem; font-size:2rem; }.role-intro p { margin:0; color:#64718d; }
.role-kicker { display:inline-block; padding:.34rem .7rem; border-radius:999px; background:#e8e0ff; color:#6540cf; font-size:.74rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
div[data-testid="stFileUploader"],div[data-testid="stTextArea"] { padding:1.25rem; border-radius:18px; background:rgba(255,255,255,.88); border:1px solid rgba(112,73,232,.16); box-shadow:0 8px 24px rgba(65,51,118,.07); }
div[data-testid="stFileUploader"] { min-height:245px; } label { color:var(--ink)!important; font-weight:700!important; }
div[data-testid="stFileUploaderDropzone"] { min-height:140px!important; border:2px dashed #bba9ed!important; border-radius:14px!important; background:#faf8ff!important; }
div[data-testid="stFileUploader"] button[kind="secondary"] { border:0!important; border-radius:10px!important; background:linear-gradient(100deg,#6844df,#a64bd6)!important; color:#fff!important; box-shadow:0 7px 14px rgba(96,60,203,.22)!important; }
div[data-testid="stFileUploader"] button[kind="secondary"] * { color:#fff!important; fill:#fff!important; }
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"],div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] > div { background:#f1edff!important; border-color:#d9ceff!important; color:#293755!important; -webkit-text-fill-color:#293755!important; border-radius:11px!important; }
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] * { color:#293755!important; -webkit-text-fill-color:#293755!important; fill:#6c47d9!important; }
div[data-testid="stTextArea"] textarea { min-height:160px!important; padding:1rem!important; border:1px solid #d3c6f7!important; border-radius:12px!important; background:#fffeff!important; color:#18233f!important; -webkit-text-fill-color:#18233f!important; line-height:1.5!important; }
div[data-testid="stTextArea"] textarea::placeholder { color:#7a8396!important; -webkit-text-fill-color:#7a8396!important; opacity:1!important; }
div[data-testid="stSelectbox"] > div > div { min-height:55px; border:1px solid #d8caff!important; border-radius:15px!important; background:#fff!important; box-shadow:0 7px 18px rgba(79,51,148,.08); }
div.stButton > button { min-height:3.2rem; border:0; border-radius:14px; font-family:'DM Sans',sans-serif; font-size:1rem; font-weight:800; background:linear-gradient(100deg,#6243df,#b64fd1); box-shadow:0 10px 22px rgba(112,73,232,.28); }
.requirements-panel,.result-card { height:100%; box-sizing:border-box; padding:1.35rem; border-radius:20px; background:rgba(255,255,255,.92); border:1px solid #e8defb; box-shadow:0 10px 28px rgba(65,51,118,.07); }
.requirements-panel h3 { margin:.05rem 0 .3rem; }.requirements-panel p { margin:0 0 .75rem; color:var(--muted); font-size:.9rem; }.primary-panel { border-top:4px solid var(--violet); }.secondary-panel { border-top:4px solid var(--teal); }
.requirement-chip { display:inline-block; margin:.2rem; padding:.36rem .67rem; border-radius:999px; background:#eee8ff; color:#5635b9; font-size:.82rem; font-weight:700; }.secondary-chip { background:#ddf7f4; color:#16736e; }
.metrics-strip { margin:.8rem 0 1.25rem; padding:1.1rem 1.4rem; border-radius:18px; background:linear-gradient(110deg,#fff,#f4f0ff); border:1px solid #e1d8fb; }
.decision { display:inline-block; padding:.45rem .8rem; border-radius:999px; font-size:.86rem; font-weight:800; letter-spacing:.04em; }.decision-yes { background:#d8faef; color:#087d5d; }.decision-no { background:#ffe4ea; color:#bd3150; }
.missing-skill { display:inline-block; margin:.22rem; padding:.38rem .65rem; background:#ffe7f4; color:#a02f70; border-radius:999px; font-size:.84rem; font-weight:600; }
</style>
""", unsafe_allow_html=True)


GENERIC_SCREENING_WORDS = {
    "ability", "abilities", "academic", "academics", "agent", "agents", "agentic",
    "analytical", "architecture", "architectures", "artificial", "assist", "based",
    "basic", "benefit", "best", "case", "cases", "clearly", "concept", "concepts",
    "consideration", "considerations", "creating", "cross", "deep", "develop",
    "experience", "experienced", "including", "knowledge", "project", "projects",
    "responsible", "role", "skills", "technology", "technologies", "understanding",
    "use", "user", "work", "working", "years", "required", "preferred", "candidate",
}
SCREENING_STOP_WORDS = ENGLISH_STOP_WORDS.union(GENERIC_SCREENING_WORDS)
PRIMARY_COVERAGE_THRESHOLD = 70


DEFAULT_ROLE_LIBRARY = {
    "Software Engineer": {
        "description": "Build reliable, scalable product features. Design backend or frontend services, write maintainable code, participate in code reviews, and collaborate with product and design.",
        "primary": ["Python or Java", "SQL", "REST APIs", "Git", "Software testing"],
        "secondary": ["React", "Docker", "AWS", "Kubernetes", "Microservices"],
    },
    "Data Analyst": {
        "description": "Turn business data into clear recommendations. Query and clean data, build dashboards, define metrics, and communicate insights to stakeholders.",
        "primary": ["SQL", "Excel", "Data visualization", "Data cleaning", "Business analysis"],
        "secondary": ["Python", "Power BI", "Tableau", "Statistics", "A/B testing"],
    },
    "Data Scientist": {
        "description": "Develop data products and decision models. Explore datasets, build and evaluate machine learning models, run experiments, and present findings to business partners.",
        "primary": ["Python", "SQL", "Statistics", "Machine learning", "Data cleaning"],
        "secondary": ["Scikit-learn", "Pandas", "Experimentation", "Forecasting", "Cloud data platforms"],
    },
    "Product Manager": {
        "description": "Define product strategy and ship customer-focused improvements. Gather customer needs, prioritize roadmaps, write requirements, track outcomes, and align teams.",
        "primary": ["Product discovery", "Roadmap planning", "Stakeholder management", "User research", "Product analytics"],
        "secondary": ["B2B SaaS", "Experimentation", "Jira", "Agile", "Product metrics"],
    },
    "Project Manager": {
        "description": "Plan, coordinate, and deliver cross-functional initiatives. Manage scope, schedules, risks, budgets, dependencies, and stakeholder communication.",
        "primary": ["Project planning", "Risk management", "Stakeholder management", "Reporting", "Agile delivery"],
        "secondary": ["PMP", "Scrum", "Jira", "Confluence", "Technical projects"],
    },
    "UX UI Designer": {
        "description": "Create intuitive, accessible digital experiences. Conduct research, map journeys, design wireframes and prototypes, and partner with product and engineering.",
        "primary": ["Figma", "Interaction design", "Visual design", "Prototyping", "Usability testing"],
        "secondary": ["Accessibility", "Design systems", "Responsive web design", "B2B products"],
    },
    "DevOps Engineer": {
        "description": "Improve delivery reliability, security, and observability. Build CI/CD pipelines, manage cloud infrastructure, automate deployments, and support incident response.",
        "primary": ["CI CD", "Docker", "Kubernetes", "Cloud infrastructure", "Linux"],
        "secondary": ["AWS", "Terraform", "Python", "Monitoring", "SRE"],
    },
    "Cybersecurity Analyst": {
        "description": "Protect systems, data, and users. Monitor alerts, investigate incidents, manage vulnerabilities, document findings, and improve security controls.",
        "primary": ["SIEM", "Incident response", "Vulnerability management", "Network security", "Risk assessment"],
        "secondary": ["Splunk", "Microsoft Sentinel", "SOC operations", "Cloud security", "Security certifications"],
    },
    "Digital Marketing Specialist": {
        "description": "Plan and optimize multi-channel campaigns, analyze performance, create content briefs, and improve conversion funnels.",
        "primary": ["Google Analytics", "SEO", "SEM", "Campaign reporting", "Copywriting"],
        "secondary": ["Google Ads", "HubSpot", "Email marketing", "CRM", "A B testing"],
    },
    "HR Recruiter": {
        "description": "Attract and hire great talent. Partner with hiring managers, source candidates, conduct screening interviews, coordinate interviews, and maintain candidate experience.",
        "primary": ["Talent sourcing", "Interview coordination", "ATS management", "Candidate assessment", "Recruiting metrics"],
        "secondary": ["LinkedIn Recruiter", "Employer branding", "Technical recruiting", "HRIS"],
    },
    "Financial Analyst": {
        "description": "Support planning and business decisions. Prepare forecasts, analyze financial results, build models, report performance, and work with operational leaders.",
        "primary": ["Financial modeling", "Budgeting", "Forecasting", "Excel", "Variance analysis"],
        "secondary": ["SQL", "Power BI", "ERP systems", "FP and A", "Accounting"],
    },
    "Customer Success Manager": {
        "description": "Help customers achieve measurable value. Onboard accounts, manage relationships, identify risks and growth opportunities, and lead business reviews.",
        "primary": ["Account management", "Customer onboarding", "Customer retention", "CRM", "Stakeholder communication"],
        "secondary": ["Salesforce", "Renewals", "Upselling", "Enterprise customers", "SaaS"],
    },
}


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join(page.extract_text() or "" for page in reader.pages)


def extract_resume_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    return file.getvalue().decode("utf-8", errors="ignore")


def requirement_items(text):
    return [item.strip() for item in re.split(r"[,\n;]+", text) if item.strip()]


def requirement_tokens(requirement):
    return {
        token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]*", requirement.lower())
        if len(token) > 1 and token not in SCREENING_STOP_WORDS
    }


def matches_requirement(resume_text, requirement):
    resume_terms = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]*", resume_text.lower()))
    tokens = requirement_tokens(requirement)
    if not tokens:
        return False
    return len(tokens.intersection(resume_terms)) / len(tokens) >= 0.7


def evaluate_candidate(file, primary, secondary):
    try:
        resume_text = extract_resume_text(file)
    except Exception:
        resume_text = ""
    matched_primary = [item for item in primary if matches_requirement(resume_text, item)]
    matched_secondary = [item for item in secondary if matches_requirement(resume_text, item)]
    missing_primary = [item for item in primary if item not in matched_primary]
    missing_secondary = [item for item in secondary if item not in matched_secondary]
    primary_score = round(100 * len(matched_primary) / len(primary), 1) if primary else 0.0
    secondary_score = round(100 * len(matched_secondary) / len(secondary), 1) if secondary else 0.0
    weighted_score = round(primary_score * 0.8 + secondary_score * 0.2, 1) if secondary else primary_score
    considered = primary_score >= PRIMARY_COVERAGE_THRESHOLD
    return {
        "Candidate": os.path.splitext(file.name)[0],
        "Primary coverage": primary_score,
        "Secondary coverage": secondary_score,
        "Overall fit": weighted_score,
        "Recommendation": "Consider" if considered else "Review later",
        "Matched primary": matched_primary,
        "Missing primary": missing_primary,
        "Matched secondary": matched_secondary,
        "Missing secondary": missing_secondary,
    }


def chips(items, secondary=False):
    css_class = "requirement-chip secondary-chip" if secondary else "requirement-chip"
    return "".join(f'<span class="{css_class}">{html.escape(item)}</span>' for item in items) or "<span class='missing-skill'>None listed</span>"


def initialise_state():
    if "role_library" not in st.session_state:
        st.session_state.role_library = {key: value.copy() for key, value in DEFAULT_ROLE_LIBRARY.items()}
    # Upgrade saved state created by earlier versions of the app.
    for name, role in list(st.session_state.role_library.items()):
        if isinstance(role, str):
            st.session_state.role_library[name] = {"description": role, "primary": [], "secondary": []}
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = next(iter(st.session_state.role_library))
    selected = st.session_state.role_library[st.session_state.selected_role]
    st.session_state.setdefault("jd_description", selected["description"])
    st.session_state.setdefault("primary_requirements", "\n".join(selected["primary"]))
    st.session_state.setdefault("secondary_requirements", "\n".join(selected["secondary"]))


def load_selected_role():
    selected_name = st.session_state.role_picker
    st.session_state.selected_role = selected_name
    selected = st.session_state.role_library[selected_name]
    st.session_state.jd_description = selected["description"]
    st.session_state.primary_requirements = "\n".join(selected["primary"])
    st.session_state.secondary_requirements = "\n".join(selected["secondary"])


def save_role_requirements():
    st.session_state.role_library[st.session_state.selected_role] = {
        "description": st.session_state.jd_description.strip(),
        "primary": requirement_items(st.session_state.primary_requirements),
        "secondary": requirement_items(st.session_state.secondary_requirements),
    }


@st.dialog("Manage role library")
def manage_role_dialog():
    st.write("Add a role with separate mandatory and preferred requirements, or remove a role from this browser session.")
    st.markdown("#### Add a new role")
    name = st.text_input("Role name", placeholder="e.g. Sales Manager")
    description = st.text_area("Role overview", height=90, placeholder="Describe the opening and core responsibilities.")
    primary = st.text_area("Mandatory requirements", height=100, placeholder="One requirement per line, e.g.\nSalesforce\nB2B sales\nPipeline management")
    secondary = st.text_area("Preferred requirements", height=90, placeholder="One requirement per line, e.g.\nSaaS\nEnterprise sales")
    if st.button("Add role to library", type="primary", use_container_width=True):
        name = name.strip()
        if not name:
            st.warning("Enter a role name first.")
        elif not requirement_items(primary):
            st.warning("Add at least one mandatory requirement.")
        elif name in st.session_state.role_library:
            st.warning("That role already exists.")
        else:
            st.session_state.role_library[name] = {
                "description": description.strip(),
                "primary": requirement_items(primary),
                "secondary": requirement_items(secondary),
            }
            st.session_state.selected_role = name
            st.session_state.jd_description = description.strip()
            st.session_state.primary_requirements = "\n".join(requirement_items(primary))
            st.session_state.secondary_requirements = "\n".join(requirement_items(secondary))
            st.rerun()
    st.divider()
    remove_role = st.selectbox("Role to remove", sorted(st.session_state.role_library))
    if st.button("Remove selected role", use_container_width=True):
        if len(st.session_state.role_library) == 1:
            st.warning("Keep at least one role in the library.")
        else:
            del st.session_state.role_library[remove_role]
            if st.session_state.selected_role == remove_role:
                load_name = sorted(st.session_state.role_library)[0]
                st.session_state.selected_role = load_name
                selected = st.session_state.role_library[load_name]
                st.session_state.jd_description = selected["description"]
                st.session_state.primary_requirements = "\n".join(selected["primary"])
                st.session_state.secondary_requirements = "\n".join(selected["secondary"])
            st.rerun()


initialise_state()

st.markdown("""
<section class="hero"><span class="eyebrow">Candidate screening toolkit</span>
<h1>Screen the candidates who meet the essentials.</h1>
<p>Separate non-negotiable requirements from preferred strengths, then review many resumes in one focused shortlist.</p></section>
<p class="section-label">Step 1 · Define the role</p>
""", unsafe_allow_html=True)
st.markdown("""
<section class="role-intro"><span class="role-kicker">✦ Smart role library</span>
<h2>Define what matters before reviewing candidates.</h2>
<p>Primary requirements drive the screening decision. Secondary requirements show added value without rejecting a strong candidate.</p></section>
""", unsafe_allow_html=True)

select_col, manage_col = st.columns([2, 1], gap="large")
role_options = sorted(st.session_state.role_library)
with select_col:
    st.selectbox("Search or select a role", role_options, index=role_options.index(st.session_state.selected_role), key="role_picker", on_change=load_selected_role)
with manage_col:
    if st.button("＋ Manage role library", use_container_width=True):
        manage_role_dialog()

st.markdown("<br><p class='section-label'>Step 2 · Set requirements and upload candidates</p>", unsafe_allow_html=True)
requirements_col, upload_col = st.columns([1.45, 1], gap="large")
with requirements_col:
    st.markdown("## 💼 Role requirements")
    st.text_area("Role overview", height=100, key="jd_description", placeholder="Describe responsibilities and context for this opening.")
    primary_col, secondary_col = st.columns(2, gap="medium")
    with primary_col:
        st.markdown("<div class='requirements-panel primary-panel'><h3>Primary requirements</h3><p>Mandatory. Candidates are evaluated mainly on this list.</p></div>", unsafe_allow_html=True)
        st.text_area("Mandatory requirements - one per line", height=185, key="primary_requirements", placeholder="Python\nSQL\nMachine learning")
    with secondary_col:
        st.markdown("<div class='requirements-panel secondary-panel'><h3>Secondary requirements</h3><p>Preferred. These strengthen a profile but do not reject it.</p></div>", unsafe_allow_html=True)
        st.text_area("Preferred requirements - one per line", height=185, key="secondary_requirements", placeholder="AWS\nDocker\nForecasting")
    save_col, reset_col = st.columns(2)
    with save_col:
        if st.button("Save role requirements", use_container_width=True):
            if not requirement_items(st.session_state.primary_requirements):
                st.warning("Add at least one primary requirement.")
            else:
                save_role_requirements()
                st.success("Role requirements saved.")
    with reset_col:
        if st.button("Reset saved role", use_container_width=True):
            load_selected_role()
            st.rerun()

with upload_col:
    st.markdown("## 📄 Candidate resumes")
    st.caption("Upload PDF or TXT resumes together. Each candidate is evaluated independently.")
    resume_files = st.file_uploader(
        "Upload one or more resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload all resumes for this role at once.",
    )
    if resume_files:
        st.info(f"{len(resume_files)} resume{'s' if len(resume_files) != 1 else ''} ready for screening.")

st.markdown("<br>", unsafe_allow_html=True)
_, action_col, _ = st.columns([1, 1.25, 1])
with action_col:
    analyze_clicked = st.button("✨ Analyze candidate batch", use_container_width=True, type="primary")

if analyze_clicked:
    primary = requirement_items(st.session_state.primary_requirements)
    secondary = requirement_items(st.session_state.secondary_requirements)
    if not resume_files:
        st.error("Upload at least one resume to begin screening.")
    elif not primary:
        st.error("Add at least one primary requirement before screening candidates.")
    else:
        with st.spinner("Checking each candidate against the primary and secondary requirements..."):
            results = [evaluate_candidate(file, primary, secondary) for file in resume_files]
        st.markdown("<br><p class='section-label'>Step 3 · Shortlist results</p>", unsafe_allow_html=True)
        considered_count = sum(item["Recommendation"] == "Consider" for item in results)
        primary_avg = round(sum(item["Primary coverage"] for item in results) / len(results), 1)
        metric_one, metric_two, metric_three = st.columns(3)
        metric_one.metric("Candidates screened", len(results))
        metric_two.metric("Recommended for review", considered_count)
        metric_three.metric("Average primary coverage", f"{primary_avg}%")

        st.markdown("<div class='metrics-strip'><strong>Decision rule:</strong> candidates are recommended when they meet at least "
                    f"<strong>{PRIMARY_COVERAGE_THRESHOLD}%</strong> of the mandatory requirements. Secondary requirements improve the overall fit score but do not cause rejection.</div>", unsafe_allow_html=True)

        table = pd.DataFrame([
            {
                "Candidate": item["Candidate"],
                "Primary coverage": f'{item["Primary coverage"]}%',
                "Secondary coverage": f'{item["Secondary coverage"]}%',
                "Overall fit": f'{item["Overall fit"]}%',
                "Recommendation": item["Recommendation"],
                "Missing primary requirements": ", ".join(item["Missing primary"]) or "None",
            }
            for item in results
        ]).sort_values(["Recommendation", "Overall fit"], ascending=[True, False])
        st.markdown("### Candidate comparison")
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.download_button("Download shortlist as CSV", table.to_csv(index=False).encode("utf-8"), "candidate_shortlist.csv", "text/csv")

        st.markdown("### Candidate summaries")
        for item in sorted(results, key=lambda result: (result["Recommendation"] != "Consider", -result["Overall fit"])):
            with st.expander(f'{item["Candidate"]} - {item["Recommendation"]} ({item["Primary coverage"]}% mandatory coverage)'):
                left, right = st.columns(2)
                with left:
                    decision_class = "decision-yes" if item["Recommendation"] == "Consider" else "decision-no"
                    st.markdown(f"<span class='decision {decision_class}'>{html.escape(item['Recommendation'].upper())}</span>", unsafe_allow_html=True)
                    st.markdown("#### Mandatory requirements")
                    st.caption("Matched")
                    st.markdown(chips(item["Matched primary"]), unsafe_allow_html=True)
                    st.caption("Missing")
                    st.markdown(chips(item["Missing primary"]), unsafe_allow_html=True)
                with right:
                    st.markdown("#### Preferred strengths")
                    st.caption("Matched")
                    st.markdown(chips(item["Matched secondary"], secondary=True), unsafe_allow_html=True)
                    st.caption("Not shown in resume")
                    st.markdown(chips(item["Missing secondary"], secondary=True), unsafe_allow_html=True)
                    if item["Recommendation"] == "Consider":
                        st.success("Worth giving a try. Use the interview to confirm the depth of the matched mandatory skills.")
                    else:
                        st.warning("Hold for now. The resume is missing too many mandatory requirements for this role.")
