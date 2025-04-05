from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Chrome WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment to run headless
    return webdriver.Chrome(options=options)

# Accept cookie popup if present
def handle_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        ).click()
        print("✅ Cookies accepted!")
    except:
        print("⚠️ No cookie popup found or already accepted.")

# Check if a cell has a green dot indicating "Yes"
def has_green_dot(cell):
    try:
        span = cell.find_element(By.CLASS_NAME, "catalogue__circle")
        class_name = span.get_attribute("class")
        return "-yes" in class_name
    except:
        return False

# Scrape a single page given its URL
def scrape_page(driver, url, page_num, retries=2):
    data = []
    for attempt in range(retries + 1):
        try:
            driver.get(url)
            print(f"\n🔍 Visiting Page {page_num} | Attempt {attempt + 1} | {url}")
            time.sleep(2)

            if page_num == 1 and attempt == 0:
                handle_cookies(driver)

            # Wait for the table to load
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Individual Test Solutions')]/ancestor::table"))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header

            if not rows:
                print(f"⚠️ No rows found on Page {page_num}")
                return []

            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")

                    link_elem = cells[0].find_element(By.TAG_NAME, "a")
                    name = link_elem.text.strip()
                    link = link_elem.get_attribute("href")

                    # Green dots are in 2nd and 3rd cells (index 1 and 2)
                    remote_testing = "Yes" if has_green_dot(cells[1]) else "No"
                    adaptive_irt = "Yes" if has_green_dot(cells[2]) else "No"

                    data.append([
                        "Individual Test Solutions", name, link,
                        remote_testing, adaptive_irt
                    ])

                except Exception as e:
                    print(f"⚠️ Error processing row: {e}")
                    continue

            print(f"✅ Page {page_num}: {len(data)} tests scraped.")
            return data

        except Exception as e:
            print(f"❌ Error scraping Page {page_num}, Attempt {attempt + 1}: {e}")
            if attempt < retries:
                print("🔁 Retrying...")
                time.sleep(5)
            else:
                print("⛔ Skipping Page", page_num)
    return []

# === MAIN SCRIPT ===
if __name__ == "__main__":
    driver = get_driver()

    base_url = "https://www.shl.com/solutions/products/product-catalog/?start={}&type=1&type=1"
    all_data = []

    for page_num in range(1, 33):
        start = (page_num - 1) * 12
        url = base_url.format(start)
        page_data = scrape_page(driver, url, page_num)

        if page_data:
            all_data.extend(page_data)

            # Save incrementally after each page
            df = pd.DataFrame(
                all_data,
                columns=["Category", "Name", "Link", "Remote Testing", "Adaptive/IRT"]
            )
            df.to_csv("data/shl_individual_test_solutions.csv", index=False)

            print(f"📦 Total tests saved so far: {len(all_data)}")
        else:
            print(f"⚠️ No data scraped from Page {page_num}")

    driver.quit()
    print("\n✅ Scraping finished.")
