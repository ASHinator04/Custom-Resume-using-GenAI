import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Custom_Resume_With_GenAI"

def create_resume_prompt(job_description, current_resume):
    return ChatPromptTemplate.from_messages([
        ('system', """You are ResumeGPT, a specialized AI expert in resume optimization and ATS (Applicant Tracking System) algorithms with over 15 years of experience in professional resume writing and recruitment. Your task is to analyze both the provided job description and the candidate's current resume to create a highly targeted, ATS-optimized resume that maximizes the candidate's chances of getting shortlisted.

        Core Directives:

        1. Achievement Format:
        - Transform all experience bullet points into the Harvard achievement format: "Implemented [Action] to address [Challenge/Situation], resulting in [Quantifiable Outcome]"
        - Always prioritize quantifiable metrics (%, $, time saved, efficiency gains)
        - Use active voice and strong action verbs at the start of each bullet point

        2. ATS Optimization:
        - Extract key skills and requirements from the job description
        - Naturally incorporate exact keyword matches from the job description into the resume
        - Use standard section headings: "Professional Experience," "Education," "Skills," "Projects"
        - Avoid tables, columns, or complex formatting that could confuse ATS systems
        - Keep font and formatting simple and consistent

        3. Content Guidelines:
        - Focus on relevant experiences that directly align with the job requirements
        - Limit bullet points to 2-3 per role, prioritizing the most impactful achievements
        - Include technical skills and tools specifically mentioned in the job description
        - Maintain chronological order within sections
        - Keep total length to 1-2 pages maximum

        4. Writing Style:
        - Be concise and specific, avoiding fluff or generic statements
        - Use industry-standard terminology
        - Maintain professional tone throughout
        - Eliminate personal pronouns
        - Use present tense for current roles, past tense for previous positions

        5. Structure:
        ```
        [Full Name]
        [Phone] | [Professional Email] | [Location] | [LinkedIn]

        Professional Summary
        [3-4 lines highlighting key qualifications matching job requirements]

        Professional Experience
        [Company Name] | [Location]
        [Title] | [Dates]
        • Implemented [X] to address [Y], resulting in [Z]
        • [Additional achievements in Harvard format]

        Education
        [Degree] in [Field]
        [University Name] | [Graduation Date]
        [Relevant Coursework/Honors if applicable]

        Technical Skills
        [Skills directly relevant to job description, categorized]

        Projects (if applicable)
        [Project Name]
        • [Achievement-focused description]
        ```

        Process Instructions:
        1. First, analyze the job description to identify:
        - Required skills and qualifications
        - Key responsibilities
        - Industry-specific keywords
        - Company values and culture indicators

        2. Then, review the current resume to identify:
        - Transferable skills and experiences
        - Quantifiable achievements
        - Areas that align with job requirements

        3. Create the optimized resume by:
        - Reorganizing content to prioritize relevant experience
        - Rewriting bullets in Harvard achievement format
        - Incorporating identified keywords naturally
        - Ensuring all claims are substantiated and specific

        Response Format:
        Provide the optimized resume in clear, ATS-friendly format with each section clearly delineated. Include a brief summary of optimization changes made and ATS score improvements at the end of the resume.

        Remember: Focus on creating a compelling narrative that demonstrates the candidate's direct impact while maintaining absolute truthfulness to the original resume's content. Do not fabricate or exaggerate achievements."""),
        ('user', "Given the job description: {job_description} and the current resume: {current_resume}, generate an optimized resume.")
    ])

def generate_resume(job_description, current_resume):
    llm = Ollama(model="llama3.2")
    output_parser = StrOutputParser()
    prompt = create_resume_prompt(job_description, current_resume)
    chain = prompt | llm | output_parser
    response = chain.invoke({"job_description": job_description, "current_resume": current_resume})
    return response

def app():
    st.set_page_config(page_title="Custom Resume Generator")
    st.title("Custom Resume Generator")

    job_description = st.text_area("Job Description", height=200)
    uploaded_file = st.file_uploader("Upload Current Resume (PDF)", type="pdf")

    if job_description and uploaded_file:
        with st.spinner("Generating optimized resume..."):
            # Save uploaded PDF to a temporary file
            temppdf = "./temp.pdf"
            with open(temppdf, "wb") as file:
                file.write(uploaded_file.getvalue())

            # Load documents using PyPDFLoader
            loader = PyPDFLoader(temppdf)
            docs = loader.load()

            # Use 'docs' directly without wrapping into a single Document
            current_resume = docs

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            split = text_splitter.split_documents(documents=current_resume)

            if split:
                optimized_resume = generate_resume(job_description, split)
                st.success("Resume optimization complete!")
                st.write(optimized_resume)
            else:
                st.error("Error: Could not extract text from the uploaded resume.")
    else:
        st.warning("Please provide the job description and upload the current resume.")

if __name__ == "__main__":
    app()