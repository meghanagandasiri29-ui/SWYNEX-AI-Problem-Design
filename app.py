import html
import re
from io import BytesIO
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepInFrame,
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f4f7fc;
    }

    [data-testid="stSidebar"] {
        background: #102447;
        border-right: 1px solid #20395e;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #d8e4f5;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent;
        padding: 7px 8px;
        border-radius: 8px;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero {
        background: linear-gradient(120deg, #163c78 0%, #2866bd 100%);
        padding: 35px 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(28, 72, 135, 0.12);
    }

    .hero h1 {
        color: white;
        font-size: 35px;
        font-weight: 800;
        margin: 0 0 12px 0;
        line-height: 1.2;
    }

    .hero p {
        color: #e6efff;
        font-size: 16px;
        margin: 0;
        line-height: 1.7;
    }

    .section-heading {
        color: #152b4d;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .muted {
        color: #65748b;
        font-size: 14px;
    }

    .feature-card {
        background: white;
        border: 1px solid #e2eaf5;
        border-radius: 16px;
        padding: 24px;
        min-height: 175px;
        box-shadow: 0 5px 18px rgba(25, 55, 100, 0.04);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .feature-title {
        color: #17345f;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #65748b;
        font-size: 14px;
        line-height: 1.6;
    }

    .tip-card {
        background: #eaf2ff;
        border: 1px solid #d5e5ff;
        border-radius: 14px;
        padding: 18px 20px;
        color: #234a80;
        margin-top: 20px;
    }

    .metric-card {
        background: white;
        border: 1px solid #e2eaf5;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .metric-number {
        color: #2162b4;
        font-size: 28px;
        font-weight: 800;
    }

    .metric-label {
        color: #65748b;
        font-size: 13px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 43px;
        border: 1px solid #cddcf0;
    }

    div.stButton > button[kind="primary"] {
        background: #2162b4;
        border-color: #2162b4;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #174b91;
        border-color: #174b91;
        color: white;
    }

    div.stDownloadButton > button {
        background: #2162b4;
        color: white;
        border-color: #2162b4;
    }

    [data-testid="stForm"] {
        background: white;
        padding: 22px;
        border: 1px solid #e2eaf5;
        border-radius: 16px;
    }

    h1, h2, h3 {
        color: #152b4d;
    }

    .footer {
        text-align: center;
        color: #8793a6;
        font-size: 12px;
        padding-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

SKILL_KEYWORDS = [
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "html", "css", "sql", "mysql",
    "postgresql", "mongodb", "streamlit", "flask",
    "django", "react", "node.js", "machine learning",
    "deep learning", "artificial intelligence", "data analysis",
    "pandas", "numpy", "excel", "power bi", "tableau",
    "git", "github", "api", "communication",
    "teamwork", "problem solving", "leadership",
    "project management", "cloud", "aws", "azure",
    "data structures", "algorithms", "testing",
]



def extract_skills(text):
    """Extract skills using whole-word matching."""
    text = text.lower()
    found = []

    for skill in SKILL_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill.title())

    return sorted(set(found))


def safe_text(value):
    """Escape text before inserting it into a ReportLab paragraph."""
    return html.escape(str(value or "").strip()).replace("\n", "<br/>")


def create_pdf(data):
    """Create a downloadable resume PDF."""
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f"{data.get('name', 'Resume')} - Resume",
        author=data.get("name", ""),
    )

    navy = colors.HexColor("#17345f")
    blue = colors.HexColor("#2162b4")
    grey = colors.HexColor("#526174")

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        textColor=navy,
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=grey,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "ResumeHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=blue,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#263449"),
        spaceAfter=4,
    )

    story = []

    name = data.get("name", "").strip() or "Your Name"
    story.append(Paragraph(safe_text(name), name_style))

    contact_parts = [
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", ""),
    ]
    contact_line = " | ".join(
        html.escape(item.strip())
        for item in contact_parts
        if item and item.strip()
    )

    if contact_line:
        story.append(Paragraph(contact_line, contact_style))

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=blue,
            spaceAfter=6,
        )
    )

    def add_section(title, content):
        content = str(content or "").strip()
        if content:
            story.append(Paragraph(title.upper(), heading_style))
            story.append(Paragraph(safe_text(content), body_style))

    add_section("Professional Summary", data.get("summary", ""))

    add_section("Technical Skills", data.get("skills", ""))

    add_section("Education", data.get("education", ""))

    add_section("Projects", data.get("projects", ""))

    add_section("Experience", data.get("experience", ""))

    add_section("Certifications", data.get("certifications", ""))

    # Keep resume content together and scale it to one A4 page.
    fitted_content = KeepInFrame(
        maxWidth=document.width,
        maxHeight=document.height - 5 * mm,
        content=story,
        mode="shrink",
        hAlign="LEFT",
        vAlign="TOP",
    )

    document.build([fitted_content])
    buffer.seek(0)

    return buffer.getvalue()


def go_to_page(target_page):
    """Change the selected sidebar page from a Home page button."""
    st.session_state["navigation_choice"] = target_page


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding:12px 0 20px 0;">
            <div style="font-size:32px;">📄</div>
            <div style="font-size:22px;font-weight:800;color:white;">
                AI Resume Builder
            </div>
            <div style="font-size:12px;color:#bdcde4;margin-top:5px;">
                Your career workspace
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("##### NAVIGATION")

    page = st.radio(
        "Choose a page",
        [
            "Home",
            "Resume Builder",
            "Job Match Analyzer",
            "About",
        ],
        key="navigation_choice",
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="padding:10px 0;">
            <div style="font-size:12px;color:#bdcde4;">YOUR CAREER, YOUR FUTURE</div>
            <div style="font-size:13px;color:white;margin-top:8px;">
                Create. Improve. Succeed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>Build a Resume That Opens Doors</h1>
            <p>
                Create a professional resume, highlight your skills, and
                understand how well your profile matches a job description.
                Start building your career with confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">Welcome to Your Career Workspace</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="muted">Everything you need to prepare for your next opportunity.</p>',
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Resume Builder</div>
                <div class="feature-text">
                    Enter your personal details, professional summary,
                    education, skills, and projects. Generate a clean,
                    downloadable PDF resume.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.button(
            "Create My Resume  →",
            key="home_resume_button",
            type="primary",
            use_container_width=True,
            on_click=go_to_page,
            args=("Resume Builder",),
        )

    with right:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Job Match Analyzer</div>
                <div class="feature-text">
                    Compare your skills with a job description, view
                    matching and missing skills, and get suggestions
                    for improving your profile.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.button(
            "Analyze Job Match  →",
            key="home_match_button",
            use_container_width=True,
            on_click=go_to_page,
            args=("Job Match Analyzer",),
        )

    st.write("")

    st.markdown(
        """
        <div class="tip-card">
            <strong>💡 Career tip</strong><br/>
            Tailor your resume to each job description. Highlight relevant
            projects and skills, use clear language, and keep your information
            accurate and up to date.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">01</div>
                <div class="metric-label">Enter Your Details</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">02</div>
                <div class="metric-label">Review Your Resume</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">03</div>
                <div class="metric-label">Download Your PDF</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# RESUME BUILDER PAGE
# --------------------------------------------------

elif page == "Resume Builder":

    st.title("📝 Resume Builder")

    st.markdown(
        "Fill in your information below to create a professional resume."
    )

    st.info(
        "Tip: Use accurate details and include projects or experience "
        "relevant to the jobs you want."
    )

    # Default values are initialized only once.
    defaults = {
        "resume_name": "",
        "resume_email": "",
        "resume_phone": "",
        "resume_location": "",
        "resume_role": "",
        "resume_summary": "",
        "resume_skills": "",
        "resume_education": "",
        "resume_projects": "",
        "resume_experience": "",
        "resume_certifications": "",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    with st.form("resume_form"):

        st.subheader("Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "Full Name *",
                key="resume_name",
                placeholder="Enter your full name",
            )

            st.text_input(
                "Email Address",
                key="resume_email",
                placeholder="you@example.com",
            )

            st.text_input(
                "Phone Number",
                key="resume_phone",
                placeholder="Your contact number",
            )

        with col2:
            st.text_input(
                "Location",
                key="resume_location",
                placeholder="City, Country",
            )

            st.text_input(
                "Target Job Role",
                key="resume_role",
                placeholder="e.g. Python Developer",
            )

        st.divider()
        st.subheader("Professional Details")

        st.text_area(
            "Professional Summary",
            key="resume_summary",
            height=100,
            placeholder=(
                "Briefly describe your background, strengths, "
                "career goals, and relevant experience."
            ),
        )

        st.text_area(
            "Skills",
            key="resume_skills",
            height=90,
            placeholder="Python, SQL, HTML, CSS, Communication...",
        )

        st.text_area(
            "Education",
            key="resume_education",
            height=100,
            placeholder=(
                "Degree | College/University | Graduation Year\n"
                "Add another qualification on a new line."
            ),
        )

        st.text_area(
            "Projects",
            key="resume_projects",
            height=110,
            placeholder=(
                "Project Name: Describe what you built, "
                "the tools you used, and the result."
            ),
        )

        st.text_area(
            "Work Experience / Internship",
            key="resume_experience",
            height=100,
            placeholder=(
                "Role | Company | Dates\n"
                "Describe your responsibilities and achievements."
            ),
        )

        st.text_area(
            "Certifications",
            key="resume_certifications",
            height=75,
            placeholder="List relevant certifications, if any.",
        )

        submitted = st.form_submit_button(
            "Generate Resume Preview",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not st.session_state["resume_name"].strip():
            st.error("Please enter your full name before generating your resume.")
        else:
            st.session_state["resume_generated"] = True
            st.success("Your resume preview is ready!")

    if st.session_state.get("resume_generated", False):

        resume_data = {
            "name": st.session_state["resume_name"],
            "email": st.session_state["resume_email"],
            "phone": st.session_state["resume_phone"],
            "location": st.session_state["resume_location"],
            "role": st.session_state["resume_role"],
            "summary": st.session_state["resume_summary"],
            "skills": st.session_state["resume_skills"],
            "education": st.session_state["resume_education"],
            "projects": st.session_state["resume_projects"],
            "experience": st.session_state["resume_experience"],
            "certifications": st.session_state["resume_certifications"],
        }

        st.divider()
        st.subheader("Resume Preview")

        st.markdown(
            """
            <div style="
                background:white;
                border:1px solid #dfe7f2;
                border-radius:14px;
                padding:28px;
            ">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<h2 style='text-align:center;color:#17345f;'>"
            f"{html.escape(resume_data['name'])}</h2>",
            unsafe_allow_html=True,
        )

        contact = " | ".join(
            item
            for item in [
                resume_data["email"],
                resume_data["phone"],
                resume_data["location"],
            ]
            if item.strip()
        )

        if contact:
            st.markdown(
                f"<p style='text-align:center;color:#526174;'>"
                f"{html.escape(contact)}</p>",
                unsafe_allow_html=True,
            )

        if resume_data["role"].strip():
            st.markdown(f"**Target Role:** {resume_data['role']}")

        for heading, field in [
            ("Professional Summary", "summary"),
            ("Skills", "skills"),
            ("Education", "education"),
            ("Projects", "projects"),
            ("Experience", "experience"),
            ("Certifications", "certifications"),
        ]:
            content = resume_data[field].strip()

            if content:
                st.markdown(f"#### {heading}")
                st.text(content)

        st.markdown("</div>", unsafe_allow_html=True)

        pdf_bytes = create_pdf(resume_data)

        safe_filename = "".join(
            character
            for character in resume_data["name"]
            if character.isalnum() or character in (" ", "-", "_")
        ).strip().replace(" ", "_")

        if not safe_filename:
            safe_filename = "resume"

        st.download_button(
            label="⬇️ Download Resume as PDF",
            data=pdf_bytes,
            file_name=f"{safe_filename}_Resume.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

# --------------------------------------------------
# JOB MATCH ANALYZER PAGE
# --------------------------------------------------

elif page == "Job Match Analyzer":

    st.title("🎯 Job Match Analyzer")

    st.markdown(
        "Compare your skills with a job description to identify "
        "matching skills and areas you may want to improve."
    )

    st.info(
        "This version uses keyword matching. Its score is an estimate "
        "based on detected skills, not an employer's actual hiring score."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Your Skills")

        resume_text = st.text_area(
            "Paste your resume or list your skills",
            height=280,
            placeholder=(
                "Example:\n"
                "Python, SQL, HTML, CSS\n"
                "Developed a web application using Streamlit."
            ),
            key="analyzer_resume",
        )

    with col2:
        st.subheader("Job Description")

        job_text = st.text_area(
            "Paste the job description",
            height=280,
            placeholder=(
                "Example:\n"
                "We are looking for a Python developer with "
                "SQL, Git, API, and problem-solving skills..."
            ),
            key="analyzer_job",
        )

    if st.button(
        "Analyze Job Match",
        type="primary",
        use_container_width=True,
    ):
        if not resume_text.strip() or not job_text.strip():
            st.warning("Please provide both your resume/skills and a job description.")
        else:
            resume_skills = set(extract_skills(resume_text))
            job_skills = set(extract_skills(job_text))

            if not job_skills:
                st.warning(
                    "No supported skill keywords were detected in the job "
                    "description. Try adding more technical or professional skills."
                )
            else:
                matched_skills = sorted(resume_skills & job_skills)
                missing_skills = sorted(job_skills - resume_skills)

                score = round(
                    len(matched_skills) / len(job_skills) * 100
                )

                st.session_state["last_match_result"] = {
                    "score": score,
                    "matched": matched_skills,
                    "missing": missing_skills,
                    "job_count": len(job_skills),
                }

    result = st.session_state.get("last_match_result")

    if result:
        st.divider()
        st.subheader("Analysis Results")

        score = result["score"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Estimated Match", f"{score}%")

        with col2:
            st.metric("Matched Skills", len(result["matched"]))

        with col3:
            st.metric("Skills to Review", len(result["missing"]))

        st.progress(score / 100)

        if score >= 75:
            st.success(
                "Strong keyword overlap! Review the job requirements "
                "and make sure your resume demonstrates your relevant skills."
            )
        elif score >= 45:
            st.warning(
                "Moderate keyword overlap. Consider strengthening the "
                "relevant skills and projects in your resume."
            )
        else:
            st.info(
                "There is limited keyword overlap. Review the role's "
                "requirements and identify skills you can develop."
            )

        matched_col, missing_col = st.columns(2, gap="large")

        with matched_col:
            st.markdown("#### ✅ Matching Skills")

            if result["matched"]:
                for skill in result["matched"]:
                    st.markdown(f"- {skill}")
            else:
                st.write("No matching supported keywords were detected.")

        with missing_col:
            st.markdown("#### 📌 Skills Not Detected")

            if result["missing"]:
                for skill in result["missing"]:
                    st.markdown(f"- {skill}")
            else:
                st.write("All detected job-description keywords were matched.")

        st.caption(
            "Note: The analyzer checks a predefined list of keywords. "
            "It does not understand context, verify proficiency, or use "
            "a trained AI model. A missing keyword does not necessarily "
            "mean you lack that skill."
        )

# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

else:

    st.title("ℹ️ About AI Resume Builder")

    st.markdown(
        """
        Welcome to **AI Resume Builder**, a web application designed to
        help job seekers create a resume and compare their skills with
        a job description.
        """
    )

    st.divider()

    st.subheader("Project Features")

    st.markdown(
        """
        - **Home Dashboard:** A central place to access the application.
        - **Resume Builder:** Enter your details and prepare a resume.
        - **PDF Export:** Download your resume as a PDF document.
        - **Job Match Analyzer:** Compare detected resume skills with
          keywords found in a job description.
        - **Skill Suggestions:** Identify job-description keywords that
          were not detected in your resume.
        - **Multi-page Navigation:** Move between features using the sidebar.
        """
    )

    st.subheader("Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🐍 Python")
        st.caption("Application logic and skill matching")

    with col2:
        st.markdown("### 🎈 Streamlit")
        st.caption("Web interface and navigation")

    with col3:
        st.markdown("### 📄 ReportLab")
        st.caption("PDF resume generation")

    st.divider()

    st.subheader("Important Note")

    st.write(
        "The current job matcher uses predefined keyword rules. "
        "It is a prototype and does not call an external AI model. "
        "The match percentage is an approximate keyword-overlap score, "
        "not a prediction of whether you will get a job."
    )

    st.subheader("Future Enhancements")

    st.markdown(
        """
        - AI-assisted professional summaries
        - More resume templates
        - Improved skill extraction
        - Multilingual resume generation
        - Saving and managing multiple resumes
        """
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        AI Resume Builder · SWYNEX Internship Project · Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
