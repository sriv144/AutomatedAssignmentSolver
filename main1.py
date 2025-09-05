import os
import psutil
import time
import logging
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import google.generativeai as genai

# Set up logging
logging.basicConfig(filename="scraper.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# --- Subject Mapping ---
# Mapping of subject names to their URL identifiers
SUBJECT_MAPPING = {
    "system commands": "ns_25t1_se2001",
    "modern application development i": "ns_25t1_cs2003"
}

# --- Step 1: Prompt for Subject and Week Number ---
def get_subject():
    print("Available subjects:")
    for subject in SUBJECT_MAPPING.keys():
        print(f"- {subject}")
    while True:
        subject = input("Enter the subject name (e.g., 'system commands'): ").strip().lower()
        if subject in SUBJECT_MAPPING:
            return subject
        print("Subject not found. Please choose from the available subjects.")

def get_week_number():
    while True:
        try:
            week = int(input("Enter the week number to complete (e.g., 1 for Week 1): "))
            if week <= 0:
                print("Please enter a positive number.")
                continue
            return week
        except ValueError:
            print("Please enter a valid number.")

subject = get_subject()
subject_id = SUBJECT_MAPPING[subject]
week_number = get_week_number()
print(f"🌟 You selected '{subject}' (ID: {subject_id}), Week {week_number}")

# --- Step 2: Close existing Chrome processes ---
def close_chrome_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == 'chrome.exe':
                proc.kill()
                logging.info(f"Closed Chrome process (PID: {proc.info['pid']})")
                print(f"🔴 Closed Chrome process (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(2)

print("🌐 Checking for and closing existing Chrome processes...")
close_chrome_processes()

# --- Step 3: Set up Chrome options ---
chrome_options = Options()
chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR", os.path.expanduser("~/AppData/Local/Google/Chrome/User Data"))
chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
chrome_options.add_argument("--profile-directory=Profile 2")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# --- Step 4: Initialize the driver ---
print("🌐 Launching Chrome with 'Srivaths' profile")
chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
if os.path.exists(chromedriver_path):
    service = Service(chromedriver_path)
    logging.info("Using local chromedriver.exe")
else:
    service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")
    logging.info("Using webdriver-manager to install ChromeDriver")

driver = None
wait = None

try:
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        print(f"❌ Failed to initialize ChromeDriver: {e}")
        print("Please ensure Chrome and ChromeDriver versions match. Try:")
        print("1. Updating Chrome to the latest version.")
        print("2. Running: pip install --upgrade webdriver-manager")
        print("3. Downloading ChromeDriver manually from https://chromedriver.chromium.org/downloads")
        print("4. Placing chromedriver.exe in the project directory.")
        raise

    # --- Step 5–13: Navigate to the practice assignment page ---
    driver.get("chrome://version")
    print("🌐 Checking 'Srivaths' profile")
    driver.get("https://app.onlinedegree.iitm.ac.in/auth/login")
    print("🌐 Portal loaded successfully")
    google_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Sign in with Google')]")
    ))
    google_btn.click()
    print("✅ Google Sign-In clicked")
    driver.switch_to.window(driver.window_handles[0])
    wait.until(EC.url_contains("https://app.onlinedegree.iitm.ac.in/student_dashboard"))
    print("🎉 Successfully logged in!")
    driver.get("https://app.onlinedegree.iitm.ac.in/student_dashboard/current_courses")
    print("🔄 Navigating to Current Courses")
    course_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//a[contains(@href, '{subject_id}')]")
    ))
    course_link.click()
    print(f"✅ '{subject}' course clicked")
    try:
        wait.until(EC.url_contains(subject_id))
        print("🔄 Course page loaded (same or new tab)")
    except TimeoutException:
        print("⚠️ Course page not loaded; checking for new tab")
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            if subject_id in driver.current_url:
                print(f"🔄 Switched to '{subject}' course tab")
            else:
                raise Exception("Failed to load course page or switch to course tab")
        else:
            raise Exception("No new tab opened and course page not loaded")
    week_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(@class, 'units__items-title') and contains(text(), 'Week {week_number}')]")
    ))
    # Scroll to Week link
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", week_link)
    time.sleep(2)
    week_link.click()
    print(f"🔄 Clicked Week {week_number} to open dropdown")

    # Scroll the dropdown container to ensure all subitems are loaded
    try:
        dropdown_container = driver.find_element(By.XPATH, f"//div[contains(@class, 'units__items-title') and contains(text(), 'Week {week_number}')]/following-sibling::div[contains(@class, 'units__subitems-show')]")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dropdown_container)
        time.sleep(2)
        print("🔄 Scrolled Week dropdown to load all subitems")
    except NoSuchElementException:
        print("⚠️ Could not find dropdown container to scroll; proceeding without scrolling")

    # Try multiple XPaths for Practice Assignment link
    practice_xpaths = [
        "//div[contains(@class, 'units__subitems') and contains(.//span, 'Practice Assignment')]",
        f"//div[contains(@class, 'units__subitems') and contains(.//span, 'Practice Assignment - {week_number}')]",
        f"//div[contains(@class, 'units__subitems') and contains(.//span, 'Practice Assignment {week_number}')]"
    ]
    practice_assignment_link = None
    for xpath in practice_xpaths:
        try:
            practice_assignment_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # Scroll to Practice Assignment link
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", practice_assignment_link)
            time.sleep(2)
            print(f"✅ Found Practice Assignment link with XPath: {xpath}")
            break
        except TimeoutException:
            logging.warning(f"XPath not found: {xpath}")
            continue

    if not practice_assignment_link:
        logging.error("Could not find Practice Assignment link. Check Week dropdown for exact title.")
        print(f"❌ Could not find Practice Assignment link. Please provide the exact link text from Week {week_number} dropdown.")
        raise Exception("Practice Assignment link not found")

    practice_assignment_link.click()
    print("✅ Practice Assignment clicked")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'gcb-question-row')]")))
        print("🔄 Practice Assignment page loaded")
    except TimeoutException:
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            print("🔄 Switched to Practice Assignment tab")
        else:
            print("⚠️ No new tab for Practice Assignment; staying on current tab")
            logging.warning("No new tab opened for Practice Assignment; proceeding with current tab")

    # --- Step 14: Scrape and extract questions ---
    print("🧠 Scraping questions from Practice Assignment page...")
    with open("practice_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Force-load dynamic content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Debug: Save pre-XPath page source
    with open("practice_pre_xpath_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'gcb-question-row')]")
        ))
    except TimeoutException:
        logging.error("Timeout waiting for question elements. Page source saved to practice_pre_xpath_page_source.html")
        print("❌ Timeout waiting for question elements. Check practice_pre_xpath_page_source.html")
        raise

    question_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'gcb-question-row')]")

    questions = []
    seen_texts = set()
    with open("practice_question_dom.txt", "w", encoding="utf-8") as dom_file:
        for i, q_elem in enumerate(question_elements, 1):
            try:
                q_elem.click()
                time.sleep(1)
            except:
                pass

            try:
                raw_text = q_elem.find_element(By.XPATH, ".//div[contains(@class, 'qt-embedded')]").text.strip()
                logging.debug(f"Q{i} raw text: {raw_text[:200]}...")
                if not raw_text or raw_text in seen_texts:
                    logging.warning(f"Skipping Q{i}: No text or duplicate")
                    continue
                seen_texts.add(raw_text)
            except Exception as e:
                logging.warning(f"Failed to extract raw text for Q{i}: {e}")
                continue

            try:
                dom_text = q_elem.get_attribute("outerHTML")
                dom_file.write(f"Q{i} DOM:\n{dom_text}\n\n")
                logging.debug(f"Q{i} DOM saved: {dom_text[:200]}...")
            except Exception as e:
                logging.warning(f"Failed to save DOM for Q{i}: {e}")

            questions.append({"number": f"Q{i}", "raw_text": raw_text})

    # Save extracted questions to questions_only.txt
    with open("questions_only.txt", "w", encoding="utf-8") as file:
        for q in questions:
            file.write(f"{q['raw_text']}\n\n---\n")
        logging.info(f"Saved {len(questions)} questions to questions_only.txt")
    print(f"✅ {len(questions)} questions saved to 'questions_only.txt'.")

    # ==== PART 2: Get answers using Gemini API ====
    print("\n🧠 Generating answers using Gemini API...")

    # Initialize Gemini client
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        logging.info("Initialized Gemini client")
    except Exception as e:
        logging.error(f"Failed to initialize Gemini client: {e}")
        print(f"❌ Failed to initialize Gemini client: {e}")
        print("Ensure GEMINI_API_KEY is valid in .env")
        raise

    # Read questions_only.txt
    try:
        with open("questions_only.txt", "r", encoding="utf-8") as file:
            questions_content = file.read().strip()
        
        if not questions_content:
            logging.error("questions_only.txt is empty")
            print("❌ questions_only.txt is empty.")
            raise Exception("questions_only.txt is empty")
        logging.info("Successfully read questions_only.txt")
    except FileNotFoundError:
        logging.error("questions_only.txt not found")
        print("❌ questions_only.txt not found.")
        raise

    # Generate answers with Gemini
    try:
        num_questions = len(questions)
        prompt = (
            f"Generate exactly {num_questions} answers for the following questions, one for each question (Q1 to Q{num_questions}). "
            "Use the 'Accepted Answers' if provided in the question text. If no 'Accepted Answers' are provided, "
            "generate the correct answer based on the question and options. "
            f"Format each answer on a new line as: 1) <option/integer/comma-separated options>\n2) <option/integer/comma-separated options>\n... up to {num_questions}), "
            "with no additional text, explanations, or extra lines. Ensure multiselect answers are comma-separated.\n\n"
            f"{questions_content}"
        )
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1000,
                "temperature": 0.7
            }
        )
        answer_text = response.text.strip()
        logging.info("Successfully generated answers with Gemini")
    except Exception as e:
        logging.error(f"Error calling Gemini API: {e}")
        print(f"❌ Error calling Gemini API: {e}")
        raise

    # Parse and save answers
    answers = []
    try:
        lines = answer_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(tuple(f"{i})" for i in range(1, num_questions + 1))):
                answer = line.split(")", 1)[1].strip()
                answers.append(answer)
            if len(answers) >= num_questions:
                break
        
        # Ensure exactly num_questions answers
        if len(answers) < num_questions:
            for i in range(len(answers) + 1, num_questions + 1):
                answers.append("Answer: Not found")
                logging.warning(f"Missing answer for Q{i}, using fallback")
        else:
            answers = answers[:num_questions]

        # Save to assignment_answers.txt
        with open("assignment_answers.txt", "w", encoding="utf-8") as file:
            for i, answer in enumerate(answers, 1):
                file.write(f"{i}) {answer}\n")
            logging.info(f"Saved {len(answers)} answers to assignment_answers.txt")
        print(f"🎉 {len(answers)} answers saved to 'assignment_answers.txt'.")
    except Exception as e:
        logging.error(f"Error parsing Gemini response: {e}")
        print(f"❌ Error parsing Gemini response: {e}")
        raise

    # ==== PART 3: Navigate back and fill answers ====
    print("\n🌐 Navigating back to Practice Assignment page to fill answers...")

    # Navigate back to Practice Assignment page using same driver
    try:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                driver.get("https://app.onlinedegree.iitm.ac.in/student_dashboard/current_courses")
                print("🔄 Navigating to Current Courses")
                course_link = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@href, '{subject_id}')]")
                ))
                course_link.click()
                print(f"✅ '{subject}' course clicked")
                try:
                    wait.until(EC.url_contains(subject_id))
                    print("🔄 Course page loaded")
                except TimeoutException:
                    print("⚠️ Course page not loaded; checking for new tab")
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        if subject_id in driver.current_url:
                            print(f"🔄 Switched to '{subject}' course tab")
                        else:
                            raise Exception("Failed to load course page or switch to course tab")
                    else:
                        raise Exception("No new tab opened and course page not loaded")
                week_link = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//div[contains(@class, 'units__items-title') and contains(text(), 'Week {week_number}')]")
                ))
                # Scroll to Week link
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", week_link)
                time.sleep(2)
                week_link.click()
                print(f"🔄 Clicked Week {week_number} to open dropdown")

                # Scroll the dropdown container to ensure all subitems are loaded
                try:
                    dropdown_container = driver.find_element(By.XPATH, f"//div[contains(@class, 'units__items-title') and contains(text(), 'Week {week_number}')]/following-sibling::div[contains(@class, 'units__subitems-show')]")
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dropdown_container)
                    time.sleep(2)
                    print("🔄 Scrolled Week dropdown to load all subitems")
                except NoSuchElementException:
                    print("⚠️ Could not find dropdown container to scroll; proceeding without scrolling")

                # Try multiple XPaths for Practice Assignment link
                practice_assignment_link = None
                for xpath in practice_xpaths:
                    try:
                        practice_assignment_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                        # Scroll to Practice Assignment link
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", practice_assignment_link)
                        time.sleep(2)
                        print(f"✅ Found Practice Assignment link with XPath: {xpath}")
                        break
                    except TimeoutException:
                        logging.warning(f"XPath not found: {xpath}")
                        continue

                if not practice_assignment_link:
                    logging.error("Could not find Practice Assignment link. Check Week dropdown for exact title.")
                    print(f"❌ Could not find Practice Assignment link. Please provide the exact link text from Week {week_number} dropdown.")
                    raise Exception("Practice Assignment link not found")

                practice_assignment_link.click()
                print("✅ Practice Assignment clicked")
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'gcb-question-row')]")))
                    print("🔄 Practice Assignment page loaded")
                except TimeoutException:
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        print("🔄 Switched to Practice Assignment tab")
                    else:
                        print("⚠️ No new tab for Practice Assignment; staying on current tab")
                        logging.warning("No new tab opened for Practice Assignment; proceeding with current tab")
                break  # Navigation successful
            except (TimeoutException, WebDriverException) as e:
                logging.warning(f"Navigation attempt {attempt + 1} failed: {e}")
                print(f"⚠️ Navigation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(5)
                else:
                    logging.error("Max retries reached. Navigation failed.")
                    print("❌ Max retries reached. Navigation failed.")
                    raise

        # Load answers from assignment_answers.txt
        answers = []
        try:
            with open("assignment_answers.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(tuple(f"{i})" for i in range(1, num_questions + 1))):
                        answer = line.split(")", 1)[1].strip()
                        answers.append(answer)
            if len(answers) != num_questions:
                logging.error(f"Expected {num_questions} answers in assignment_answers.txt, found {len(answers)}")
                print(f"❌ Expected {num_questions} answers in assignment_answers.txt, found {len(answers)}")
                raise Exception("Answer count mismatch")
            logging.info(f"Successfully loaded {num_questions} answers from assignment_answers.txt")
        except FileNotFoundError:
            logging.error("assignment_answers.txt not found")
            print("❌ assignment_answers.txt not found.")
            raise

        # Fill answers
        print("🧠 Filling answers on Practice Assignment page...")
        try:
            wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'gcb-question-row')]")
            ))
        except TimeoutException:
            logging.error("Timeout waiting for question elements during filling.")
            print("❌ Timeout waiting for question elements during filling.")
            raise

        question_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'gcb-question-row')]")
        if len(question_elements) < num_questions:
            logging.warning(f"Found only {len(question_elements)} question elements, expected {num_questions}")
            print(f"⚠️ Found only {len(question_elements)} question elements, expected {num_questions}")

        for i, (q_elem, answer) in enumerate(zip(question_elements, answers), 1):
            try:
                # Scroll to question with centering
                driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center', inline: 'center'});
                    window.scrollBy(0, -150);  // Adjust for headers
                """, q_elem)
                time.sleep(2)  # Wait for scroll and dynamic load
                logging.info(f"Scrolled to Q{i}")

                # Click to expand question if needed
                try:
                    q_elem.click()
                    time.sleep(1)
                except:
                    logging.warning(f"Q{i}: Could not click question element")
                    pass

                logging.info(f"Processing Q{i} with answer: {answer}")

                # --- Check if question is already filled ---
                is_filled = False

                # Text input check (Q4, Q8)
                if i in [4, 8]:
                    try:
                        text_input = q_elem.find_element(By.XPATH, ".//input[not(@type='checkbox') and not(@type='radio')] | .//textarea")
                        if text_input.get_attribute("value").strip():
                            is_filled = True
                            logging.info(f"Q{i}: Text input already filled with '{text_input.get_attribute('value')}'")
                            print(f"✅ Q{i}: Text input already filled, skipping")
                    except NoSuchElementException:
                        pass

                # Radio button check (Q3, Q5, Q7, Q9)
                if i in [3, 5, 7, 9]:
                    try:
                        radios = q_elem.find_elements(By.XPATH, ".//input[@type='radio'] | .//div[@role='radio']")
                        for radio in radios:
                            if radio.get_attribute("checked") or radio.get_attribute("aria-checked") == "true":
                                is_filled = True
                                logging.info(f"Q{i}: Radio button already selected")
                                print(f"✅ Q{i}: Radio button already selected, skipping")
                                break
                    except NoSuchElementException:
                        pass

                # Checkbox check (Q1 and potential multiselects)
                if i == 1 or any(part in answer for part in ["True", "False", "A", "B", "C", "D"]):  # Heuristic for multiselect
                    try:
                        checkboxes = q_elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                        answer_parts = [part.strip() for part in answer.split(",") if part.strip()]
                        all_checked = True
                        checked_count = 0
                        for checkbox in checkboxes:
                            if checkbox.get_attribute("checked"):
                                checked_count += 1
                            if checked_count >= len(answer_parts):
                                break
                        if checked_count >= len(answer_parts):
                            is_filled = True
                            logging.info(f"Q{i}: All required checkboxes already checked")
                            print(f"✅ Q{i}: All required checkboxes already checked, skipping")
                    except NoSuchElementException:
                        pass

                # Matching question check (Q2, Q6)
                if i in [2, 6]:
                    try:
                        dropdowns = q_elem.find_elements(By.XPATH, ".//select")
                        all_selected = True
                        for dropdown in dropdowns:
                            selected = dropdown.find_elements(By.XPATH, "./option[@selected]")
                            if not selected:
                                all_selected = False
                                break
                        if all_selected:
                            is_filled = True
                            logging.info(f"Q{i}: All dropdowns already selected")
                            print(f"✅ Q{i}: All dropdowns already selected, skipping")
                        else:
                            radios = q_elem.find_elements(By.XPATH, ".//input[@type='radio']")
                            groups = set()
                            for radio in radios:
                                name = radio.get_attribute("name")
                                if name:
                                    groups.add(name)
                            selected_count = 0
                            for group in groups:
                                if q_elem.find_elements(By.XPATH, f".//input[@type='radio'][@name='{group}'][@checked]"):
                                    selected_count += 1
                            answer_pairs = dict(re.findall(r"(\d+)-([A-D])", answer))
                            if selected_count >= len(answer_pairs):
                                is_filled = True
                                logging.info(f"Q{i}: All radio groups already selected")
                                print(f"✅ Q{i}: All radio groups already selected, skipping")
                    except NoSuchElementException:
                        pass

                if is_filled:
                    continue

                # --- Fill the question ---
                # Handle text input (Q4, Q8)
                if i in [4, 8]:  # Expected text input
                    try:
                        text_input = q_elem.find_element(By.XPATH, ".//input[not(@type='checkbox') and not(@type='radio')] | .//textarea")
                        text_input.clear()
                        text_input.send_keys(answer)
                        logging.info(f"Q{i}: Filled text input with '{answer}'")
                        print(f"✅ Q{i}: Filled text input with '{answer}'")
                        continue
                    except NoSuchElementException:
                        logging.info(f"Q{i}: No text input found")
                        print(f"⚠️ Q{i}: No text input found, trying other input types")

                # Handle True/False radio buttons (Q3, Q5, Q7, Q9)
                if i in [3, 5, 7, 9]:  # Expected True/False
                    try:
                        options = q_elem.find_elements(By.XPATH, ".//input[@type='radio'] | .//div[@role='radio']")
                        if options:
                            answer = answer.strip().lower()
                            found = False
                            for option in options:
                                try:
                                    label = option.find_element(By.XPATH, "./following-sibling::label | ./parent::label").text.strip().lower()
                                    if label == answer or (answer == "true" and label in ["true", "yes"]) or (answer == "false" and label in ["false", "no"]):
                                        driver.execute_script("arguments[0].click();", option)
                                        logging.info(f"Q{i}: Selected radio '{label}' for answer '{answer}'")
                                        print(f"✅ Q{i}: Selected radio '{label}' for answer '{answer}'")
                                        found = True
                                        break
                                except NoSuchElementException:
                                    continue
                            if not found:
                                logging.warning(f"Q{i}: No matching radio found for answer '{answer}'")
                                print(f"⚠️ Q{i}: No matching radio found for answer '{answer}', skipping")
                        else:
                            logging.warning(f"Q{i}: No radio buttons found")
                            print(f"⚠️ Q{i}: No radio buttons found, skipping")
                        continue
                    except Exception as e:
                        logging.warning(f"Q{i}: Error processing radio buttons: {e}")
                        print(f"⚠️ Q{i}: Error processing radio buttons: {e}, skipping")
                        continue

                # Handle multiselect checkboxes (Q1 and potential others)
                if i == 1 or any(part in answer for part in ["True", "False", "A", "B", "C", "D"]):  # Heuristic for multiselect
                    try:
                        options = q_elem.find_elements(By.XPATH, ".//div[contains(@class, 'qt-choices')]//input[@type='checkbox']")
                        if options:
                            answer_parts = [part.strip() for part in answer.split(",") if part.strip()]
                            found_any = False
                            for option in options:
                                try:
                                    label = option.find_element(By.XPATH, "./following-sibling::label").text.strip()
                                    for answer_part in answer_parts:
                                        if answer_part.lower() in label.lower():
                                            driver.execute_script("arguments[0].click();", option)
                                            logging.info(f"Q{i}: Selected checkbox '{label}' for answer part '{answer_part}'")
                                            print(f"✅ Q{i}: Selected checkbox '{label}' for answer part '{answer_part}'")
                                            found_any = True
                                            break
                                except NoSuchElementException:
                                    continue
                            if not found_any:
                                logging.warning(f"Q{i}: No matching checkboxes found for answer '{answer}'")
                                print(f"⚠️ Q{i}: No matching checkboxes found for answer '{answer}', skipping")
                        else:
                            logging.warning(f"Q{i}: No checkboxes found")
                            print(f"⚠️ Q{i}: No checkboxes found, skipping")
                        continue
                    except Exception as e:
                        logging.warning(f"Q{i}: Error processing checkboxes: {e}")
                        print(f"⚠️ Q{i}: Error processing checkboxes: {e}, skipping")
                        continue

                # Handle matching questions (Q2, Q6)
                if i in [2, 6]:  # Expected matching
                    try:
                        # Parse answer format: "1-B, 2-C, 3-A, 4-D"
                        answer_pairs = dict(re.findall(r"(\d+)-([A-D])", answer))
                        if not answer_pairs:
                            logging.warning(f"Q{i}: Invalid matching answer format: '{answer}'")
                            print(f"⚠️ Q{i}: Invalid matching answer format: '{answer}', skipping")
                            continue

                        # Try dropdowns
                        dropdowns = q_elem.find_elements(By.XPATH, ".//select")
                        if dropdowns:
                            found_any = False
                            for sub_idx, dropdown in enumerate(dropdowns, 1):
                                answer_key = str(sub_idx)
                                if answer_key not in answer_pairs:
                                    continue
                                answer_value = answer_pairs[answer_key]
                                try:
                                    options = dropdown.find_elements(By.XPATH, "./option")
                                    for option in options:
                                        option_text = option.text.strip()
                                        if option_text == answer_value or option_text.lower() == answer_value.lower():
                                            option.click()
                                            logging.info(f"Q{i}.{sub_idx}: Selected dropdown option '{option_text}' for answer '{answer_value}'")
                                            print(f"✅ Q{i}.{sub_idx}: Selected dropdown option '{option_text}' for answer '{answer_value}'")
                                            found_any = True
                                            break
                                except NoSuchElementException:
                                    continue
                            if not found_any:
                                logging.warning(f"Q{i}: No matching dropdown options found for answer '{answer}'")
                                print(f"⚠️ Q{i}: No matching dropdown options found for answer '{answer}', skipping")
                            continue

                        # Try radio buttons
                        radios = q_elem.find_elements(By.XPATH, ".//input[@type='radio']")
                        if radios:
                            found_any = False
                            groups = {}
                            for radio in radios:
                                name = radio.get_attribute("name")
                                if name:
                                    if name not in groups:
                                        groups[name] = []
                                    groups[name].append(radio)
                            for sub_idx, (group_name, radio_group) in enumerate(groups.items(), 1):
                                answer_key = str(sub_idx)
                                if answer_key not in answer_pairs:
                                    continue
                                answer_value = answer_pairs[answer_key]
                                for radio in radio_group:
                                    try:
                                        label = radio.find_element(By.XPATH, "./following-sibling::label | ./parent::label").text.strip()
                                        if label == answer_value or label.lower() == answer_value.lower():
                                            driver.execute_script("arguments[0].click();", radio)
                                            logging.info(f"Q{i}.{sub_idx}: Selected radio '{label}' for answer '{answer_value}'")
                                            print(f"✅ Q{i}.{sub_idx}: Selected radio '{label}' for answer '{answer_value}'")
                                            found_any = True
                                            break
                                    except NoSuchElementException:
                                        continue
                            if not found_any:
                                logging.warning(f"Q{i}: No matching radio options found for answer '{answer}'")
                                print(f"⚠️ Q{i}: No matching radio options found for answer '{answer}', skipping")
                            continue

                        logging.warning(f"Q{i}: No dropdowns or radios found for matching question")
                        print(f"⚠️ Q{i}: No dropdowns or radios found for matching question, skipping")
                        continue
                    except Exception as e:
                        logging.warning(f"Q{i}: Error processing matching question: {e}")
                        print(f"⚠️ Q{i}: Error processing matching question: {e}, skipping")
                        continue

                # Fallback if no specific type matched
                logging.warning(f"Q{i}: No input type matched, skipping")
                print(f"⚠️ Q{i}: No input type matched, skipping")

            except Exception as e:
                logging.error(f"Error processing Q{i}: {e}")
                print(f"❌ Error processing Q{i}: {e}")
                continue  # Continue to next question

        print("🎉 Finished filling answers on Practice Assignment page.")

        # --- Submit by clicking "Check Answers" ---
        print("📤 Submitting by clicking 'Check Answers'...")
        try:
            # Scroll to bottom to ensure button is visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Try multiple XPaths for the "Check Answers" button
            check_xpaths = [
                "//button[contains(., 'Check Answers') or contains(., 'check answers') or contains(., 'Check') or contains(., 'check')]",
                "//button[contains(., 'Submit') or contains(., 'submit')]",  # Fallback to Submit if Check Answers not found
                "//input[@type='submit' and (contains(@value, 'Check') or contains(@value, 'check') or contains(@value, 'Submit') or contains(@value, 'submit'))]"
            ]
            check_button = None
            for xpath in check_xpaths:
                try:
                    check_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    print(f"✅ Found 'Check Answers' button with XPath: {xpath}")
                    break
                except TimeoutException:
                    logging.warning(f"Button XPath not found: {xpath}")
                    continue

            if not check_button:
                logging.error("Could not find 'Check Answers' or 'Submit' button.")
                print("❌ Could not find 'Check Answers' or 'Submit' button. Please provide the exact button text or XPath.")
                raise Exception("Check Answers/Submit button not found")

            # Click the button
            driver.execute_script("arguments[0].click();", check_button)
            print("✅ 'Check Answers' button clicked successfully")

            # Wait for confirmation (e.g., success message, URL change, or page update)
            try:
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'success-message')] | //*[contains(text(), 'successfully')] | //*[contains(text(), 'checked')]")
                ))
                print("✅ Answers checked successfully")
            except TimeoutException:
                logging.warning("No confirmation message found; checking URL change")
                if "submission" in driver.current_url.lower() or "completed" in driver.current_url.lower() or "checked" in driver.current_url.lower():
                    print("✅ Submission likely successful (URL changed)")
                else:
                    print("⚠️ Could not confirm submission; please check the page")

        except Exception as e:
            logging.error(f"Error during 'Check Answers' submission: {str(e)}")
            print(f"❌ Error during 'Check Answers' submission: {str(e)}")
            raise

    except Exception as e:
        logging.error(f"Error during answer filling: {str(e)}")
        print(f"❌ Error during answer filling: {str(e)}")
        raise

finally:
    if driver:
        print("🌐 Staying on the page after checking answers. Press Ctrl+C to interrupt and close the browser.")
        try:
            while True:
                time.sleep(60)  # Sleep to keep the script running
        except KeyboardInterrupt:
            print("🛑 Browser closed manually via interruption.")
            driver.quit()