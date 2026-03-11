# UnionHunter

UnionHunter is a lightweight SQL Injection reconnaissance tool written in Python.

It automates the early discovery phase of **UNION-based SQL Injection** vulnerabilities.
The tool helps security researchers quickly identify the structure of vulnerable SQL queries.

## Features

* Detects number of columns in the SQL query
* Tests UNION-based injection
* Detects which columns reflect user input
* Attempts to identify the backend database
* Tries to extract database version information

## Supported Databases

* MySQL / MariaDB
* PostgreSQL
* Microsoft SQL Server
* Oracle

## Installation

Clone the repository:

```
git clone https://github.com/YOURUSERNAME/unionhunter.git
```

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the script:

```
python unionhunter.py
```

Enter the target URL when prompted:

```
https://target.com/filter?category=Lifestyle
```

Example output:

```
[+] Column count: 2
[+] Reflected column: 2
[+] Database: PostgreSQL
```

## Disclaimer

This tool is created for **educational purposes and authorized security testing only**.
Do not use it against systems without explicit permission.

## Author

Songül Kızılay
