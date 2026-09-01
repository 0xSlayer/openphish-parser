import requests
from bs4 import BeautifulSoup


url = "https://openphish.com/"

response = requests.get(url, timeout=10)

print("HTTP status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("HTML size:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

print("Page title:", soup.title)
print("Title text:", soup.title.text)

tables = soup.find_all("table")

print("Tables found:", len(tables))

for index, table in enumerate(tables, start=1):
    print()
    print("Table:", index)

    rows = table.find_all("tr")

    print("Rows:", len(rows))

    for row in rows[:3]:
        cells = row.find_all(["th", "td"])
        values = [cell.get_text(" ", strip=True) for cell in cells]

        print(values)