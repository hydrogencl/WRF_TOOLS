import requests
from bs4 import BeautifulSoup
import csv

url = "https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/namelist_variables.html"
resp = requests.get(url)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

rows = []
for section in soup.find_all(["h2","h3"]):
    title = section.get_text().strip()
    if not title.startswith("&"):
        continue
    tbl = section.find_next_sibling("table")
    if not tbl:
        continue
    for tr in tbl.find_all("tr")[1:]:  
        cols = [td.get_text().strip() for td in tr.find_all("td")]
        if len(cols) < 4:
            continue
        varname = cols[0]
        default = cols[1]
        entry_type = cols[-1]
        rows.append((title, varname, default, entry_type))

with open("wrf_namelist_vars.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "variable name", "default input", "Entry (single or max_dom)"])
    for r in rows:
        writer.writerow(r)

print(f"Output totally {len(rows)} rows to  wrf_namelist_vars.csv")


