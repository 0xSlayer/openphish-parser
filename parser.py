import csv
import time
import requests

from datetime import datetime
from pathlib import Path


FEED_URL = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
CSV_FILE = Path("data/openphish.csv")

INTERVAL_SECONDS = 300
DURATION_SECONDS = 3600

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


def collect_once():
    collected_at = datetime.now().astimezone().isoformat(timespec="seconds")

    feed_text = fetch_feed(FEED_URL)
    urls = clean_urls(feed_text)

    unique_urls = set(urls)
    existing_urls = load_existing_urls(CSV_FILE)

    new_urls = []
    seen_urls = set()

    for url in urls:
        if url in seen_urls:
            continue

        seen_urls.add(url)

        if url not in existing_urls:
            new_urls.append(url)

    print("Collected at:", collected_at)
    print("URLs in current feed:", len(urls))
    print("Unique URLs in current feed:", len(unique_urls))
    print("Already saved URLs:", len(existing_urls))
    print("New URLs:", len(new_urls))

    save_new_urls(CSV_FILE, new_urls, collected_at)

    print("Saved to:", CSV_FILE)

def main():
    start_datetime = datetime.now().astimezone()
    start_monotonic = time.monotonic()

    end_monotonic = start_monotonic + DURATION_SECONDS
    next_run = start_monotonic

    iteration = 0

    print("Parser started:", start_datetime.isoformat(timespec="seconds"))
    print("Collection interval:", INTERVAL_SECONDS, "seconds")
    print("Collection duration:", DURATION_SECONDS, "seconds")

    while next_run < end_monotonic:
        now = time.monotonic()

        if now < next_run:
            sleep_time = next_run - now

            print("Waiting:", round(sleep_time), "seconds...")
            time.sleep(sleep_time)

        iteration += 1

        print()
        print("Collection:", iteration)

        collect_once()

        next_run = start_monotonic + iteration * INTERVAL_SECONDS

    remaining = end_monotonic - time.monotonic()

    if remaining > 0:
        print()
        print("Waiting until collection period ends:", round(remaining), "seconds...")
        time.sleep(remaining)

    end_datetime = datetime.now().astimezone()

    print()
    print("Parser finished:", end_datetime.isoformat(timespec="seconds"))
    print("Total collections:", iteration)

if __name__ == "__main__":
    main()
