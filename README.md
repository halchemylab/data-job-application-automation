# Job-Application-Automation-Tool

## 🚀 Project Summary

The **Job Application Automation Tool** is designed to streamline and simplify the job application process. By automating key steps such as customizing resumes and cover letters, organizing files, and tracking applications, this tool enhances efficiency for job seekers.

## ✨ Features

### 📄 Resume and Cover Letter Customization
- Uses **Natural Language Processing (NLP)** to extract key skills and requirements from job descriptions.
- Customizes predefined resume and cover letter templates to match job postings.

### 📁 File Management
- Automatically creates organized folders for each job application.
- Stores customized resumes and cover letters efficiently.

### 📊 Application Tracker
- Maintains a **CSV-based tracker** to log job applications.
- Records details such as job titles, company names, application status, and feedback.

### 🎨 Streamlit Interface
- Provides a user-friendly **Streamlit-based** web interface.
- Enables easy input of job descriptions, selection of templates, and application management.

## 📂 Proposed File Structure

```
job_application_tool/
├── app/                      # Main application code
│   ├── main.py               # Streamlit app entry point
│   ├── resume_templates/     # Directory for resume templates
│   │   ├── template1.docx
│   │   └── template2.docx
│   ├── cover_letter_templates/  # Directory for cover letter templates
│   │   ├── template1.docx
│   │   └── template2.docx
│   ├── utils/                # Helper functions
│   │   ├── file_manager.py   # File and folder management
│   │   ├── nlp_processor.py  # NLP processing for job descriptions
│   │   ├── tracker.py        # Functions to update CSV tracker
│   │   ├── notification.py   # Twilio SMS notifications
│   │   └── scheduler.py      # Follow-up scheduling
│   ├── data/                 # Data storage
│   │   ├── application_tracker.csv  # CSV file to track applications
│   └── static/               # Static assets (if any)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🛠️ Technologies Used
- **Python** (Core functionality)
- **Streamlit** (User Interface)
- **OpenAI API** (Natural Language Processing)
- **Pandas** (Data tracking and management)
- **Docx** (Template handling)
- **CSV** (Application tracking)

## 🎯 Future Enhancements
- ✅ AI-powered resume and cover letter creation.
- ✅ Automated job search tracking.
- ✅ Integration with job boards (LinkedIn, Indeed).
- ✅ Email automation for follow-ups.

## 💡 Contribution
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License
This project is licensed under the MIT License.

## 🚀 Happy Job Hunting!