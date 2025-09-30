# Data Job Application Automation

## 🚀 Project Summary

The **Data Job Application Automation Tool** is a desktop application designed to streamline the job application process. It uses AI to extract key details from a job posting URL, and then uses that information to generate a customized resume and cover letter from your templates.

## ✨ Features

-   **Web Scraping:** Extracts job details (position, company, skills, etc.) from a provided URL using **Selenium**.
-   **AI-Powered Data Extraction:** Uses **OpenAI (gpt-4o-mini)** to parse the scraped text and extract structured information.
-   **Document Generation:** Populates your `.docx` resume and cover letter templates with the extracted job details.
-   **File Organization:** Automatically creates a new folder for each application, containing the customized documents.
-   **Application Tracking:** Appends a record of each scraped job to a central `tracker.csv` file.
-   **Simple UI:** Provides a user-friendly interface built with **Tkinter**.

## 🛠️ Technologies Used

-   **Python**
-   **Tkinter** for the GUI
-   **Selenium** for web scraping
-   **OpenAI API** for data extraction
-   **python-docx** for Word document manipulation

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd data-job-application-automation
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Create a copy of the `.env.example` file and name it `.env`.
    -   Open the `.env` file and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ```

## ▶️ How to Run

Once you have completed the setup, run the following command in your terminal to start the application:

```bash
python app.py
```

## 💡 Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License

This project is licensed under the MIT License.