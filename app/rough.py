from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = r"C:\Users\deepa\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def login_and_go_to_pledge(username: str, password: str):
    options = Options()
    # For debugging, comment out headless to see browser UI
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://jewelbankers.com/login")

        wait = WebDriverWait(driver, 15)

        # Wait for username input to be visible and fill
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys(username)

        # Wait for password input to be visible and fill
        password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys(password)

        # Click the login button (adjust selector as per site)
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # Wait until login finishes and URL or page changes - example:
        wait.until(EC.url_contains("/dashboard"))  # or whatever is the landing URL after login

        # Navigate to /pledge page
        driver.get("https://jewelbankers.com/pledge")

        # Wait for pledge page to load, e.g. presence of an element
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

        # Now you can extract or fill data here
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print(page_text)

    finally:
        driver.quit()

# Example usage:
login_and_go_to_pledge("omprakash", "Deepak@2005")
