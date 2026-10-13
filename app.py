import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

# Configure the page
st.set_page_config(page_title="Resume Matcher", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');
:root { --ink: #18233f; --muted: #63708b; --violet: #7049e8; }
.stApp { background: radial-gradient(circle at 8% 6%, #d9f8ff 0, transparent 23%), radial-gradient(circle at 90% 0%, #f8d9ff 0, transparent 28%), linear-gradient(145deg, #f7f6ff 0%, #fdfaff 48%, #effcff 100%); color: var(--ink); font-family: 'DM Sans', sans-serif; }
/* Override Streamlit's dark-theme variables inside components that otherwise
   keep their default dark surfaces (uploaded file rows and dialogs). */
.stApp, div[data-testid="stFileUploader"], div[data-testid="stDialog"], div[role="dialog"] {
    --background-color: #ffffff; --secondary-background-color: #f3efff;
    --text-color: #18233f; --primary-color: #7049e8;
    --gray-900: #f1edff; --gray-800: #e8e1ff; --gray-700: #d9ceff;
    --gray-600: #b8a7ee; --gray-500: #7c69aa; --gray-300: #53617a;
}
.block-container { max-width: 1180px; padding-top: 2.5rem; padding-bottom: 3rem; }
#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; color: var(--ink); }
.hero { position: relative; overflow: hidden; padding: 2.45rem 2.7rem; margin: 0 0 2rem; border-radius: 28px; background: linear-gradient(115deg, #4930ad 0%, #7648e8 52%, #c052d6 100%); color: white; box-shadow: 0 20px 45px rgba(83, 48, 173, .27); }
.hero:after { content: ''; position: absolute; width: 250px; height: 250px; right: -70px; top: -110px; border-radius: 50%; background: rgba(255,255,255,.13); }
.hero:before { content: ''; position: absolute; width: 140px; height: 140px; right: 150px; bottom: -80px; border-radius: 50%; background: rgba(0,219,235,.27); }
.eyebrow { position: relative; z-index: 1; display: inline-block; padding: .35rem .7rem; border-radius: 999px; background: rgba(255,255,255,.18); font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.hero h1 { position: relative; z-index: 1; color: white; font-size: clamp(2rem, 4vw, 3.25rem); margin: .55rem 0 .45rem; letter-spacing: -.04em; }
.hero p { position: relative; z-index: 1; max-width: 650px; margin: 0; font-size: 1.05rem; line-height: 1.6; color: #f5eeff; }
.section-label { color: var(--violet); font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .11em; margin: 0 0 .35rem; }
div[data-testid="stFileUploader"], div[data-testid="stTextArea"] { padding: 1.25rem; border-radius: 18px; background: rgba(255,255,255,.76); border: 1px solid rgba(112,73,232,.13); box-shadow: 0 8px 24px rgba(65,51,118,.07); }
div[data-testid="stFileUploader"] { min-height: 252px; } label, div[data-testid="stFileUploader"] label { color: var(--ink)!important; font-weight: 700!important; }
div[data-testid="stTextArea"] textarea { min-height: 176px!important; border-radius: 12px; border-color: #e4def8; background: #fffeff!important; color: #18233f!important; -webkit-text-fill-color: #18233f!important; caret-color: #18233f!important; } div[data-testid="stTextArea"] textarea::placeholder { color: #7a8396!important; -webkit-text-fill-color: #7a8396!important; opacity: 1; }
div[data-testid="stFileUploaderDropzone"], section[data-testid="stFileUploaderDropzone"] { border: 2px dashed #bba9ed!important; border-radius: 14px; background: #faf8ff!important; color: #18233f!important; }
div[data-testid="stFileUploaderDropzone"] *, section[data-testid="stFileUploaderDropzone"] * { color: #18233f!important; }
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"], div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] > div { background: #f1edff!important; border: 1px solid #d9ceff!important; border-radius: 11px!important; }
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *, div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] small { color: #293755!important; -webkit-text-fill-color: #293755!important; }
/* Streamlit uses different test IDs for the file wrapper, name, and delete
   control across versions. Style the complete file component family. */
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"],
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] > div,
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] > span { background-color: #f1edff!important; border-color: #d9ceff!important; color: #293755!important; -webkit-text-fill-color: #293755!important; }
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] * { color: #293755!important; -webkit-text-fill-color: #293755!important; fill: #6c47d9!important; }
div[data-testid="stFileUploader"] [data-testid^="stFileUploaderFile"] { border-radius: 11px!important; box-shadow: none!important; }
div[data-testid="stFileUploader"] button[kind="secondary"] { min-height: 2.65rem!important; padding: .45rem 1rem!important; border: 0!important; border-radius: 10px!important; background: linear-gradient(100deg, #6844df, #a64bd6)!important; color: #ffffff!important; box-shadow: 0 7px 14px rgba(96, 60, 203, .22)!important; font-weight: 800!important; }
div[data-testid="stFileUploader"] button[kind="secondary"] * { color: #ffffff!important; fill: #ffffff!important; }
div[data-testid="stFileUploader"] button[kind="tertiary"] { min-height: 2.65rem!important; min-width: 2.65rem!important; padding: .45rem!important; border: 1px solid #d9ceff!important; border-radius: 10px!important; background: #ffffff!important; color: #6c47d9!important; box-shadow: none!important; }
div[data-testid="stFileUploader"] button[kind="tertiary"] * { color: #6c47d9!important; fill: #6c47d9!important; } div[data-testid="stFileUploader"] button:hover { filter: brightness(1.03); transform: translateY(-1px); }
div.stButton > button { border: 0; min-height: 3.35rem; border-radius: 14px; font-family: 'DM Sans', sans-serif; font-size: 1rem; font-weight: 800; background: linear-gradient(100deg, #6243df, #b64fd1); box-shadow: 0 10px 22px rgba(112,73,232,.28); } div.stButton > button:hover { transform: translateY(-2px); }
.prediction-card, .summary-card {
    height: 100%; box-sizing: border-box; padding: 1.8rem; border-radius: 22px;
    background: rgba(255,255,255,.92); border: 1px solid #e8defb;
    box-shadow: 0 12px 30px rgba(92, 67, 159, .10);
}
.card-label { color: #7049e8; font-size: .78rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 .5rem; }
.prediction-card h2, .summary-card h2 { color: #192746; font-size: 1.75rem; margin: 0 0 .7rem; }
.decision { display: inline-block; padding: .45rem .8rem; border-radius: 999px; font-size: .86rem; font-weight: 800; letter-spacing: .04em; }
.decision-yes { background: #d8faef; color: #087d5d; }.decision-no { background: #ffe4ea; color: #bd3150; }
.threshold { margin: 1.15rem 0; padding: 1rem; border-radius: 14px; background: #f5f1ff; color: #514276; line-height: 1.5; }
.summary-lead { color: #45546f; line-height: 1.55; }.watch-list { margin: 1rem 0 0; padding-left: 0; list-style: none; }
.watch-list li { margin: .65rem 0; color: #45546f; line-height: 1.45; }.watch-list li:before { content: '•'; color: #8552e6; font-weight: 900; margin-right: .55rem; }
.missing-skill { display: inline-block; margin: .22rem; padding: .38rem .65rem; background: #ffe7f4; color: #a02f70; border-radius: 999px; font-size: .84rem; font-weight: 600; }

/* Role workspace */
.role-intro { position: relative; overflow: hidden; margin: .4rem 0 1.2rem; padding: 1.65rem 1.8rem; border: 1px solid rgba(117, 76, 227, .22); border-radius: 24px; background: linear-gradient(110deg, #ffffff 0%, #f4efff 62%, #e4fbff 100%); box-shadow: 0 14px 34px rgba(71, 49, 132, .09); }
.role-intro:after { content: ''; position: absolute; width: 210px; height: 210px; right: -70px; top: -105px; border: 35px solid rgba(114, 72, 231, .12); border-radius: 50%; }
.role-kicker { position: relative; z-index: 1; display: inline-flex; gap: .45rem; align-items: center; padding: .34rem .7rem; border-radius: 999px; background: #e8e0ff; color: #6540cf; font-size: .74rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
.role-intro h2 { position: relative; z-index: 1; margin: .7rem 0 .35rem; font-size: 2rem; letter-spacing: -.035em; }.role-intro p { position: relative; z-index: 1; max-width: 650px; margin: 0; color: #64718d; font-size: 1rem; }
div[data-testid="stSelectbox"] > div > div { min-height: 57px; border: 1px solid #d8caff!important; border-radius: 15px!important; background: #fff!important; box-shadow: 0 7px 18px rgba(79, 51, 148, .08); }
div[data-testid="stSelectbox"] [data-baseweb="select"] > div { color: #263553!important; font-weight: 700; }
div[data-testid="stSelectbox"] label { color: #5b39c5!important; font-size: .8rem!important; letter-spacing: .06em; text-transform: uppercase; }
.manage-role-action button { min-height: 57px!important; border-radius: 15px!important; background: #ffffff!important; color: #5b39c5!important; border: 1px solid #d8caff!important; box-shadow: 0 7px 18px rgba(79, 51, 148, .08)!important; font-size: .92rem!important; }.manage-role-action button:hover { background: #f4efff!important; transform: translateY(-1px)!important; }
.role-dialog-note { margin: 0 0 1.2rem; color: #68738c; line-height: 1.5; }.role-dialog-divider { margin: 1.6rem 0; border: 0; border-top: 1px solid #e7defb; }
div[data-testid="stDialog"] [role="dialog"], div[role="dialog"] { background: #ffffff!important; color: #18233f!important; border: 1px solid #ded3ff!important; border-radius: 24px!important; box-shadow: 0 24px 65px rgba(39, 24, 86, .28)!important; }
div[data-testid="stDialog"] h1, div[role="dialog"] h1, div[data-testid="stDialog"] h2, div[role="dialog"] h2, div[data-testid="stDialog"] h3, div[role="dialog"] h3 { color: #18233f!important; }
div[data-testid="stDialog"] label, div[role="dialog"] label { color: #5436af!important; }
div[data-testid="stDialog"] input, div[role="dialog"] input, div[data-testid="stDialog"] textarea, div[role="dialog"] textarea { background: #fbfaff!important; color: #18233f!important; -webkit-text-fill-color: #18233f!important; border-color: #cdbfff!important; }
div[data-testid="stDialog"] input::placeholder, div[role="dialog"] input::placeholder, div[data-testid="stDialog"] textarea::placeholder, div[role="dialog"] textarea::placeholder { color: #77839d!important; -webkit-text-fill-color: #77839d!important; opacity: 1!important; }
div[data-testid="stDialog"] button[kind="secondary"], div[role="dialog"] button[kind="secondary"] { background: #ffffff!important; color: #6741cf!important; border: 1px solid #cdbfff!important; }
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stFileUploader"]), div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextArea"]) { align-items: stretch; }
div[data-testid="stFileUploader"] { min-height: 310px; padding: 1.4rem!important; background: linear-gradient(150deg, #ffffff, #f5f1ff)!important; }
div[data-testid="stFileUploaderDropzone"], section[data-testid="stFileUploaderDropzone"] { min-height: 150px!important; display: flex!important; align-items: center!important; justify-content: center!important; border-style: solid!important; border-color: #bda7ff!important; background: #fbfaff!important; }
div[data-testid="stTextArea"] { padding: 1.4rem!important; background: linear-gradient(150deg, #ffffff, #f3fbff)!important; } div[data-testid="stTextArea"] textarea { padding: 1rem!important; font-size: 1rem!important; line-height: 1.6!important; border: 1px solid #d3c6f7!important; box-shadow: inset 0 1px 3px rgba(72, 48, 127, .06)!important; }
div[data-testid="stTextArea"] + div[data-testid="stHorizontalBlock"] button { min-height: 2.8rem!important; background: #fff!important; color: #6741cf!important; border: 1px solid #cfc0fa!important; box-shadow: none!important; font-size: .9rem!important; } div[data-testid="stTextArea"] + div[data-testid="stHorizontalBlock"] button:hover { background: #f0ebff!important; transform: none!important; }
div[data-testid="stFileUploader"] label, div[data-testid="stTextArea"] label { display: inline-flex; margin-bottom: .75rem!important; padding: .35rem .6rem; border-radius: 7px; background: #ede8ff; color: #5135ad!important; font-size: .79rem!important; letter-spacing: .02em; }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# These describe generic writing rather than a skill or qualification. They are
# excluded from the similarity score and from the "What is missing" panel.
GENERIC_SCREENING_WORDS = {
    "ability", "abilities", "academic", "academics", "agent", "agents", "agentic",
    "analytical", "architecture", "architectures", "artificial", "assist", "based",
    "basic", "benefit", "best", "case", "cases", "clearly", "concept", "concepts",
    "consideration", "considerations", "creating", "cross", "deep", "develop",
    "experience", "experienced", "including", "knowledge", "project", "projects",
    "responsible", "role", "skills", "technology", "technologies", "understanding",
    "use", "user", "work", "working", "years",
}
# CountVectorizer accepts a list here. Keeping it as a frozenset causes newer
# scikit-learn versions to reject the configuration and produce empty results.
SCREENING_STOP_WORDS = sorted(ENGLISH_STOP_WORDS.union(GENERIC_SCREENING_WORDS))


def meaningful_terms(text):
    """Return role-specific terms only, leaving generic prose out of screening."""
    try:
        vectorizer = CountVectorizer(stop_words=SCREENING_STOP_WORDS)
        vectorizer.fit([text])
        return set(vectorizer.get_feature_names_out())
    except ValueError:
        return set()


DEFAULT_ROLE_JDS = {
    "Software Engineer": """We are hiring a Software Engineer to build reliable, scalable product features. Responsibilities include designing and delivering backend or frontend services, writing maintainable code, participating in code reviews, and collaborating with product and design partners. Required: proficiency in Python, Java, JavaScript, or a similar language; experience with APIs, Git, SQL, testing, and cloud-based deployment. Preferred: React, Docker, AWS, or Kubernetes.""",
    "Data Analyst": """We are seeking a Data Analyst to turn business data into clear recommendations. You will query and clean data, build dashboards, define metrics, and communicate insights to stakeholders. Required: SQL, Excel or Google Sheets, data visualization, and analytical problem solving. Preferred: Python, Power BI, Tableau, statistics, and experience working with product or operational data.""",
    "Data Scientist": """We are hiring a Data Scientist to develop data products and decision models. You will explore datasets, build and evaluate machine learning models, run experiments, and present findings to business partners. Required: Python, SQL, statistics, machine learning, data cleaning, and visualization. Preferred: scikit-learn, pandas, experimentation, forecasting, and cloud data platforms.""",
    "Product Manager": """We are looking for a Product Manager to define product strategy and ship customer-focused improvements. You will gather customer needs, prioritize roadmaps, write requirements, track outcomes, and align engineering, design, and business teams. Required: product discovery, roadmap planning, stakeholder management, user research, analytics, and agile delivery. Preferred: B2B SaaS, experimentation, Jira, and product metrics.""",
    "Project Manager": """We are hiring a Project Manager to plan, coordinate, and deliver cross-functional initiatives. You will manage scope, schedules, risks, budgets, dependencies, and stakeholder communications. Required: project planning, agile or waterfall delivery, risk management, reporting, facilitation, and stakeholder management. Preferred: PMP, Scrum, Jira, Confluence, or experience managing technical projects.""",
    "UX/UI Designer": """We are seeking a UX/UI Designer to create intuitive, accessible digital experiences. You will conduct user research, map journeys, design wireframes and prototypes, maintain design systems, and partner with product and engineering. Required: Figma, interaction design, visual design, prototyping, usability testing, and accessibility. Preferred: design systems, responsive web design, and experience with B2B products.""",
    "DevOps Engineer": """We are hiring a DevOps Engineer to improve delivery reliability, security, and observability. You will build CI/CD pipelines, manage cloud infrastructure, automate deployments, monitor systems, and support incident response. Required: AWS, Azure, or GCP; Docker; Kubernetes; Terraform; Linux; Git; and CI/CD. Preferred: Python or Bash, monitoring tools, security practices, and SRE experience.""",
    "Cybersecurity Analyst": """We are looking for a Cybersecurity Analyst to help protect systems, data, and users. You will monitor security alerts, investigate incidents, manage vulnerabilities, document findings, and improve security controls. Required: SIEM, incident response, vulnerability management, network security, risk assessment, and security fundamentals. Preferred: Splunk, Microsoft Sentinel, SOC operations, cloud security, and relevant certifications.""",
    "Digital Marketing Specialist": """We are seeking a Digital Marketing Specialist to plan and optimize multi-channel campaigns. You will manage paid and organic campaigns, analyze performance, create content briefs, and improve conversion funnels. Required: Google Analytics, SEO, SEM, social media marketing, campaign reporting, and copywriting. Preferred: Google Ads, HubSpot, email marketing, CRM, and A/B testing.""",
    "HR Recruiter": """We are hiring an HR Recruiter to attract and hire great talent. You will partner with hiring managers, source candidates, conduct screening interviews, coordinate interview processes, and maintain an excellent candidate experience. Required: talent sourcing, interview coordination, ATS management, candidate assessment, stakeholder communication, and recruiting metrics. Preferred: LinkedIn Recruiter, employer branding, technical recruiting, and HRIS experience.""",
    "Financial Analyst": """We are seeking a Financial Analyst to support planning and business decisions. You will prepare forecasts, analyze financial results, build models, report performance, and work with operational leaders. Required: financial modeling, budgeting, forecasting, Excel, variance analysis, and financial reporting. Preferred: SQL, Power BI, ERP systems, FP&A, and accounting knowledge.""",
    "Customer Success Manager": """We are hiring a Customer Success Manager to help customers achieve measurable value from our product. You will onboard accounts, manage relationships, identify risks and growth opportunities, lead business reviews, and coordinate with support and product teams. Required: account management, onboarding, customer retention, CRM, stakeholder communication, and SaaS experience. Preferred: Salesforce, renewals, upselling, and enterprise customer experience.""",
}


def initialize_role_library():
    if "role_library" not in st.session_state:
        st.session_state.role_library = DEFAULT_ROLE_JDS.copy()
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = next(iter(st.session_state.role_library))
    if "jd_text" not in st.session_state:
        st.session_state.jd_text = st.session_state.role_library[st.session_state.selected_role]
    if "pending_role_picker" in st.session_state:
        selected = st.session_state.pop("pending_role_picker")
        st.session_state.role_picker = selected
        st.session_state.selected_role = selected
        st.session_state.jd_text = st.session_state.role_library[selected]


def load_selected_role():
    selected = st.session_state.role_picker
    st.session_state.selected_role = selected
    st.session_state.jd_text = st.session_state.role_library[selected]


def reset_job_description():
    st.session_state.jd_text = st.session_state.role_library[st.session_state.selected_role]


@st.dialog("Manage role library")
def manage_role_dialog():
    st.markdown("<p class='role-dialog-note'>Add a tailored role and its job description, or remove a role that is no longer needed.</p>", unsafe_allow_html=True)
    st.markdown("#### Add a new role")
    new_role = st.text_input("Role name", placeholder="e.g. Sales Manager", key="new_role_name")
    new_role_jd = st.text_area("Job description", height=175, placeholder="Add responsibilities, required skills, and preferred qualifications...", key="new_role_jd")
    if st.button("Add role to library", type="primary", use_container_width=True):
        clean_name = new_role.strip()
        if not clean_name:
            st.warning("Enter a role name first.")
        elif clean_name in st.session_state.role_library:
            st.warning("That role already exists.")
        else:
            st.session_state.role_library[clean_name] = new_role_jd.strip() or f"We are hiring a {clean_name}. Add the responsibilities, required skills, and preferred qualifications for this role."
            st.session_state.pending_role_picker = clean_name
            st.rerun()

    st.markdown("<hr class='role-dialog-divider'>", unsafe_allow_html=True)
    st.markdown("#### Remove a role")
    role_to_remove = st.selectbox("Choose a role to remove", sorted(st.session_state.role_library), key="remove_role_picker")
    if st.button("Remove selected role", use_container_width=True):
        if len(st.session_state.role_library) == 1:
            st.warning("Keep at least one role in the library.")
        else:
            del st.session_state.role_library[role_to_remove]
            if st.session_state.selected_role == role_to_remove:
                st.session_state.pending_role_picker = sorted(st.session_state.role_library)[0]
            st.rerun()


initialize_role_library()

# Main Header
st.markdown("""
<section class="hero">
    <span class="eyebrow">Candidate screening toolkit</span>
    <h1>Find the right candidate faster.</h1>
    <p>Compare a resume with the job description, get a clear hiring prediction, and know what to explore in the interview.</p>
</section>
<p class="section-label">Step 1 · Choose a role and add candidate materials</p>
""", unsafe_allow_html=True)

st.markdown("""
<section class="role-intro">
    <span class="role-kicker">✦ Smart role library</span>
    <h2>Start with a role. Make it yours.</h2>
    <p>Pick a ready-to-use job description, personalise it for the opening, then evaluate the candidate against it.</p>
</section>
""", unsafe_allow_html=True)
library_col, manage_col = st.columns([2, 1], gap="large")
with library_col:
    role_options = sorted(st.session_state.role_library)
    current_index = role_options.index(st.session_state.selected_role) if st.session_state.selected_role in role_options else 0
    st.selectbox(
        "Search or select a role",
        role_options,
        index=current_index,
        key="role_picker",
        on_change=load_selected_role,
        placeholder="Search roles such as Data Analyst or Recruiter",
    )
with manage_col:
    st.markdown('<div class="manage-role-action">', unsafe_allow_html=True)
    if st.button("＋ Manage role library", use_container_width=True):
        manage_role_dialog()
    st.markdown('</div>', unsafe_allow_html=True)

# Layout columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📄 Resume")
    resume_file = st.file_uploader("Upload candidate resume (PDF or TXT format)", type=["pdf", "txt"])

with col2:
    st.markdown("## 💼 Job Description")
    st.caption(f"Using the pre-written description for: **{st.session_state.selected_role}**")
    jd_text_input = st.text_area("Edit job description", height=250, key="jd_text")
    edit_col, reset_col = st.columns(2)
    with edit_col:
        if st.button("Save edits to this role", use_container_width=True):
            st.session_state.role_library[st.session_state.selected_role] = st.session_state.jd_text
            st.success("Job description saved.")
    with reset_col:
        st.button("Reset to saved JD", use_container_width=True, on_click=reset_job_description)

st.markdown("<br>", unsafe_allow_html=True)

# Centered Action Button
col_center = st.columns([1, 1, 1])
with col_center[1]:
    match_clicked = st.button("✨ Analyze candidate", use_container_width=True, type="primary")

# Logic when button is clicked
if match_clicked:
    if resume_file is not None and jd_text_input.strip() != "":
        with st.spinner('✨ Analyzing documents and calculating match score...'):
            # Extract text from Resume
            resume_text = ""
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = resume_file.getvalue().decode("utf-8")
                
            jd_text = jd_text_input
                
            # Compare only role-specific terms, not generic writing such as
            # "basic", "ability", or "based".
            text_list = [resume_text, jd_text]
            cv = CountVectorizer(stop_words=SCREENING_STOP_WORDS)
            try:
                count_matrix = cv.fit_transform(text_list)
                match_percentage = cosine_similarity(count_matrix)[0][1] * 100
                match_percentage = round(match_percentage, 2)
            except ValueError:
                match_percentage = 0.0

            st.markdown("<br><p class='section-label'>Step 2 · Candidate results</p>", unsafe_allow_html=True)
            st.header("📊 Match Results")
            
            # Use Streamlit metrics for a clean, built-in colorful look
            score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
            with score_col2:
                # Display score nicely with colored alert boxes
                if match_percentage >= 70:
                    st.success(f"### 🎉 Strong Candidate!\n## Match Score: {match_percentage}%")
                else:
                    st.error(f"### 🛑 Weak Alignment\n## Match Score: {match_percentage}%")

            st.markdown("---")
            
            missing_keywords = meaningful_terms(jd_text) - meaningful_terms(resume_text)
            
            # Results Layout
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                if match_percentage >= 70:
                    st.markdown("""
                    <div class="prediction-card">
                        <p class="card-label">Hiring prediction</p>
                        <h2>Candidate can be considered</h2>
                        <span class="decision decision-yes">✓ CONSIDERED</span>
                        <div class="threshold"><strong>70%+ match score</strong><br>This candidate meets the score threshold for a recruiter or hiring manager review.</div>
                        <p class="summary-lead">The resume has enough alignment with the job description to move to the next stage.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="prediction-card">
                        <p class="card-label">Hiring prediction</p>
                        <h2>Candidate is not considered</h2>
                        <span class="decision decision-no">× NOT CONSIDERED</span>
                        <div class="threshold"><strong>Below 70% match score</strong><br>This candidate does not meet the minimum score threshold for the next stage.</div>
                        <p class="summary-lead">The resume needs stronger evidence of the skills and experience requested for this role.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            with res_col2:
                if match_percentage >= 70:
                    st.markdown("""
                    <div class="summary-card">
                        <p class="card-label">Candidate summary</p>
                        <h2>Worth giving a try: Yes</h2>
                        <p class="summary-lead">The candidate shows meaningful overlap with the role and is worth a closer conversation.</p>
                        <p class="card-label" style="margin-top:1.2rem">Keep an eye on</p>
                        <ul class="watch-list">
                            <li>Depth of hands-on experience with the role's core tools.</li>
                            <li>Specific outcomes from the projects most relevant to this position.</li>
                            <li>Whether the candidate can explain how they applied these skills in practice.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    missing_chips = "".join(
                        f'<span class="missing-skill">{skill}</span>'
                        for skill in sorted(missing_keywords)[:12]
                    ) or '<span class="missing-skill">Core role requirements</span>'
                    st.markdown(f"""
                    <div class="summary-card">
                        <p class="card-label">Candidate summary</p>
                        <h2>Worth giving a try: No</h2>
                        <p class="summary-lead">The current resume does not show enough evidence that the candidate meets this role's core requirements.</p>
                        <p class="card-label" style="margin-top:1.2rem">What is missing</p>
                        <div>{missing_chips}</div>
                        <p class="summary-lead" style="margin-top:1rem">Consider the candidate after their resume clearly demonstrates relevant skills, responsibilities, and measurable outcomes.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
    else:
        st.error("⚠️ Please make sure you have uploaded a resume AND pasted the job description!")
