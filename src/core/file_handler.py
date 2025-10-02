import os
import csv
from datetime import datetime
from src.config import PROJECT_ROOT
from src.logger import logger

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
    except PermissionError as e:
        logger.error(f"Permission error while writing to CSV file: {e}")
    except IOError as e:
        logger.error(f"I/O error while writing to CSV file: {e}")
    except OSError as e:
        logger.error(f"OS error while writing to CSV file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while writing to the CSV file: {e}")