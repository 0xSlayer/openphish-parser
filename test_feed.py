import csv
import requests

from datetime import datetime
from pathlib import Path


feed_url = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
csv_file = Path("data/openphish.csv")

response = requests.get(feed_url, timeout=10)

print("HTTP status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Size:", len(response.text))

urls = response.text.splitlines()

clean_urls = []

for url in urls:
    url = url.strip()

    if url:
        clean_urls.append(url)

unique_urls = set(clean_urls)

collected_at = datetime.now().astimezone().isoformat(timespec="seconds")

existing_urls = set()

if csv_file.exists():
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            existing_urls.add(row["url"])

new_urls = []

for url in clean_urls:
    if url not in existing_urls:
        new_urls.append(url)

print()
print("Collected at:", collected_at)
print("Raw lines:", len(urls))
print("Clean URLs:", len(clean_urls))
print("Unique URLs in current feed:", len(unique_urls))
print("Already saved URLs:", len(existing_urls))
print("New URLs:", len(new_urls))

file_exists = csv_file.exists()

with open(csv_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["url", "collected_at"])

    for url in new_urls:
        writer.writerow([url, collected_at])

print()
print("Saved to:", csv_file)