"""HTMLファイルを翻訳する"""

import html
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

# File paths
input_file = Path(__file__).parent / "templates" / "ja.html"
output_file = Path(__file__).parent / "results" / "en.html"


def translate_text(text, source_lang="ja", target_lang="en"):
    """Translate text using Google Cloud Translation API with API key."""
    url = "https://translation.googleapis.com/language/translate/v2"

    params = {
        "key": api_key,
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "html",  # Specify HTML format to preserve tags
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        result = response.json()
        return result["data"]["translations"][0]["translatedText"]
    else:
        raise Exception(f"Translation failed: {response.text}")


def main():
    # Check if API key is available
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_PROJECT_API_KEY not found in environment variables")

    # Read the input HTML file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Translate the content
    try:
        print("Translating content...")
        translated_content = translate_text(content)

        # Unescape HTML entities if needed (API sometimes returns escaped HTML)
        translated_content = html.unescape(translated_content)

        # Write to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated_content)

        print(f"Translation complete. Output saved to {output_file}")
    except Exception as e:
        print(f"Error during translation: {e}")


if __name__ == "__main__":
    main()
