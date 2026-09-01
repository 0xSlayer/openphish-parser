import csv

from pathlib import Path


CSV_FILE = Path("data/openphish.csv")


def load_urls(csv_file):
    urls = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            urls.append(row["url"])

    return urls


def main():
    urls = load_urls(CSV_FILE)
    unique_urls = set(urls)

    print("===== OpenPhish analysis =====")
    print()
    print("Stored URLs:", len(urls))
    print("Unique URLs:", len(unique_urls))
    print("Duplicates:", len(urls) - len(unique_urls))


if __name__ == "__main__":
    main()