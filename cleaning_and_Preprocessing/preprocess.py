import pandas as pd

# Load original file
input_file = "data/shl_detailed_test_info.csv"
output_file = "data/shl_detailed_test_info_cleaned.csv"
final_output_file = "data/shl_detailed_test_info_final.csv"

df = pd.read_csv(input_file)

# 1. Rename columns
df.columns = [
    "assessment_name", "url", "description", "assessment_length",
    "remote_testing_support", "adaptive_irt_support",
    "test_type_code", "category_description",
    "job_levels", "category_group", "extra"
]

# 2. Drop 'extra' column
df.drop(columns=["extra"], inplace=True)

# 3. Strip whitespace from all string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# 4. Normalize Yes/No to boolean
df["remote_testing_support"] = df["remote_testing_support"].str.lower().map({"yes": True, "no": False})
df["adaptive_irt_support"] = df["adaptive_irt_support"].str.lower().map({"yes": True, "no": False})

# 5. Category code to full name mapping
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

# 6. Save intermediate cleaned data (before splitting)
df.to_csv(output_file, index=False)
print(f"✅ Cleaned (but not split) data saved to '{output_file}'")

# 7. Split rows with multiple test_type_code values
def expand_row(row):
    codes = [code.strip() for code in str(row["test_type_code"]).split(",")]
    expanded = []
    for code in codes:
        new_row = row.copy()
        new_row["test_type_code"] = code
        new_row["test_type_full"] = CATEGORY_MAP.get(code, "Unknown")
        expanded.append(new_row)
    return expanded

expanded_rows = []
for _, row in df.iterrows():
    expanded_rows.extend(expand_row(row))

df_expanded = pd.DataFrame(expanded_rows)

# 8. Reorder columns
df_expanded = df_expanded[
    [
        "assessment_name", "url", "description", "assessment_length",
        "remote_testing_support", "adaptive_irt_support",
        "test_type_code", "test_type_full",
        "category_description", "job_levels", "category_group"
    ]
]

# 9. Save final cleaned and expanded file
df_expanded.to_csv(final_output_file, index=False)
print(f"✅ Final cleaned and expanded data saved to '{final_output_file}'")
