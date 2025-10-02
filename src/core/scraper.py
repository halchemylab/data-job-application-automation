from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from src.logger import logger
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidArgumentException

# Download stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def scrape_job_posting(url):
    """Scrapes job details from a given URL using Selenium."""
    try:
        options = Options()
        options.headless = True  # Runs browser in headless mode (no UI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        page_text = driver.page_source  # Get full rendered page source
        driver.quit()
    except InvalidArgumentException:
        logger.error(f"Invalid URL provided: {url}")
        return None
    except TimeoutException:
        logger.error(f"Timeout while trying to load URL: {url}")
        return None
    except WebDriverException as e:
        logger.error(f"Error with Selenium WebDriver: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during scraping: {e}")
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
    
    return minimized_text
