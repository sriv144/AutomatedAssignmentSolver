📚 IITM Assignment Scraper
IITM Assignment Scraper is a Python-based automation tool designed to streamline the process of completing practice assignments on the IITM Online Degree platform. It scrapes questions, generates answers using the Gemini API, and automatically fills them into the platform, supporting subjects like System Commands and Modern Application Development I.

✨ Features

Subject & Week Selection: Choose from predefined subjects and specify the week number for targeted assignment scraping.
Automated Navigation: Seamlessly navigates the IITM platform to locate and access practice assignments.
Question Scraping: Extracts questions from assignment pages and saves them to questions_only.txt.
Answer Generation: Leverages the Gemini API to generate accurate answers, saved to assignment_answers.txt.
Answer Submission: Automatically fills answers for various question types (multiple-choice, text, matching) and submits them.
Robust Error Handling: Includes detailed logging (scraper.log) and retry mechanisms for reliable operation.
Chrome Profile Integration: Uses a specific Chrome profile for streamlined authentication via Google Sign-In.


⚙️ Installation

Clone the Repository:
git clone https://github.com/your-username/iitm-assignment-scraper.git
cd iitm-assignment-scraper


Set Up Python Environment:The project is preferred to run with Python 3.8 or higher. It is recommended to use a virtual environment.
# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


Install Dependencies:First, upgrade pip to avoid potential issues.
python -m pip install --upgrade pip
pip install -r requirements.txt

Key dependencies include selenium, webdriver-manager, psutil, python-dotenv, and google-generativeai.

Set Up Environment Variables:Create a .env file in the project root and add:
GEMINI_API_KEY=your_gemini_api_key_here
CHROME_USER_DATA_DIR=C:/Users/YourUsername/AppData/Local/Google/Chrome/User Data


Install ChromeDriver:The script uses webdriver-manager to automatically install ChromeDriver. Alternatively, download it manually from chromedriver.chromium.org and place it in the project directory as chromedriver.exe.



▶️ Usage

Run the Script:Start the automation process by running the main script.
python main1.py


Follow Prompts:

Select a subject from the list (e.g., system commands or modern application development i).
Enter the week number for the practice assignment (e.g., 1 for Week 1).


Script Execution:The script will:

Terminate existing Chrome processes to prevent conflicts.
Launch Chrome with the specified profile (Profile 2).
Log in to the IITM platform via Google Sign-In.
Navigate to the selected course and week’s practice assignment.
Scrape questions and save them to questions_only.txt.
Generate answers using the Gemini API and save them to assignment_answers.txt.
Fill and submit answers on the platform.

Output Files:

questions_only.txt: Extracted assignment questions.
assignment_answers.txt: Generated answers.
scraper.log: Detailed logs for debugging.
practice_page_source.html: Full page source for troubleshooting.
practice_pre_xpath_page_source.html: Page source before XPath extraction.
practice_question_dom.txt: DOM of question elements.


Post-Execution:The browser remains open for manual verification after submission. Press Ctrl+C to close it.



📚 Project Structure

main1.py: The core script handling navigation, scraping, answer generation, and submission.
requirements.txt: Lists the Python libraries required to run the project.
README.md: This file, providing an overview and instructions for the project.
.env: Configuration file for storing the Gemini API key and Chrome user data directory (not tracked in git).
scraper.log: Log file generated during execution for debugging.
questions_only.txt: Output file containing scraped questions.
assignment_answers.txt: Output file containing generated answers.
practice_page_source.html: Saved HTML of the assignment page.
practice_pre_xpath_page_source.html: HTML before XPath processing.
practice_question_dom.txt: DOM of scraped question elements.


🛠️ Configuration

Subject Mapping: Update the SUBJECT_MAPPING dictionary in main1.py to include additional subjects or modify existing ones.
Chrome Profile: Modify CHROME_USER_DATA_DIR and --profile-directory in main1.py to match your Chrome setup.
Logging: Adjust the logging level in logging.basicConfig within main1.py for more or less verbose output.


🩺 Troubleshooting

ChromeDriver Issues: Ensure Chrome and ChromeDriver versions match. Update Chrome or download the correct ChromeDriver.
Gemini API Errors: Verify the GEMINI_API_KEY in .env. Check API quotas and permissions.
Navigation Failures: Review scraper.log for errors. Confirm the subject ID and week number are correct.
Question Type Mismatches: The script assumes specific question types (e.g., Q1 is multiselect, Q4/Q8 are text inputs). Update the answer-filling logic in main1.py for different formats.


🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m "Add YourFeature").
Push to the branch (git push origin feature/YourFeature).
Open a pull request.


📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

⚠️ Disclaimer
This script is intended for educational purposes to assist with practice assignments. Ensure compliance with the IITM Online Degree platform's terms of service. Misuse may violate academic integrity policies.
