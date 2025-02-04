from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openai
import os
import re
from bs4 import BeautifulSoup

# Temporary hardcoded OpenAI API Key for testing
openai.api_key = "your_openai_api_key_here"

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
    
    # Print raw scraped data (for debugging)
    # print("\n=== Raw Scraped Page Text ===")
    # print(page_text[:2500])  # Print first 2500 chars only
    # print("===========================\n")
    
    # Send full page text to OpenAI for structured extraction
    prompt = f"""
    Extract structured information from the following job posting:
    
    {page_text}
    
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
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract structured job details."},
                  {"role": "user", "content": prompt}]
    )
    
    extracted_data = response["choices"][0]["message"]["content"].strip()
    
    # Convert structured text into a dictionary
    job_details_dict = {}
    for line in extracted_data.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            job_details_dict[key.strip()] = value.strip()
    
    # Store extracted details in separate variables for easy access
    job_position = job_details_dict.get("Job Position", "Unknown")
    company_name = job_details_dict.get("Company Name", "Unknown")
    specific_job_project = job_details_dict.get("Specific Job Project", "Unknown")
    required_it_skills = job_details_dict.get("Required IT Skills", "Unknown")
    job_type = job_details_dict.get("Job Type", "Unknown")
    remote_work = job_details_dict.get("Remote Work", "Unknown")
    job_description_summary = job_details_dict.get("Job Description Summary", "Unknown")
    perks_summary = job_details_dict.get("Perks Summary", "Unknown")
    
    return {
        "Job Position": job_position,
        "Company Name": company_name,
        "Specific Job Project": specific_job_project,
        "Required IT Skills": required_it_skills,
        "Job Type": job_type,
        "Remote Work": remote_work,
        "Job Description Summary": job_description_summary,
        "Perks Summary": perks_summary
    }

# Example usage
if __name__ == "__main__":
    job_url = "https://www.ziprecruiter.com/c/2002-United-Services-Automobile-Asn/Job/Data-Scientist-Intermediate-level/-in-Charlotte,NC?jid=c327f1daa48d5aef"
    job_details = extract_job_details(job_url)
    
    if job_details:
        print("\nExtracted Job Details:")
        for key, value in job_details.items():
            print(f"{key}: {value}")
