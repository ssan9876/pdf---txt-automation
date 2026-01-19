import pdfplumber
import time
from pathlib import Path
import re

# CHANGE THIS to your real root folder
ROOT_FOLDER = Path(r"C:WatchFolder")

print("Root exists:", ROOT_FOLDER.exists())
print("Starting recursive PDF scan...")

def clean_text(text):
    # Remove hyphenated line breaks
    text = re.sub(r"-\n", "", text)
    # Normalize excessive newlines
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text

def extract_pdf_to_txt(pdf_path):
    txt_path = pdf_path.with_suffix(".txt")

    # Skip if already processed
    if txt_path.exists():
        return

    try:
        with pdfplumber.open(pdf_path) as pdf, \
             open(txt_path, "w", encoding="utf-8") as f:

            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    text = clean_text(text)
                    f.write(f"\n--- Page {page_num} ---\n")
                    f.write(text + "\n")

        print(f"[✓] Extracted: {pdf_path}")

    except Exception as e:
        print(f"[!] Failed to process {pdf_path}: {e}")

# Continuous automation loop
while True:
    found_any = False

    for item in ROOT_FOLDER.rglob("*"):
        if item.is_file() and item.suffix.lower() == ".pdf":
            found_any = True
            extract_pdf_to_txt(item)

    if not found_any:
        print("No PDFs found during this scan.")

    time.sleep(10)  # scan interval (seconds)
