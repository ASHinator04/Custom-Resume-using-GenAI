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

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Custom_Resume_With_GenAI"

st.secrets["LANGCHAIN_API_KEY"] == "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"

def extract_and_suggest_keywords(job_description: str, resume_text: str, llm: Ollama) -> Dict:
    """
    Analyzes existing keywords and suggests additional relevant ones.
    """
    # Create prompt for keyword suggestion
    keyword_prompt = ChatPromptTemplate.from_messages([
        ('system', """You are a technical keyword optimization specialist. 
        Analyze the job description and current resume, then provide two lists:
        1. The top 22 most important technical keywords present in the job description but missing from the resume
        2. 10 additional highly relevant keywords based on industry standards and common requirements

        Format your response EXACTLY as follows (including the exact headings):
        Top 22 Keywords:
        keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8, keyword9, keyword10, keyword11, keyword12, keyword13, keyword14, keyword15, keyword16, keyword17, keyword18, keyword19, keyword20, keyword21, keyword22

        Additional 10 Keywords:
        keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8, keyword9, keyword10"""),
        ('user', """Job Description: {job_description}
        Current Resume: {resume_text}
        
        Generate the requested keywords.""")
    ])
    
    # Create chain for keyword suggestion
    keyword_chain = LLMChain(llm=llm, prompt=keyword_prompt)
    
    # Get suggested keywords
    response = keyword_chain.run(
        job_description=job_description,
        resume_text=resume_text
    )
    
    try:
        # Split the response into sections
        sections = response.strip().split('\n\n')
        
        # Find the sections with our keywords
        top_keywords_section = None
        additional_keywords_section = None
        
        for section in sections:
            if 'Top 22 Keywords:' in section:
                top_keywords_section = section
            elif 'Additional 10 Keywords:' in section:
                additional_keywords_section = section
        
        if not top_keywords_section or not additional_keywords_section:
            # Fallback values if parsing fails
            return {
                "original_total_keywords": 0,
                "original_matched_keywords": 0,
                "original_match_percentage": 0,
                "top_22_keywords": ["Error parsing keywords"],
                "additional_10_keywords": ["Error parsing keywords"]
            }
        
        # Extract and clean the keywords
        top_22_keywords = top_keywords_section.split(':', 1)[1].strip().split(', ')
        additional_10_keywords = additional_keywords_section.split(':', 1)[1].strip().split(', ')
        
        # Original keyword analysis
        job_desc_lower = job_description.lower()
        resume_lower = resume_text.lower()
        job_keywords = set([word.strip() for word in job_desc_lower.split() 
                           if len(word.strip()) > 3])
        
        original_matches = sum(1 for keyword in job_keywords 
                              if keyword in resume_lower)
        
        return {
            "original_total_keywords": len(job_keywords),
            "original_matched_keywords": original_matches,
            "original_match_percentage": round((original_matches / len(job_keywords)) * 100 if job_keywords else 0, 2),
            "top_22_keywords": top_22_keywords,
            "additional_10_keywords": additional_10_keywords
        }
        
    except Exception as e:
        # Fallback values if any error occurs
        return {
            "original_total_keywords": 0,
            "original_matched_keywords": 0,
            "original_match_percentage": 0,
            "top_22_keywords": [f"Error parsing keywords: {str(e)}"],
            "additional_10_keywords": [f"Error parsing keywords: {str(e)}"]
        }

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

        IMPORTANT: Include and naturally incorporate the following additional keywords into the optimized resume:
        {suggested_keywords}
        
        Ensure these keywords are integrated naturally and relevantly into the resume content.

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


def create_cover_letter_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for generating a customized cover letter.
    """
    return ChatPromptTemplate.from_messages([
        ('system', """You are an expert cover letter writer with deep experience in professional writing and HR. 
        Create a compelling cover letter that:
        
        1. Structure:
        - Uses a professional business letter format
        - Includes today's date, recipient's information (if available), and proper salutation
        - Consists of 3-4 concise paragraphs
        
        2. Content Guidelines:
        - Opening: Hook the reader with enthusiasm for the specific role and company
        - Body: Focus on 2-3 most relevant achievements that match job requirements
        - Closing: Express interest in an interview and provide contact information
        
        3. Style Requirements:
        - Maintain a professional yet personable tone
        - Use industry-specific keywords from the job description
        - Keep the letter concise (250-350 words)
        - Incorporate achievements and skills from the optimized resume
        
        4. Technical Considerations:
        - Include relevant technical skills and certifications
        - Highlight specific projects or implementations that match job requirements
        - Demonstrate understanding of industry trends and challenges
        
        Format the letter professionally with proper spacing and sections."""),
        ('user', """Job Description: {job_description}
        
        Optimized Resume: {optimized_resume}
        
        Generate a compelling cover letter.""")
    ])

def generate_cover_letter(job_description: str, optimized_resume: str, llm: Ollama) -> str:
    """
    Generates a customized cover letter based on the job description and optimized resume.
    """
    prompt = create_cover_letter_prompt()
    chain = LLMChain(llm=llm, prompt=prompt)
    
    cover_letter = chain.run(
        job_description=job_description,
        optimized_resume=optimized_resume
    )
    
    return cover_letter
def generate_resume(job_description: str, current_resume: List[Document], llm: Ollama) -> tuple:
    """
    Generates an optimized resume with additional relevant keywords and provides analysis metrics.
    """
    # Extract text from resume documents
    resume_text = extract_resume_text(current_resume)
    
    # Get keyword analysis and suggestions
    keyword_analysis = extract_and_suggest_keywords(job_description, resume_text, llm)
    
    # Create and execute the optimization chain
    prompt = create_resume_prompt()
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Generate optimized resume
    response = chain.run(
        job_description=job_description,
        current_resume=resume_text,
        suggested_keywords=", ".join(keyword_analysis["top_22_keywords"] + keyword_analysis["additional_10_keywords"])
    )
    
    # Analyze final keyword matching
    final_analysis = analyze_keywords(job_description, response)
    
    # Combine analyses
    combined_analysis = {
        "original_metrics": {
            "total_keywords": keyword_analysis["original_total_keywords"],
            "matched_keywords": keyword_analysis["original_matched_keywords"],
            "match_percentage": keyword_analysis["original_match_percentage"]
        },
        "final_metrics": final_analysis,
        "top_22_keywords": keyword_analysis["top_22_keywords"],
        "additional_10_keywords": keyword_analysis["additional_10_keywords"]
    }
    
    return response, combined_analysis

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
                # [Previous resume generation code remains the same until after displaying the download button]
                
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
                    optimized_resume, combined_analysis = generate_resume(
                        job_description, split_docs, llm
                    )

                    # Display results
                    st.success("✅ Resume optimization complete!")
                    
                    # Display metrics
                    st.markdown("### 📊 Optimization Metrics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original Metrics**")
                        st.metric(
                            "Initial Keyword Match Rate",
                            f"{combined_analysis['original_metrics']['match_percentage']}%"
                        )
                        st.metric(
                            "Initial Keywords Matched",
                            combined_analysis['original_metrics']['matched_keywords']
                        )
                    
                    with col2:
                        st.markdown("**Final Metrics**")
                        st.metric(
                            "Final Keyword Match Rate",
                            f"{combined_analysis['final_metrics']['match_percentage']}%"
                        )
                        st.metric(
                            "Final Keywords Matched",
                            combined_analysis['final_metrics']['matched_keywords']
                        )
                    
                    # Display top 22 keywords from job description
                    st.markdown("### 🔑 Top 22 Keywords from Job Description")
                    st.write(", ".join(combined_analysis["top_22_keywords"]))
                    
                    # Display additional 10 suggested keywords
                    st.markdown("### 🌟 Additional 10 Suggested Keywords")
                    st.write(", ".join(combined_analysis["additional_10_keywords"]))
                    
                    # Display optimized resume
                    st.markdown("### 📄 Optimized Resume")
                    st.markdown(optimized_resume)

                    # Download button for resume
                    st.download_button(
                        "📥 Download Optimized Resume",
                        optimized_resume,
                        file_name="optimized_resume.txt",
                        mime="text/plain"
                    )

                    # Add cover letter section
                    st.markdown("### 📝 Cover Letter Generation")
                    generate_cover = st.checkbox("Would you like to generate a matching cover letter?")
                    
                    if generate_cover:
                        with st.spinner("🔄 Generating your cover letter..."):
                            cover_letter = generate_cover_letter(
                                job_description, 
                                optimized_resume,
                                llm
                            )
                            
                            st.markdown("### 📋 Generated Cover Letter")
                            st.markdown(cover_letter)
                            
                            # Download button for cover letter
                            st.download_button(
                                "📥 Download Cover Letter",
                                cover_letter,
                                file_name="cover_letter.txt",
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
