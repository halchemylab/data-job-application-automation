from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
import os
import re
import csv
import json
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from dotenv import load_dotenv
from datetime import datetime
from src.config import PROJECT_ROOT
from src.logger import logger

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

from selenium.common.exceptions import WebDriverException
from openai import APIError

def extract_job_details(url):
    """Scrapes job details from a given URL using Selenium and extracts structured information using OpenAI API."""
    try:
        options = Options()
        options.headless = True  # Runs browser in headless mode (no UI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        page_text = driver.page_source  # Get full rendered page source
        driver.quit()
    except WebDriverException as e:
        logger.error(f"Error with Selenium WebDriver: {e}")
        return None
    
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
    Extract structured information from the following job posting and return it as a JSON object.

    {minimized_text}

    ### **JSON Schema**
    {{
      "Job Position": "string",
      "Company Name": "string",
      "Specific Job Project": "string",
      "Required IT Skills": "string (comma-separated)",
      "Job Type": "string (e.g., Full-Time, Part-Time, Contract)",
      "Remote Work": "string (Yes/No)",
      "Job Description Summary": "string (1-2 sentences)",
      "Perks Summary": "string (1-2 sentences)"
    }}

    If a value is not found, use "Unknown".
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an expert in extracting job details and returning them as a valid JSON object."},
                {"role": "user", "content": prompt}
            ]
        )
    except APIError as e:
        logger.error(f"Error with OpenAI API: {e}")
        return None

    try:
        extracted_data = response.choices[0].message.content
        job_details_dict = json.loads(extracted_data)
    except (json.JSONDecodeError, IndexError) as e:
        logger.error(f"Failed to parse JSON response from OpenAI: {e}")
        logger.debug(f"Invalid JSON response: {extracted_data}")
        return None

    return job_details_dict

def save_job_to_csv(job_details, url, csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(PROJECT_ROOT, 'data', 'tracker.csv')
    try:
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
    except (IOError, OSError) as e:
        logger.error(f"Error writing to CSV file: {e}")
