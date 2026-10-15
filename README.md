# 📄 SWYNEX AI Problem Design: AI-Powered Resume Builder

## 🚀 Project Overview

The **AI-Powered Resume Builder and Job Description Matcher** is a Python-based web application designed to help students, fresh graduates, and job seekers create professional resumes tailored to specific job opportunities.

The application will collect information about a candidate's education, skills, projects, certifications, and experience. It will compare the candidate's profile with a target job description, identify matching skills, highlight requirements not found in the profile, and suggest improvements.

The goal is to make resume preparation easier, more organized, and more relevant to individual job applications.

**Internship:** SWYNEX Technologies  
**Task:** AI Problem Design  
**Duration:** 30 days  
**Project Status:** In Development

## 🎯 Problem Statement

Many job seekers struggle to create resumes that clearly communicate their qualifications for a particular position. Using the same resume for every job may result in important relevant skills being overlooked.

Manually comparing a resume with a job description can also take time. This project aims to simplify that process by organizing candidate information and automatically comparing listed skills with job requirements.

The application will provide an estimated skill-match score and suggestions while ensuring that it does not invent qualifications or experience.

## 👥 Target Users

- Students applying for internships.
- Fresh graduates looking for their first job.
- Job seekers applying for different positions.
- Candidates who want to improve their resume presentation.
- Career changers comparing their existing skills with new job requirements.

## 💡 Proposed Solution

The application will allow users to:

1. Enter their personal and educational details.
2. Add technical skills, projects, certifications, and experience.
3. Enter a target job title and job description.
4. Generate a structured resume using the information provided.
5. Compare candidate skills with job requirements.
6. View matching skills and requirements not found in their profile.
7. Receive suggestions for improving their resume.
8. Preview and download the resume as a PDF.

These are the planned features; their implementation and testing will take place during development.

## 🛠️ Technologies

- **Python** — Application logic and text processing.
- **Streamlit** — Web application interface.
- **Natural Language Processing (NLP)** — Planned text analysis and skill extraction.
- **GitHub** — Source code management and project documentation.
- **PDF generation library** — Planned resume export functionality.

The initial version will use a simple, transparent keyword-matching approach before considering more advanced NLP methods.

## 📥 Input Data

The application will use information provided by the user, including:

- Education and qualifications.
- Technical and soft skills.
- Academic and personal projects.
- Certifications and achievements.
- Work experience, if applicable.
- Target job title.
- Job description and required skills.

Sample candidate profiles and job descriptions will be used for testing. Real personal information will not be necessary for initial evaluation.

## ⚙️ How It Will Work

1. The user enters candidate details.
2. The user provides a target job description.
3. The application processes the text and identifies relevant skills.
4. The system compares the identified job requirements with the candidate's listed skills.
5. The application calculates an estimated match percentage.
6. Matching skills and requirements not found in the profile are displayed.
7. The application organizes the candidate's information into a resume.
8. The user reviews the resume and downloads it as a PDF when export is implemented.

## 🧮 Skill-Matching Approach

The first version will use keyword-based matching.

**Formula:**

Match Percentage = (Number of Matched Required Skills / Total Identified Required Skills) × 100

For example, if a job description contains five identified required skills and three are present in the candidate's profile, the estimated match score is 60%.

This score measures skill overlap only. It does not measure a candidate's complete ability or guarantee selection for a job.

If no required skills are identified, the application will explain that a meaningful score cannot be calculated.

## 📏 Constraints and Limitations

- Results depend on the accuracy of the information entered.
- Keyword matching may not recognize synonyms or related expressions.
- Missing skills mean they were not found in the supplied profile, not necessarily that the candidate lacks them.
- The initial version will not independently verify qualifications or employment history.
- The application will not guarantee ATS compatibility or employment.
- Generated resume content must be reviewed by the user.
- The application must not fabricate skills, experience, certifications, or achievements.

## 🧪 Evaluation Approach

The application will be tested using sample candidate profiles and job descriptions.

Evaluation will check:

- Whether the application accepts and validates user input.
- Whether expected skills are identified correctly.
- Whether matching and missing skills are displayed accurately.
- Whether the match percentage follows the documented formula.
- Whether generated resumes preserve the supplied information.
- Whether PDF output is readable and properly formatted.
- Whether the interface is understandable and easy to use.

Expected results will be prepared manually and compared with the application's output. Any errors found during testing will be documented and corrected.

## 📅 30-Day Development Plan

**Days 1–7: Problem Design and Setup**
- Define the problem and target users.
- Document inputs, constraints, and evaluation criteria.
- Create the GitHub repository.
- Build the initial Streamlit interface.

**Days 8–14: Resume Generation**
- Create candidate information forms.
- Organize candidate information into resume sections.
- Implement resume preview and PDF export.

**Days 15–21: Skill Matching**
- Process job descriptions.
- Identify required skills.
- Calculate the match percentage.
- Display matching and missing skills.
- Add improvement suggestions.

**Days 22–26: Testing**
- Test multiple sample profiles and job descriptions.
- Verify calculations and generated content.
- Improve usability and fix errors.

**Days 27–30: Finalization**
- Complete documentation.
- Record evaluation results.
- Capture application screenshots.
- Organize the repository for submission.

This is the planned schedule and may be adjusted as development progresses.

## 🔐 Responsible Use and Privacy

The application will use user-provided information and sample data during initial testing. Personal details should not be uploaded to public repositories.

The system will not create false qualifications or claim that a candidate possesses skills they have not provided. Users should review the generated resume before submitting it to employers.

The skill-match percentage will be presented as an estimate rather than a hiring prediction.

## 📈 Expected Outcome

The expected outcome is a working web application that helps job seekers organize their information, generate tailored resumes, compare their listed skills with job requirements, and identify areas for improvement.

The project will be considered successful when the main functions work correctly on sample data and the results are documented.

## 🔮 Future Enhancements

Possible future improvements include:

- Semantic skill matching using advanced NLP.
- Additional resume templates.
- Multilingual resume support.
- Grammar and readability assistance.
- More detailed job requirement analysis.
- Additional customization options.

These enhancements will be considered after the core application has been developed and evaluated.

## 🏁 Conclusion

This project explores how Python, Streamlit, and text-processing techniques can help make resume preparation more efficient and job-focused.

The initial goal is to develop a practical, understandable prototype that compares supplied candidate information with job descriptions, provides transparent matching results, and supports structured resume generation.

The application will be developed, tested, and documented during the 30-day SWYNEX internship.

---

**Project Repository:** SWYNEX-AI-Problem-Design  
**Developer:** Meghana Gandasiri  
**Internship Organization:** SWYNEX# SWYNEX-AI-Problem-Design
AI-powered resume builder that helps job seekers create tailored resumes from their skills, education, and experience. Compares candidate skills with job descriptions, identifies skill gaps, suggests improvements, and supports professional resume generation using Python and Streamlit. 
