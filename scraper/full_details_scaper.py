import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    return webdriver.Chrome(options=options)

def handle_cookies(driver):
    try:
        time.sleep(3)
        accept_btn = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        accept_btn.click()
        print("✅ Cookies accepted!")
        time.sleep(2)
    except:
        print("⚠️ No cookie popup found.")

CATEGORY_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def extract_test_details(driver, url, is_first):
    driver.get(url)

    if is_first:
        handle_cookies(driver)

    time.sleep(2)

    result = {
        "Assessment Name": "",
        "URL": url,
        "Description": "Not Found",
        "Assessment Length": "Not Found",
        "Remote Testing Support": "No",
        "Adaptive/IRT Support": "No",
        "Test Type": "Not Found",
        "Test Type (Category)": "Not Found",
        "Job Level": "Not Found"
    }

    try:
        # Assessment Name
        name_elem = driver.find_element(By.TAG_NAME, "h1")
        result["Assessment Name"] = name_elem.text.strip()

        # Attribute sections
        sections = driver.find_elements(By.CSS_SELECTOR, "div.product-catalogue-training-calendar__row.typ")

        for section in sections:
            text = section.text

            if "Description" in text:
                try:
                    result["Description"] = section.find_element(By.TAG_NAME, "p").text.strip()
                except:
                    pass

            if "Assessment length" in text:
                try:
                    result["Assessment Length"] = section.find_element(By.TAG_NAME, "p").text.strip()
                except:
                    pass

            if "Job levels" in text or "Job level" in text:
                try:
                    result["Job Level"] = section.find_element(By.TAG_NAME, "p").text.strip()
                except:
                    pass

        # Test Type & Remote Testing/Adaptive flags
        d_flex_blocks = driver.find_elements(By.CSS_SELECTOR, "div.d-flex")

        for block in d_flex_blocks:
            block_text = block.text.lower()

            if "test type" in block_text:
                type_spans = block.find_elements(By.CLASS_NAME, "product-catalogue__key")
                test_types = [span.text.strip() for span in type_spans if span.text.strip()]
                result["Test Type"] = ", ".join(test_types)
                result["Test Type (Category)"] = ", ".join([CATEGORY_MAP.get(t, "Unknown") for t in test_types])

            if "remote testing" in block_text:
                try:
                    circle = block.find_element(By.CLASS_NAME, "catalogue__circle")
                    if "-yes" in circle.get_attribute("class"):
                        result["Remote Testing Support"] = "Yes"
                except:
                    pass

            if "adaptive" in block_text or "irt" in block_text:
                try:
                    circle = block.find_element(By.CLASS_NAME, "catalogue__circle")
                    if "-yes" in circle.get_attribute("class"):
                        result["Adaptive/IRT Support"] = "Yes"
                except:
                    pass

    except Exception as e:
        print(f"⚠️ Error processing {url}: {e}")

    return result

# === MAIN SCRIPT ===
input_file = "data/shl_individual_test_solutions.csv"
output_file = "data/shl_detailed_test_info.csv"

df = pd.read_csv(input_file)
print(f"🔍 Loaded {len(df)} test URLs")

driver = get_driver()

# Prepare output file
if not os.path.exists(output_file):
    pd.DataFrame(columns=[
        "Assessment Name", "URL", "Description", "Assessment Length",
        "Remote Testing Support", "Adaptive/IRT Support",
        "Test Type", "Test Type (Category)", "Job Level",
        "Category Code", "Category Description"
    ]).to_csv(output_file, index=False)

is_first_page = True

for idx, row in df.iterrows():
    category_code, name, url = row["Category"], row["Name"], row["Link"]
    category_desc = CATEGORY_MAP.get(category_code.strip(), "Unknown")

    print(f"\n🔗 Visiting [{idx + 1}/{len(df)}]: {name} [{category_desc}]")
    details = extract_test_details(driver, url, is_first=is_first_page)
    is_first_page = False

    details["Category Code"] = category_code
    details["Category Description"] = category_desc

    df_temp = pd.DataFrame([details])
    df_temp.to_csv(output_file, mode='a', header=False, index=False)
    print(f"💾 Saved: {details['Assessment Name']}")

driver.quit()
print(f"\n✅ All data saved to '{output_file}'")
