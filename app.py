import html
import os
import re

import pandas as pd
import PyPDF2
import streamlit as st
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


st.set_page_config(
    page_title="Resume Matcher | AI Candidate Screening",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

:root {
    --ink: #111827;
    --muted: #4b5563;
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --success: #059669;
    --warning: #d97706;
    --danger: #dc2626;
    --surface: #ffffff;
    --border: #e5e7eb;
}

.stApp {
    background: radial-gradient(circle at 10% 5%, #eef2ff 0%, transparent 30%),
                radial-gradient(circle at 90% 10%, #fdf4ff 0%, transparent 35%),
                #f9fafb;
    color: var(--ink);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.75rem;
    padding-bottom: 3.5rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    color: var(--ink);
    font-weight: 700;
}

/* Hero Section */
.hero-card {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2.6rem;
    margin-bottom: 2rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #4338ca 0%, #6366f1 55%, #8b5cf6 100%);
    color: #ffffff;
    box-shadow: 0 16px 36px rgba(79, 70, 229, 0.22);
}

.hero-card::after {
    content: '';
    position: absolute;
    width: 240px;
    height: 240px;
    right: -50px;
    top: -80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #ffffff;
}

.hero-title {
    font-size: clamp(2rem, 3.5vw, 2.85rem);
    font-weight: 800;
    line-height: 1.2;
    margin: 0.65rem 0 0.45rem;
    color: #ffffff;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.55;
    color: #e0e7ff;
    max-width: 720px;
    margin: 0;
}

/* Section Header Badges */
.step-badge {
    display: inline-block;
    padding: 0.28rem 0.75rem;
    border-radius: 999px;
    background: #e0e7ff;
    color: #4338ca;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

/* Requirements & Decision Chips */
.chip {
    display: inline-block;
    padding: 0.34rem 0.75rem;
    margin: 0.2rem 0.25rem 0.2rem 0;
    border-radius: 8px;
    font-size: 0.84rem;
    font-weight: 600;
    line-height: 1.4;
}

.chip-primary-matched {
    background: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.chip-primary-missing {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.chip-secondary-matched {
    background: #f0fdfa;
    color: #115e59;
    border: 1px solid #99f6e4;
}

.chip-secondary-missing {
    background: #f8fafc;
    color: #64748b;
    border: 1px solid #e2e8f0;
}

.chip-empty {
    background: #f3f4f6;
    color: #6b7280;
    font-style: italic;
}

/* Decision Status Pills */
.decision-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.4rem 0.95rem;
    border-radius: 999px;
    font-size: 0.86rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

.decision-consider {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}

.decision-review {
    background: #fef3c7;
    color: #b45309;
    border: 1px solid #fde68a;
}

.decision-error {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

/* Banner for screening policy */
.policy-banner {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem 0 1.5rem;
    font-size: 0.92rem;
    color: #334155;
    line-height: 1.5;
}

/* Compact candidate tiles */
.candidate-score-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 0.85rem;
}

.candidate-card-name {
    min-height: 4.25rem;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    color: #0f2a5f;
    font-family: 'Outfit', sans-serif;
    font-size: 1.32rem;
    font-weight: 700;
    line-height: 1.35;
    margin: 0.85rem 0 0.5rem;
}

.candidate-score-label {
    color: #64748b;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.candidate-score-value {
    color: #172554;
    font-family: 'Outfit', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 0.15rem;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-marker) {
    min-height: 250px;
    border-width: 1px;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.08);
    transition: transform 180ms ease, box-shadow 180ms ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-marker):hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 30px rgba(79, 70, 229, 0.15);
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-consider) {
    background: linear-gradient(145deg, #f0fdf4, #ffffff 68%);
    border-color: #86efac;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-review) {
    background: linear-gradient(145deg, #fffbeb, #ffffff 68%);
    border-color: #fde68a;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-error) {
    background: linear-gradient(145deg, #fff1f2, #ffffff 68%);
    border-color: #fecdd3;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-marker) div[data-testid="stButton"] > button {
    min-height: 2.75rem;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border: none;
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 7px 14px rgba(79, 70, 229, 0.2);
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-card-marker) div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9);
    color: #ffffff;
}

/* Subtle styling polish */
div[data-testid="stFileUploader"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
}
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
        "description": "Build reliable, scalable product features. Design backend or frontend services, write maintainable code, participate in code reviews, and collaborate with product and design teams.",
        "primary": ["Python or Java", "SQL", "REST APIs", "Git", "Software testing"],
        "secondary": ["React", "Docker", "AWS", "Kubernetes", "Microservices"],
    },
    "Data Analyst": {
        "description": "Turn business data into clear recommendations. Query and clean data, build dashboards, define key metrics, and communicate actionable insights to stakeholders.",
        "primary": ["SQL", "Excel", "Data visualization", "Data cleaning", "Business analysis"],
        "secondary": ["Python", "Power BI", "Tableau", "Statistics", "A/B testing"],
    },
    "Data Scientist": {
        "description": "Develop data products and predictive models. Explore datasets, build and evaluate machine learning models, design experiments, and present findings to business leaders.",
        "primary": ["Python", "SQL", "Statistics", "Machine learning", "Data cleaning"],
        "secondary": ["Scikit-learn", "Pandas", "Experimentation", "Forecasting", "Cloud data platforms"],
    },
    "Product Manager": {
        "description": "Define product strategy and ship customer-focused improvements. Gather customer needs, prioritize roadmaps, write detailed requirements, track metrics, and align teams.",
        "primary": ["Product discovery", "Roadmap planning", "Stakeholder management", "User research", "Product analytics"],
        "secondary": ["B2B SaaS", "Experimentation", "Jira", "Agile", "Product metrics"],
    },
    "Project Manager": {
        "description": "Plan, coordinate, and deliver cross-functional initiatives. Manage scope, schedules, risks, budgets, dependencies, and cross-team stakeholder communication.",
        "primary": ["Project planning", "Risk management", "Stakeholder management", "Reporting", "Agile delivery"],
        "secondary": ["PMP", "Scrum", "Jira", "Confluence", "Technical projects"],
    },
    "UX UI Designer": {
        "description": "Create intuitive, accessible digital experiences. Conduct user research, map journeys, design wireframes and interactive prototypes, and partner with product and engineering.",
        "primary": ["Figma", "Interaction design", "Visual design", "Prototyping", "Usability testing"],
        "secondary": ["Accessibility", "Design systems", "Responsive web design", "B2B products"],
    },
    "DevOps Engineer": {
        "description": "Improve delivery reliability, security, and observability. Build automated CI/CD pipelines, manage cloud infrastructure, automate deployments, and support incident response.",
        "primary": ["CI CD", "Docker", "Kubernetes", "Cloud infrastructure", "Linux"],
        "secondary": ["AWS", "Terraform", "Python", "Monitoring", "SRE"],
    },
    "Cybersecurity Analyst": {
        "description": "Protect systems, infrastructure, and user data. Monitor security alerts, investigate incidents, manage vulnerabilities, document findings, and strengthen security controls.",
        "primary": ["SIEM", "Incident response", "Vulnerability management", "Network security", "Risk assessment"],
        "secondary": ["Splunk", "Microsoft Sentinel", "SOC operations", "Cloud security", "Security certifications"],
    },
    "Digital Marketing Specialist": {
        "description": "Plan and optimize multi-channel acquisition campaigns, analyze marketing performance, create content briefs, and improve conversion funnels.",
        "primary": ["Google Analytics", "SEO", "SEM", "Campaign reporting", "Copywriting"],
        "secondary": ["Google Ads", "HubSpot", "Email marketing", "CRM", "A B testing"],
    },
    "HR Recruiter": {
        "description": "Attract, assess, and hire top talent. Partner with hiring managers, source candidates, conduct structured screening interviews, coordinate hiring pipelines, and ensure an excellent candidate experience.",
        "primary": ["Talent sourcing", "Interview coordination", "ATS management", "Candidate assessment", "Recruiting metrics"],
        "secondary": ["LinkedIn Recruiter", "Employer branding", "Technical recruiting", "HRIS"],
    },
    "Financial Analyst": {
        "description": "Support corporate financial planning and strategic business decisions. Prepare forecasts, analyze financial performance, build valuation models, and partner with operational leaders.",
        "primary": ["Financial modeling", "Budgeting", "Forecasting", "Excel", "Variance analysis"],
        "secondary": ["SQL", "Power BI", "ERP systems", "FP and A", "Accounting"],
    },
    "Customer Success Manager": {
        "description": "Ensure enterprise customers achieve measurable business value. Onboard new accounts, build lasting stakeholder relationships, mitigate churn risk, and drive product adoption.",
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
    extraction_error = None
    try:
        resume_text = extract_resume_text(file)
    except Exception:
        resume_text = ""
        extraction_error = "The file could not be read. Upload a text-based PDF or TXT file and try again."
    matched_primary = [item for item in primary if matches_requirement(resume_text, item)]
    matched_secondary = [item for item in secondary if matches_requirement(resume_text, item)]
    missing_primary = [item for item in primary if item not in matched_primary]
    missing_secondary = [item for item in secondary if item not in matched_secondary]
    primary_score = round(100 * len(matched_primary) / len(primary), 1) if primary else 0.0
    secondary_score = round(100 * len(matched_secondary) / len(secondary), 1) if secondary else 0.0
    weighted_score = round(primary_score * 0.8 + secondary_score * 0.2, 1) if secondary else primary_score
    considered = primary_score >= PRIMARY_COVERAGE_THRESHOLD and not extraction_error
    return {
        "Candidate": os.path.splitext(file.name)[0],
        "Primary coverage": primary_score,
        "Secondary coverage": secondary_score,
        "Overall fit": weighted_score,
        "Recommendation": "Unable to read" if extraction_error else ("Consider" if considered else "Review later"),
        "Processing status": "Needs a readable file" if extraction_error else "Ready for review",
        "Matched primary": matched_primary,
        "Missing primary": missing_primary,
        "Matched secondary": matched_secondary,
        "Missing secondary": missing_secondary,
    }


def render_chips(items, style="primary-matched"):
    if not items:
        return "<span class='chip chip-empty'>None identified</span>"
    css_class = f"chip chip-{style}"
    return "".join(f'<span class="{css_class}">{html.escape(item)}</span>' for item in items)


def candidate_card_label(candidate_name, max_length=34):
    """Create a readable, compact label for a filename-derived candidate name."""
    label = re.sub(r"[_-]+", " ", candidate_name).strip()
    return f"{label[:max_length - 1].rstrip()}…" if len(label) > max_length else label


def initialise_state():
    if "role_library" not in st.session_state:
        st.session_state.role_library = {key: value.copy() for key, value in DEFAULT_ROLE_LIBRARY.items()}
    for name, role in list(st.session_state.role_library.items()):
        if isinstance(role, str):
            st.session_state.role_library[name] = {"description": role, "primary": [], "secondary": []}
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = next(iter(st.session_state.role_library))
    selected = st.session_state.role_library[st.session_state.selected_role]
    st.session_state.setdefault("jd_description", selected["description"])
    st.session_state.setdefault("primary_requirements", "\n".join(selected["primary"]))
    st.session_state.setdefault("secondary_requirements", "\n".join(selected["secondary"]))
    if "screening_results" not in st.session_state:
        st.session_state.screening_results = None
    if "screening_signature" not in st.session_state:
        st.session_state.screening_signature = None


def load_selected_role():
    selected_name = st.session_state.role_picker
    st.session_state.selected_role = selected_name
    selected = st.session_state.role_library[selected_name]
    st.session_state.jd_description = selected["description"]
    st.session_state.primary_requirements = "\n".join(selected["primary"])
    st.session_state.secondary_requirements = "\n".join(selected["secondary"])
    st.session_state.screening_results = None
    st.session_state.screening_signature = None


def reset_selected_role():
    """Restore the active role values before its widgets are created."""
    selected = st.session_state.role_library[st.session_state.selected_role]
    st.session_state.jd_description = selected["description"]
    st.session_state.primary_requirements = "\n".join(selected["primary"])
    st.session_state.secondary_requirements = "\n".join(selected["secondary"])
    st.session_state.screening_results = None
    st.session_state.screening_signature = None


def save_role_requirements():
    st.session_state.role_library[st.session_state.selected_role] = {
        "description": st.session_state.jd_description.strip(),
        "primary": requirement_items(st.session_state.primary_requirements),
        "secondary": requirement_items(st.session_state.secondary_requirements),
    }
    st.session_state.screening_results = None
    st.session_state.screening_signature = None


@st.dialog("Manage Role Library")
def manage_role_dialog():
    st.caption("Add custom roles with structured mandatory and preferred requirements, or remove unneeded profiles.")

    st.subheader("Add new role")
    name = st.text_input("Role title", placeholder="e.g. Sales Manager")
    description = st.text_area("Role overview", height=80, placeholder="Briefly describe the responsibilities and scope of this role.")
    primary = st.text_area("Mandatory Requirements (One Per Line)", height=95, placeholder="Salesforce\nB2B Sales\nPipeline Management")
    secondary = st.text_area("Preferred Requirements (One Per Line)", height=85, placeholder="SaaS Experience\nEnterprise Deal Closing")

    if st.button("Add role to library", type="primary", width="stretch"):
        name = name.strip()
        if not name:
            st.warning("Please enter a role title.")
        elif not requirement_items(primary):
            st.warning("Please specify at least one mandatory requirement.")
        elif name in st.session_state.role_library:
            st.warning("A role with this title already exists.")
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
    st.subheader("Remove role")
    remove_role = st.selectbox("Select role to remove", sorted(st.session_state.role_library))
    if st.button("Delete selected role", width="stretch"):
        if len(st.session_state.role_library) <= 1:
            st.warning("At least one role must remain in the library.")
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


@st.dialog("Candidate report")
def candidate_report_dialog(candidate):
    """Show the full evidence only when a recruiter opens a candidate card."""
    is_recommended = candidate["Recommendation"] == "Consider"
    unreadable = candidate["Recommendation"] == "Unable to read"
    status_icon = "🟢" if is_recommended else ("🔴" if unreadable else "🟠")
    badge_class = (
        "decision-consider"
        if is_recommended
        else ("decision-error" if unreadable else "decision-review")
    )

    st.markdown(f"## {status_icon} {candidate['Candidate']}")
    st.caption("Candidate report · requirement evidence and recommendation")
    st.markdown(
        f"<div class='decision-badge {badge_class}'>● {candidate['Recommendation'].upper()}</div>",
        unsafe_allow_html=True,
    )

    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Mandatory match", f"{candidate['Primary coverage']}%")
    metric_b.metric("Preferred match", f"{candidate['Secondary coverage']}%")
    metric_c.metric("Overall fit", f"{candidate['Overall fit']}%")

    st.divider()
    mandatory_col, preferred_col = st.columns(2, gap="large")
    with mandatory_col:
        st.markdown("#### Mandatory Requirements")
        st.caption("Matched core requirements")
        st.markdown(render_chips(candidate["Matched primary"], style="primary-matched"), unsafe_allow_html=True)
        st.caption("Missing core requirements")
        st.markdown(render_chips(candidate["Missing primary"], style="primary-missing"), unsafe_allow_html=True)
    with preferred_col:
        st.markdown("#### Preferred Strengths")
        st.caption("Matched bonus skills")
        st.markdown(render_chips(candidate["Matched secondary"], style="secondary-matched"), unsafe_allow_html=True)
        st.caption("Unmatched bonus skills")
        st.markdown(render_chips(candidate["Missing secondary"], style="secondary-missing"), unsafe_allow_html=True)

    st.markdown("#### Recruiter recommendation")
    if unreadable:
        st.error(
            "This file could not be read. Upload a text-based PDF or TXT version before evaluating this candidate.",
            icon=":material/error:",
        )
    elif is_recommended:
        st.success(
            "Candidate satisfies the core threshold. Advance to a preliminary interview and verify the practical depth of matched competencies.",
            icon=":material/thumb_up:",
        )
    else:
        st.warning(
            "Candidate falls below the mandatory coverage threshold. Keep on file for suitable openings or review their portfolio for evidence expressed differently.",
            icon=":material/pending_actions:",
        )


initialise_state()

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-pill">🎯 Smart Hiring Engine</div>
    <div class="hero-title">AI-Powered Talent Evaluation</div>
    <p class="hero-subtitle">
        Screen and rank applicant batches against mandatory qualifications and preferred strengths.
        Identify candidates who meet the essentials and make skill gaps clear at a glance.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# STEP 1: ROLE SELECTION
# ---------------------------------------------------------
st.markdown("<span class='step-badge'>Step 1 · Role Configuration</span>", unsafe_allow_html=True)

with st.container(border=True):
    header_col, action_col = st.columns([3, 1], vertical_alignment="center")
    with header_col:
        st.subheader("Select Target Role", anchor=False)
        st.caption("Pick a predefined position from the library or manage custom role templates.")
    with action_col:
        if st.button(":material/settings: Manage role library", width="stretch"):
            manage_role_dialog()

    role_options = sorted(st.session_state.role_library)
    selected_idx = role_options.index(st.session_state.selected_role) if st.session_state.selected_role in role_options else 0
    st.selectbox(
        "Active job role",
        role_options,
        index=selected_idx,
        key="role_picker",
        on_change=load_selected_role,
        label_visibility="collapsed",
    )


# ---------------------------------------------------------
# STEP 2 & STEP 3: REQUIREMENTS & RESUME UPLOAD
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
req_col, upload_col = st.columns([1.35, 1], gap="large")

with req_col:
    st.markdown("<span class='step-badge'>Step 2 · Criteria Setup</span>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Screening Criteria", anchor=False)
        st.caption("Specify non-negotiable core requirements and bonus attributes.")

        st.text_area(
            "Role overview & responsibilities",
            height=150,
            key="jd_description",
            placeholder="Context, daily responsibilities, and team mission.",
        )

        p_col, s_col = st.columns(2, gap="medium")
        with p_col:
            st.markdown("##### 📌 Mandatory Requirements")
            st.caption("Non-negotiable. Determines 80% of fit score.")
            st.text_area(
                "Mandatory skills (one per line)",
                height=170,
                key="primary_requirements",
                placeholder="Python\nSQL\nREST APIs",
                label_visibility="collapsed",
            )
        with s_col:
            st.markdown("##### 🌟 Preferred Strengths")
            st.caption("Bonus assets. Enhances profile (20% of fit score).")
            st.text_area(
                "Preferred skills (one per line)",
                height=170,
                key="secondary_requirements",
                placeholder="Docker\nAWS\nCI/CD",
                label_visibility="collapsed",
            )

        btn_save, btn_reset = st.columns(2)
        with btn_save:
            if st.button(":material/save: Save criteria", width="stretch", type="secondary"):
                if not requirement_items(st.session_state.primary_requirements):
                    st.warning("Please specify at least one mandatory requirement.")
                else:
                    save_role_requirements()
                    st.success("Criteria saved to active role.")
        with btn_reset:
            st.button(
                ":material/refresh: Revert to default",
                width="stretch",
                on_click=reset_selected_role,
            )

with upload_col:
    st.markdown("<span class='step-badge'>Step 3 · Candidate Input</span>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Candidate Resumes", anchor=False)
        st.caption("Upload multiple PDF or TXT resumes for concurrent evaluation.")

        resume_files = st.file_uploader(
            "Upload candidate resumes (PDF or TXT)",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            help="Select one or multiple candidate files to screen in batch.",
            label_visibility="collapsed",
        )

        if resume_files:
            st.success(f":material/check_circle: {len(resume_files)} candidate resume{'s' if len(resume_files) != 1 else ''} loaded and ready.")
        else:
            st.info(":material/info: Drag & drop PDF or TXT resumes above to start screening.")

current_screening_signature = (
    st.session_state.selected_role,
    st.session_state.jd_description,
    st.session_state.primary_requirements,
    st.session_state.secondary_requirements,
    tuple((file.name, file.size) for file in (resume_files or [])),
)


# ---------------------------------------------------------
# STEP 4: RUN SCREENING
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
_, action_center_col, _ = st.columns([1, 1.4, 1])
with action_center_col:
    st.markdown("<div class='step-badge'>Step 4 · Run screening</div>", unsafe_allow_html=True)
    screen_clicked = st.button(
        ":material/manage_search: Screen & Rank Candidates",
        type="primary",
        width="stretch",
    )

if screen_clicked:
    primary = requirement_items(st.session_state.primary_requirements)
    secondary = requirement_items(st.session_state.secondary_requirements)
    if not resume_files:
        st.error("Please upload at least one candidate resume before analyzing.")
    elif not primary:
        st.error("Please provide at least one mandatory requirement before analyzing.")
    else:
        with st.spinner("Extracting resumes and matching qualification patterns..."):
            st.session_state.screening_results = [
                evaluate_candidate(file, primary, secondary) for file in resume_files
            ]
            st.session_state.screening_signature = current_screening_signature


# ---------------------------------------------------------
# STEP 5: RESULTS & DASHBOARD
# ---------------------------------------------------------
if (
    st.session_state.screening_results
    and st.session_state.screening_signature == current_screening_signature
):
    results = st.session_state.screening_results
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<span class='step-badge'>Step 5 · Candidate insights</span>", unsafe_allow_html=True)

    with st.container(border=True):
        head_l, head_r = st.columns([3, 1], vertical_alignment="center")
        with head_l:
            st.subheader("Screening Overview", anchor=False)
            st.caption(f"Analysis completed for role: **{st.session_state.selected_role}**")
        with head_r:
            if st.button(":material/clear_all: Clear results", width="stretch"):
                st.session_state.screening_results = None
                st.session_state.screening_signature = None
                st.rerun()

        # Key Metrics
        total_candidates = len(results)
        considered_count = sum(item["Recommendation"] == "Consider" for item in results)
        avg_primary = round(sum(item["Primary coverage"] for item in results) / total_candidates, 1)
        top_fit = max(item["Overall fit"] for item in results)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Screened applicants", total_candidates)
        m2.metric("Recommended for review", considered_count, delta=f"{round(100*considered_count/total_candidates)}% shortlist rate" if total_candidates else None)
        m3.metric("Avg mandatory match", f"{avg_primary}%")
        m4.metric("Top overall fit", f"{top_fit}%")

        st.markdown(f"""
        <div class="policy-banner">
            <strong>Decision Rule & Threshold:</strong> Candidates are recommended (<em>"Consider"</em>) when meeting at least
            <strong>{PRIMARY_COVERAGE_THRESHOLD}%</strong> of mandatory requirements.
            Preferred strengths boost the overall fit score (80% mandatory weight / 20% preferred weight) without penalizing eligible candidates.
        </div>
        """, unsafe_allow_html=True)

        # Tabular Comparison
        table_data = [
            {
                "Candidate": item["Candidate"],
                "Recommendation": item["Recommendation"],
                "Mandatory match": f'{item["Primary coverage"]}%',
                "Preferred match": f'{item["Secondary coverage"]}%',
                "Overall fit": f'{item["Overall fit"]}%',
                "Missing mandatory skills": ", ".join(item["Missing primary"]) or "None (Full Match)",
            }
            for item in results
        ]
        df_display = pd.DataFrame(table_data).sort_values(
            ["Recommendation", "Overall fit"],
            ascending=[True, False],
        )

        st.markdown("#### Candidate Ranking")
        st.caption("Compare the complete batch, then open each candidate report for requirement-level detail.")
        st.dataframe(
            df_display,
            width="stretch",
            hide_index=True,
            column_config={
                "Candidate": st.column_config.TextColumn("Candidate Name", help="Name extracted from file"),
                "Recommendation": st.column_config.TextColumn("Recommendation", help="Threshold outcome"),
                "Mandatory match": st.column_config.TextColumn("Mandatory Match", help="Coverage of core criteria"),
                "Preferred match": st.column_config.TextColumn("Preferred Match", help="Coverage of bonus strengths"),
                "Overall fit": st.column_config.TextColumn("Overall Fit Score", help="Weighted total evaluation"),
                "Missing mandatory skills": st.column_config.TextColumn("Skill Gaps", help="Unmatched mandatory requirements"),
            },
        )

        st.download_button(
            label=":material/download: Export shortlist to CSV",
            data=df_display.to_csv(index=False).encode("utf-8"),
            file_name=f"shortlist_{st.session_state.selected_role.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

        # Candidate Breakdown
        st.divider()
        st.markdown("#### Candidate Reports")
        st.caption("Select a candidate card to open the complete requirement evidence and recruiter recommendation.")

        recommendation_order = {"Consider": 0, "Review later": 1, "Unable to read": 2}
        sorted_results = sorted(
            results,
            key=lambda x: (recommendation_order[x["Recommendation"]], -x["Overall fit"]),
        )

        report_columns = st.columns(3, gap="medium")
        for index, candidate in enumerate(sorted_results):
            is_rec = candidate["Recommendation"] == "Consider"
            unreadable = candidate["Recommendation"] == "Unable to read"
            rec_badge_class = (
                "decision-consider" if is_rec else ("decision-error" if unreadable else "decision-review")
            )
            card_state = "error" if unreadable else ("consider" if is_rec else "review")
            card_label = candidate_card_label(candidate["Candidate"])

            with report_columns[index % 3]:
                with st.container(border=True):
                    st.markdown(f"<span class='candidate-card-marker candidate-card-{card_state}'></span>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='decision-badge {rec_badge_class}'>● {candidate['Recommendation'].upper()}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<div class='candidate-card-name'>{html.escape(card_label)}</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        ":material/description: View full report",
                        key=f"candidate_report_{index}",
                        width="stretch",
                        type="secondary",
                    ):
                        candidate_report_dialog(candidate)
                    st.caption("Mandatory qualifications are the decision driver.")

                    st.markdown(
                        f"""
                        <div class="candidate-score-grid">
                            <div>
                                <div class="candidate-score-label">Overall fit</div>
                                <div class="candidate-score-value">{candidate['Overall fit']}%</div>
                            </div>
                            <div>
                                <div class="candidate-score-label">Mandatory</div>
                                <div class="candidate-score-value">{candidate['Primary coverage']}%</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
