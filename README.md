---
license: mit
title: Cumstomized Resume Builder
sdk: streamlit
emoji: 📈
colorFrom: yellow
colorTo: red
pinned: true
---
# FFA Key If you dont have one
If You Dont have a Groq API key then i have created a Free For All groq key so that anyone can use this project. But its recommended to use your own key.

```"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"```

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
- Groq (LLama3)
- PyPDF2
- python-dotenv

# USAGE 📝

To use the Deployed Version of Custom Resume Builder visit [https://huggingface.co/spaces/AAkshatSharmaa/customizeyourresume].

1. Use the Groq API key if you dont have one then I have provided one for you
   
```"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"```

2. Paste the job description

3. Upload your current resume (PDF format)

4. Click to generate your optimized resume

5. Optionally generate a matching cover letter

5. Download your optimized documents

6. Or Copy the desired points given by the application to your custom resume

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
Check the updated requirements.txt
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support, please open an issue in the GitHub repository or contact [sharma.akshat0410@gmail.com] or at [https://www.linkedin.com/in/impact-by-akshat-sharma/].

## Acknowledgments 🙏

- LangChain for the excellent LLM framework
- Streamlit for the amazing web interface
- Groq for providing the LLM capabilities

## Note ⚠️

This tool is designed to assist in resume optimization but should not replace human judgment. Always review and verify the generated content before using it in your job applications.
