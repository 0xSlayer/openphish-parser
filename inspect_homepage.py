import csv
import requests

from datetime import datetime
from pathlib import Path


FEED_URL = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
CSV_FILE = Path("data/openphish.csv")


def fetch_feed(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text


def clean_urls(text):
    urls = text.splitlines()

    clean = []

    for url in urls:
        url = url.strip()

        if url:
            clean.append(url)

    return clean


def load_existing_urls(csv_file):
    existing_urls = set()

    if not csv_file.exists():
        return existing_urls

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            existing_urls.add(row["url"])

    return existing_urls


def save_new_urls(csv_file, new_urls, collected_at):
    file_exists = csv_file.exists()

    csv_file.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["url", "collected_at"])

        for url in new_urls:
            writer.writerow([url, collected_at])


def main():
    collected_at = datetime.now().astimezone().isoformat(timespec="seconds")

    feed_text = fetch_feed(FEED_URL)
    urls = clean_urls(feed_text)

    unique_urls = set(urls)
    existing_urls = load_existing_urls(CSV_FILE)

    new_urls = []

    for url in urls:
        if url not in existing_urls:
            new_urls.append(url)

    print("Collected at:", collected_at)
    print("URLs in current feed:", len(urls))
    print("Unique URLs in current feed:", len(unique_urls))
    print("Already saved URLs:", len(existing_urls))
    print("New URLs:", len(new_urls))

    save_new_urls(CSV_FILE, new_urls, collected_at)

    print("Saved to:", CSV_FILE)


if __name__ == "__main__":
    main()