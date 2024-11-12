# Custom Resume Generator with GenAI

This project is a Custom Resume Generator application that optimizes resumes based on specific job descriptions, improving Applicant Tracking System (ATS) compatibility and relevance for each role. Built using Streamlit and LangChain with Llama3.2 from Ollama, the application enables job seekers to create a highly targeted and professional resume.

## Features

- **Job Description Analysis**: Extracts relevant skills, qualifications, and keywords from the provided job description.
- **Resume Parsing**: Loads an existing PDF resume, analyzes it, and extracts the text for further processing.
- **ATS Optimization**: Reformats resumes to meet ATS requirements, enhancing the likelihood of being shortlisted.
- **Harvard Achievement Format**: Rewrites experience bullet points using an impact-driven style, focusing on quantifiable outcomes.
- **Resume Summary**: Generates a brief summary highlighting optimizations and potential ATS score improvements.

## How It Works

### Input:
- **Job Description**: A text area where the user pastes the job description for which they want to tailor their resume.
- **Current Resume**: Upload the resume as a PDF file.

### Processing:
- **Resume Parsing**: The app parses and extracts content from the PDF resume using `PyPDFLoader`.
- **Text Splitting**: Text is split into chunks for easier processing using LangChain's `RecursiveCharacterTextSplitter`.
- **LLM Processing**: A custom LLM chain leverages the Ollama model and generates an optimized resume in ATS-friendly format based on the job description.

### Output:
- Displays the optimized resume and summarizes key changes made for ATS improvements.

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- LangChain
- Ollama for the Llama model
- dotenv for managing environment variables

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/custom-resume-generator.git
   cd custom-resume-generator
