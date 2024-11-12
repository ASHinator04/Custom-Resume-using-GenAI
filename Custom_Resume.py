import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
import tempfile
from typing import List, Dict
import json

# Load environment variables
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Custom_Resume_With_GenAI"

def create_resume_prompt() -> ChatPromptTemplate:
    """
    Creates an enhanced resume optimization prompt template with improved ATS optimization
    and professional language patterns.
    """
    return ChatPromptTemplate.from_messages([
        ('system', """You are CareerForge AI, an elite resume optimization specialist combining 15+ years of expertise in executive recruiting, ATS systems, and professional writing. Your mission is to transform resumes into compelling professional narratives that achieve maximum ATS scores while highlighting candidates' true potential.

        Core Optimization Framework:

        1. Enhanced Achievement Format:
        - Transform experiences using the STAR+Impact method:
          "[Strategic Action Verb] [Specific Task/Challenge] through [Approach/Action], generating [Quantified Results + Business Impact]"
        - Prioritize metrics: ROI, revenue impact, efficiency gains, cost savings, user growth
        - Lead with premium action verbs categorized by achievement type:
          • Leadership: Spearheaded, Orchestrated, Championed, Pioneered
          • Innovation: Transformed, Revolutionized, Engineered, Optimized
          • Analysis: Synthesized, Formulated, Diagnosed, Evaluated
          • Technical: Architected, Implemented, Automated, Deployed
          • Growth: Accelerated, Maximized, Scaled, Generated
          • Collaboration: Fostered, Mobilized, Mentored, Facilitated

        2. Advanced ATS Optimization:
        - Implement intelligent keyword matching:
          • Primary keywords in first 2 bullets of each role
          • Include both full terms and acronyms (e.g., "Artificial Intelligence (AI)")
          • Match exact phrases from job description
        - Use ATS-optimized section headers:
          • Professional Experience
          • Technical Expertise
          • Education & Certifications
          • Notable Projects
        - Maintain clean, ATS-friendly formatting
        - Strategic keyword density of 3-5% per section

        3. Enhanced Content Structure:
        ```
        [Full Name]
        [Phone] | [Professional Email] | [Location] | [LinkedIn]

        Professional Summary
        [Achievement-focused overview aligning experience with role requirements]
        [Key metrics and recognized expertise]
        [Forward-looking statement tied to target role]

        Professional Experience
        [Company Name] | [Location] | [Industry/Scale indicator]
        [Title with Keywords] | [MM/YYYY - MM/YYYY]
        • [STAR+Impact achievement with primary keywords]
        • [Technical implementation with quantified results]
        • [Leadership/Innovation achievement with business impact]

        Technical Expertise
        [Categorized skills matching job requirements]
        • Core Technologies: [Primary technical skills]
        • Frameworks & Tools: [Relevant platforms/tools]
        • Methodologies: [Processes/approaches]

        Education & Certifications
        [Degree] in [Field aligned with role]
        [Institution] | [Graduation Date]
        [Relevant specialized training/certifications]

        Notable Projects
        [Project Name aligned with job requirements]
        • [Technical achievement with measurable impact]
        • [Implementation details with business value]
        ```

        4. Professional Language Enhancement:
        - Replace weak phrases with powerful alternatives:
          • "Responsible for" → "Directed"
          • "Helped with" → "Orchestrated"
          • "Worked on" → "Spearheaded"
        - Use industry-specific terminology from job description
        - Maintain authoritative tone throughout

        5. Quantification Framework:
        Transform achievements into metrics:
        - Percentages: Efficiency, growth, accuracy
        - Scale: Team size, user base, geographic reach
        - Time: Delivery speed, frequency, optimization
        - Value: Revenue, savings, ROI

        Process Execution:
        1. Job Analysis:
        - Extract core requirements and keywords
        - Identify culture indicators and values
        - Map technical requirements

        2. Resume Enhancement:
        - Upgrade achievements using STAR+Impact
        - Integrate keywords strategically
        - Amplify leadership and innovation
        - Ensure truthful representation

        Output Requirements:
        1. Deliver ATS-optimized resume with:
        - Keyword-rich, achievement-focused content
        - Clean, consistent formatting
        - Strategic section ordering
        - Quantified impacts

        2. Provide optimization summary:
        - Keyword match rate
        - ATS compatibility score
        - Key improvements made
        - Interview talking points

        Remember: Focus on authentic achievements while maximizing ATS compatibility and professional impact."""),
        ('user', "Given the job description: {job_description} and the current resume: {current_resume}, generate an optimized resume.")
    ])

def extract_resume_text(docs: List[Document]) -> str:
    """
    Extracts and combines text from document chunks into a single string.
    """
    return "\n".join([doc.page_content for doc in docs])

def analyze_keywords(job_description: str, resume_text: str) -> Dict:
    """
    Analyzes keyword matching between job description and resume.
    """
    # Convert texts to lowercase for comparison
    job_desc_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    # Extract significant words from job description
    job_keywords = set([word.strip() for word in job_desc_lower.split() 
                       if len(word.strip()) > 3])  # Ignore small words
    
    # Count matches
    matches = sum(1 for keyword in job_keywords 
                 if keyword in resume_lower)
    
    return {
        "total_keywords": len(job_keywords),
        "matched_keywords": matches,
        "match_percentage": round((matches / len(job_keywords)) * 100 if job_keywords else 0, 2)
    }

def generate_resume(job_description: str, current_resume: List[Document], llm: Ollama) -> tuple:
    """
    Generates an optimized resume and provides analysis metrics.
    """
    # Extract text from resume documents
    resume_text = extract_resume_text(current_resume)
    
    # Create and execute the optimization chain
    prompt = create_resume_prompt()
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Generate optimized resume
    response = chain.run(job_description=job_description, 
                        current_resume=resume_text)
    
    # Analyze keyword matching
    keyword_analysis = analyze_keywords(job_description, response)
    
    return response, keyword_analysis

def app():
    st.set_page_config(
        page_title="Advanced Resume Optimizer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🚀 Advanced Resume Optimizer")
    st.markdown("""
    This tool uses AI to create ATS-optimized resumes tailored to specific job descriptions.
    Upload your current resume and paste the job description to get started.
    """)

    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            job_description = st.text_area(
                "Job Description",
                height=300,
                placeholder="Paste the job description here..."
            )
            
        with col2:
            uploaded_file = st.file_uploader(
                "Upload Current Resume (PDF)",
                type="pdf",
                help="Upload your current resume in PDF format"
            )

    if job_description and uploaded_file:
        try:
            with st.spinner("🔄 Analyzing and optimizing your resume..."):
                # Create temporary file for PDF processing
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                # Load and process PDF
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()

                # Split documents
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=100,
                    separators=["\n\n", "\n", " ", ""]
                )
                split_docs = text_splitter.split_documents(documents=docs)

                if split_docs:
                    # Initialize LLM
                    llm = Ollama(model="llama3.2")
                    
                    # Generate optimized resume and analysis
                    optimized_resume, keyword_analysis = generate_resume(
                        job_description, split_docs, llm
                    )

                    # Display results
                    st.success("✅ Resume optimization complete!")
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "Keyword Match Rate",
                            f"{keyword_analysis['match_percentage']}%"
                        )
                    with col2:
                        st.metric(
                            "Keywords Matched",
                            keyword_analysis['matched_keywords']
                        )
                    with col3:
                        st.metric(
                            "Total Job Keywords",
                            keyword_analysis['total_keywords']
                        )

                    # Display optimized resume
                    st.markdown("### 📄 Optimized Resume")
                    st.markdown(optimized_resume)

                    # Download button
                    st.download_button(
                        "📥 Download Optimized Resume",
                        optimized_resume,
                        file_name="optimized_resume.txt",
                        mime="text/plain"
                    )

                else:
                    st.error("❌ Could not extract text from the uploaded resume.")

                # Cleanup temporary file
                os.unlink(tmp_path)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please try again with a different PDF file or check the job description format.")

    else:
        st.info("👆 Please provide both the job description and your current resume to begin optimization.")

if __name__ == "__main__":
    app()