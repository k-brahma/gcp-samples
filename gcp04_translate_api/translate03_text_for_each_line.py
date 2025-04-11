"""通常の .txt ファイルでは改行が保存されない場合がある

そこで、1行ずつ翻訳する方法を試してみる(APIリクエスト回数が増えるのでコストはかかる)
"""

import html
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

# File paths
input_file = Path(__file__).parent / "templates" / "ja.txt"
output_file = Path(__file__).parent / "results" / "en_for_each_line.txt"


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

    # Read the input file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Split content into lines
        lines = content.split("\n")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Translate each line separately
    try:
        print("Translating content...")
        translated_lines = []

        for line in lines:
            if line.strip():  # Skip empty lines
                translated_line = translate_text(line)
                translated_line = html.unescape(translated_line)
                translated_lines.append(translated_line)
            else:
                translated_lines.append("")  # Keep empty lines

        # Join the translated lines with newlines
        final_content = "\n".join(translated_lines)

        # Write to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"Translation complete. Output saved to {output_file}")
    except Exception as e:
        print(f"Error during translation: {e}")


if __name__ == "__main__":
    main()
