import csv
import requests

from pathlib import Path

from bs4 import BeautifulSoup


CSV_FILE = Path("data/openphish.csv")
LOGS_DIR = Path("logs")

HOMEPAGE_URL = "https://openphish.com/"


def load_urls(csv_file):
    urls = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            urls.append(row["url"])

    return urls


def find_latest_log(logs_dir):
    log_files = list(logs_dir.glob("collection_*.log"))

    if not log_files:
        return None

    return max(log_files, key=lambda file: file.stat().st_mtime)


def load_run_info(log_file):
    start_time = None
    end_time = None
    total_collections = None

    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("Parser started:"):
                start_time = line.split("Parser started:", 1)[1].strip()

            elif line.startswith("Parser finished:"):
                end_time = line.split("Parser finished:", 1)[1].strip()

            elif line.startswith("Total collections:"):
                total_collections = line.split("Total collections:", 1)[1].strip()

    return start_time, end_time, total_collections


def fetch_homepage(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text


def get_top_brands(html, limit=3):
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")

    if not tables:
        return []

    brand_table = tables[0]

    brands = []

    rows = brand_table.find_all("tr")

    for row in rows:
        cells = row.find_all(["th", "td"])
        values = [cell.get_text(" ", strip=True) for cell in cells]

        if len(values) == 2:
            brand = values[0]
            percentage = values[1]

            brands.append((brand, percentage))

    return brands[:limit]


def main():
    urls = load_urls(CSV_FILE)
    unique_urls = set(urls)

    latest_log = find_latest_log(LOGS_DIR)

    if latest_log:
        start_time, end_time, total_collections = load_run_info(latest_log)
    else:
        start_time = None
        end_time = None
        total_collections = None

    html = fetch_homepage(HOMEPAGE_URL)
    brands = get_top_brands(html)

    print("===== OpenPhish analysis =====")
    print()

    print("Collection:")
    print("Parsing started:", start_time)
    print("Parsing finished:", end_time)
    print("Total collections:", total_collections)

    print()
    print("URLs:")
    print("Stored URLs:", len(urls))
    print("Unique URLs:", len(unique_urls))
    print("Duplicates:", len(urls) - len(unique_urls))

    print()
    print("Top 3 targeted brands:")
    print("(aggregated statistics from the OpenPhish homepage)")

    for index, (brand, percentage) in enumerate(brands, start=1):
        print(f"{index}. {brand} - {percentage}")


if __name__ == "__main__":
    main()