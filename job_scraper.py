from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
import os
import re
import csv
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OpenAI API key not found. Make sure to set it in a .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Download stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def extract_job_details(url):
    """Scrapes job details from a given URL using Selenium and extracts structured information using OpenAI API."""
    options = Options()
    options.headless = True  # Runs browser in headless mode (no UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    page_text = driver.page_source  # Get full rendered page source
    driver.quit()
    
    # Parse the page with BeautifulSoup to extract readable text
    soup = BeautifulSoup(page_text, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    
    # Remove excessive new lines and blank spaces
    page_text = "\n".join([line.strip() for line in page_text.split("\n") if line.strip()])
    
    # Remove stop words to minimize text size
    words = page_text.split()
    minimized_text = ' '.join([word for word in words if word.lower() not in stop_words])
    
    # Limit character count to avoid unnecessary OpenAI token usage
    max_chars = 8000  # Limit input to 8000 characters
    minimized_text = minimized_text[:max_chars]
    
    # Send filtered text to OpenAI for structured extraction
    prompt = f"""
    Extract structured information from the following job posting:
    
    {minimized_text}

    ### **Response Formatting Guidelines**

    - **Use the exact format below.**
    - **Do not add any extra text or explanations.**
    - **Ensure each field is formatted as: `- **Field Name**: Value`**
    - **Field names must be exactly as given below.**
    - **If information is missing, write "Unknown". Do NOT modify field names.**

    ### **Response Format (Example)**
    - **Job Position**: Software Engineer
    - **Company Name**: Google
    - **Specific Job Project**: Developing cloud-based AI solutions
    - **Required IT Skills**: Python, TensorFlow, Cloud Computing
    - **Job Type**: Full-Time
    - **Remote Work**: Yes
    - **Job Description Summary**: You will design and develop scalable machine learning applications.
    - **Perks Summary**: Competitive salary, stock options, remote work options, and health benefits.

    Now, extract details from the job posting and follow the exact format above.

    Provide the following details:
    - Job Position
    - Company Name
    - Specific Job Project (What the role is focused on)
    - Required IT Skills (comma-separated)
    - Job Type (Full Time, Part Time, Contract, etc.)
    - Remote Work (Yes/No)
    - 1-2 sentence Job Description Summary
    - 1-2 sentence Perks Summary
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract structured job details."},
                  {"role": "user", "content": prompt}]
    )

    extracted_data = response.choices[0].message.content.strip()
    
    # Convert structured text into a dictionary
    job_details_dict = {}
    for line in extracted_data.split("\n"):
        line = line.strip()
        match = re.match(r"^\s*-?\s*\*\*(.+?)\*\*:\s*(.+)$", line)
        
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            job_details_dict[key] = value
        else:
            print(f"Failed to match line: {line}")

    return job_details_dict

def save_job_to_csv(job_details, url, csv_path='data/tracker.csv'):
    file_exists = os.path.isfile(csv_path)
    
    headers = [
        "Status", "Date Applied", "URL", "Company Name", "Job Position", 
        "Specific Job Project", "Required IT Skills", "Job Type", 
        "Remote Work", "Job Description Summary", "Perks Summary", 
        "Notes/Feedback"
    ]
    
    row = [
        "",  # Status
        datetime.now().strftime("%Y-%m-%d"),  # Date Applied
        url,
        job_details.get("Company Name", "Unknown"),
        job_details.get("Job Position", "Unknown"),
        job_details.get("Specific Job Project", "Unknown"),
        job_details.get("Required IT Skills", "Unknown"),
        job_details.get("Job Type", "Unknown"),
        job_details.get("Remote Work", "Unknown"),
        job_details.get("Job Description Summary", "Unknown"),
        job_details.get("Perks Summary", "Unknown"),
        ""  # Notes/Feedback
    ]
    
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)

if __name__ == "__main__":
    job_url = "https://www.ziprecruiter.com/c/2002-United-Services-Automobile-Asn/Job/Data-Scientist-Intermediate-level/-in-Charlotte,NC?jid=c327f1daa48d5aef"
    job_details = extract_job_details(job_url)
    
    if job_details:
        print("\nExtracted Job Details:")
        for key, value in job_details.items():
            print(f"{key}: {value}")
        
        save_job_to_csv(job_details, job_url)
        print("\nJob details saved to data/tracker.csv")

