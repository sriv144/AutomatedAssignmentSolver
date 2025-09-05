<readme>
    <title>IITM Online Degree Assignment Scraper</title>

    <section name="Overview">
        <content>
            This Python script automates the process of scraping practice assignment questions from the IITM Online Degree platform, generating answers using the Gemini API, and filling them back into the platform. It supports specific subjects like "System Commands" and "Modern Application Development I" and handles various question types, including multiple-choice, text input, and matching questions.
        </content>
    </section>

    <section name="Features">
        <content>
            - **Subject Selection**: Choose from predefined subjects (e.g., System Commands, Modern Application Development I).
            - **Week Navigation**: Automatically navigates to the specified week's practice assignment.
            - **Question Scraping**: Extracts questions from the practice assignment page and saves them to `questions_only.txt`.
            - **Answer Generation**: Uses the Gemini API to generate answers for the scraped questions, saved to `assignment_answers.txt`.
            - **Automated Answer Filling**: Fills answers on the platform, supporting multiple-choice, text input, and matching question formats.
            - **Error Handling**: Robust logging and error recovery for navigation, scraping, and API interactions.
            - **Chrome Profile Support**: Uses a specific Chrome profile for seamless authentication.
        </content>
    </section>

    <section name="Prerequisites">
        <content>
            - Python 3.8 or higher
            - Google Chrome browser installed
            - ChromeDriver compatible with your Chrome version (or use `webdriver-manager` to auto-install)
            - A valid Gemini API key (stored in a `.env` file)
            - Required Python packages (listed in `requirements.txt`)
        </content>
    </section>

    <section name="Installation">
        <content>
            <step number="1">
                <title>Clone the Repository</title>
                <command>
                    git clone https://github.com/your-username/iitm-assignment-scraper.git
                    cd iitm-assignment-scraper
                </command>
            </step>
            <step number="2">
                <title>Set Up a Virtual Environment</title>
                <description>(optional but recommended)</description>
                <command>
                    python -m venv venv
                    source venv/bin/activate  # On Windows: venv\Scripts\activate
                </command>
            </step>
            <step number="3">
                <title>Install Dependencies</title>
                <command>
                    pip install -r requirements.txt
                </command>
            </step>
            <step number="4">
                <title>Set Up Environment Variables</title>
                <description>Create a `.env` file in the project root and add:</description>
                <command>
                    GEMINI_API_KEY=your_gemini_api_key_here
                    CHROME_USER_DATA_DIR=C:/Users/YourUsername/AppData/Local/Google/Chrome/User Data
                </command>
            </step>
            <step number="5">
                <title>Ensure ChromeDriver</title>
                <description>
                    The script uses `webdriver-manager` to download ChromeDriver automatically. Alternatively, download ChromeDriver manually from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads) and place it in the project directory as `chromedriver.exe`.
                </description>
            </step>
        </content>
    </section>

    <section name="Usage">
        <content>
            <step number="1">
                <title>Run the Script</title>
                <command>
                    python main1.py
                </command>
            </step>
            <step number="2">
                <title>Follow Prompts</title>
                <description>
                    - Select a subject from the provided list (e.g., `system commands`).
                    - Enter the week number for the practice assignment (e.g., `1` for Week 1).
                </description>
            </step>
            <step number="3">
                <title>Script Execution</title>
                <description>
                    The script will:
                    - Close existing Chrome processes to avoid conflicts.
                    - Launch Chrome with the specified profile (`Profile 2`).
                    - Log in to the IITM Online Degree platform via Google Sign-In.
                    - Navigate to the selected course and week.
                    - Scrape practice assignment questions.
                    - Generate answers using the Gemini API.
                    - Fill and submit answers on the platform.
                </description>
                <output-files>
                    - `questions_only.txt`: Extracted questions.
                    - `assignment_answers.txt`: Generated answers.
                    - `scraper.log`: Detailed logs for debugging.
                    - `practice_page_source.html`: Page source for troubleshooting.
                    - `practice_pre_xpath_page_source.html`: Page source before XPath extraction.
                    - `practice_question_dom.txt`: DOM of question elements.
                </output-files>
            </step>
            <step number="4">
                <title>Post-Execution</title>
                <description>
                    The browser remains open after submission for manual verification. Press `Ctrl+C` to close the browser.
                </description>
            </step>
        </content>
    </section>

    <section name="Requirements">
        <content>
            Create a `requirements.txt` file with the following dependencies:
            ```plaintext
            selenium==4.9.0
            webdriver-manager==4.0.0
            psutil==5.9.5
            python-dotenv==1.0.0
            google-generativeai==0.3.2
            ```
            Install them using:
            ```bash
            pip install -r requirements.txt
            ```
        </content>
    </section>

    <section name="Configuration">
        <content>
            - **Subject Mapping**: Modify the `SUBJECT_MAPPING` dictionary in `main1.py` to add or update subjects and their corresponding URL identifiers.
            - **Chrome Profile**: Adjust the `CHROME_USER_DATA_DIR` and `--profile-directory` in the script to match your Chrome setup.
            - **Logging**: Logs are saved to `scraper.log` for debugging. Adjust the logging level in `logging.basicConfig` if needed.
        </content>
    </section>

    <section name="Troubleshooting">
        <content>
            - **ChromeDriver Issues**: Ensure Chrome and ChromeDriver versions match. Update Chrome or download the correct ChromeDriver version.
            - **Gemini API Errors**: Verify your `GEMINI_API_KEY` in the `.env` file. Check API quotas and permissions.
            - **Navigation Failures**: Check `scraper.log` for detailed errors. Ensure the subject ID and week number are correct.
            - **Question Type Mismatches**: The script assumes specific question types (e.g., Q1 is multiselect, Q4/Q8 are text inputs). Adjust the answer-filling logic in `main1.py` for different question formats.
        </content>
    </section>

    <section name="Contributing">
        <content>
            Contributions are welcome! Please:
            1. Fork the repository.
            2. Create a feature branch (`git checkout -b feature/YourFeature`).
            3. Commit your changes (`git commit -m "Add YourFeature"`).
            4. Push to the branch (`git push origin feature/YourFeature`).
            5. Open a pull request.
        </content>
    </section>

    <section name="License">
        <content>
            This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
        </content>
    </section>

    <section name="Disclaimer">
        <content>
            This script is intended for educational purposes to assist with practice assignments. Ensure compliance with the IITM Online Degree platform's terms of service. Misuse may violate academic integrity policies.
        </content>
    </section>
</readme>
