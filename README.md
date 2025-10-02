# Data Job Application Automation

## 🚀 Project Summary

The **Data Job Application Automation Tool** is a desktop application designed to streamline the job application process. It uses AI to extract key details from a job posting URL, and then uses that information to generate a customized resume and cover letter from your templates.

## ✨ Features

-   **Web Scraping:** Extracts job details from a provided URL using Selenium.
-   **AI-Powered Data Extraction:** Uses OpenAI (gpt-4o-mini) to parse the scraped text and extract structured information.
-   **Document Generation:** Populates your `.docx` resume and cover letter templates with the extracted job details.
-   **File Organization:** Automatically creates a new folder for each application, containing the customized documents.
-   **Application Tracking:** Appends a record of each scraped job to a central `tracker.csv` file.
-   **Simple UI:** Provides a user-friendly interface built with Tkinter.
-   **Modular Architecture:** The code is organized into distinct modules for scraping, AI interaction, file handling, and UI components, making it easy to maintain and extend.
-   **Robust Error Handling:** Implements comprehensive error handling to provide a stable and reliable user experience.

## 🛠️ Technologies Used

-   **Python**
-   **Tkinter** for the GUI
-   **Selenium** for web scraping
-   **OpenAI API** for data extraction
-   **python-docx** for Word document manipulation
-   **NLTK** for text processing

## Project Structure

The project is organized into the following main directories:

-   `src/core`: Contains the core application logic, including modules for web scraping (`scraper.py`), AI-powered data extraction (`ai_extractor.py`), file handling (`file_handler.py`), and document generation (`generator.py`).
-   `src/gui`: Contains the user interface code, including the main application window (`main_window.py`), UI components (`ui_components.py`), and animations (`animations.py`).
-   `src/config.py`: Contains the application configuration, including UI settings and file paths.
-   `src/logger.py`: Contains the logging configuration.
-   `data`: Contains the `tracker.csv` file for tracking job applications.
-   `static`: Contains the resume and cover letter templates.
-   `output`: Contains the generated resumes and cover letters.

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
