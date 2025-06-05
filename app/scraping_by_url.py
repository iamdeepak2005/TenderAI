from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

chromedriver_path = r"C:\Users\deepa\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def scrape(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Extract full visible text of <body>
        body_text = driver.find_element("tag name", "body").text

        # Clean text for readability
        clean_text = re.sub(r'\n\s*\n+', '\n\n', body_text)  # collapse multiple blank lines
        clean_text = re.sub(r'[ \t]+', ' ', clean_text)      # normalize whitespace
        clean_text = clean_text.strip()

        # Extract and format all tables
        tables = driver.find_elements("tag name", "table")
        def table_to_markdown(table):
            rows = table.find_elements("tag name", "tr")
            markdown_rows = []
            for row in rows:
                cells = row.find_elements("tag name", "th") or row.find_elements("tag name", "td")
                row_text = [cell.text.strip().replace('\n', ' ') for cell in cells]
                markdown_rows.append("| " + " | ".join(row_text) + " |")
            if len(markdown_rows) > 1:
                header_len = len(markdown_rows[0].split("|")) - 2
                separator = "| " + " | ".join(["---"] * header_len) + " |"
                markdown_rows.insert(1, separator)
            return "\n".join(markdown_rows)

        all_tables_text = ""
        for i, table in enumerate(tables):
            try:
                md_table = table_to_markdown(table)
                all_tables_text += f"\n\nTable {i+1}:\n{md_table}\n"
            except Exception as e:
                print(f"Error processing table {i+1}: {e}")

        # Combine clean body text and markdown tables
        final_output = clean_text + all_tables_text
        return final_output

    finally:
        driver.quit()

# print(scrape_gem_page("https://jewelbankers.com/"))  # Example URL, replace with actual tender page