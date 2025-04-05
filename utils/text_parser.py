import re

def extract_duration(text):
    match = re.search(r"(\d+)\s*(?:min|minutes?)", text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_keywords(text):
    return re.findall(r"\b\w{4,}\b", text.lower())
