
import pytest
from unittest import mock
from src.core.scraper import extract_job_details
import json

# Mock the selenium webdriver and the OpenAI client
@mock.patch('src.core.scraper.webdriver.Chrome')
@mock.patch('src.core.scraper.client.chat.completions.create')
def test_extract_job_details_with_json_response(mock_openai_create, mock_chrome):
    # 1. Setup the mock for Selenium
    mock_driver_instance = mock_chrome.return_value
    mock_driver_instance.page_source = "<html><body>Mocked job description to be processed.</body></html>"

    # 2. Setup the mock for the OpenAI API response
    mock_completion = mock.Mock()
    mock_message = mock.Mock()
    
    expected_dict = {
        "Job Position": "Software Engineer",
        "Company Name": "Gemini",
        "Specific Job Project": "Building a world-class AI assistant",
        "Required IT Skills": "Python, AI, Machine Learning",
        "Job Type": "Full-Time",
        "Remote Work": "Yes",
        "Job Description Summary": "Join our team to build the future of AI.",
        "Perks Summary": "Competitive salary, great benefits, and a chance to work on cutting-edge technology."
    }
    
    # The response from the API is a JSON string
    mock_message.content = json.dumps(expected_dict)
    mock_completion.choices = [mock.Mock(message=mock_message)]
    mock_openai_create.return_value = mock_completion
    
    # 3. Call the function with a dummy URL
    job_details = extract_job_details("http://example-job-board.com")

    # 4. Assert that the function returns the expected dictionary
    assert job_details == expected_dict
    
    # 5. Verify that the mocks were called as expected
    mock_chrome.assert_called_once()
    mock_openai_create.assert_called_once()
