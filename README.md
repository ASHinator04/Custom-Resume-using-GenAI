# AI-Powered Resume Optimizer 🚀

An advanced resume optimization tool that uses AI to create ATS-optimized resumes and cover letters tailored to specific job descriptions. Built with Streamlit and LangChain, this application helps job seekers improve their resume's compatibility with Applicant Tracking Systems (ATS).

## Features 🌟

- **Resume Analysis**: Analyzes your current resume against job descriptions
- **Keyword Optimization**: Identifies and suggests relevant keywords from the job description
- **ATS Optimization**: Reformats content for better ATS compatibility
- **Cover Letter Generation**: Creates matching cover letters
- **Detailed Metrics**: Shows before/after keyword matching statistics
- **Easy Export**: Download optimized resumes and cover letters as text files

## Tech Stack 💻

- Python 3.x
- Streamlit
- LangChain
- Ollama (LLama3.2)
- PyPDF2
- python-dotenv

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-optimizer.git
cd resume-optimizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```env
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Custom_Resume_With_GenAI
```

## Usage 📝

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload your current resume (PDF format)

4. Paste the job description

5. Click to generate your optimized resume

6. Optionally generate a matching cover letter

7. Download your optimized documents

## Core Components 🔧

### Resume Optimization

- Analyzes existing resume content
- Extracts key technical keywords
- Suggests additional relevant keywords
- Reformats content using STAR+Impact method
- Optimizes for ATS compatibility

### Cover Letter Generation

- Creates customized cover letters
- Matches job description requirements
- Highlights relevant achievements
- Maintains professional tone

### Metrics and Analysis

- Original keyword match rate
- Optimized keyword match rate
- Top keywords from job description
- Additional suggested keywords

## Code Structure 📂

```
resume-optimizer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
└── README.md            # Project documentation
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Requirements 📋

```txt
streamlit
langchain
langchain-community
python-dotenv
PyPDF2
ollama
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support, please open an issue in the GitHub repository or contact [your-email@example.com].

## Acknowledgments 🙏

- LangChain for the excellent LLM framework
- Streamlit for the amazing web interface
- Ollama for providing the LLM capabilities

## Note ⚠️

This tool is designed to assist in resume optimization but should not replace human judgment. Always review and verify the generated content before using it in your job applications.
