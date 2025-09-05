IITM Online Degree Assignment Scraper
Overview
This Python script automates the process of scraping practice assignment questions from the IITM Online Degree platform, generating answers using the Gemini API, and filling them back into the platform. It supports specific subjects like "System Commands" and "Modern Application Development I" and handles various question types, including multiple-choice, text input, and matching questions.
Features

Subject Selection: Choose from predefined subjects (e.g., System Commands, Modern Application Development I).
Week Navigation: Automatically navigates to the specified week's practice assignment.
Question Scraping: Extracts questions from the practice assignment page and saves them to questions_only.txt.
Answer Generation: Uses the Gemini API to generate answers for the scraped questions, saved to assignment_answers.txt.
Automated Answer Filling: Fills answers on the platform, supporting multiple-choice, text input, and matching question formats.
Error Handling: Robust logging and error recovery for navigation, scraping, and API interactions.
Chrome Profile Support: Uses a specific Chrome profile for seamless authentication.

Prerequisites

Python 3.8 or higher
Google Chrome browser installed
ChromeDriver compatible with your Chrome version (or use webdriver-manager to auto-install)
A valid Gemini API key (stored in a .env file)
Required Python packages (listed in requirements.txt)

Installation

Clone the Repository:
git clone https://github.com/your-username/iitm-assignment-scraper.git
cd iitm-assignment-scraper


Set Up a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:

Create a .env file in the project root.
Add your Gemini API key and Chrome user data directory (optional):GEMINI_API_KEY=your_gemini_api_key_here
CHROME_USER_DATA_DIR=C:/Users/YourUsername/AppData/Local/Google/Chrome/User Data




Ensure ChromeDriver:

The script will attempt to use webdriver-manager to download ChromeDriver automatically.
Alternatively, download ChromeDriver manually from chromedriver.chromium.org and place it in the project directory as chromedriver.exe.



Usage

Run the Script:
python main1.py


Follow Prompts:

Select a subject from the provided list (e.g., system commands).
Enter the week number for the practice assignment (e.g., 1 for Week 1).


Script Execution:

The script will:
Close existing Chrome processes to avoid conflicts.
Launch Chrome with the specified profile (Profile 2).
Log in to the IITM Online Degree platform via Google Sign-In.
Navigate to the selected course and week.
Scrape practice assignment questions.
Generate answers using the Gemini API.
Fill and submit answers on the platform.


Output files:
questions_only.txt: Extracted questions.
assignment_answers.txt: Generated answers.
scraper.log: Detailed logs for debugging.
practice_page_source.html and practice_pre_xpath_page_source.html: Page source for troubleshooting.
practice_question_dom.txt: DOM of question elements.




Post-Execution:

The browser remains open after submission for manual verification.
Press Ctrl+C to close the browser.



Requirements
Create a requirements.txt file with the following dependencies:
selenium==4.9.0
webdriver-manager==4.0.0
psutil==5.9.5
python-dotenv==1.0.0
google-generativeai==0.3.2

Install them using:
pip install -r requirements.txt

Configuration

Subject Mapping: Modify the SUBJECT_MAPPING dictionary in main1.py to add or update subjects and their corresponding URL identifiers.
Chrome Profile: Adjust the CHROME_USER_DATA_DIR and --profile-directory in the script to match your Chrome setup.
Logging: Logs are saved to scraper.log for debugging. Adjust the logging level in logging.basicConfig if needed.

Troubleshooting

ChromeDriver Issues: Ensure Chrome and ChromeDriver versions match. Update Chrome or download the correct ChromeDriver version.
Gemini API Errors: Verify your GEMINI_API_KEY in the .env file. Check API quotas and permissions.
Navigation Failures: Check scraper.log for detailed errors. Ensure the subject ID and week number are correct.
Question Type Mismatches: The script assumes specific question types (e.g., Q1 is multiselect, Q4/Q8 are text inputs). Adjust the answer-filling logic in main1.py for different question formats.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m "Add YourFeature").
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Disclaimer
This script is intended for educational purposes to assist with practice assignments. Ensure compliance with the IITM Online Degree platform's terms of service. Misuse may violate academic integrity policies.
