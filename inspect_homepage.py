import requests
from bs4 import BeautifulSoup


URL = "https://openphish.com/"


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
    html = fetch_homepage(URL)

    brands = get_top_brands(html)

    print("===== OpenPhish homepage analysis =====")
    print()

    if not brands:
        print("Targeted brands not found.")
        return

    print("Top 3 targeted brands:")

    for index, (brand, percentage) in enumerate(brands, start=1):
        print(f"{index}. {brand} - {percentage}")


if __name__ == "__main__":
    main()