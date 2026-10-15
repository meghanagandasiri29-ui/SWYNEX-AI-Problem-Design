
import streamlit as st

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI-Powered Resume Builder")
st.write("Create a resume tailored to your dream job!")

st.header("👤 Personal Information")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
education = st.text_input("Education")
skills = st.text_area("Your Skills")
projects = st.text_area("Your Projects or Experience")

st.header("💼 Target Job")

job_title = st.text_input("Target Job Title")
job_description = st.text_area("Paste the Job Description")

if st.button("✨ Generate My Resume"):
    if not name or not job_title or not job_description:
        st.warning("Please enter your name, target job title, and job description.")
    else:
        st.success("Resume preview generated!")

        st.title(name)
        st.write("Email:", email)
        st.write("Phone:", phone)

        st.header("Professional Profile")
        st.write("Education:", education)
        st.write("Skills:", skills)
        st.write("Projects and Experience:", projects)

        st.header("Target Job")
        st.write("Position:", job_title)
        st.write(job_description)
